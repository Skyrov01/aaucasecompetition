from automate_pull_requests import *
import re
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

    print("\n🔁 Related Changes (Grouped by File & Hunk):")
    print(commit_changes)
    for file, hunks in commit_changes.items():
        print(f"\n📄 {file}")
        for idx, hunk in enumerate(hunks):
            print(f"  🔸 Change #{idx + 1}")
            if hunk["-"]:
                print("   ➖ Removed:")
                for line in hunk["-"]:
                    print("     -", line)
            if hunk["+"]:
                print("   ➕ Added:")
                for line in hunk["+"]:
                    print("     +", line)


    # STEP 1: Handle title
    is_user_happy = False
    msg = get_input("Want me to generate the title? yes:no\n")
    if msg.lower() == "yes":
        while not is_user_happy:
            title = generate_title()
            msg = get_input("Is the title ok? yes:no\n")
            if msg.lower() == "yes":
                is_user_happy = True
            
    else:
        title = get_input("Enter PR Title: ")

    pr_type = select_pr_type()
    final_title = f"{pr_type}: {title}"

    # STEP 2: Handle description
    is_user_happy = False
    msg = get_input("Want me to generate the description? yes:no\n")
    if msg.lower() == "yes":
        while not is_user_happy:
            description = generate_description()
            msg = get_input("Is the description ok? yes:no\n")
            if msg.lower() == "yes":
                is_user_happy = True
            
    else:
        description = get_input("Enter PR Description: ")

    

    push_branch(repo, branch)

    github = Github(GITHUB_TOKEN)
    current_user = github.get_user().login
    
    changed_file_list = list(changed_files.keys())  # just the filenames
    # Load eligible reviewers from developers.json - smart assign them based on the files extensions
    available_reviewers = smart_reviewer_picker("developers.json", current_user, changed_file_list)

    # Optional: filter valid ones against GitHub collaborators
    valid_reviewers = filter_valid_reviewers(github, REPO_NAME, available_reviewers, current_user)

    print(valid_reviewers)

    
    # Now. Before creating the PR we need to specifiy some stuff. 
    # create_pr(github, REPO_NAME, base, branch, final_title, description, valid_reviewers)



if __name__ == "__main__":
    main()

    # A minor change added here.
    # NEW_FEATURE:START

    print("This is the best feature ever.")
    print("Changed the main")

    # NEW_FEATURE:END
