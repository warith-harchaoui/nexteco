# Contributing

Thanks for wanting to improve these prompts.

## Ground rules

- **The prompts are the product.** Don't add tooling, CI, or infrastructure that doesn't directly improve agent behavior.
- **Test before submitting.** Run the prompt against at least one real repository. Describe what changed in agent output in your PR.
- **Honesty over completeness.** If a change makes the agent produce more confident-looking output at the cost of accuracy, it's not a good change.

## What makes a good change

- Fixes a case where the agent invented a number it shouldn't have
- Improves disambiguation (e.g. the `data_quality` vs `status` rename)
- Adds a language to a toolchain table
- Adds a missing edge case (e.g. monorepo guidance)
- Improves the final report structure
- Fixes a wording ambiguity that caused inconsistent agent behavior

## What to avoid

- Adding new deliverables that increase the agent's footprint without clear benefit
- Weakening the "never invent" rules
- Making the prompts longer without improving agent behavior
- Adding CI, linting, or testing infrastructure to this repo itself

## Submitting

Open a PR with:
1. The change
2. A one-sentence description of the problem it solves
3. What you observed in agent output before and after

That's it.
