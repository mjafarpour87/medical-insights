import click
from triplea.config.settings import SETTINGS
import triplea.service.repository.persist as persist
from triplea.service.click_logger import logger
from triplea.schemas.article import Article
from triplea.utils.general import print_error

import spacy
import pytextrank  # noqa: F401

nlp = spacy.load("en_core_web_sm")
nlp.add_pipe("textrank")


def extract_textrank(text: str):
    """
    Extracts the top 10 ranked phrases from the input text.

    Args:
        text (str): The input text to be processed.

    Returns:
        list: A list of the top 10 ranked phrases in the input text.
    """
    doc = nlp(text)

    l_phrase = []
    for phrase in doc._.phrases[:10]:
        row = {"text": phrase.text, "rank": phrase.rank}
        l_phrase.append(row)

    return l_phrase


def extract_topic_abstract(article: Article):
    article.FlagExtractTopic = 1
    if article.Title is None:
        title = ""
    else:
        title = article.Title

    if article.Abstract is None:
        abstract = ""
    else:
        abstract = article.Abstract

    text = title + " " + abstract
    text = text.replace("\n", "")
    try:
        result = extract_textrank(text)
        article.Topics = result
    except Exception:
        print_error()
        article.FlagExtractTopic = -1

    return article


def go_extract_topic(proccess_bar=True):
    max_refresh_point = SETTINGS.AAA_CLI_ALERT_POINT
    l_id = persist.get_article_id_list_by_state(2)
    total_article_in_current_state = len(l_id)
    n = 0
    logger.DEBUG(str(
            len(l_id)
        ) + " Article(s) is in FlagExtractTopic " + str(0))

    if proccess_bar:
        bar = click.progressbar(length=len(l_id),
                                show_pos=True,
                                show_percent=True)

    refresh_point = 0

    for id in l_id:
        try:
            n = n + 1
            current_state = None

            if refresh_point == max_refresh_point:
                refresh_point = 0
                persist.refresh()
                if proccess_bar:
                    print()
                    logger.INFO(
                        f"""There are {str(
                            total_article_in_current_state - n
                            )} article(s) left """,
                        forecolore="yellow",
                    )
                if proccess_bar is False:
                    bar.label = f"""There are {str(
                        total_article_in_current_state - n
                        )} article(s) left """
                    bar.update(max_refresh_point)
            else:
                refresh_point = refresh_point + 1

            a = persist.get_article_by_id(id)
            try:
                updated_article = Article(**a.copy())
            except Exception:
                print()
                print(logger.ERROR(f"Error in parsing article. ID = {id}"))
                raise Exception("Article Not Parsed.")
            try:
                current_state = updated_article.FlagExtractTopic  # -----------
            except Exception:
                current_state = 0

            if proccess_bar:
                bar.label = f"""Article {id}, topic were extracted."""
                bar.update(1)

            if current_state is None:
                updated_article = extract_topic_abstract(updated_article)
            elif current_state == -1:
                updated_article = extract_topic_abstract(updated_article)
            elif current_state == 0:
                updated_article = extract_topic_abstract(updated_article)
            elif current_state == 1:
                pass

            else:
                raise NotImplementedError

            persist.update_article_by_id(updated_article, id)

        except Exception:
            if current_state == 0 or current_state is None:
                updated_article = Article(**a.copy())
                updated_article.FlagExtractTopic = -1
                persist.update_article_by_id(updated_article, id)
                persist.refresh()
                print_error()

            else:
                persist.refresh()
                print_error()
    persist.refresh()


if __name__ == "__main__":
    go_extract_topic()
