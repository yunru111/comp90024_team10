####Comp90024_group10
###Shanrui Huang - 1533562
###Lingyi Zhang - 1470460
###Jiaxing Wang - 1511557
###Yunru Zhu - 1470423

import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/519', methods=['GET'])
def main():
    def get_all_site():
        epa_site_url = 'https://gateway.api.epa.vic.gov.au/environmentMonitoring/v1/sites?environmentalSegment=air'

        headers = {
            'X-API-Key': 'bc9313eda801413ba990997c058ad13a',
            'Content-Type': 'application/json',
            'User-Agent': 'shanruih'
        }

        response = requests.get(epa_site_url, headers=headers)

        if response.status_code == 200:
            print("Data retrieved successfully!")
            data=response.json()

            site_data_dic={}
            for site_data in data["records"]:
                site_data_dic[site_data['siteName']]=site_data['siteID']
            return site_data_dic
        else:
            return "Failed to retrieve data: " + str(response.status_code) + " " + response.text
    
    def get_date_two_days_before(date_str):
        year, month, day = map(int, date_str.split('-'))
        
        days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        day -= 2
        if day < 1:
            month -= 1
            if month < 1:
                month = 12
                year -= 1
            day += days_in_month[month - 1]
        
        if month == 2 and is_leap_year(year):
            if day == 28:
                day = 29
            elif day < 1:
                month -= 1
                day += 31
        new_date_str = f'{year:04d}-{month:02d}-{day:02d}'
        return new_date_str

    def is_leap_year(year):
        return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

    site = request.args.get('site')
    date = request.args.get('date')
    site_id_dic=get_all_site()

    if site in site_id_dic:
        siteid =site_id_dic[site]
    else:
        return f'do not have site {site}'
    sincedate=get_date_two_days_before(date)
    sincetime=f"{sincedate}T00:00:00Z"
    untiltime=f"{date}T23:59:59Z"
    url = f"https://gateway.api.epa.vic.gov.au/environmentMonitoring/v1/sites/{siteid}/parameters?since={sincetime}&until={untiltime}&interval=1HR_AV" 
    headers = {
        'X-API-Key': 'bc9313eda801413ba990997c058ad13a',
        'Content-Type': 'application/json',
        'User-Agent': 'shanruih'
    }
    response = requests.get(url,headers=headers)

    if response.status_code == 200:
        store_url = 'http://router.fission/epastore'

        store_response = requests.post(store_url, json=response.json()) #, headers={'Content-Type': 'application/json'}
        return jsonify({"status": "forwarded to store", "store_response": store_response.status_code})
    else:
        return jsonify({"error": "failed to retrieve data", "status_code": response.status_code})
    





    
if __name__ == "__main__":
    main()
