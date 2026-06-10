from rdflib import Graph, RDF, OWL, RDFS

class AgentAnalyst:
    def __init__(self, ontology_a_path, ontology_b_path):
        self.g_a = Graph().parse(ontology_a_path, format="turtle")
        self.g_b = Graph().parse(ontology_b_path, format="turtle")

    def _extract_entities(self, graph):
        """Extrait les classes et propriétés avec leurs labels et commentaires."""
        entities = {"classes": [], "properties": []}
        
        # Extraction des Classes
        for s in graph.subjects(RDF.type, OWL.Class):
            label = graph.value(s, RDFS.label) or s.split("/")[-1]
            comment = graph.value(s, RDFS.comment) or "Aucune description disponible."
            entities["classes"].append({"uri": str(s), "label": str(label), "comment": str(comment)})
            
        # Extraction des Propriétés (Datatype et Object)
        for p_type in [OWL.DatatypeProperty, OWL.ObjectProperty]:
            for s in graph.subjects(RDF.type, p_type):
                label = graph.value(s, RDFS.label) or s.split("/")[-1]
                comment = graph.value(s, RDFS.comment) or "Aucune description disponible."
                entities["properties"].append({"uri": str(s), "label": str(label), "comment": str(comment)})
                
        return entities

    def prepare_matching_tasks(self):
        """Génère les paires à comparer (Classes vs Classes et Propriétés vs Propriétés)."""
        ent_a = self._extract_entities(self.g_a)
        ent_b = self._extract_entities(self.g_b)
        
        tasks = []
        
        # Appariement des classes
        for ca in ent_a["classes"]:
            for cb in ent_b["classes"]:
                tasks.append({"type": "class", "entity_a": ca, "entity_b": cb})
                
        # Appariement des propriétés
        for pa in ent_a["properties"]:
            for pb in ent_b["properties"]:
                tasks.append({"type": "property", "entity_a": pa, "entity_b": pb})
                
        return tasks

# Test de l'Agent Analyste
if __name__ == "__main__":
    analyst = AgentAnalyst("data/schema_news.ttl", "data/bbc_news.ttl")
    pairs_a_comparer = analyst.prepare_matching_tasks()
    print(f"📊 L'Agent Analyste a préparé {len(pairs_a_comparer)} paires à analyser par le LLM.")
    print("Exemple de paire :", pairs_a_comparer[0])