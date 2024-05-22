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

@app.route('/eachday', methods=['POST'])
def main():

    def air_everyday(data):

        site_data = {}
        for feature in data['features']:
            site_name = feature['properties']['site_name']
            pm2p5 = feature['properties']['pm2p5']
            pm10 = feature['properties']['pm10']
            date = feature['properties']['time_stamp'][:10]

            key=f"{date}--{site_name}"

            if key not in site_data:
                site_data[key] = {
                    "pm2p5_sum": 0,
                    "pm10_sum": 0,
                    "count": 0,
                    'date':date
                }

            if pm2p5 is not None:
                site_data[key]["pm2p5_sum"] += pm2p5
            if pm10 is not None:
                site_data[key]["pm10_sum"] += pm10
            site_data[key]["count"] += 1

        average_data = {}
        for key, values in site_data.items():
            date=key[:10]
            site_name=key[12:]
            pm2p5_avg = values["pm2p5_sum"] / values["count"] if values["count"] > 0 else None
            pm10_avg = values["pm10_sum"] / values["count"] if values["count"] > 0 else None

            if date not in average_data:
                average_data[date] = [{
                    "pm2p5_avg": pm2p5_avg,
                    "pm10_avg": pm10_avg,
                    "site_name": site_name
                }]

            elif date in average_data:
                average_data[date].append({
                    "pm2p5_avg": pm2p5_avg,
                    "pm10_avg": pm10_avg,
                    "site_name": site_name
                })
            
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

    everyday_mean_data=air_everyday(data)

    try:
        actions=[]
        for date, values in everyday_mean_data.items():
            for site in values:
                action = {
                    "_index": "mean_eachday",
                    "_source": {
                        "date": date,
                        "site_name": site["site_name"],
                        "pm2p5_avg": site["pm2p5_avg"],
                        "pm10_avg": site["pm10_avg"]
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

