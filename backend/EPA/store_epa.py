####Comp90024_group10
###Shanrui Huang - 1533562
###Lingyi Zhang - 1470460
###Jiaxing Wang - 1511557
###Yunru Zhu - 1470423

import logging
from flask import Flask, request, jsonify
from elasticsearch8 import Elasticsearch
from elasticsearch8.helpers import bulk

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.route('/epa', methods=['POST'])
####Comp90024_group10
###Shanrui Huang - 1533562
###Lingyi Zhang - 1470460
###Jiaxing Wang - 1511557
###Yunru Zhu - 1470423


def main():
    es_client = Elasticsearch(
        'https://elasticsearch-master.elastic.svc.cluster.local:9200',
        verify_certs=False,
        ssl_show_warn=False,
        basic_auth=('elastic', 'elastic')
    )

    data=request.get_json(force=True)
    if not data:
        app.logger.error("No data received")
        return jsonify({"error": "No data received"}), 400

    app.logger.info(f'Observations to add: {data}')
    try:
        actions=[]
        for hour_data in data['siteHealthAdvices']:
            try:
                if "averageValue" not in hour_data:
                    hour_data['averageValue']=0
                action = {
                    "_index": "epa",
                    "_source": {   
                        'site_name': data['siteName'],
                        'since': hour_data['since'],
                        'PM2.5': hour_data['averageValue'],
                    }
                }
                actions.append(action)
            except:
                pass

        bulk(es_client, actions)
        app.logger.info("Bulk data upload complete.")
        return jsonify({"message": "Data processed successfully", "uploaded": len(actions)}), 200

    except Exception as e:
        app.logger.error(f'Error indexing data: {str(e)}')
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)

