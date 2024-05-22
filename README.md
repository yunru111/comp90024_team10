# comp90024_team10


### introduction

The research question our group aims to discover is the correlation between air quality and lung diseases, and correlation between air quality and wind strength. We use real-time data including Victoria air quality data from National Air Quality Database, Victoria air quality data from Environment Protection Authority and Victoria weather data from Bureau of Meteorology Victoria. We also manually download COPD/Asthma/Respiratory System Disease data from SUDO. 

## folders

- backend: Obtain data from various sources and then send the data to Elasticsearch for storage.
- frontend: Retrieve data from Elasticsearch and perform data analysis.
- test: For testing backend scripts
- database: Query and mapping used to operate Elasticsearch
- data: Data downloaded from SUDO
- doc: report



### Backend  


## Pre-requirements

- OpenStack RC file and API password obtained and sourced in current shell 
- A Kubernetes cluster created on NeCTAR 
- Connect to Campus network if on-campus or UniMelb Student VPN if off-campus
- Kubernetes cluster is accessible 
- ElasticSearch is installed 
- Fission CLI is installed on the client 
- Fission is installed on the cluster 

## scripts

- airqualityharvst519.py: Get air quality data from naqd and send to url "http://router.fission/airqualitystore519"

- airquality_all: The folder includes the script that accepts data from the url "http://router.fission/airqualitystore519" and sends it to Elasticsearch and the files needed to create the package for the script.

- harvst_to_mean.py: Get air quality data from naqd and send to url "http://router.fission/cleandata"

- airquality_mean: The folder includes the script that accepts data from the url "http://router.fission/cleandata" and sends it to Elasticsearch and the files needed to create the package for the script.

- harvst_to_eachday.py: Get air quality data from naqd and send to url "http://router.fission/eachday"

- airquality_eachday: The folder includes the script that accepts data from the url "http://router.fission/eachday" and sends it to Elasticsearch and the files needed to create the package for the script.

- harvst_epa.py: Get air quality data from epa and send to url "http://router.fission/epastore"

- store_epa: The folder includes the script that accepts data from the url "http://router.fission/epastore" and sends it to Elasticsearch and the files needed to create the package for the script.

- harvst_bom.py: Get air quality data from BoM and send to url "http://router.fission/bomstore"

- store_bom: The folder includes the script that accepts data from the url "http://router.fission/bomstore" and sends it to Elasticsearch and the files needed to create the package for the script.

- store_sudo.py: Send data downloaded from sudo to Elasticsearch


## Configuration

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/yourproject.git
    ```

2. Create the Python environment and Node.js environment on the cluster with the builder:
    ```sh
    fission env create --name python --image fission/python-env --builder fission/python-builder
    fission env create --name nodejs --image fission/node-env --builder fission/node-builder
    ```

The configuration process of functions are relatively similar. Only two different examples (airqualityharvest519.py and final_store_airquality) is listed below and all the routes we use are provided.

3. airqualityharvest519.py

    Create function and route:
    ```sh
    fission function create --name airqualityharvest519 --env python --fntimeout 300 --code ./fission/functions/airqualityharvest519.py
    fission route create --url /airqualityharvest519 --function airqualityharvest519 --name airqualityharvest519
    ```

4. final_store_airquality

    create a zip of "final_store_airquality" folder
    ```sh
    (
    cd ~/comp90024_team10/backend/airquality_all
    zip -r final_store_airquality.zip .
    mv final_store_airquality.zip ../
    )
    ```

    create package 
    ```sh
    fission package create --sourcearchive ~/comp90024_team10/backend/final_store_airquality.zip\
      --env python\ 
      --name final_store_airquality\
      --buildcmd './build.sh'
    ```

    create function
    ```sh
    fission fn create --name airqualitystore519\
      --pkg airqualitystore519\
      --fntimeout 300\
      --env python\
      --entrypoint "final_store_airquality.main" 
    ```
    
    create route
    ```sh
    fission route create --url /airqualitystore519 --function airqualitystore519 --name airqualitystore519 --method POST--spec
    ```


## Running

1. Get and upload all air quality data in naqd
    ```sh
    curl "http://127.0.0.1:9090/airqualityharvest519?stie={sitename}&date={date}"
    ```
where the {date} must exist and needs to be a date in a format similar to ‘2023-05-25’, also you can change {sitename} to the site you want.
If sitename is not set, the entire site will be returned.

2. Get and upload mean air quality data in naqd
    ```sh
    curl "http://127.0.0.1:9090/postcleandata?stie={sitename}&date={date}"
    ```
where the {date} must exist and needs to be a date in a format similar to ‘2023-05-25’, also you can change {sitename} to the site you want.
If sitename is not set, the entire site will be returned.

3. Get and upload mean air quality data of each day in naqd
    ```sh
    curl "http://127.0.0.1:9090/posteachday?stie={sitename}&date={date}"
    ```
where the {date} must exist and needs to be a date in a format similar to ‘2023-05-25’, also you can change {sitename} to the site you want.
If sitename is not set, the entire site will be returned.

4. Obtain data from a certain site in epa within two days
    ```sh
    curl "http://127.0.0.1:9090/epa?stie={sitename}&date={date}"
    ```
where the {date} must be the date of today, also you must set {sitename} to the site you want.

5. Obtain data from a certain site in BoM within two days
    ```sh
    curl "http://127.0.0.1:9090/bom?stie={sitename}"
    ```
where you must set {sitename} to the site you want, but due to some restrictions we only have a few sites available here.

6. Upload SUDO data
    ```sh
    cd ./backend
    python3 store_sudo.py
    ```
where you need to save the data in path ./backend/data.json



### frontend


## Pre-requirements

- Anaconda3 has been installed


## Folder

1. Air Quality & Lung Diseases

    - getdata_air_disease.py: Retrieve air quality data and data on people suffering from different lung diseases for the same site from ElasticSearch

    - getdata_air_everyday.py: Retrieve daily average air quality data for the different sites from ElasticSearch

    - data_analysis.ipynb: Call the functions in the above two scripts to get data for data visualization

2. Wind Speed & Air Quality

    - get_bom_data.py: Retrieve wind speed data for a certain site during a short time period from ElasticSearch

    - get_epa_data.py: Retrieve PM2.5 concentration data for a certain site during a short time period from ElasticSearch

    - scenario2.ipynb: Call the functions in the above two scripts to get data for data visualization




## Running

1. Active jupter notebook
    ```sh
    jupter notebook
    ```

2. Open the link you get and find our jupter notebook


### test

## Pre-requirements

- Fission FaaS installed and running on a cluster
- ElasticSearch installed on the cluster
- Fission client installed
- Python 3.10 or newer

## Running

```sh
cd ./test
python3 unitest end2end.py
```
