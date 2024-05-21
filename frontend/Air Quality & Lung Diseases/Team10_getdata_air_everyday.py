# getdata_air_everyday.py
# Team 10
# Shanrui Huang - 1533562
# Lingyi Zhang - 1470460
# Jiaxing Wang - 1511557
# Yunru Zhu - 1470423


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

