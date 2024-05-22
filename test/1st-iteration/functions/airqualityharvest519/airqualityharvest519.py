import requests
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/airqualityharvest519', methods=['GET'])
def main():
    site = request.args.get('site', '*')
    date = request.args.get('date')
    year = date[:4] if len(date) >= 4 else '2023'
    if site == '*':  # all site
        site_filter = ''
    else:
        site_filter = f"site_name='{site}' and "  # Specific site
    if len(date) == 4:  # Yearly data
        date_filter = f"time_stamp>={date}-01-01T00:00:00Z and time_stamp<={date}-12-31T23:59:59Z"
    else:  # Specific date
        date_filter = f"time_stamp>={date}T00:00:00Z and time_stamp<={date}T23:59:59Z"
    url = f"https://naqd.eresearch.unimelb.edu.au/geoserver/wfs?service=WFS&version=2.0.0&request=GetFeature&typeName=geonode:vic_observations_{year}&outputFormat=application/json&cql_filter={site_filter}{date_filter}"
    print("Requesting URL:", url)
    response = requests.get(url)

    if response.status_code == 200:
        store_url = 'http://router.fission/airqualitystore519'

        store_response = requests.post(store_url,json=response.json())  # , headers={'Content-Type': 'application/json'}
        return jsonify({"status": "forwarded to store", "store_response": store_response.status_code})
    else:
        return jsonify({"error": "failed to retrieve data", "status_code": response.status_code})


if __name__ == "__main__":
    main()