import json
import click
from triplea.schemas.article import Article
from triplea.service.repository.export.engine import export_engine
from triplea.service.repository.export.unified_export_json import json_converter_01
from triplea.service.repository.export.unified_export_json.convert import Converter
from triplea.utils.general import safe_csv
from config import OUTPUT_DIR


# ROOT = pathlib.Path(__file__).resolve().parent.parent


def fx_filter(article:Article):
    # return True
    # if article.Topics is not None:
    #     if len(article.Topics) > 0:
    #         return True

    for i in article.ReviewLLM:
        if i['TemplateID'] == "extract-topic":
            r = i['Response']
            if 'StringContent' in r:
                return False
            else:
                return True

    # Finally
    return False


def fx_transform(article:Article):
    # convert article info into unified format
    ainfo = json_converter_01(article)

    output = {}


    output['title'] = safe_csv(ainfo["title"])
    output['year'] = ainfo["year"]
    output['pmid'] = ainfo["pmid"]

    
    list_keywords = []
    if ainfo["keywords"] is not None:
        for k in ainfo["keywords"]:
            list_keywords.append(safe_csv(k.Text))
    output['keywords'] = list_keywords

    list_topic = []
    if ainfo["topics"] is not None:
        for t in ainfo["topics"]:
            list_topic.append(safe_csv(t['text']))
    # output['topics'] = list_topic
    output['textrank_topics'] = list_topic

    # For LLM
    # output['extract-topic_SP'] = None
    # output['extract-topic_topics'] = None
    output['llm_topics']= None


    # Custom fields from LLM review
    for i in article.ReviewLLM:
        if i['TemplateID'] == "extract-topic":
            r = i['Response']
            if 'StringContent' in r:
                pass
                # output['extract-topic_SP'] = 1
                # # output['extract-topic_SP'] = safe_csv(r['ErrorMsg'])
            else:
                # output['extract-topic_topics'] = r['Topics']
                output['llm_topics'] = r['Topics']

    return output


def fx_output(output):
    if output !="":
        return output
    else:
        return ""
    

if __name__ == "__main__":
    ol = export_engine(fx_filter,fx_transform,fx_output,
                       limit_sample=0,
                       proccess_bar=True)
    print()
    print(f"{len(ol)} Articles selected and transform.")
    
    # DATA_FILE = ROOT / "output" / "dataset_llm_topic.json"
    DATA_FILE = OUTPUT_DIR / "dataset.json"
    with open(DATA_FILE, 'w') as fp:
        json.dump(ol, fp)


