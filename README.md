# Alignement d'Ontologies Assisté par LLM (Pipeline Multi-Agents)

* **Projet :** Réconciliation et interopérabilité des flux d'actualités internationaux (Schema.org ↔ BBC News)

---

## 📝 Présentation du Projet
Ce projet implémente une architecture multi-agents autonome capable d'aligner des ontologies hétérogènes décrivant le domaine des médias. En combinant la puissance algorithmique de graph-parsing de `RDFLib` avec les capacités cognitives et contextuelles d'un Grand Modèle de Langage (LLM) via l'API Groq, le système identifie, valide et sérialise les équivalences de classes et de propriétés selon les standards du W3C.

### Objectifs atteints :
* **Collecte autonome** et mise en cache des fragments d'ontologies au format Turtle (`.ttl`).
* **Extraction structurelle** des classes et des propriétés via requêtes ciblées.
* **Prompt Engineering avancé** pour éliminer les hallucinations.
* **Génération automatique** de triplets d'alignements standardisés (`owl:equivalentClass`, `owl:equivalentProperty`).
* **Évaluation scientifique** automatique des performances (Précision, Rappel, F1-Score) face à un *Gold Standard*.

---

## Architecture Multi-Agents

Le framework est découpé en agents logiciels à responsabilité unique, pilotés par un orchestrateur central :

1. **`AgentOrchestrator` :** Le chef d'orchestre. Centralise la logique globale, gère le cycle de vie du pipeline et la tolérance aux pannes.
2. **`AgentCollector` :** Assure le téléchargement et la gestion du cache local des schémas sources.
3. **`AgentAnalyst` :** Parse les fichiers RDF et prépare le produit cartésien des paires candidates.
4. **`AgentSemantic` :** Interroge le LLM (`llama-3.1-8b-instant`) en utilisant un format de réponse JSON strict et un raisonnement pas à pas.
5. **`AgentValidator` :** Applique le seuil de confiance ($\ge 0.70$) et écrit le fichier d'alignement RDF final.
6. **`AgentEvaluator` :** Compare le résultat au corrigé idéal et génère le rapport statistique.

---

## Résultats de l'Évaluation (Métriques Finales)

Grâce aux itérations successives d'ingénierie de prompt (notamment l'introduction de contraintes d'exclusion métier), le pipeline affiche d'excellentes performances :

* **Vrais Positifs (TP) :** 4
* **Faux Positifs (FP) :** 0 (Aucune hallucination)
* **Faux Négatifs (FN) :** 0

| Métrique | Score obtenu |
| :--- | :---: |
| **Précision** | **100.00 %** |
| **Rappel (Recall)** | **100.00 %** |
| **F1-Score** | **100.00 %** |

---

## Installation et Utilisation

### Prérequis
Assurez-vous d'avoir Python 3.10+ installé ainsi qu'une clé d'API Groq valide.
