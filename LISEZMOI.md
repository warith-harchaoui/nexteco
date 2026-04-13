# NextEco

NextEco rend le **coût de fonctionnement** du code.

[🇺🇸](README.md)&nbsp;[🇫🇷](LISEZMOI.md)


![NextEco](assets/logo-fr.png)

NextEco est un **framework d'ingénierie prêt pour les agents** qui ajoute une fonctionnalité **Coût de fonctionnement** reproductible et testée à n'importe quelle base de code.

Il aide les équipes à estimer et documenter le coût de fonctionnement d'un logiciel selon quatre dimensions :

- 💰 **argent**
- ⏱️ **temps**
- 🪫 **énergie**
- 💨 **carbone**

en s'appuyant sur des artefacts d'ingénierie auxquels les développeurs font déjà confiance :

- formules explicites
- benchmarks reproductibles
- programmation pilotée par les tests et donc des sorties testables
- fichiers sources versionnés
- gestion honnête de l'incertitude

Pour l'estimation carbone, NextEco utilise une méthodologie transparente et auditable, alignée avec des références telles que [Green Algorithms](https://calculator.green-algorithms.org/ai) et des routines OS de bas niveau comme `powermetrics` sur macOS et leurs équivalents sur les autres systèmes.

Ce n'est **pas** un tableau de bord.  
Ce n'est **pas** du théâtre RSE pour les certif.  
Ce ne sont **pas** des chiffres d'une IA hallucinée.

NextEco aide les agents de codage à intégrer directement un modèle de coûts dans votre dépôt, de sorte que le résultat soit :

- vérifiable
- reproductible
- adossé à un benchmark
- intégré aux tests
- maintenable dans le temps

Collez un prompt dans Cursor, Claude Code, Copilot Agent, Antigravity, Windsurf ou un autre IDE agentique.  
L'agent audite votre dépôt et construit la couche d'estimation des coûts directement dans la base de code.

> **Combien coûte réellement l'exécution de mon code ?**

À mesure que les logiciels deviennent plus gourmands en calcul, en modèles et en APIs, les équipes doivent comprendre l'empreinte opérationnelle de ce qu'elles livrent :

- Combien coûte une requête ?
- Combien coûte un job ?
- Combien coûte une inférence ?
- Combien coûte un entraînement IA ?
- Où l'énergie est-elle gaspillée ?
- Quelle part revient au calcul local et quelle part aux dépenses d'API externes ?
- Quelles hypothèses sont mesurées et lesquelles sont des estimations provisoires ?

C'est le problème que NextEco résout.

> **Traiter l'estimation des coûts comme de l'ingénierie, pas comme de l'administratif ou du marketing.**

Cela signifie :

- une seule source de vérité
- une seule unité de travail canonique
- des formules explicites
- des hypothèses mesurables
- des données de temps d'exécution adossées à un benchmark
- une documentation générée
- une programmation pilotée par les tests pour l'arithmétique et la synchronisation
- des `TODO` honnêtes plutôt qu'une fausse confiance

---

## Le pitch

**NextEco transforme « Combien coûte l'exécution de ceci ? » en une fonctionnalité reproductible et testée dans le dépôt.**

### ⚠️ Problème / Opportunité
- La plupart des dépôts sont livrés sans aucune donnée honnête sur les coûts — ni argent, ni temps, ni énergie, ni carbone.
- Les agents IA interrogés naïvement inventent des chiffres vraisemblables avec une fausse confiance.
- Les équipes ne découvrent généralement le manque que lorsqu'un opérateur demande : *« Combien coûte réellement l'exécution de ce logiciel ? »*

### 💎 Proposition de valeur
- Insérez un prompt, obtenez un modèle de coûts reproductible et testé en quelques minutes.
- Honnête par conception : une taxonomie stricte — **mesuré / estimé / provisoire / TODO** — prévient les chiffres hallucinés.
- Fonctionne avec n'importe quel outil agentique (Claude Code, Cursor, Copilot Agent, Windsurf…).

### 🧪 Ingrédient secret
- Une seule unité de travail canonique ancre chaque chiffre à quelque chose de mesurable.
- Le YAML est la source de vérité ; la section README en est générée.
- Des tests cohérents avec les formules détectent toute dérive entre le modèle et la documentation.
- Des benchmarks et des profils in situ avec des routines OS bas niveau (powermetrics, etc.)

