from github import Github
from git import Repo
import os
import sys
from dotenv import load_dotenv

load_dotenv()

# ========== CONFIGURATION ========== #
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  
REPO_NAME = "Skyrov01/aaucasecompetition"  
PREDEFINED_REVIEWERS = ["dev-lead", "team-reviewer"]
PR_TYPES = ["task", "bug", "feature", "hotfix", "fix", "style", "refactor", "test"]
# =================================== #

def get_current_branch(repo):
    return repo.active_branch.name

def select_pr_type():
    print("Select PR Type:")
    for i, opt in enumerate(PR_TYPES, start=1):
        print(f"{i}) {opt}")
    while True:
        try:
            choice = int(input(f"Enter a number (1-{len(PR_TYPES)}): "))
            if 1 <= choice <= len(PR_TYPES):
                return PR_TYPES[choice - 1]
        except ValueError:
            pass
        print("❌ Invalid choice, try again.")

def get_input(prompt):
    val = input(prompt).strip()
    if not val:
        print("❌ This field is required!")
        sys.exit(1)
    return val

def push_branch(repo, branch_name):
    origin = repo.remote(name='origin')
    origin.push(branch_name)

def create_pr(g, repo_name, base, head, title, body, reviewers):
    repo = g.get_repo(repo_name)
    pr = repo.create_pull(
        title=title,
        body=body,
        head=head,
        base=base
    )
    pr.create_review_request(reviewers=reviewers)
    print(f"✅ Pull request created: {pr.html_url}")

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
    create_pr(github, REPO_NAME, base, branch, final_title, description, PREDEFINED_REVIEWERS)

if __name__ == "__main__":
    main()
