
from triplea.service.repository.state.initial import get_article_list_from_pubmed_all_store_to_arepo

if __name__ == "__main__":
    # Get article from Pubmed
    pubmed_search_string = '("Breast Cancer"[Title]) AND (Therapy[Title])'
    get_article_list_from_pubmed_all_store_to_arepo(pubmed_search_string)