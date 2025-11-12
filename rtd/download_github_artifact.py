import os
import sys
import shutil
import json
import subprocess

# this must be set as a an environament variable of the readthedocs project at https://app.readthedocs.org/dashboard/triocfd-documentation/environmentvariables/
GITHUB_TOKEN=os.getenv("GITHUB_TOKEN")

# see https://docs.github.com/en/rest/actions/artifacts?apiVersion=2022-11-28
# for a documentation of the various curl command used here to download artifact data from the github api
curl_request_api_cmd=f"curl -L -H 'Accept: application/vnd.github+json' -H 'Authorization: token {GITHUB_TOKEN}' -H 'X-GitHub-Api-Version: 2022-11-28'"


# set by readthedocs and used to find the resulting html files (and other outputs)
READTHEDOCS_OUTPUT=os.getenv("READTHEDOCS_OUTPUT", "/tmp/rtd-triocfd") # default in /tmp to test script manually

# may not exist
os.makedirs(READTHEDOCS_OUTPUT, exist_ok=True)

print("Will download to", READTHEDOCS_OUTPUT)



# downloads global data about artifacts
path_artifacts_json=os.path.join(READTHEDOCS_OUTPUT, "artifacts.json")
url_api_artifacts="https://api.github.com/repos/cea-trust-platform/triocfd-documentation/actions/artifacts"
os.system(f"{curl_request_api_cmd} -o '{path_artifacts_json}' {url_api_artifacts}")

# get current commit SHA ID
result = subprocess.run(['git', 'rev-parse', 'HEAD'], stdout=subprocess.PIPE)
commit_sha=(result.stdout.decode('utf-8')).replace("\n", "")
print("Current commit ID:", commit_sha)

# search for correct html artifact
commit_artifact=None
with open(path_artifacts_json) as f:
    d = json.load(f)
    for art in d["artifacts"]:
        if art["name"]==f"html{commit_sha}":
            commit_artifact=art

if commit_artifact  is None:
    raise Exception("No html artifact found for current commit. Likely a problem in github workflow")

print("Found artifact matching commit ID:")
print(json.dumps(commit_artifact, indent=4))

# Download the artifact data (in zip archive)
url_api_dl_archive=commit_artifact["archive_download_url"]

path_html_zip=os.path.join(READTHEDOCS_OUTPUT, "html.zip")
os.system(f"{curl_request_api_cmd} -o '{path_html_zip}' {url_api_dl_archive}")

# Extract the archive to the readthedocs output directory
extract_dest=os.path.join(READTHEDOCS_OUTPUT, "html")
print("Extracing to ", extract_dest)
os.system(f"unzip {path_html_zip} -d {extract_dest} > {os.path.join(READTHEDOCS_OUTPUT, "log_unzip")}")