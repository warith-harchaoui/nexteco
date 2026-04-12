# NextEco

Prompts de programmation pour ajouter une estimation des coûts honnête à n'importe quel dépôt logiciel.

![NextEco](assets/logo-fr.png)


Insérez l'un de ces prompts [core.md](core.md) ou [advanced.md](advanced.md) dans votre IDE : VS Code (Copilot Agent), Cursor, Antigravity, Windsurf, Claude Code ou tout autre outil de programmation agentique. L'IA auditora votre dépôt et implémentera une fonctionnalité « Coût de fonctionnement » reproductible et testée, couvrant :
  + 💰 l'argent
  + 🪫 l'énergie
  + 💨 le $\text{CO}_2$

L'ambition de ce dépôt est d'incarner les bonnes pratiques d'estimation des coûts selon six dimensions :
1. *reproductibilité* : l'estimation des coûts peut être régénérée à partir du code et des artefacts versionnés
2. *honnêteté* : les inconnues restent clairement marquées comme inconnues et les hypothèses sont explicites
3. *traçabilité* : chaque chiffre a une provenance claire
4. *testabilité* : les formules et la synchronisation du README sont vérifiées par des tests (déjà une bonne pratique en développement)
5. *pertinence opérationnelle* : l'unité de travail canonique est significative pour les utilisateurs et les opérateurs réels
6. *minimalisme* : la solution reste légère, pratique et exempte de toute posture (trop souvent répandu sur ces sujets)

---

## Doctrine pour le coût de fonctionnement

> A. Les tests prouvent que le livrable fonctionne.
>
> B. L'IA identifie le coût et son unité de travail canonique.
>
> C. Le benchmark mesure ce coût.
>
> D. Le profileur explique ce coût. *(Avancé uniquement)*

---

## Le problème que ces prompts résolvent

La plupart des dépôts n'ont pas de réponse honnête à : *« Combien coûte réellement l'exécution de ce logiciel ? »*

L'estimation des coûts est un aspect fastidieux et négligé du développement logiciel. Ces prompts résolvent ce problème en fournissant un moyen simple et efficace d'ajouter une estimation honnête des coûts à n'importe quel dépôt. Le résultat est un modèle de coûts immédiatement utile et honnête sur ce qu'il ne sait pas.




## Quel prompt utiliser

Deux prompts similaires sont disponibles :
  + [core.md](core.md) orienté tests
  + [advanced.md](advanced.md) orienté tests avec une approche par profileur

| Situation | Utiliser |
|---|---|
| Tout dépôt nécessitant une estimation honnête des coûts | **Core** |
| Le temps d'exécution, la mémoire ou l'énergie sont une préoccupation principale pour les utilisateurs/opérateurs | **Advanced** |
| Un benchmark existe déjà dans le dépôt | **Advanced** |
| Vous souhaitez un profilage pour expliquer l'origine des coûts | **Advanced** |

En cas de doute, commencez par Core. Vous pouvez toujours relancer Advanced plus tard.

---

## Ce que l'agent produira

Les deux prompts demandent à l'agent de créer ou mettre à jour :

| Fichier | Objectif |
|---|---|
| `README.md` | Section `## Coût de fonctionnement` avec tableau de scénarios, hypothèses, méthodologie |
| `cost_of_running.yaml` | Source de vérité unique pour toutes les données de coût |
| `scripts/update_cost_of_running.py` (ou équivalent) | Script auxiliaire pour régénérer la section README depuis le YAML |
| Fichiers de tests | Tests cohérents avec les formules, validation YAML, vérification de synchronisation README |
| Fichier de benchmark | Benchmark reproductible ciblant l'unité de travail canonique |
| `scripts/profile_*.py` (Avancé uniquement, si justifié) | Script de profilage léger |
| `AGENTS.md` (si présent) | Note de maintenance pour les agents futurs |

---

## Comment utiliser

**Claude Code :**
```bash
claude "$(cat core.md)"
# ou
claude "$(cat advanced.md)"
```

**Cursor / Antigravity / Windsurf / VS Code Agent :**
Ouvrez le chat de l'agent, collez le contenu de [`core.md`](core.md) ou [`advanced.md`](advanced.md) et envoyez.

**Tout autre outil agentique :**
Collez le contenu du prompt dans l'entrée de l'agent. Le prompt est autonome.

---

## Principes de conception

Ces prompts ont été conçus à partir de quelques leçons difficiles :

**L'honnêteté prime sur l'exhaustivité.** L'agent est explicitement invité à préférer `TODO` à des chiffres inventés. Un espace réservé honnête est plus utile qu'un mensonge confiant.

**Les tests ne sont pas facultatifs.** Tout modèle de coûts créé par l'agent doit être soutenu par des tests cohérents avec les formules. Si `total_usd = local_compute_usd + api_usd`, un test vérifie cette arithmétique.

**Une seule unité de travail canonique.** L'agent en choisit exactement une et la justifie. Plusieurs tableaux concurrents créent de la confusion.

**Valeurs par défaut conservatrices.** En l'absence de données, l'agent utilise des hypothèses conservatrices et les indique clairement.

**Empreinte minimale.** Pas de tableaux de bord, pas de télémétrie, pas d'infrastructure lourde. Le mécanisme le plus léger possible pour maintenir le modèle de coûts à jour.

---

## Le schéma YAML

Les deux prompts produisent un `cost_of_running.yaml` avec cette structure :

