# Sample update response base of JSONDecodeError
# copy of sample_update_response_jsondecodererror
import json
from triplea.service.click_logger import logger
from bson import ObjectId
import click
from pymongo import MongoClient
import triplea.service.repository.persist as PERSIST
from triplea.schemas.article import Article
from triplea.config.settings import SETTINGS
from triplea.utils.general import print_error, print_pretty_dict


def get_list_id():
    _connection_url = SETTINGS.AAA_MONGODB_CONNECTION_URL
    client = MongoClient(_connection_url)
    db = client[SETTINGS.AAA_MONGODB_DB_NAME]
    col_article = db["articledata"]
    # myquery = {"ReviewLLM.Response.StringContent": {"$exists": True}}
    # myquery = {"ReviewLLM.TemplateID": "CardioBioBank1"}
    myquery = {
        "ReviewLLM.Response.StringContent": {"$exists": True},
        "ReviewLLM.TemplateID": "extract-topic",
    }
    cursor = col_article.find(
        myquery, projection={"SourceBank": "$SourceBank", "_id": 1}
    )
    # TODO _id

    la = list(cursor)
    new_la = []
    for c in la:
        new_la.append(c["_id"])

    if len(new_la) == 0:
        return []
    else:
        return new_la


def update_llm_response(document_id, template_id, new_response):
    _connection_url = SETTINGS.AAA_MONGODB_CONNECTION_URL
    client = MongoClient(_connection_url)
    db = client[SETTINGS.AAA_MONGODB_DB_NAME]
    col_article = db["articledata"]

    col_article.update_one(
        {"_id": ObjectId(document_id), "ReviewLLM.TemplateID": template_id},
        {"$set": {"ReviewLLM.$.Response": new_response}},
    )


def try_json_decoding(json_string):
    try:
        new_response = json.loads(json_string)
        return new_response
    except Exception as e:
        if isinstance(e, json.JSONDecodeError):
            # If you don't want try again
            new_response = {
                "StringContent": json_string,
                "ErrorMsg": e.msg,
                "colno": e.colno,
            }
            return new_response  # if you want update error message
            return None  # if you not want update error message
        else:
            new_response = {"StringContent": json_string, "ErrorMsg": type(e)}
            return new_response  # if you want update error message
            return None  # if you not want update error message


def error_analysis(response, json_error):
    if isinstance(json_error, json.JSONDecodeError):
        e = json_error
    else:
        print()
        print(f"Error type is not JSONDecodeError. It is {type(e)}.")
        return None

    if e.msg == "Expecting property name enclosed in double quotes":
        print()
        logger.WARNING(f"Error: {e.msg}")
        print(response)
        logger.DEBUG(response[0: e.colno - 2])
        logger.DEBUG("Please fix :")
        value = click.prompt("-->", type=str)
        response = response[0: e.colno - 2] + value
        print(response)
        new_response = try_json_decoding(response)
        if new_response is None:
            return None
        else:
            logger.WARNING("Fixed")
            return new_response
    elif e.msg == "Extra data":
        # "Sample" : "Over 300,000" }
        # Note: The sample size was not explicitly mentioned in the abstract,
        new_response = try_json_decoding(response[0: e.colno - 1])
        if new_response is None:
            return None
        else:
            return new_response
    elif e.msg == "Expecting ',' delimiter":
        pass
        # "Sample" : 285 (acute COVID-19)
        # + 77 (convalescent COVID-19)
        # + 54 (controls) = 316

        return None
    else:
        print()
        print(response)
        print(e.msg)
        return None


def check_error_for_sample_cut_it(response, json_error):
    if isinstance(json_error, json.JSONDecodeError):
        e = json_error
    else:
        print()
        print(f"Error type is not JSONDecodeError. It is {type(e)}.")
        return None

    response[0: e.colno - 1]
    start_tag = "Sample"
    tag_start = response.find(start_tag)
    if tag_start == -1:
        return None
    if e.colno > tag_start:
        tag_end = str.find(response, "}", tag_start)
        if len(response) - tag_end > 5:
            # print()
            # print("-----------------------------??------------")
            # print(response)
            # print("-----------------------------??------------")
            return None
        else:
            # print()
            # print(response)
            # print()
            sample_value = response[tag_start + len(start_tag) + 3: tag_end]
            new_response = response[0: tag_start + len(
                start_tag) + 3] + str(-3) + "}"
            new_response = try_json_decoding(new_response)
            if new_response is None:
                return None
            else:
                new_response["Sample1"] = sample_value
                # print_pretty_dict(new_response)
                return new_response
    else:
        return None


