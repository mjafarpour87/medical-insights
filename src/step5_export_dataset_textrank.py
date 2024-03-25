import json
import click
from triplea.schemas.article import Article
from triplea.service.repository.export.engine import export_engine
from triplea.service.repository.export.unified_export_json import json_converter_01
from triplea.service.repository.export.unified_export_json.convert import Converter
from triplea.utils.general import safe_csv
import os
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent


def fx_filter(article:Article):
    # return True
    if article.Topics is not None:
        if len(article.Topics) > 0:
            return True           
    # Finally
    return False

def harmonization_string_field(f):
    if isinstance(f,str):
        output = []
        if f.__contains__(','):
            list_f = f.split(',')
            for i in list_f:
                output.append(safe_csv(i.strip()))
        elif f.__contains__(' or '):
            list_f = f.split(' or ')
            for i in list_f:
                output.append(safe_csv(i.strip()))
        elif f.__contains__(' and '):
            list_f = f.split(' and ')
            for i in list_f:
                output.append(safe_csv(i.strip()))
        else:        
            output = [safe_csv(f)]
    elif isinstance(f,list):
        output = f
    elif f is None:
        output = None
    else:
        # print()
        # print(f"in harmonization_string_field - {f} with type {type(f)} is unhandel.")
        output = ['Can not parse.']

    return output

def fx_transform(article:Article):
    # convert article info into unified format
    ainfo = json_converter_01(article)

    output = {}

    # General one to one info of article
    output['title'] = safe_csv(ainfo["title"])
    output['year'] = ainfo["year"]
    # output['publisher'] = safe_csv(ainfo["publisher"])
    # output['journal_issn'] = ainfo["journal_issn"]
    # output['journal_iso_abbreviation'] = safe_csv(ainfo["journal_iso_abbreviation"])
    # output['language'] = safe_csv(ainfo["language"])
    # output['publication_type'] = safe_csv(ainfo["publication_type"])
    # output['url'] = ainfo["url"]
    # output['abstract'] = safe_csv(ainfo["abstract"])
    # output['doi'] =safe_csv( ainfo["doi"])
    output['pmid'] = ainfo["pmid"]
    # output['state'] = ainfo["state"]
    # output['citation_count'] = ainfo["citation_count"]

    # # General one to many info of article
    # output['authors'] = ainfo["authors"]
    
    # list_keywords = []
    # if ainfo["keywords"] is not None:
    #     for k in ainfo["keywords"]:
    #         list_keywords.append(safe_csv(k.Text))
    # output['keywords'] = list_keywords

    list_topic = []
    if ainfo["topics"] is not None:
        for t in ainfo["topics"]:
            list_topic.append(safe_csv(t['text']))
    output['topics'] = list_topic

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
    
    DATA_FILE = ROOT / "output" / "dataset_textrank.json"
    with open(DATA_FILE, 'w') as fp:
        json.dump(ol, fp)








