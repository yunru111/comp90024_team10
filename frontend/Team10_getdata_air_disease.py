#getdata_air_disease.py

import pandas as pd

def usable(es,index1,index2):
    # Query index "mean"
    query1 = {
        "size":10000,
        "query": {
            "exists": {
                "field": "site_name"
            }
        }
    }
    response1 = es.search(index=index1, body=query1)
    index1_data = response1['hits']['hits']

    # Query index "lung_disease"
    query2 = {
        "size":10000,
        "query": {
            "exists": {
                "field": "area_name"
            }
        }
    }
    response2 = es.search(index=index2, body=query2)
    index2_data = response2['hits']['hits']

    # Process and compare results
    names_index1 = {doc['_source']['site_name'].lower(): doc['_source'] for doc in index1_data}
    common_names = []
    for doc in index2_data:
        name = doc['_source']['area_name'].lower()
        if name in names_index1:
            # Merge index1_data and index2_data into one dictionary
            merged_data = {**names_index1[name], **doc['_source']}
            del merged_data['area_name']
            del merged_data['site_name'] 
            common_names.append({
                "site_name": name,
                "merged_data": merged_data
            })
    
    return common_names


def clean(es,index1, index2):
    ml = usable(es,index1,index2)
    df = pd.json_normalize([item["merged_data"] for item in ml])
    df["site_name"] = [item["site_name"] for item in ml]
    # df.set_index("site_name", inplace=True)

    df.drop(columns=['area_code'], inplace=True)
    df.rename(columns={
        'asthma_me_1_no_3_11_7_13': 'asthma_count',
        'asthma_me_2_rate_3_11_7_13': 'asthma_rate',
        'copd_me_1_no_3_11_7_13': 'COPD_count',
        'copd_me_2_rate_3_11_7_13': 'COPD_rate',
        'respirtry_me_1_no_3_11_7_13': 'respirtry_count',
        'respirtry_me_2_rate_3_11_7_13': 'respirtry_rate'
    }, inplace=True)
    cols = ['site_name','asthma_count', 'asthma_rate', 'COPD_count', 'COPD_rate', 'respirtry_count', 'respirtry_rate', 'pm10_avg', 'pm2p5_avg']
    df = df[cols]

    return df

