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

@app.route('/sudodata', methods=['POST'])
def main():

    def air_usable(data):
        # Create a dictionary to store PM2.5 and PM10 values for each site
        site_data = {}
        for feature in data['features']:
            site_name = feature['properties']['site_name']
            pm2p5 = feature['properties']['pm2p5']
            pm10 = feature['properties']['pm10']

            if site_name not in site_data:
                site_data[site_name] = {
                    "pm2p5_sum": 0,
                    "pm10_sum": 0,
                    "count": 0
                }

            if pm2p5 is not None:
                site_data[site_name]["pm2p5_sum"] += pm2p5
            if pm10 is not None:
                site_data[site_name]["pm10_sum"] += pm10
            site_data[site_name]["count"] += 1

        # Create a new dictionary to store the average for each site
        average_data = {}
        # Calculate the average for each site
        for site_name, values in site_data.items():
            pm2p5_avg = values["pm2p5_sum"] / values["count"] if values["count"] > 0 else None
            pm10_avg = values["pm10_sum"] / values["count"] if values["count"] > 0 else None
            average_data[site_name] = {
                "pm2p5_avg": pm2p5_avg,
                "pm10_avg": pm10_avg
            }

        return average_data
    

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

    mean_data=air_usable(data)

    try:
        actions=[]
        for site_name, measurements in mean_data.items():
            action = {
                "_index": "mean",
                "_source": {
                    "site_name": site_name,
                    "pm2p5_avg": measurements["pm2p5_avg"],
                    "pm10_avg": measurements["pm10_avg"]
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

