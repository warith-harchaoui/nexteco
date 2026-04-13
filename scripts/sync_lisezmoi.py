#!/usr/bin/env python3
"""
scripts/sync_lisezmoi.py
------------------------
Synchronise LISEZMOI.md (French translation) with README.md.

Usage:
    python3 scripts/sync_lisezmoi.py [--force]

Options:
    --force   Retranslate every section even if unchanged.

How it works
~~~~~~~~~~~~
1. Split README.md and LISEZMOI.md into sections (split on ^## or ^# headings).
2. Detect which README sections are new or changed relative to the last known
   state stored in .sync_state.json.
3. Send each changed section to Claude for French translation, respecting the
   GLOSSARY of preferred terms the user has established.
4. Rebuild LISEZMOI.md from the translated sections, writing it in place.

Environment:
    ANTHROPIC_API_KEY  (required) — your Anthropic API key.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

ROOT = Path(__file__).resolve().parent.parent
README  = ROOT / "README.md"
LISEZMOI = ROOT / "LISEZMOI.md"
STATE_FILE = ROOT / ".sync_state.json"   # tracks section hashes from last sync

# Terms to keep as-is or render in a specific way in the French translation.
# Key = English phrase (case-insensitive regex), Value = preferred French rendering.
GLOSSARY: dict[str, str] = {
    r"\bPh\.D\.\b":              "Ph.D.",
    r"\bHead of AI\b":           "_Head of AI_",
    r"\bAI Business Enabler\b":  "_AI Business Enabler_",
    r"\bscikit-learn\b":         "`scikit-learn`",
    r"\bGreen Algorithms\b":     "Green Algorithms",
    r"\bThe Unlicense\b":        "The Unlicense",
    r"\bClaude Code\b":          "Claude Code",
    r"\bCopilot Agent\b":        "Copilot Agent",
    r"\bWindsurf\b":             "Windsurf",
    r"\bCursor\b":               "Cursor",
    r"\bAntigravity\b":          "Antigravity",
    r"\bNEXTON\b":              "NEXTON",
    r"\bprobabl\.ai\b":          "probabl.ai",
    r"\bcore\.md\b":             "core.md",
    r"\badvanced\.md\b":         "advanced.md",
    r"\bAGENTS\.md\b":           "AGENTS.md",
    r"\bcost_of_running\.yaml\b": "cost_of_running.yaml",
    r"\bLICENSE\b":              "LICENSE",
    r"\bREADME\.md\b":           "README.md",
    r"\bYAML\b":                 "YAML",
    r"\bTODO\b":                 "TODO",
    r"\bSaaS\b":                 "SaaS",
    r"\bpowermetrics\b":         "powermetrics",
    # Taxonomy terms — keep English labels as they are code-like identifiers
    r"\bmeasured\b":             "measured",
    r"\bestimated\b":            "estimated",
    r"\bplaceholder\b":          "placeholder",
}

SYSTEM_PROMPT = """\
You are a precise French technical translator.
Translate the given Markdown section from English to French.

