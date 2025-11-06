import os
import sys
import shutil
import json
import subprocess
GITHUB_TOKEN=os.getenv("GITHUB_TOKEN")
READTHEDOCS_OUTPUT=os.getenv("READTHEDOCS_OUTPUT")

# Useful refs: (will move somewhere else later)

# ref to github api here:
# https://docs.github.com/en/rest/actions/artifacts?apiVersion=2022-11-28

# rtd generic API:
# https://docs.readthedocs.com/platform/stable/guides/setup/git-repo-manual.html#using-the-generic-api-integration
# rtd build custom
# https://docs.readthedocs.com/platform/stable/build-customization.html

# if os.path.exists("artifacts.json"):
#     os.remove("artifacts.json")
# if os.path.exists("html.zip"):
#     os.remove("html.zip")
# if os.path.exists("html"):
#     shutil.rmtree("html")

os.system(f"curl -L -H 'Accept: application/vnd.github+json' -H 'Authorization: token {GITHUB_TOKEN}' -H 'X-GitHub-Api-Version: 2022-11-28'  -o 'artifacts.json' https://api.github.com/repos/cea-trust-platform/triocfd-documentation/actions/artifacts")

result = subprocess.run(['git', 'rev-parse', 'HEAD'], stdout=subprocess.PIPE)

commit_sha=(result.stdout.decode('utf-8')).replace("\n", "")
print("Current commit ID:", commit_sha)

with open('artifacts.json') as f:
    d = json.load(f)
    # print(d)
    # print(d["artifacts"])
    commit_artifact=None
    for art in d["artifacts"]:
        if art["name"]==f"html{commit_sha}":
            commit_artifact=art
            # print(art["url"])

    if commit_artifact  is None:
        raise Exception("No artifact found for current commit")

    print("Found artifact matching commit ID:")
    print(commit_artifact)

    dl_url=commit_artifact["archive_download_url"]

    os.system(f"curl -L -H 'Accept: application/vnd.github+json' -H 'Authorization: token {GITHUB_TOKEN}' -H 'X-GitHub-Api-Version: 2022-11-28'  -o 'html.zip'  {dl_url}")

    extract_dest=os.path.join(READTHEDOCS_OUTPUT, "html")
    print("Extracing to ", extract_dest)
    os.makedirs(READTHEDOCS_OUTPUT)
    os.system(f"unzip html.zip -d {extract_dest}")