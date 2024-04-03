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
from config import OUTPUT_DIR


ROOT = pathlib.Path(__file__).resolve().parent.parent


#region Basic Table
_topic_normalize_data = [
    ("test","test1")
]

_topic_blacklist = [
    "=",
    "+",
    "patients",
    "breast cancer",
    "breast",
    "treatment",
    "cancer",
    "women",
    "therapy",
    "breast cancer patients",
    "breast neoplasms",
    "humans",
    "female",
    "male",
    "animals",
    "mice",
    "adult",
    "aged",
    "middle aged",
]




#endregion    


llm_topics_co_occurrence_matrix = defaultdict(int)
keyword_co_occurrence_matrix = defaultdict(int)
textrank_topics_co_occurrence_matrix = defaultdict(int)

with open(ROOT / "output" / "dataset.json" ) as json_file:
    data = json.load(json_file)

def _emmanuel(d: list) -> list:
    """Base on [this](https://stackoverflow.com/questions/9427163/remove-duplicate-dict-in-list-in-python)

    Args:
        d (list): _description_

    Returns:
        list: _description_
    """
    return [i for n, i in enumerate(d) if i not in d[n + 1 :]]

def _co_occurring_llm_topics(topics):
    for i in range(len(topics)):
        for j in range(i+1, len(topics)):
            llm_topics_co_occurrence_matrix[(topics[i], topics[j])] += 1

def _co_occurring_keywords(keywords):
    for i in range(len(keywords)):
        for j in range(i+1, len(keywords)):
            keyword_co_occurrence_matrix[(keywords[i], keywords[j])] += 1

def _co_occurring_topics(topics):
    for i in range(len(topics)):
        for j in range(i+1, len(topics)):
            textrank_topics_co_occurrence_matrix[(topics[i], topics[j])] += 1

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

    return _emmanuel(new_topics)


def _correct_topic_list(topics):
    new_topics = []
    topics = list(dict.fromkeys(topics))
    for t in topics:
        t = str.lower(t)

        for a,b in _topic_normalize_data:
            if t == str.lower(a):
                t = b
        for black in _topic_blacklist:
            if str.lower(black) == t:
                t = ""
                        
        # for total
        if len(t) < 2:
            pass
        else:
            new_topics.append(t)

    return _emmanuel(new_topics)

def generate_co_occurring_matrix():
    proccess_bar = True
    if proccess_bar:
        bar = click.progressbar(length=len(data),
                                show_pos=True,
                                show_percent=True)
    n = 0
    print(len(data))
    for a in data:
        n = n + 1
        if proccess_bar:
            bar.label = f"""{n} Article(s) calculated."""
            bar.update(1)
        else:
            if n % SETTINGS.AAA_CLI_ALERT_POINT == 0:
                logger.INFO(f"{n} Article(s) exported.")


        # analyze the co-occurring topics from LLM
        if isinstance(a['llm_topics'],list):
            _co_occurring_llm_topics(_correct_topic_list(a['llm_topics']))
        else:
            print("not List")

        
        # analyze the co-occurring keywords
        _co_occurring_keywords(_correct_topic_list(a['keywords']))

        # analyze the co-occurring topics from TextRank
        _co_occurring_topics(_correct_topic_list(a['textrank_topics']))



def matrix2graph(matrix,
                 link_weight_limit = 0,
                 degree_limit= 0):
    G = nx.Graph()
    # Add nodes and edges based on co-occurrence matrix
    for pair, count in matrix.items():
        keyword1, keyword2 = pair
        if link_weight_limit == 0: # unlimited
            G.add_edge(keyword1, keyword2, weight=count)
        else:
            if  count > link_weight_limit:  
                G.add_edge(keyword1, keyword2, weight=count)

    # Remove nodes with degree less than degree_limit
    nodes_to_remove = [node for node, degree in dict(G.degree()).items() if degree < degree_limit]
    G.remove_nodes_from(nodes_to_remove)
    return G

def graph2vos(G):
    graph_data = {
    "network": {
        "items": [{"id": node,
                    "label": node,
                    "x": round(random.uniform(-1.1515,0.200),4),
                    "y": round(random.uniform(-1.1515,0.200),4)} for node, node_name in G.nodes(data="label")],
        "links": [{"source_id": source, "target_id": target, "strength": data["weight"]} for source, target, data in G.edges(data=True)]
    }
    }
    return graph_data
    
# def export_vos_viewer_llm_topics_co_occurring(
#                                             filename:str,
#                                             link_weight_limit = 0,
#                                             degree_limit= 0 ):
#     G = nx.Graph()
#     # Add nodes and edges based on co-occurrence matrix
#     for pair, count in llm_topics_co_occurrence_matrix.items():
#         keyword1, keyword2 = pair
#         if c._topic_in_blacklist(keyword1) or c._topic_in_blacklist(keyword2):
#             pass
#         else:
#             # keyword1 = self._normalize_topic(keyword1)
#             # keyword2 = self._normalize_topic(keyword2)
#             if link_weight_limit == 0: # unlimited
#                 G.add_edge(keyword1, keyword2, weight=count)
#             else:
#                 if  count > link_weight_limit:  
#                     G.add_edge(keyword1, keyword2, weight=count)

