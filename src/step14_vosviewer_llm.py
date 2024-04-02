from collections import defaultdict
import json
import os
import pathlib
from matplotlib import pyplot as plt
import networkx as nx
import random
import click
from triplea.service.click_logger import logger
from triplea.config.settings import SETTINGS
import json
import pathlib

import click
from co_occurrence_calculation import OUTPUT_DIR, CoCalculator


ROOT = pathlib.Path(__file__).resolve().parent.parent


c = CoCalculator()

llm_topics_co_occurrence_matrix = defaultdict(int)

with open(ROOT / "output" / "dataset_llm_topic.json" ) as json_file:
    data = json.load(json_file)

def _co_occurring_llm_topics(topics):
    for i in range(len(topics)):
        for j in range(i+1, len(topics)):
            llm_topics_co_occurrence_matrix[(topics[i], topics[j])] += 1


def _normalize_llm_topics(self,topics):
    new_topics = []
    topics = list(dict.fromkeys(topics))
    for t in topics:
        t = str.lower(t)
        # # If you can split
        # ts = str.split(t," ")
        # for topic in ts: # Delete like '='
        #     if len(topic) < 4:
        #         pass
        #     else:
        #         new_topics.append(topic)

        # for total
        if len(t) < 2:
            pass
        else:
            new_topics.append(t)

    return c._emmanuel(new_topics)


def calculate_all():
    proccess_bar = True
    if proccess_bar:
        bar = click.progressbar(length=len(data),
                                show_pos=True,
                                show_percent=True)
    n = 0 
    for a in data:
        n = n + 1
        if proccess_bar:
            bar.label = f"""{n} Article(s) calculated."""
            bar.update(1)
        else:
            if n % SETTINGS.AAA_CLI_ALERT_POINT == 0:
                logger.INFO(f"{n} Article(s) exported.")


        # analyze the co-occurring topics from LLM
        if isinstance(a['extract-topic_topics'],list):
            a['new_topics'] = c._normalize_topics(a['extract-topic_topics'])
            _co_occurring_llm_topics(a['new_topics'])
        else:
            print("not List")


def export_vos_viewer_llm_topics_co_occurring(
                                            filename:str,
                                            link_weight_limit = 0,
                                            degree_limit= 0 ):
    G = nx.Graph()
    # Add nodes and edges based on co-occurrence matrix
    for pair, count in llm_topics_co_occurrence_matrix.items():
        keyword1, keyword2 = pair
        if c._topic_in_blacklist(keyword1) or c._topic_in_blacklist(keyword2):
            pass
        else:
            # keyword1 = self._normalize_topic(keyword1)
            # keyword2 = self._normalize_topic(keyword2)
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

    # Draw the graph
    # pos = nx.spring_layout(G)  # positions for all nodes
    pos = nx.spring_layout(G)
    plt.clf()
    # nx.draw(G, pos, with_labels=True, node_size=7000, font_size=10, node_color='skyblue', edge_color='gray', width=2, edge_cmap=plt.cm.Blues)
    
    # Adjust figure size to accommodate the graph without overlap
    plt.figure(figsize=(15, 16))

    nx.draw(G,
            pos,
            with_labels=False,
            node_size=4,
            # node_color=[G.nodes[n]['color'] for n in G.nodes],
            edge_color=[G[u][v]['weight'] for u, v in G.edges])
    plt.show()
    plt.title("LLM Topics Co-occurrence Graph")
    plt.axis("off")
    # plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR ,"llm_topics_co_occurrence.png"),bbox_inches='tight')

if __name__ == "__main__":

    

    #------------------------------Manual Calcularion of LLM Topics------------
    calculate_all()
    export_vos_viewer_llm_topics_co_occurring("vos_topicllm.json",
                                            degree_limit= 3,
                                            link_weight_limit=7)
    

    #------------------------------Manual Calcularion of LLM Topics------------