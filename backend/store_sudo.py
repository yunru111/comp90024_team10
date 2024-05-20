import requests
import json
from requests.auth import HTTPBasicAuth

local_json_file = "sudodata.json"
with open(local_json_file, 'r') as f:
    data = json.load(f)

for entry in data["features"]:
    properties = entry["properties"]
    doc_id = entry["id"]

    store_url = f'https://127.0.0.1:9200/sudo/_doc/{doc_id}'
    store_response = requests.post(store_url, json=properties, auth=HTTPBasicAuth('elastic', 'elastic'), verify=False) #, headers={'Content-Type': 'application/json'}

    print(store_response)

