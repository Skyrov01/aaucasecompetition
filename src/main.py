from automate_pull_requests import *


from github import Github
import os
access_token=os.environ.get("GITHUB_TOKEN")

# using an access 

tokeng = Github(access_token)
for repo in g.get_user().get_repos():
    print(repo.name)


