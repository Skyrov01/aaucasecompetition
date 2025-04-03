from automate_pull_requests import *


def main():
    if not GITHUB_TOKEN:
        print("❌ GITHUB_TOKEN is not set in your environment.")
        sys.exit(1)

    repo = Repo("../")
    if repo.bare:
        print("❌ Not a Git repository.")
        sys.exit(1)

    branch = get_current_branch(repo)
    pr_type = select_pr_type()
    base = get_input("Enter the base branch (e.g., main, develop): ")
    title = get_input("Enter PR Title: ")
    description = get_input("Enter PR Description: ")
    final_title = f"{pr_type}: {title}"

    push_branch(repo, branch)

    github = Github(GITHUB_TOKEN)
    current_user = github.get_user().login

    valid_reviewers = filter_valid_reviewers(github, REPO_NAME, PREDEFINED_REVIEWERS, current_user)

    # Get the filles that are gonna be inspected by LLM
    changed_files = get_committed_files(repo, base, branch)
    print("\n📄 Files to be included in PR:")
    for file in changed_files:
        print(f"- {file}")

        description += "\n " + file
    # Now. Before creating the PR we need to specifiy some stuff. 
    create_pr(github, REPO_NAME, base, branch, final_title, description, valid_reviewers)



if __name__ == "__main__":
    main()

    # A minor change added here.
    # NEW_FEATURE:START

    print("This is the best feature ever.")
    print("Changed the main")

    # NEW_FEATURE:END
