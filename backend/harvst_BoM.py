####Comp90024_group10
###Shanrui Huang - 1533562
###Lingyi Zhang - 1470460
###Jiaxing Wang - 1511557
###Yunru Zhu - 1470423

import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/BoM', methods=['GET'])
def main():
    site = request.args.get('site')

    site_id_dic={
        "Kerang": "94844",
        "Mildura":"94693",
        "Horsham":"95839"
    }

    if site in site_id_dic:
        siteid =site_id_dic[site]
    else:
        return f'do not have site {site}'
    
    url = f"http://www.bom.gov.au/fwo/IDV60801/IDV60801.{siteid}.json" 
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'shanruih'
    }
    response = requests.get(url,headers=headers)

    if response.status_code == 200:
        store_url = 'http://router.fission/bomstore'

        store_response = requests.post(store_url, json=response.json()) #, headers={'Content-Type': 'application/json'}
        return jsonify({"status": "forwarded to store", "store_response": store_response.status_code})
    else:
        return jsonify({"error": "failed to retrieve data", "status_code": response.status_code})
    





    
if __name__ == "__main__":
    main()
