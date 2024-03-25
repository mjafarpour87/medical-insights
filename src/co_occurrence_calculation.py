



from collections import defaultdict
import json
import os
import pathlib
import networkx as nx
import random
import click
from triplea.service.click_logger import logger
from triplea.config.settings import SETTINGS


ROOT = pathlib.Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT / "output"

class CoCalculator:
    proccess_bar = True
    data = []
    keyword_co_occurrence_matrix = defaultdict(int)
    topics_co_occurrence_matrix = defaultdict(int)


#region Basic Table
    _topic_normalize_data = [
        ("test","test1")
    ]

    _topic_blacklist = [
        "=",
        "+"
    ]


    _keyword_normalize_data = [
        ("test","test1")
    ]

    _keyword_blacklist = [
        "test1",
    ]

#endregion    

    def set_data(self,data_list):
        self.data = data_list

    def _normalize_topic(self, topic_text:str):
        if topic_text == "":
            return ""
        topic = str.lower(topic_text)
        for a,b in self._topic_normalize_data:
            if topic == str.lower(a):
                return b

        return topic_text

    def _topic_in_blacklist(self, topic_text:str):
        if topic_text == "":
            return False
        topic = str.lower(topic_text)        
        for t in self._topic_blacklist:
            if str.lower(t) == topic:
                return True
        return False

    def _normalize_topics(self,topics):
        new_topics = []
        topics = list(dict.fromkeys(topics))
        for t in topics:
            t = str.lower(t)
            ts = str.split(t," ")
            for topic in ts: # Delete like '='
                if len(topic) < 2:
                    pass
                else:
                    new_topics.append(topic)
        return new_topics

    def _normalize_keyword(self, keyword_text:str):
        if keyword_text == "":
            return ""
        keyword = str.lower(keyword_text)
        for a,b in self._keyword_normalize_data:
            if keyword == str.lower(a):
                return str.lower(b)

        return str.lower(keyword_text)

    def _keyword_in_blacklist(self, keyword_text:str):
        if keyword_text == "":
            return False
        keyword = str.lower(keyword_text)
        for t in self._keyword_blacklist:
            if str.lower(t) == keyword:
                return True
        return False    

    def _co_occurring_topics(self, topics):
        for i in range(len(topics)):
            for j in range(i+1, len(topics)):
                self.topics_co_occurrence_matrix[(topics[i], topics[j])] += 1

    def _co_occurring_keywords(self, keywords):
        for i in range(len(keywords)):
            for j in range(i+1, len(keywords)):
                self.keyword_co_occurrence_matrix[(keywords[i], keywords[j])] += 1

    def calculate_all(self):
        if self.proccess_bar:
            bar = click.progressbar(length=len(self.data),
                                    show_pos=True,
                                    show_percent=True)
        n = 0 
        for a in self.data:
            n = n + 1
            if self.proccess_bar:
                bar.label = f"""{n} Article(s) calculated."""
                bar.update(1)
            else:
                if n % SETTINGS.AAA_CLI_ALERT_POINT == 0:
                    logger.INFO(f"{n} Article(s) exported.")


            # analyze the co-occurring keywords
            self._co_occurring_keywords(a['keywords'])    

            # analyze the co-occurring topics
            a['new_topics'] = self._normalize_topics(a['topics'])
            self._co_occurring_topics(a['new_topics'])


    def export_vos_viewer_topics_co_occurring(self,
                                                filename:str,
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
        with open(os.path.join(OUTPUT_DIR ,filename), 'w') as outfile:
            json.dump(graph_data, outfile, indent=4)


    def export_vos_viewer_keywords_co_occurring(self,
                                                filename:str,
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
        with open(os.path.join(OUTPUT_DIR ,filename), 'w') as outfile:
            json.dump(graph_data, outfile, indent=4)

