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

@app.route('/bomstore', methods=['POST'])
def main():
    def convert_date_format(date_str):
        year = date_str[0:4]
        month = date_str[4:6]
        day = date_str[6:8]
        hour = date_str[8:10]
        minute = date_str[10:12]
        second = date_str[12:14]

        formatted_date = f"{year}-{month}-{day}T{hour}:{minute}:{second}Z"
        
        return formatted_date

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
        for hour_data in data['observations']['data']:
            action = {
                "_index": "bom",
                "_source": {   
                    'since': convert_date_format(hour_data['local_date_time_full']),
                    'site_name': hour_data['name'],
                    'wind_speed': hour_data['wind_spd_kmh']
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

