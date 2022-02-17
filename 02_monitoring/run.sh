#!/bin/bash

sudo docker-compose down
sudo docker-compose build --no-cache
sudo docker-compose up -d
#sleep 2
#docker exec mongodb bash -c "mongo < /data/mongo-init.js"


#echo "Grafana: http://127.0.0.1:3000 - admin/admin"
#
#echo "Waiting for influxdb start..."
#sleep 10
#echo "Current database list"
#curl -G http://localhost:8086/query?pretty=true --data-urlencode "db=glances" --data-urlencode "q=SHOW DATABASES"
#
#echo
#echo "Create a new database ?"
#echo "curl -XPOST 'http://localhost:8086/query' --data-urlencode 'q=CREATE DATABASE mydb'"
