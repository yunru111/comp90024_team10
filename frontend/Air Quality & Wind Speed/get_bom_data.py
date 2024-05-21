####Comp90024_group10
###Shanrui Huang - 1533562
###Lingyi Zhang - 1470460
###Jiaxing Wang - 1511557
###Yunru Zhu - 1470423
import json
from elasticsearch import Elasticsearch

def search_bom(es, index):
    query = {
        "query": {
            "term": {
                "site_name.keyword": "Mildura"
            }
        }
    }

    response = es.search(index=index, body=query, size=10000)
    hits = response['hits']['hits']
    with open("bom_data.json", "w") as f:
        for hit in hits:
            json.dump(hit["_source"], f)
            f.write("\n")
    data = [hit['_source'] for hit in hits]
    return data

