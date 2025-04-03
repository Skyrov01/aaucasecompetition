from automate_pull_requests import *
import re
from LLM_calls import *

title = ""
description = ""
is_user_happy = False

def main():

    global title, description, is_user_happy

    if not GITHUB_TOKEN:
        print("❌ GITHUB_TOKEN is not set in your environment.")
        sys.exit(1)

    repo = Repo("../")
    if repo.bare:
        print("❌ Not a Git repository.")
        sys.exit(1)

    # Analyse changes
    branch = get_current_branch(repo)
    base = get_input("Enter the base branch (e.g., main, develop): ")
    
    # Get the filles that are gonna be inspected by LLM
    changed_files = get_committed_files(repo, base, branch)
    print("\n📄 Files to be included in PR:")
    for file in changed_files:
        print(f"- {file}")

    commit_changes = get_commit_diff_details(repo, base, branch)

    # STEP 1: Handle description
    is_user_happy = False
    msg = get_input("Want me to generate the description? yes:no\n")
    if msg.lower() == "yes":
        while not is_user_happy:
            description = generate_description(commits = commit_changes)
            msg = get_input("Is the description ok? yes:no\n")
            if msg.lower() == "yes":
                is_user_happy = True
            
    else:
        description = get_input("Enter PR Description: ")


    # STEP 2: Handle title
    is_user_happy = False
    msg = get_input("Want me to generate the title? yes:no\n")
    if msg.lower() == "yes":
        while not is_user_happy:
            title = generate_title(description=description)
            msg = get_input("Is the title ok? yes:no\n")
            if msg.lower() == "yes":
                is_user_happy = True
            
    else:
        title = get_input("Enter PR Title: ")

    pr_type = select_pr_type()
    final_title = f"{pr_type}: {title}"

    

    push_branch(repo, branch)

    github = Github(GITHUB_TOKEN)
    current_user = github.get_user().login

    valid_reviewers = filter_valid_reviewers(github, REPO_NAME, PREDEFINED_REVIEWERS, current_user)

    
    # Now. Before creating the PR we need to specifiy some stuff. 
    create_pr(github, REPO_NAME, base, branch, final_title, description, valid_reviewers)



if __name__ == "__main__":
    main()

    # A minor change added here.
    # NEW_FEATURE:START

    print("This is the best feature ever.")
    print("Changed the main")

    # NEW_FEATURE:END