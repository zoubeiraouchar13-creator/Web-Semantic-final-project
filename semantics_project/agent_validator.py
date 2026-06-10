import os
from rdflib import Graph, URIRef, Namespace
from rdflib.namespace import OWL, RDF
from agent_semantic import AgentSemantic

class AgentValidator:
    def __init__(self, confidence_threshold=0.7):
        self.threshold = confidence_threshold
        self.alignment_graph = Graph()
        self.alignment_graph.bind("owl", OWL)
        self.alignment_graph.bind("schema", Namespace("https://schema.org/"))
        self.alignment_graph.bind("bbc", Namespace("http://www.bbc.co.uk/ontologies/news/"))

    def validate_and_serialize(self, pairs):
        """Prend les paires préparées, appelle le LLM et génère le fichier RDF."""
        semantic_agent = AgentSemantic()
        alignments_found = 0
        
        print("🤖 [Agent Sémantique] Analyse des correspondances en cours...")
        for pair in pairs:
            label_a = pair["entity_a"]["label"]
            label_b = pair["entity_b"]["label"]
            
            decision = semantic_agent.evaluate_pair(pair)
            
            if decision and decision.get("equivalent") is True:
                confidence = decision.get("confidence", 0.0)
                if confidence >= self.threshold:
                    print(f"   ✅ Alignement Validé : {label_a} <--> {label_b} (Confiance: {confidence})")
                    print(f"      ↳ Raison : {decision.get('reason')}")
                    
                    uri_a = URIRef(decision["uri_a"])
                    uri_b = URIRef(decision["uri_b"])
                    
                    if decision["type"] == "class":
                        self.alignment_graph.add((uri_a, OWL.equivalentClass, uri_b))
                    elif decision["type"] == "property":
                        self.alignment_graph.add((uri_a, OWL.equivalentProperty, uri_b))
                        
                    alignments_found += 1
                else:
                    print(f"   ⚠️ Alignement Rejeté (Confiance faible : {confidence}) pour {label_a} / {label_b}")
            else:
                print(f"   ❌ Aucun alignement pour : {label_a} / {label_b}")
                
        base_dir = os.path.dirname(os.path.abspath(__file__))
        output_file = os.path.join(base_dir, "data", "alignment_result.ttl")
        self.alignment_graph.serialize(destination=output_file, format="turtle")
        print("--------------------------------------------------")
        print(f"💾 [Agent Valideur] Alignements sauvegardés dans : {output_file}")