def repair_value_between_tag(text, start_tag, end_tag):
    tag_start = text.find(start_tag)
    if tag_start == -1:
        print("error")
        return ""
    tag_end = text.find(end_tag, tag_start + len(start_tag))
    v = text[tag_start + len(start_tag): tag_end]
    v = v.strip()
    if v.__contains__('"'):
        v = v.replace('"', "'")

    dic_str = f" {text[0:tag_start]} {start_tag}{v}{end_tag}"
    return dic_str


def fx_response_remodel(response):
    if isinstance(response, dict):
        if "StringContent" in response:
            # ------------------------Temporary----------------------------
            print_pretty_dict(response)
            return None
            # ------------------------Temporary----------------------------
            sc = response["StringContent"]
            if "ErrorMsg" in response:
                errormsg = response["ErrorMsg"]
                if errormsg == "Expecting ',' delimiter":
                    sc = rf"{sc}"
                    v = repair_value_between_tag(sc, '"description": "', '" }')
                    return try_json_decoding(v)
                elif errormsg == "Expecting value":
                    sc = rf"{sc}"
                    # start = sc.find('{"')
                    start = sc.find('{   "')
                    if start == -1:
                        start = sc.find('{    "')
                    if start == -1:
                        return None
                    # print(sc[start:len(sc)])
                    return try_json_decoding(sc[start: len(sc)])
                elif errormsg == "Extra data":
                    sc = sc[0: int(response["colno"]) - 1]
                    sc = rf"{sc}"
                    return try_json_decoding(sc)
                elif errormsg == "Invalid \\escape":
                    sc = rf"{sc}"
                    if sc.__contains__('medical\\_related'):
                        sc = sc.replace("medical\\_related", "medical_related")
                        return try_json_decoding(sc)
                    else:
                        return None

                else:  # Not Define
                    print_pretty_dict(response)
                    return None
                    sc = rf"{sc}"

                    print("Response is :")
                    logger.DEBUG(sc)
                    logger.DEBUG("Please fix :")
                    value = click.prompt("-->", type=str)
                    return try_json_decoding(value)
                    return None

            else:  # ErrorMsg is not exist
                sc = rf"{sc}"
                return try_json_decoding(sc)
                return None

            print_pretty_dict(response)
            return None

        else:
            return None
    else:
        return None


def remodel_llm_response(
    remodel_fx, template_id: str, limit_sample=0, proccess_bar=True
):
    l_id = get_list_id()
    logger.DEBUG(f"{len(l_id)} Records found.")
    doc_number = len(l_id)
    if doc_number == 0:
        return
    n = 0
    updated_number = 0
    if proccess_bar:
        bar = click.progressbar(length=doc_number,
                                show_pos=True,
                                show_percent=True)
        bar.label = f"{len(l_id)} Records found..."
        bar.update(1)

    for id in l_id:
        n = n + 1
        try:
            a = PERSIST.get_article_by_id(id)
            article = Article(**a.copy())
            need_update = False
            new_response = None
            for temp in article.ReviewLLM:
                if temp["TemplateID"] == template_id:
                    if "Response" in temp:
                        new_response = remodel_fx(temp["Response"])
                        if new_response is None:
                            need_update = False
                        else:
                            need_update = True
                    else:
                        need_update = False

            # if needed uodate
            if need_update is True:
                if isinstance(new_response, dict):
                    update_llm_response(id, template_id, new_response)

                    # For View Proccess
                    updated_number = updated_number + 1
                    if proccess_bar:
                        bar.label = f"""{id} update complete. {
                            updated_number} Article(s) Updated."""
                        bar.update(n_steps=1, current_item=n)
                else:
                    raise Exception("Response is not Dict!")
            else:
                if proccess_bar:
                    bar.update(1)

            if limit_sample != 0:  # Unlimited
                if n > limit_sample:
                    break
        except Exception:
            print()
            print(logger.ERROR(f"article. ID = {id}"))
            print_error()


if __name__ == "__main__":
    remodel_llm_response(
        fx_response_remodel, "extract-topic", limit_sample=0, proccess_bar=True
    )
