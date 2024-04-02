import triplea.service.repository.persist as PERSIST
from triplea.service.repository.pipeline_core import move_state_forward

if __name__ == "__main__":

    # ------------------------Print RepoInfo-----------------------------------
    PERSIST.print_article_info_from_repo()
    # ------------------------Print RepoInfo-----------------------------------

    # Moving from `0` to `1`  - original details of article saved (json Form)
    move_state_forward(0)

    # Step 5 - Moving from `1` to `2` - parse details info of article
    move_state_forward(1)