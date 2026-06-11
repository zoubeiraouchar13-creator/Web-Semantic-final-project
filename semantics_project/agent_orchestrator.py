import os
import sys

from pydantic import validator

# Importation de l'ensemble de ton équipe d'agents
try:
    from agents.agent_collectors import AgentCollectorSchema, AgentCollectorBBC
    from agents.agent_analyst import AgentAnalyst
    from agents.agent_semantic import AgentSemantic
    from agents.agent_validator import AgentValidator
    from agents.agent_evaluator import AlignmentEvaluator
except ImportError as e:
    print(f"❌ Erreur d'importation des sous-agents : {e}")
    print("Vérifiez que tous vos fichiers d'agents sont bien dans le même dossier.")
    sys.exit(1)

class AgentOrchestrator:
    def __init__(self, confidence_threshold=0.7):
        self.confidence_threshold = confidence_threshold
        print("  [Agent Orchestrator] Initialisé et prêt à piloter l'équipe.")

    def run_full_pipeline(self):
        print("\n==================================================================")
        print("   [Agent Orchestrator] DÉMARRAGE DU PIPELINE D'ALIGNEMENT SÉMANTIQUE")
        print("==================================================================")

        # ÉTAPE 1 : Collecte des données (Agents Collectors)
        print("\n[Étape 1/4] Déploiement des Agents Collecteurs...")
        collector_schema = AgentCollectorSchema()
        collector_bbc = AgentCollectorBBC()
        
        success_schema = collector_schema.collect()
        success_bbc = collector_bbc.collect()
        
        if not success_schema or not success_bbc:
            print("❌ [Agent Orchestrator] Échec lors de la phase de collecte. Arrêt du pipeline.")
            return False
        print("➡️ [Agent Orchestrator] Étape 1 validée avec succès.")

        # ÉTAPE 2 : Analyse et préparation des tâches (Agent Analyst)
        print("\n[Étape 2/4] Déploiement de l'Agent Analyste (Parsing RDFLib)...")
        try:
            analyst = AgentAnalyst("data/schema_news.ttl", "data/bbc_news.ttl")
            pairs_to_analyze = analyst.prepare_matching_tasks()
            print(f"📊 [Agent Analyste] Extraction terminée. {len(pairs_to_analyze)} paires candidates identifiées.")
        except Exception as e:
            print(f"❌ [Agent Orchestrator] Échec de l'Agent Analyste : {e}")
            return False
        print("➡️ [Agent Orchestrator] Étape 2 validée avec succès.")

        # ÉTAPE 3 : Alignement LLM & Sérialisation (Agents Semantic & Validator)
        print("\n[Étape 3/4] Déploiement du duo Agent Sémantique & Agent Valideur...")
        # Note : On réutilise la structure de ton script validator qui intègre l'appel à l'agent sémantique
        try:
            # Vérification de sécurité pour la clé API avant de lancer les requêtes LLM
            if not os.environ.get("GROQ_API_KEY"):
                print("❌ [Agent Orchestrator] Erreur : La variable d'environnement GROQ_API_KEY n'est pas définie.")
                return False
                
            validator = AgentValidator(confidence_threshold=self.confidence_threshold)
            # On adapte légèrement l'appel pour exécuter uniquement la partie matching/validation
            # puisque la collecte a déjà été faite à l'étape 1
            validator = AgentValidator(confidence_threshold=self.confidence_threshold)
            validator.validate_and_serialize(pairs_to_analyze)
        except Exception as e:
            print(f"❌ [Agent Orchestrator] Échec durant la phase d'alignement/validation : {e}")
            return False
        print("➡️ [Agent Orchestrator] Étape 3 validée avec succès.")

        # ÉTAPE 4 : Évaluation métrique finale (Agent Evaluator)
        print("\n[Étape 4/4] Déploiement de l'Agent Évaluateur (Calcul de performance)...")
        try:
            evaluator = AlignmentEvaluator("data/alignment_result.ttl")
            evaluator.compute_metrics()
        except Exception as e:
            print(f"❌ [Agent Orchestrator] Échec de l'Agent Évaluateur : {e}")
            return False
        
        print("\n==================================================================")
        print("  [Agent Orchestrator] TOUTES LES TÂCHES ONT ÉTÉ EXÉCUTÉES AVEC SUCCÈS")
        print("==================================================================")
        return True

if __name__ == "__main__":
    # Paramétrage global : seuil de confiance fixé à 70%
    orchestrator = AgentOrchestrator(confidence_threshold=0.7)
    orchestrator.run_full_pipeline()