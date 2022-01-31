import requests
import json
import sys

repos = [
    'kubernetes',
    'kubernetes-client',
    'kubernetes-csi',
    'kubernetes-incubator',
    'kubernetes-sigs',
]

config = {
    "max-concurrent-indexers": 10,
    "dbpath": "data",
    "vcs-config": {
        "git": {
            "detect-ref" : True,
         }
    },
    "repos": {}
}

for repo in repos:
    page = 0
    while True:
        page += 1
        resp = requests.get(url= "https://api.github.com/orgs/" + repo + "/repos?per_page=100&page=" + str(page))
        data = resp.json()
        if len(data) == 0:
            break
        if 'message' in data:
            print(data["message"], file=sys.stderr)
            sys.exit(1)
            break
        for item in data:
            name = item['full_name'].split('/')[1]
            config["repos"][repo + "/" + name] = {
                "url": "https://github.com/%s/%s.git" % (repo, name),
                "ms-between-poll": 360000
            }

print(json.dumps(config, indent=4, sort_keys=True))
