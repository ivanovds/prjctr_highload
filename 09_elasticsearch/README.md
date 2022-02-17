# Elasticsearch


## Run Elasticsearch and Kibana:
```
sudo docker-compose up
```

## Kibana UI
http://localhost:5602/app/home#/

## Create index:
```
curl -XPUT 'http://localhost:9200/countries' -H 'Content-Type: application/json' -d'
{
 "mappings": {
    "properties" : {
      "Name" : {
        "type": "text",
        "fields": {
            "standard": {
                "type" : "text"
              },  
            "completion": {
              "type": "completion"
            }
        }              
      },
      "Code" : {
        "type" : "keyword"
      }
    }
  }
}
'
```

## Upload data to index:
```
curl -H 'Content-Type: application/json' -XPOST 'http://localhost:9200/countries/_doc/_bulk?pretty' --data-binary @countries.json
```

## Install requirements for search script and Run it: 
```
pip install -r requirements.txt 

python main.py
```

## Results
### length <= 7, without typos
```
Input country`s name and press Enter or q to exist:
Turkey
I found: [{'_index': 'countries', '_type': '_doc', '_id': 'AV23jH0BKF0rUHUV13Ln', '_score': 5.9141097, '_source': {'Name': 'Turkey', 'Code': 'TR'}}]
```

### length <= 7, with 1 typo
```
Input country`s name and press Enter or q to exist:
Turke
I found: []
```

### length > 7, with 1 typo
```
Input country`s name and press Enter or q to exist:
Afghanista
I found: [{'text': 'Afghanistan', '_index': 'countries', '_type': '_doc', '_id': 'H123jH0BKF0rUHUV13Hn', '_score': 8.0, '_source': {'Name': 'Afghanistan', 'Code': 'AF'}}]
```



### length > 7, with 2 typos
```
Input country`s name and press Enter or q to exist:
Afghanizdan
I found: [{'text': 'Afghanistan', '_index': 'countries', '_type': '_doc', '_id': 'H123jH0BKF0rUHUV13Hn', '_score': 7.0, '_source': {'Name': 'Afghanistan', 'Code': 'AF'}}]
```

### length > 7, with 4 typos
```
Input country`s name and press Enter or q to exist:
Afganis
I found: []
```
