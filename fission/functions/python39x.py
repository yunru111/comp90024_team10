from elasticsearch8 import Elasticsearch
import pandas as pd
import scipy as sc
import numpy as np

def main():
    client = Elasticsearch (
        'https://elasticsearch-master.elastic.svc.cluster.local:9200',
        verify_certs= False,
        ssl_show_warn= False,
        basic_auth=('elastic', 'elastic')
    )

    return f'ElasticSearch:{client.info()["version"]["number"]}\nSciPy:{sc.__version__}\nNumPy:{np.version.version}\n'