### 💰 Modèle économique
- Les prompts sont le produit — gratuits, ouverts, domaine public ([The Unlicense](https://unlicense.org)).
- Les modèles de coûts produits sont des actifs versionnés appartenant à l'équipe du dépôt.
- Pas de télémétrie, pas de SaaS, pas de dépendance propriétaire.

### 📣 Marketing
- Storytelling : *« Combien coûte réellement l'exécution de ce logiciel ? »*
- Démo : lancez le prompt sur n'importe quel dépôt → obtenez un tableau de coûts honnête en une passe.
- Positionnement : *« Un espace réservé honnête vaut mieux qu'un mensonge confiant. »*

### 🦅 Concurrence
- Sections README écrites à la main (obsolètes, non vérifiées, non testées).
- Requêtes IA naïves (chiffres hallucinés, pas de taxonomie, pas de tests).
- Infrastructure lourde de suivi des coûts (tableaux de bord, agents de télémétrie, factures cloud).

---

## Pourquoi les ingénieurs l'apprécient

### Honnête
Si l'agent ne connaît pas un chiffre, il doit le dire.

Il utilise des statuts tels que :

- `measured`
- `estimated`
- `placeholder`
- `TODO`

Un modèle de coûts devient vérifiable plutôt que théâtral.

### Léger
Pas de tableaux de bord. Pas de SaaS. Pas de dépendance propriétaire.

Juste un petit ensemble de fichiers, de scripts, de tests et de documentation à l'intérieur du dépôt.

### Piloté par les tests
Si le modèle dit :

```text
total_usd = local_compute_usd + external_api_usd
```

le dépôt doit contenir un test qui le vérifie.

### Pertinent opérationnellement
NextEco oblige l'agent à choisir une **unité de travail canonique**, par exemple :

- une invocation CLI
- une requête API
- une vidéo traitée
- un job d'entraînement
- un rapport généré

Sans cet ancrage, les tableaux de coûts ne sont généralement que du bruit.

---

## Ce que vous obtenez

Lancez un prompt et l'agent crée ou met généralement à jour :

| Fichier | Objectif |
|---|---|
| `README.md` | Section `Coût de fonctionnement` gérée, avec hypothèses, scénarios et méthode |
| `cost_of_running.yaml.example` | **Critique :** modèle de config de déploiement (matériel et localisation) |
| `cost_of_running.yaml` | Source de vérité lisible par les machines |
| `scripts/update_cost_of_running.py` | Régénère la section README des coûts depuis le YAML |
| fichiers de tests | Vérifient les formules, la cohérence du schéma et la synchronisation README |
| fichier de benchmark | Mesure l'unité de travail canonique de manière reproductible |
| aide(s) au profilage | Expliquent l'origine des coûts *(avancé uniquement)* |
| `AGENTS.md` | Indications de maintenance pour les agents de codage futurs, si présent |

Le résultat n'est pas un rapport.  
C'est un **sous-système maintenable**.

---

## Deux modes

NextEco est livré avec deux niveaux de prompt :

- [`core.md`](core.md) : workflow d'estimation des coûts par défaut, axé sur les tests
- [`advanced.md`](advanced.md) : profilage plus approfondi et métrologie consciente du matériel

### Utiliser Core quand

- vous voulez le chemin le plus rapide vers quelque chose d'utile
- vous vous souciez davantage d'une structure fiable que d'un profilage approfondi
- vous souhaitez une estimation honnête des coûts dans n'importe quel dépôt

### Utiliser Advanced quand

- le temps d'exécution ou l'énergie est une préoccupation sérieuse pour le produit
- un benchmark existe déjà
- vous voulez expliquer l'origine des coûts, pas seulement reporter des totaux
- vous avez besoin d'un profilage plus approfondi ou d'une métrologie spécifique au matériel

En cas de doute, commencez par [`core.md`](core.md).

---

## Méthodologie

NextEco suit une doctrine simple :

> A. Les tests **prouvent** que le livrable fonctionne  
> B. L'IA **identifie** le coût et son unité de travail canonique  
> C. Le benchmark **mesure** ce coût  
> D. Le profileur **explique** ce coût *(Avancé uniquement)*

Le coût est traité comme une métrique logicielle, au même titre que la correction, la latence, la mémoire et la fiabilité.

Cela comprend au moins quatre dimensions :

- 💰 **argent**
- ⏱️ **temps**
- 🪫 **énergie**
- 💨 **carbone**

---

## Mathématiques simples, explicites et auditables

NextEco repose sur des formules simples que l'agent doit documenter et préserver.

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
| $E_{\mathrm{kWh}}$ | Énergie consommée | kWh |
| $t_{\mathrm{h}}$ | Temps d'exécution réel | h |
| $P_{\mathrm{kW}}$ | Puissance moyenne | kW |
| $C_{\mathrm{USD}}$ | Coût électrique du calcul local | USD |
| $p_{\mathrm{USD}/\mathrm{kWh}}$ | Prix de l'électricité | USD/kWh |
| $\mathrm{CO_2e}_{\mathrm{g}}$ | Empreinte carbone | g CO₂e |
| $I_{\mathrm{g\ CO_2e}/\mathrm{kWh}}$ | Intensité carbone du réseau électrique | g CO₂e/kWh |

L'objectif n'est pas la sophistication.  
L'objectif est la **clarté, l'auditabilité et la testabilité**.

---

## Métrologie

NextEco pousse l'agent vers une mesure locale réelle dès que possible, en utilisant des outils OS tels que :

- `powermetrics` sur macOS
- `powertop` sur Linux
- `powercfg` sur Windows

Lorsque la mesure n'est pas encore possible, le framework exige que l'agent le dise explicitement et laisse un espace réservé visible ou un `TODO`.

Ce n'est pas une faiblesse, c'est de l'hygiène scientifique.

---

## Exemple de schéma

Parce que l'intensité carbone du réseau varie considérablement à l'échelle mondiale (ex: France ~56 gCO₂e/kWh vs Australie ~620 gCO₂e/kWh) et que la consommation électrique diffère selon le matériel, NextEco oblige les développeurs à définir explicitement leur environnement.

Vous définissez le contexte matériel d'exécution et l'échelle de travail dans un fichier très commenté `cost_of_running.yaml.example` que les utilisateurs copient, modifient et enregistrent sous `cost_of_running.yaml` :

```yaml
deployment:
  provider: "unknown"        # ex : aws / gcp / azure / oracle / on-prem / local / unknown
  instance_type: "unknown"   # ex : m2-pro, p3.2xlarge, a2-highgpu-1g
  region: "unknown"          # ex : eu-west-1, us-central1, local
  country: "France"          # La définition explicite utilisée pour les tables de carbone/électricité

workload:
  type: "unknown"            # ex : training / inference / batch / api / unknown
  scale: "unknown"           # ex : one-off / daily / continuous / 1M_requests_month
```

Un fichier `cost_of_running.yaml` généré intègre cette base et peut ressembler à ceci :

```yaml
date_updated: YYYY-MM-DD

deployment:
  provider: "on-prem"
  instance_type: "custom-server"
  region: "local"
  country: "France"

workload:
  type: "inference"
  scale: "daily"

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
    status: "estimated"

scenarios:
  - name: "typical"
    per_unit:
      runtime_s: 4.2
      energy_kwh: 0.00023
      total_usd: 0.0042
      carbon_gco2e: 0.11
    data_quality: "medium"

todos:
  - "TODO: valider le temps d'exécution sur le matériel cible"
```

Deux distinctions importent :

- `status` décrit la provenance d'une hypothèse spécifique
- `data_quality` décrit la confiance globale dans le scénario dans son ensemble

Cette séparation maintient le modèle propre.

---

## Comment utiliser

### Claude Code

```bash
claude "$(cat core.md)"
# ou
claude "$(cat advanced.md)"
```

### Cursor / Windsurf / VS Code Agent / Copilot Agent

Ouvrez le chat de l'agent, collez le contenu de [`core.md`](core.md) ou [`advanced.md`](advanced.md) et envoyez.

### Tout autre outil de codage agentique

Collez le prompt complet dans l'entrée de l'agent.  
Les prompts sont conçus pour être autonomes.

---

## À qui s'adresse ce projet

NextEco est particulièrement pertinent pour :

- les équipes utilisant des APIs payantes
- les produits IA avec des coûts d'inférence non négligeables
- les outils développeurs avec un usage significatif de calcul local
- les workflows de données avec des jobs récurrents
- les dépôts où les utilisateurs ou les opérateurs se soucient de l'empreinte d'exécution
- les organisations d'ingénierie souhaitant des discussions crédibles sur la durabilité plutôt que du théâtre

---

## Ce que NextEco n'est pas

NextEco ne cherche pas à remplacer les plateformes de facturation cloud, les suites d'observabilité ou les systèmes d'entreprise de comptabilité carbone.

Il résout un problème plus précis :

> **Comment ajouter un modèle de coûts honnête, léger et de qualité ingénierie directement dans un dépôt logiciel.**

Cette étroitesse est l'une de ses forces.

---

## Contribuer

Issues et pull requests bienvenues.

Les prompts sont le produit.

Les bonnes contributions améliorent généralement un ou plusieurs des aspects suivants :

- le comportement de l'agent
- la reproductibilité
- la clarté
- la portabilité
- l'auditabilité
- la testabilité
- l'honnêteté face à l'incertitude

Lors de la modification d'un prompt, testez-le sur au moins un dépôt réel.

---

## Auteur

**Warith Harchaoui, Ph.D.**  

_Head of AI_ chez [NEXTON](https://nexton-group.com)

---

## Remerciements

Ce projet est né de discussions avec :

- [Yann Lechelle](https://www.linkedin.com/in/ylechelle), dirigeant et cofondateur de [probabl.ai](https://probabl.ai)
- [Laurent Panatanacce](https://www.linkedin.com/in/panatanacce), mentor en affaires et _AI Business Enabler_ chez [NEXTON](https://nexton-group.com)

---

## Licence

[The Unlicense](https://unlicense.org) — domaine public, sans conditions.  
Voir [LICENSE](LICENSE).
