"""
Setup grafana by creating dashboard and datasource for it with metrics
Based on json files
"""
import datetime

import requests
from elasticsearch import Elasticsearch


# GRAFANA SETUP - board and datasource
headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'}

# Dashboard creating
with open('grafana/dashboard.json', 'rb') as f:
    dashboard_data = f.read()

response = requests.post(
    'http://admin:admin@localhost:3000/api/dashboards/db',
    data=dashboard_data,
    headers=headers)

if response.status_code == 412:
    print('Dashboard with the same name already exists!')
elif response.status_code != 200:
    raise Exception(f'Problem with dashboard creation, status code: {response.status_code}\nError: {response.text}')
else:
    print('Grafana Dashboard created!')

# Datasource creating
with open('grafana/datasource.json', 'rb') as f:
    datasource_data = f.read()


response = requests.post(
    'http://admin:admin@localhost:3000/api/datasources',
    data=datasource_data,
    headers=headers)

if response.status_code == 409:
    print('Datasource with the same name already exists!')
elif response.status_code != 200:
    raise Exception(f'Problem with datasource creation, status code: {response.status_code}\nError: {response.text}')
else:
    print('Grafana Datasource created!')


# ELASTICSEARCH INDEX CREATE
es = Elasticsearch('http://localhost:9200')

es.indices.create(index='test-index')
print('Elasticsearch test index created!')
