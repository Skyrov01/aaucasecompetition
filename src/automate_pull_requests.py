from github import Github
from git import Repo
import os
import sys
from dotenv import load_dotenv

load_dotenv()

# ========== CONFIGURATION ========== #
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  
REPO_NAME = "Skyrov01/aaucasecompetition"  
PREDEFINED_REVIEWERS = ["Skyrov01", "DavideRago"]
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

def filter_valid_reviewers(g, repo_name, reviewers, author_login):
    repo = g.get_repo(repo_name)
    valid = []
    for user in reviewers:
        if user == author_login:
            print(f"⚠️ Skipping {user} (PR author cannot review their own PR).")
            continue
        try:
            if repo.has_in_collaborators(user):
                valid.append(user)
            else:
                print(f"⚠️ {user} is not a collaborator. Skipping.")
        except Exception as e:
            print(f"⚠️ Could not validate {user}: {e}")
    return valid


# The Magic of LLMs #
# Here we need to extract all the information need for the LLM.

def get_committed_files(repo, base_branch, current_branch):
    """
    Returns a list of file paths that were changed between base_branch and current_branch.
    """
    try:
        # Fetch latest from origin to ensure we compare against up-to-date base
        repo.git.fetch()
        diff = repo.git.diff('--name-only', f'origin/{base_branch}...{current_branch}')
        changed_files = diff.strip().split('\n') if diff else []
        return changed_files
    except Exception as e:
        print(f"❌ Error getting committed files: {e}")
        return []