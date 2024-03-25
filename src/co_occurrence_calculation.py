



from collections import defaultdict
import json
import os
import networkx as nx
import random


class CoCalculator:
    proccess_bar = True
    data = []
    keyword_co_occurrence_matrix = defaultdict(int)
    topics_co_occurrence_matrix = defaultdict(int)

    def set_data(self,data_list):
        self.data = data_list

    def co_occurring_topics(self, topics):
        for i in range(len(topics)):
            for j in range(i+1, len(topics)):
                self.topics_co_occurrence_matrix[(topics[i], topics[j])] += 1

    def co_occurring_keywords(self, keywords):
        for i in range(len(keywords)):
            for j in range(i+1, len(keywords)):
                self.keyword_co_occurrence_matrix[(keywords[i], keywords[j])] += 1

    def export_vos_viewer_topics_co_occurring(self,
                                                 link_weight_limit = 0,
                                                 degree_limit= 0 ):
        G = nx.Graph()
        # Add nodes and edges based on co-occurrence matrix
        for pair, count in self.topics_co_occurrence_matrix.items():
            keyword1, keyword2 = pair
            if self._topic_in_blacklist(keyword1) or self._topic_in_blacklist(keyword2):
                pass
            else:
                keyword1 = self._normalize_topic(keyword1)
                keyword2 = self._normalize_topic(keyword2)
                if link_weight_limit == 0: # unlimited
                    G.add_edge(keyword1, keyword2, weight=count)
                else:
                    if  count > link_weight_limit:  
                        G.add_edge(keyword1, keyword2, weight=count)

        print(G.number_of_nodes())
        # Remove nodes with degree less than 10
        nodes_to_remove = [node for node, degree in dict(G.degree()).items() if degree < degree_limit]
        G.remove_nodes_from(nodes_to_remove)

        print(G.number_of_nodes())
        graph_data = {
        "network": {
            "items": [{"id": node,
                        "label": node,
                        "x": round(random.uniform(-1.1515,0.200),4),
                        "y": round(random.uniform(-1.1515,0.200),4)} for node, node_name in G.nodes(data="label")],
            "links": [{"source_id": source, "target_id": target, "strength": data["weight"]} for source, target, data in G.edges(data=True)]
        }
    }

        # Convert the dictionary to JSON format and save it to a file
        with open(os.path.join(OUTPUT_DIR ,"vos_viewer_topics_co_occurrence.json"), 'w') as outfile:
            json.dump(graph_data, outfile, indent=4)


    def export_vos_viewer_keywords_co_occurring(self,
                                                 link_weight_limit = 0,
                                                 degree_limit= 0 ):
        G = nx.Graph()
        # Add nodes and edges based on co-occurrence matrix
        for pair, count in self.keyword_co_occurrence_matrix.items():
            keyword1, keyword2 = pair
            if self._keyword_in_blacklist(keyword1) or self._keyword_in_blacklist(keyword2):
                pass
            else:
                keyword1 = self._normalize_keyword(keyword1)
                keyword2 = self._normalize_keyword(keyword2)
                if link_weight_limit == 0: # unlimited
                    G.add_edge(keyword1, keyword2, weight=count)
                else:
                    if  count > link_weight_limit:  
                        G.add_edge(keyword1, keyword2, weight=count)

        print(G.number_of_nodes())
        # Remove nodes with degree less than 10
        nodes_to_remove = [node for node, degree in dict(G.degree()).items() if degree < degree_limit]
        G.remove_nodes_from(nodes_to_remove)

        print(G.number_of_nodes())
        graph_data = {
        "network": {
            "items": [{"id": node,
                        "label": node,
                        "x": round(random.uniform(-1.1515,0.200),4),
                        "y": round(random.uniform(-1.1515,0.200),4)} for node, node_name in G.nodes(data="label")],
            "links": [{"source_id": source, "target_id": target, "strength": data["weight"]} for source, target, data in G.edges(data=True)]
        }
    }

        # Convert the dictionary to JSON format and save it to a file
        with open(os.path.join(OUTPUT_DIR ,"vos_viewer_keyword_co_occurrence.json"), 'w') as outfile:
            json.dump(graph_data, outfile, indent=4)