```yaml
date_updated: YYYY-MM-DD
unit_of_work:
  name: "une invocation CLI"
  description: "..."
  rationale: "..."
methodology:
  approach: "Inspiré de Green Algorithms"
  formula_notes:
    - "energy_kwh = runtime_hours * average_power_kw"
    - "carbon_gco2e = energy_kwh * carbon_intensity_gco2e_per_kwh"
  benchmark:
    status: "measured|not_run|TODO"
assumptions:
  electricity:
    usd_per_kwh: 0.12
    status: "estimated"   # measured | estimated | placeholder
scenarios:
  - name: "typical"
    per_unit:
      runtime_s: 4.2
      energy_kwh: 0.00023
      total_usd: 0.0042
      carbon_gco2e: 0.11
    data_quality: "medium"  # low | medium | high
todos:
  - "TODO: valider le temps d'exécution avec powermetrics sur le matériel cible"
```

Le champ `status` sur les hypothèses décrit la provenance des données. Le champ `data_quality` sur les scénarios décrit la confiance globale dans les chiffres de ce scénario. Ils sont intentionnellement distincts.

---

## Méthodologie

Les deux prompts utilisent une méthodologie [Green Algorithms](https://calculator.green-algorithms.org/ai) :

$$
E_{\text{kWh}} = t_{\text{h}} \times P_{\text{kW}}
$$

$$
C_{\text{USD}} = E_{\text{kWh}} \times p_{\text{USD/kWh}}
$$

$$
\text{CO}_2\text{e}_{\text{g}} = E_{\text{kWh}} \times I_{\text{gCO}_2\text{e/kWh}}
$$

| Symbole | Signification | Unité |
|---|---|---|
| $E_{\text{kWh}}$ | Énergie consommée | kWh |
| $t_{\text{h}}$ | Temps d'exécution réel | heures |
| $P_{\text{kW}}$ | Puissance moyenne du matériel | kW |
| $C_{\text{USD}}$ | Coût électrique du calcul local | USD |
| $p_{\text{USD/kWh}}$ | Prix de l'électricité | USD / kWh |
| $\text{CO}_2\text{e}_{\text{g}}$ | Empreinte carbone | g CO₂e |
| $I_{\text{gCO}_2\text{e/kWh}}$ | Intensité carbone du réseau électrique | g CO₂e / kWh |

Toutes les formules sont explicites dans le YAML et vérifiées par des tests.

---

## Pitch *(style Guy Kawasaki)*

#### ⚠️ Problème / Opportunité
- La plupart des dépôts sont livrés sans aucune donnée honnête sur les coûts — ni argent, ni énergie, ni carbone.
- Les agents IA interrogés naïvement inventent des chiffres vraisemblables avec une fausse confiance.
- Les équipes ne découvrent le manque que lorsqu'un opérateur demande « combien coûte réellement l'exécution de ce logiciel ? »

#### 💎 Proposition de valeur
- Insérez un prompt, obtenez un modèle de coûts reproductible et testé en quelques minutes.
- Honnête par conception : une taxonomie stricte — **mesuré / estimé / provisoire / TODO** — prévient les chiffres hallucinés.
- Fonctionne avec n'importe quel outil agentique (Claude Code, Cursor, Copilot Agent, Windsurf…).

#### 🧪 Ingrédient secret
- Une seule unité de travail canonique ancre chaque chiffre à quelque chose de mesurable.
- Le YAML est la source de vérité ; la section README en est générée.
- Des tests cohérents avec les formules détectent toute dérive entre le modèle et la documentation.

#### 💰 Modèle économique
- Les prompts sont le produit — gratuits, ouverts, domaine public ([The Unlicense](https://unlicense.org)).
- Les modèles de coûts produits sont des actifs versionnés appartenant à l'équipe du dépôt.
- Pas de télémétrie, pas de SaaS, pas de dépendance propriétaire.

#### 📣 Marketing
- Storytelling : *« Combien coûte réellement l'exécution de ce logiciel ? »*
- Démo : lancez le prompt sur n'importe quel dépôt → obtenez un tableau de coûts honnête en une passe.
- Positionnement : « Un espace réservé honnête vaut mieux qu'un mensonge confiant. »

#### 🦅 Concurrence
- Sections README écrites à la main (obsolètes, non vérifiées, non testées).
- Requêtes IA naïves (chiffres hallucinés, pas de taxonomie, pas de tests).
- Infrastructure lourde de suivi des coûts (tableaux de bord, agents de télémétrie, factures cloud).

---

## Contribuer

Issues et PR bienvenues. Les prompts sont le produit — gardez les modifications focalisées sur l'amélioration du comportement de l'agent, pas sur l'ajout d'infrastructure.

Lors de la modification d'un prompt, testez-le sur au moins un dépôt réel avant de soumettre.

---

## Auteur

[Warith Harchaoui](https://www.linkedin.com/in/warith-harchaoui/), docteur et directeur de l'IA chez [NEXTON](https://nexton-group.com)

---

## Remerciements

Ce projet est né de discussions avec :
  + [Yann Lechelle](https://www.linkedin.com/in/ylechelle), dirigeant et cofondateur de [probabl.ai](https://probabl.ai), la société derrière `scikit-learn`
  + [Laurent Panatanacce](https://www.linkedin.com/in/panatanacce), mon mentor en affaires et facilitateur IA chez [NEXTON](https://nexton-group.com)


---

## Licence

[The Unlicense](https://unlicense.org) — domaine public, sans conditions. Voir [LICENSE](LICENSE).
