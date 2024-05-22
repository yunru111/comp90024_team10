####Comp90024_group10
###Shanrui Huang - 1533562
###Lingyi Zhang - 1470460
###Jiaxing Wang - 1511557
###Yunru Zhu - 1470423
from elasticsearch8 import Elasticsearch
from elasticsearch8.helpers import bulk
from flask import Flask, request, jsonify
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.route('/airqualitystore519', methods=['POST'])
def main():
    es_client = Elasticsearch(
        'https://elasticsearch-master.elastic.svc.cluster.local:9200',
        verify_certs=False,
        ssl_show_warn=False,
        basic_auth=('elastic', 'elastic')
    )

    data = request.get_json(force=True)
    if not data:
        app.logger.error("No data received")
        return jsonify({"error": "No data received"}), 400

    actions = []
    try:
        for feature in data["features"]:
            action = {
                "_index": "airquality_520",
                "_source": {
                    "site_name": feature["properties"]["site_name"],
                    "time_stamp": feature["properties"]["time_stamp"],
                    "geo": {
                        "lat": feature["properties"]["latitude"],
                        "lon": feature["properties"]["longitude"]
                    },
                    "ozone": feature["properties"]["ozone"],
                    "pm10": feature["properties"]["pm10"],
                    "pm2p5": feature["properties"]["pm2p5"]
                }
            }
            actions.append(action)

        bulk(es_client, actions)
        app.logger.info("Bulk data upload complete.")
        return jsonify({"message": "Data processed successfully", "uploaded": len(actions)}), 200

    except Exception as e:
        app.logger.error(f'Error indexing data: {str(e)}')
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
