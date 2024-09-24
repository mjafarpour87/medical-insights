# Unveiling Medical Insights: Advanced Topic Extraction from Scientific Articles

This repository accompanies the research paper "Unveiling Medical Insights: Advanced Topic Extraction from Scientific Articles," which explores the use of advanced Natural Language Processing (NLP) techniques for extracting key topics from scientific literature, with a focus on breast cancer research. The work leverages the TextRank algorithm and Large Language Models (LLMs) using the TripleA tool to analyze and extract topics from nearly 10,000 scientific paper abstracts.

[![commits](https://badgen.net/github/commits/mjafarpour87/medical-insights/main)](https://github.com/mjafarpour87/medical-insights/commits/main?icon=github&color=green)
[![GitHub Last commit](https://img.shields.io/github/last-commit/mjafarpour87/medical-insights)](https://github.com/mjafarpour87/medical-insights/main)
![Open Issue](https://img.shields.io/github/issues-raw/mjafarpour87/medical-insights)

![Repo Size](https://img.shields.io/github/repo-size/mjafarpour87/medical-insights)

![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/mjafarpour87/medical-insights)

![Code Quality](https://github.com/mjafarpour87/medical-insights/actions/workflows/python-flake.yml/badge.svg)


<!-- TOC start (generated with https://github.com/derlin/bitdowntoc) -->

- [Key Features:](#key-features)
- [Usage](#usage)
- [Basic concept](#basic-concept)
   * [Topic Extraction](#topic-extraction)
   * [Co-ocurrence topic map](#co-ocurrence-topic-map)
- [How to use](#how-to-use)
   * [Install from source](#install-from-source)
   * [Run Step by Step](#run-step-by-step)
- [Dataset](#dataset)
- [GraphMl Files](#graphml-files)
- [Graph Info](#graph-info)
- [Article](#article)
- [Contributors](#contributors)
- [License](#license)

<!-- TOC end -->

# Key Features:
<ul>
<li>
<b>Data Extraction</b>: The repository includes scripts for retrieving and processing scientific paper abstracts using the PubMed API.
</li>
<li>
<b>Topic Extraction</b>: Implements TextRank and an open-source LLM (Mistral) to extract and compare topics from the abstracts.
</li>
<li>
<b>Graph Construction</b>: Generates co-occurrence graphs of extracted topics, enabling visualization and further analysis of relationships between key terms.
</li>
<li>
<b>Visualization</b>: Utilizes VOSviewer for visualizing the co-occurrence graphs, providing insights into trends and patterns within the data.
</li>
<li>
<b>Comparative Analysis</b>: The repository offers a comparative analysis of the performance of TextRank and LLMs in topic extraction, showing that LLMs tend to produce more clustered and interconnected topic networks.
</li>
</ul>

# Usage
The pipeline is designed for reproducibility, allowing researchers to apply the methodology to other domains or datasets.
Potential applications include bibliometric analysis, trend identification in research fields, and development of knowledge graphs for clinical decision support.
The full code, datasets, and documentation are available within this repository to facilitate further research and application in the biomedical field.








# Basic concept
## Topic Extraction
Topic Extraction, also known as "automatic topic discovery" or "topic modeling," is a text analysis technique used to identify the main themes or concepts in a collection of documents or a large text body. The goal is to automatically summarize and categorize the content by extracting the most relevant keywords, phrases, or topics, thereby enabling users to better understand and explore the information. Topic extraction algorithms detect patterns and probabilistically determine topics based on the frequency and distribution of words, as well as their co-occurrence in the text. These techniques help in a variety of applications, such as sentiment analysis, content recommendation, and search optimization.

## Co-ocurrence topic map
A Co-occurrence Topic Map is a visual representation of the relationships between topics, keywords, or concepts based on their co-occurrence within a collection of documents or a large text body. In a Co-occurrence Topic Map, topics that frequently appear together in the text are connected by lines, edges, or proximity, indicating a thematic or semantic relationship between the connected items. The map can be used to explore and analyze the structure and content of a text corpus, identify key themes or trends, and support navigation and knowledge discovery. This type of visualization can provide a comprehensive and intuitive overview of the data, revealing hidden patterns and enabling users to gain insights that might be difficult to discern from the raw text alone.

# How to use
If you want to use the outputs of this program and [this article](#article), you can use its dataset and perform other methods or other research on its data. [GraphMl files](#graphml-files) have been prepared for different co-occurrence graphs that you can use.
But if you want to start this program to generate a new dataset and get the outputs you want, you have to go through the pipeline steps completely. We have used [TripleA library](https://github.com/EhsanBitaraf/triple-a) in this program. We have explained this in the "[Install from source](#install-from-source)" section.

## Install from source

Clone repository:
```shell
git clone https://github.com/mjafarpour87/medical-insights.git
```

or 

```shell
git clone git@github.com:mjafarpour87/medical-insights.git
```

Create virtual environment:
```shell
python -m venv venv
```

Activate virtual environment:

*Windows*
```sh
$ .\venv\Scripts\activate
```

*Linux*
```sh
$ source venv/bin/activate
```

Install requirements:
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

<!-- For run web view of article:

*Windows*
```sh
streamlit run web.py --server.port 7186
``` -->

## Run Step by Step

|#     |File Name            |Description|
|-|-|-|
|Step 1|step01_check_config.py|Check TripleA Configuration|
|step 2|step02_get_pubmed.py|To retrieve relevant papers with minimum quality content, we used the search strategy keywords: `("Breast Cancer"[Title]) AND (Therapy[Title])`.|
|Step 3|step03_move_state_forward.py|In this step, "Triple A" operators were used to process paper metadata and content at different states, including extracting keywords and MeSH terms from the metadata.|
|Step 4|step04_extract_topic_textrank.py|Extract topic from abstract and title with method textrank|
|Step 5|step05_extract_topic_with_llm.py|Extract topic from abstract and title with LLM. In this step, a template has been used to extract topics from the abstract of the articles, which you can see [here](https://raw.githubusercontent.com/mjafarpour87/medical-insights/main/src/extract-topic.json). We used the [Mistral-7B-Instruct-v0.2](https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.2) model for this.|
|Step 6|step06_repair_response.py|Repair Json format in response of LLM|
|Step 7|step07_export_dataset.py|Export Dataset|
|Step 8|step08_generate_co_occurrence_graph.py|Generate Co-occurrence graph and export GraphMl and [VOSviewer](https://www.vosviewer.com/)|

# Dataset

In step 7, a dataset is formed that can be used in the next steps and various studies can be done on it.
This dataset includes the title of the article, the list of topics extracted using LLM and the topics extracted using the Textrank method, as well as the keywords of the article. In addition, this dataset can be downloaded from [here](https://doi.org/10.6084/m9.figshare.25533532). The format of the dataset is Json.

Below is the format of each article in the dataset as Json:

```json
{
        "title": "Review of recent preclinical and clinical research on ligand-targeted liposomes as delivery systems in triple negative breast cancer therapy.",
        "year": "2024",
        "pmid": "38520185",
        "keywords": [
            "Triple negative breast cancer",
            "drug carriers",
            "ligand-targeted liposomes",
            "liposome"
        ],
        "textrank_topics": [
            "TNBC treatment",
            "progressed TNBC treatment",
            "various treatment methods",
            "targeted treatment",
            "triple negative breast cancer therapy",
            "targeted drug carriers",
            "TNBC",
            "breast cancer patients",
            "appropriate treatment",
            "drug delivery"
        ],
        "llm_topics": [
            "Triple-negative breast cancer (TNBC)",
            "Chemotherapy",
            "Targeted treatment",
            "Liposomes",
            "Drug delivery",
            "Ligand-targeted liposomes",
            "TNBC therapy",
            "Preclinical research",
            "Clinical research",
            "MDR cancer cells"
        ]
    },

```

If you use this dataset in another scientific work, you can refer to it as follows:


> Bitaraf, Ehsan (2024). Topic Extraction Dataset. figshare. Dataset. https://doi.org/10.6084/m9.figshare.25533532


[![DOI:10.6084/m9.figshare.25533532](https://zenodo.org/badge/doi/10.6084/m9.figshare.25533532.svg)](https://doi.org/10.6084/m9.figshare.25533532)

# GraphMl Files
The output in [**GraphMl** format](http://graphml.graphdrawing.org/) has been extracted for all three co-occurrence graphs:

- Co-occurrence topic graphs (Topic Extraction with LLM) [GraphMl file](/output/llm_topic.grapml)
- Co-occurrence topic graphs (Topic Extraction with TextRank) [GraphMl file](/output/textrank_topic.grapml)
- Co-occurrence keyword graphs [GraphMl file](/output/keyword.grapml)



# Graph Info

|Method|Graph Nodes|Graph Edges|Graph Average Degree|Graph Density         |Graph Average Clustering Coefficient|Graph Degree Assortativity Coefficient|Components|
|------|-----------|-----------|--------------------|----------------------|------------------------------------|--------------------------------------|----------|
|LLM   |45806      |357482     |7.804261450465004   |0.00034076024235192684|0.9052766558811535                  |-0.06969792652358299|514|
|Keyword|15555     |337659      |21.707425265188043 |0.0027912338003327816 |0.8692939688222773|-0.1513162822347413|69|
|Textrank|41185|288024|6.9934199344421515|0.00033961829518464216|0.8905241147162223|-0.07659374291256468|86|

A comparison of the constructed topic/keyword co-occurrence networks with metrics.


<!-- 
 |Graph Nodes|Graph Edges|Graph Average Degree|Graph Density|Graph Transitivity|Graph Average Clustering Coefficient|Graph Degree Assortativity Coefficient|Graph Radius|Number of Components|
|-|-|-|-|-|-|-|-|-|
|45805|357225|7.798821089400721|0.00034053013227668854|0.062225593356894295|0.9052876260320849|-0.06974728372125498|NaN|514|
|13512|257502|19.05728241563055|0.0028210025039790616|0.1110493731105105|0.8443954256641666|-0.21809378726182685|NaN|39|
|41181|287947|6.99222942619169|0.00033959346411810057|0.050900985991725836|0.8905355367079815|-0.07659661402195801|NaN|86|

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
-->

Topic Co-occurrence network using TextRank Algorithm

![Topic Co-occurrence network using TextRank Algorithm](/assets/img/vos/fig1.png)

Topic Co-occurrence network using LLM

![Topic Co-occurrence network using LLM](/assets/img/vos/fig2.png)

Keyword co-occurrence network

![Keyword co-occurrence network](/assets/img/vos/fig3.png)


# Article
The [Paper](https://pubmed.ncbi.nlm.nih.gov/39176947/) is accepted and published at MIE 2024. To cite this work:

Bitaraf E, Jafarpour M, Shool S, Saboori Amleshi R. Unveiling Medical Insights: Advanced Topic Extraction from Scientific Articles. Stud Health Technol Inform. 2024 Aug 22;316:944-948. doi: 10.3233/SHTI240566. PMID: 39176947.

# Contributors

[![01 project contributors](https://contrib.rocks/image?repo=mjafarpour87/medical-insights)](https://github.com/mjafarpour87/medical-insights/graphs/contributors)

Made with [contrib.rocks](https://contrib.rocks).

Please see our [contributing guidelines](CONTRIBUTING.md) for more details on how to get involved.

---

# License

This Repository is available under the [MIT License](LICENSE).