#     print(G.number_of_nodes())
#     # Remove nodes with degree less than 10
#     nodes_to_remove = [node for node, degree in dict(G.degree()).items() if degree < degree_limit]
#     G.remove_nodes_from(nodes_to_remove)

#     print(G.number_of_nodes())
#     graph_data = {
#     "network": {
#         "items": [{"id": node,
#                     "label": node,
#                     "x": round(random.uniform(-1.1515,0.200),4),
#                     "y": round(random.uniform(-1.1515,0.200),4)} for node, node_name in G.nodes(data="label")],
#         "links": [{"source_id": source, "target_id": target, "strength": data["weight"]} for source, target, data in G.edges(data=True)]
#     }
# }

#     # Convert the dictionary to JSON format and save it to a file
#     with open(os.path.join(OUTPUT_DIR ,filename), 'w') as outfile:
#         json.dump(graph_data, outfile, indent=4)

#     # Draw the graph
#     # pos = nx.spring_layout(G)  # positions for all nodes
#     pos = nx.spring_layout(G)
#     plt.clf()
#     # nx.draw(G, pos, with_labels=True, node_size=7000, font_size=10, node_color='skyblue', edge_color='gray', width=2, edge_cmap=plt.cm.Blues)
    
#     # Adjust figure size to accommodate the graph without overlap
#     plt.figure(figsize=(15, 16))

#     nx.draw(G,
#             pos,
#             with_labels=False,
#             node_size=4,
#             # node_color=[G.nodes[n]['color'] for n in G.nodes],
#             edge_color=[G[u][v]['weight'] for u, v in G.edges])
#     plt.show()
#     plt.title("LLM Topics Co-occurrence Graph")
#     plt.axis("off")
#     # plt.tight_layout()
#     plt.savefig(os.path.join(OUTPUT_DIR ,"llm_topics_co_occurrence.png"),bbox_inches='tight')

if __name__ == "__main__":
    from triplea.service.graph.analysis.info import info
   
    lwl = 3
    dl = 7
    info_list = []
    #------------------------------Manual Calcularion of LLM Topics------------
    print("Generate Co-occurring Matrix start...")
    generate_co_occurring_matrix()
    print("Generate Co-occurring Matrix end")
    
    print("Generate Co-occurring LLM Graph start...")
    g_llm_topic = matrix2graph(llm_topics_co_occurrence_matrix,
                 link_weight_limit = lwl,
                 degree_limit= dl)
    print("Generate Co-occurring LLM Topic Graph end.")
    info_list.append(info(g_llm_topic,"json"))

    print("Generate Co-occurring Keyword Graph start...")
    g_keyword = matrix2graph(keyword_co_occurrence_matrix,
                 link_weight_limit = lwl,
                 degree_limit= dl)
    print("Generate Co-occurring Keyword Graph end.")
    info_list.append(info(g_keyword,"json"))

    print("Generate Co-occurring TextRank Topic Graph start...")
    g_textrank_topic = matrix2graph(textrank_topics_co_occurrence_matrix,
                 link_weight_limit = lwl,
                 degree_limit= dl)
    print("Generate Co-occurring TextRank Topic Graph end.")
    info_list.append(info(g_textrank_topic,"json"))


    with open(os.path.join(OUTPUT_DIR ,"info.json"), 'w') as outfile:
        json.dump(info_list, outfile, indent=4)

    # # Export graphml Format
    # print("Export Graphml format file start ...")
    # nx.write_graphml(g_llm_topic, os.path.join(OUTPUT_DIR ,"llm_topic.grapml"))
    # nx.write_graphml(g_keyword, os.path.join(OUTPUT_DIR ,"keyword.grapml"))
    # nx.write_graphml(g_textrank_topic, os.path.join(OUTPUT_DIR ,"textrank_topic.grapml"))
    # print("Export Graphml format file end.")
        

    # Convert the dictionary to JSON format and save it to a file for VOSviewer
    dict_g_llm_topic = graph2vos(g_llm_topic)
    dict_g_keyword = graph2vos(g_keyword)
    dict_g_textrank_topic = graph2vos(g_textrank_topic)

    with open(os.path.join(OUTPUT_DIR ,"vos_topic_llm.json"), 'w') as outfile:
        json.dump(dict_g_llm_topic, outfile, indent=4)

    with open(os.path.join(OUTPUT_DIR ,"vos_keyword.json"), 'w') as outfile:
        json.dump(dict_g_keyword, outfile, indent=4)

    with open(os.path.join(OUTPUT_DIR ,"vos_topic_textrank.json"), 'w') as outfile:
        json.dump(dict_g_textrank_topic, outfile, indent=4)


    # export_vos_viewer_llm_topics_co_occurring("vos_topicllm.json",
    #                                         degree_limit= 3,
    #                                         link_weight_limit=7)
    

    #------------------------------Manual Calcularion of LLM Topics------------