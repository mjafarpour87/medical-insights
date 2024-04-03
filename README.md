# medical-insights
This Repo design for article that submmit in [MIE 2024](https://mie2024.org/)



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
|Step 1|step01_check_config.py|Check TripleA Configuration|
|step 2|step02_get_pubmed.py||
|Step 3|step03_move_state_forward.py||
|Step 4|step04_extract_topic_textrank.py|Extract topic from abstract and title with method textrank|
|Step 5|step05_extract_topic_with_llm.py|Extract topic from abstract and title with LLM|
|Step 6|step06_repair_response.py|Repair Json format in response of LLM|
|Step 7|step07_export_dataset.py|Export Dataset|
|Step 8|step08_generate_co_occurrence_graph.py|Generate Co-occurrence graph and export graphml and vosviewer|




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

3-7

|Graph Nodes|Graph Edges|Graph Average Degree|Graph Density|Graph Transitivity|Graph Average Clustering Coefficient|Graph Degree Assortativity Coefficient|Graph Radius|Number of Components|
|-|-|-|-|-|-|-|-|-|
|180|1869|10.383333333333333|0.11601489757914339|0.33822583239504583|0.6287495176290473|-0.26864279905481586|2|1|
|1106|23179|20.95750452079566|0.037932134879268165|0.18028782814226374|0.8656427256105894|-0.3634106013533251|1|1|
|85|441|5.188235294117647|0.12352941176470589|0.35589388001205907|0.5677863710428314|-0.14805472645939238|2|1|

0-7

|Graph Nodes|Graph Edges|Graph Average Degree|Graph Density|Graph Transitivity|Graph Average Clustering Coefficient|Graph Degree Assortativity Coefficient|Graph Radius|Number of Components|
|-|-|-|-|-|-|-|-|-|
|45741|356983|7.80444240397018|0.00034125240069830256|0.062251828346278654|0.9051982234160808|-0.06977365378359335|NaN|509|
|10995|248968|22.643747157798998|0.004119291824231217|0.11401194246943137|0.823940403480553|-0.2240567505762541|NaN|2|
|37023|270895|7.316938119547308|0.00039527514016246063|0.054351639999606426|0.8842263711703248|-0.07624538974062134|NaN|43|


# Article


# Contributors

[![01 project contributors](https://contrib.rocks/image?repo=OpenInterpreter/01&max=2000)](https://github.com/OpenInterpreter/01/graphs/contributors)

Please see our [contributing guidelines](CONTRIBUTING.md) for more details on how to get involved.