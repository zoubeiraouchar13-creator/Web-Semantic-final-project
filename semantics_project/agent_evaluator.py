import os
from rdflib import Graph, Namespace, OWL

class AlignmentEvaluator:
    def __init__(self, system_alignment_path):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.system_graph = Graph().parse(os.path.join(base_dir, system_alignment_path), format="turtle")
        
        # Définition manuelle du Gold Standard (Le corrigé idéal attendu)
        self.gold_standard = {
            ("https://schema.org/NewsArticle", "http://www.bbc.co.uk/ontologies/news/NewsItem", "class"),
            ("https://schema.org/Organization", "http://www.bbc.co.uk/ontologies/news/Agency", "class"),
            ("https://schema.org/author", "http://www.bbc.co.uk/ontologies/news/creator", "property"),
            ("https://schema.org/datePublished", "http://www.bbc.co.uk/ontologies/news/dateCreated", "property") # On attendait celui-là !
        }

    def _extract_system_alignments(self):
        """Extrait les alignements trouvés par notre pipeline sous forme de set."""
        system_alignments = set()
        
        # Extraction des classes équivalentes
        for s, p, o in self.system_graph.triples((None, OWL.equivalentClass, None)):
            system_alignments.add((str(s), str(o), "class"))
            
        # Extraction des propriétés équivalentes
        for s, p, o in self.system_graph.triples((None, OWL.equivalentProperty, None)):
            system_alignments.add((str(s), str(o), "property"))
            
        return system_alignments

    def compute_metrics(self):
        system_set = self._extract_system_alignments()
        gold_set = self.gold_standard
        
        # Calcul des Vrais Positifs (TP), Faux Positifs (FP) et Faux Négatifs (FN)
        true_positives = system_set.intersection(gold_set)
        false_positives = system_set.difference(gold_set)
        false_negatives = gold_set.difference(system_set)
        
        tp = len(true_positives)
        fp = len(false_positives)
        fn = len(false_negatives)
        
        # Calcul des formules standard
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
        
        print("📊 === RAPPORT D'ÉVALUATION DU PIPELINE MULTI-AGENTS ===")
        print(f"✅ Vrais Positifs (Trouvés avec raison) : {tp}")
        print(f"❌ Faux Positifs (Hallucinations/Erreurs) : {fp}")
        print(f"📉 Faux Négatifs (Manqués par le LLM)    : {fn}")
        print("-" * 50)
        print(f"🎯 PRÉCISION : {precision:.2%}")
        print(f"🎯 RAPPEL    : {recall:.2%}")
        print(f"🏆 F1-SCORE  : {f1_score:.2%}")
        print("-" * 50)
        
        if fn:
            print("💡 Conseil pour le rapport : Le LLM a manqué les correspondances suivantes :")
            for item in false_negatives:
                print(f"   -> {item[0].split('/')[-1]} <--> {item[1].split('/')[-1]}")

if __name__ == "__main__":
    evaluator = AlignmentEvaluator("data/alignment_result.ttl")
    evaluator.compute_metrics()