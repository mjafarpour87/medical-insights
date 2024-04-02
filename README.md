# medical-insights




<br>

---

⚠️ **WARNING:** This experimental project is under rapid development and lacks basic safeguards. Until a stable `1.0` release, **ONLY** run this repository on devices without sensitive information or access to paid services. ⚠️

---

<br>

# How to use


## Install from source

Clone repository:
```shell
git clone https://github.com/mjafarpour87/medical-insights.git
```

or 

```shell
git clone git@github.com:mjafarpour87/medical-insights.git
```

Create environment variable:
```shell
python -m venv venv
```

Activate environment variable:

*Windows*
```sh
$ .\venv\Scripts\activate
```

*Linux*
```sh
$ source venv/bin/activate
```


```sh
pip install -r requirements.txt
```

You can install last version of triplea with this command
```sh
pip install git+https://github.com/EhsanBitaraf/triple-a.git
```

```sh
python -m spacy download en_core_web_sm
```

For run web view of article:

*Windows*
```sh
streamlit run web.py --server.port 7186
```

## Run Step to Step

|#     |File Name            |Description|
|-|-|-|
|Step 1|step1_check_config.py|Check TripleA Configuration|
|step 2|step2_get_pubmed.py||
|Step 3|step3_move_state_forward.py||
|Step 4|step4_extract_topic_textrank.py|Extract topic from abstract and title with method textrank|
|Step 5|step5_extract_topic_with_llm.py|Extract topic from abstract and title with LLM|
|Step 6|step6_repair_response.py|Repair Json format in response of LLM|
|Step 7|step7_export_dataset.py|Export Dataset|

step3
step4
step10.2
step10.4
step11
step12
step13
step14



|method|Graph Nodes|Graph Edges|Graph Average Degree|Graph Density         |Graph Average Clustering Coefficient|Graph Degree Assortativity Coefficient|Components|
|------|-----------|-----------|--------------------|----------------------|------------------------------------|--------------------------------------|----------|
|LLM   |45806      |357482     |7.804261450465004   |0.00034076024235192684|0.9052766558811535                  |-0.06969792652358299|514|
|Keyword|15555     |337659      |21.707425265188043 |0.0027912338003327816 |0.8692939688222773|-0.1513162822347413|69|
|Textrank|41185|288024|6.9934199344421515|0.00033961829518464216|0.8905241147162223|-0.07659374291256468|86|



g_textrank_topic
Elapsed Time Calculation Report : 34.7201886177063
Graph Type: Undirected
Graph Nodes: 41185
Graph Edges: 288024
Graph Average Degree : 6.9934199344421515
Graph Density : 0.00033961829518464216
Graph Transitivity : 0.050903166471327685
Graph max path length : NaN
Graph Average Clustering Coefficient : 0.8905241147162223
Graph Degree Assortativity Coefficient : -0.07659374291256468
Graph Radius : NaN Found infinite path length because the graph is not connected
SCC: Can not calculate in undirected graph.
WCC: Can not calculate in undirected graph.
Reciprocity : Can not calculate in undirected graph.
Graph Diameter : 
Number of Components : 86

g_llm_topic
Elapsed Time Calculation Report : 44.90726280212402
Graph Type: Undirected
Graph Nodes: 45806
Graph Edges: 357482
Graph Average Degree : 7.804261450465004
Graph Density : 0.00034076024235192684
Graph Transitivity : 0.062294261111459366
Graph max path length : NaN
Graph Average Clustering Coefficient : 0.9052766558811535
Graph Degree Assortativity Coefficient : -0.06969792652358299
Graph Radius : NaN Found infinite path length because the graph is not connected
SCC: Can not calculate in undirected graph.
WCC: Can not calculate in undirected graph.
Reciprocity : Can not calculate in undirected graph.
Graph Diameter : 
Number of Components : 514

g_keyword
Elapsed Time Calculation Report : 125.76658606529236
Graph Type: Undirected
Graph Nodes: 15555
Graph Edges: 337659
Graph Average Degree : 21.707425265188043
Graph Density : 0.0027912338003327816
Graph Transitivity : 0.045427854941359314
Graph max path length : NaN
Graph Average Clustering Coefficient : 0.8692939688222773
Graph Degree Assortativity Coefficient : -0.1513162822347413
Graph Radius : NaN Found infinite path length because the graph is not connected
SCC: Can not calculate in undirected graph.
WCC: Can not calculate in undirected graph.
Reciprocity : Can not calculate in undirected graph.
Graph Diameter : 
Number of Components : 69






# Article


# Contributors

[![01 project contributors](https://contrib.rocks/image?repo=OpenInterpreter/01&max=2000)](https://github.com/OpenInterpreter/01/graphs/contributors)

Please see our [contributing guidelines](CONTRIBUTING.md) for more details on how to get involved.