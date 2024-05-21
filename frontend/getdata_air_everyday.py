# getdata_air_everyday.py

import json

def search(es, index):
    query = {
        "query": {
            "match_all": {
            }
        }
    }

    response = es.search(index=index, body=query, size=10000)
    hits = response['hits']['hits']
    with open("airquality_data.json", "w") as f:
        for hit in hits:
            json.dump(hit["_source"], f)
            f.write("\n")
    data = [hit['_source'] for hit in hits]
    return data