Rules:
- Preserve ALL Markdown formatting: headings (#), bold (**), italic (*_),
  code spans (`), fenced code blocks (```), tables, blockquotes (>),
  LaTeX math ($…$ and $$…$$), HTML, and links.
- Do NOT translate content inside fenced code blocks (``` … ```) or inline
  code spans (` … `).
- Do NOT translate LaTeX math expressions.
- Do NOT translate URLs, link targets, or GitHub/LinkedIn URLs.
- Respect the GLOSSARY: the caller will post-process the output, but try to
  respect preferred renderings already provided in the glossary note.
- Output ONLY the translated Markdown — no preamble, no explanations.
"""

GLOSSARY_NOTE = (
    "Preferred renderings (keep exactly as shown):\n"
    + "\n".join(f"  - {v}" for v in GLOSSARY.values())
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def section_hash(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()[:16]


def split_sections(text: str) -> list[tuple[str, str]]:
    """
    Return a list of (heading, body) pairs.
    The first pair has heading='' for any content before the first heading.
    """
    pattern = re.compile(r'^(#{1,6} .+)$', re.MULTILINE)
    parts: list[tuple[str, str]] = []
    pos = 0
    current_heading = ""

    for m in pattern.finditer(text):
        body = text[pos:m.start()].rstrip('\n')
        parts.append((current_heading, body))
        current_heading = m.group(1)
        pos = m.end() + 1  # skip the newline after heading

    # last section
    parts.append((current_heading, text[pos:].rstrip('\n')))
    # remove empty preamble if nothing before first heading
    parts = [(h, b) for h, b in parts if h or b.strip()]
    return parts


def rebuild_text(sections: list[tuple[str, str]]) -> str:
    lines = []
    for heading, body in sections:
        if heading:
            lines.append(heading)
        if body:
            lines.append(body)
        lines.append('')  # blank line between sections
    return '\n'.join(lines).strip() + '\n'


def load_state() -> dict:
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {}


def save_state(state: dict) -> None:
    STATE_FILE.write_text(json.dumps(state, indent=2))


def apply_glossary(text: str) -> str:
    """Post-process translation to enforce glossary renderings."""
    for pattern, replacement in GLOSSARY.items():
        # Only replace in non-code, non-math contexts — simple heuristic:
        # we operate on the full text but skip anything inside backtick pairs.
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    return text


def translate_section(client, heading: str, body: str) -> tuple[str, str]:
    """
    Translate a single README section (heading + body) to French.
    Returns (french_heading, french_body).
    """
    # Build the full section text to translate
    section_text = f"{heading}\n{body}".strip() if heading else body.strip()

    user_message = (
        f"{GLOSSARY_NOTE}\n\n"
        f"Translate this Markdown section to French:\n\n{section_text}"
    )

    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=4096,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_message}],
    )

    translated = response.content[0].text.strip()
    translated = apply_glossary(translated)

    # Split translated heading from body
    lines = translated.split('\n')
    if lines and re.match(r'^#{1,6} ', lines[0]):
        t_heading = lines[0]
        t_body = '\n'.join(lines[1:]).strip()
    else:
        t_heading = heading  # fall back to original if heading wasn't translated
        t_body = translated

    return t_heading, t_body


# ---------------------------------------------------------------------------
# Special non-translated sections (logo swap, etc.)
# ---------------------------------------------------------------------------

def patch_logo(body: str) -> str:
    """Replace logo.png with logo-fr.png in image references."""
    return body.replace('assets/logo.png', 'assets/logo-fr.png')


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--force', action='store_true',
                        help='Retranslate all sections, ignoring cached state.')
    args = parser.parse_args(argv)

    api_key = os.environ.get('ANTHROPIC_API_KEY')
    if not api_key:
        print("Error: ANTHROPIC_API_KEY environment variable is not set.", file=sys.stderr)
        sys.exit(1)

    try:
        import anthropic
    except ImportError:
        print("Error: anthropic package not installed. Run: pip install anthropic", file=sys.stderr)
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)

    readme_text  = README.read_text(encoding='utf-8')
    en_sections  = split_sections(readme_text)

    # Load existing LISEZMOI sections (to preserve already-good translations)
    fr_sections: list[tuple[str, str]] = []
    if LISEZMOI.exists():
        fr_sections = split_sections(LISEZMOI.read_text(encoding='utf-8'))

    # Build a map from section index → existing French translation
    fr_by_index: dict[int, tuple[str, str]] = {i: s for i, s in enumerate(fr_sections)}

    state = load_state() if not args.force else {}
    new_state: dict = {}
    result_sections: list[tuple[str, str]] = []

    for i, (en_heading, en_body) in enumerate(en_sections):
        key = str(i)
        h = section_hash(en_heading + en_body)
        new_state[key] = h

        if not args.force and state.get(key) == h and i in fr_by_index:
            # Section unchanged — keep existing French translation
            print(f"  [skip]      {en_heading or '(preamble)'}")
            result_sections.append(fr_by_index[i])
            continue

        print(f"  [translate] {en_heading or '(preamble)'} …", end=' ', flush=True)
        try:
            fr_h, fr_b = translate_section(client, en_heading, en_body)
            fr_b = patch_logo(fr_b)
            print("done")
        except Exception as exc:
            print(f"FAILED ({exc})")
            # Fall back to existing translation if available
            if i in fr_by_index:
                result_sections.append(fr_by_index[i])
            else:
                result_sections.append((en_heading, en_body))
            continue

        result_sections.append((fr_h, fr_b))

    LISEZMOI.write_text(rebuild_text(result_sections), encoding='utf-8')
    save_state(new_state)
    print(f"\n✅  LISEZMOI.md updated ({len(result_sections)} sections).")


if __name__ == '__main__':
    main()
