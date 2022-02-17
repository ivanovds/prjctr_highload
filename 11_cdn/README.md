# Handmade CDN

Goal: to create own cdn  
- Set up 5 containers - bind server, load balancer, node1, node2, node3.
- Try to implement different balancing approaches. 
- Implement efficient caching 

# Installing

```
git clone https://github.com/ivanovds/prjctr_cdn
cd prjctr_cdn
sudo docker-compose build
sudo docker network create --gateway 172.16.1.1 --subnet 172.16.1.0/24 hw13_subnet
```

# Testing CDN
```
sudo docker exec -it prjctr_cdn_tester ping cdn.picture.com

PING cdn.picture.com (172.16.1.30) 56(84) bytes of data.
64 bytes from highload-homework-13_load_balancer_world_1.hw13_subnet (172.16.1.30): icmp_seq=1 ttl=64 time=0.351 ms
```

# Testing Load Balancers
```
docker-compose run --rm siege -c25 -t10s -b "http://cdn.picture.com/1.jpg"
```

- **Cache on**
```
Transactions:                  12559 hits           14104 hits           15459 hits
Availability:                 100.00 %             100.00 %             100.00 %
Elapsed time:                   9.24 secs            9.16 secs            9.63 secs
Data transferred:             986.37 MB           1107.79 MB           1214.13 MB
Response time:                  0.00 secs            0.02 secs            0.03 secs
Transaction rate:            1359.20 trans/sec    1539.74 trans/sec    1605.30 trans/sec
Throughput:                   106.75 MB/sec        120.94 MB/sec        126.08 MB/sec
Concurrency:                    4.91                24.80                49.53
Successful transactions:       12559                14105                15459
Failed transactions:               0                    0                    0
Longest transaction:            0.02                 0.05                 0.33
Shortest transaction:           0.00                 0.01                 0.00
```

- **Cache off**
- **Round Robin**
```
Transactions:                   8280 hits           13919 hits           13419 hits
Availability:                 100.00 %             100.00 %             100.00 %
Elapsed time:                   9.46 secs            9.92 secs            9.48 secs
Data transferred:             650.30 MB           1093.18 MB           1053.91 MB
Response time:                  0.01 secs            0.02 secs            0.03 secs
Transaction rate:             875.26 trans/sec    1403.12 trans/sec    1415.51 trans/sec
Throughput:                    68.74 MB/sec        110.20 MB/sec        111.17 MB/sec
Concurrency:                    4.93                24.77                49.53
Successful transactions:        8280                13919                13419
Failed transactions:               0                    0                    0
Longest transaction:            0.03                 0.07                 0.12
Shortest transaction:           0.00                 0.00                 0.00
```

- **Cache off**
- **least_conn**
```
Transactions:                   9251 hits          10850 hits            13114 hits
Availability:                 100.00 %            100.00 %              100.00 %
Elapsed time:                   9.85 secs           9.52 secs             9.08 secs
Data transferred:             726.56 MB           852.15 MB            1029.96 MB
Response time:                  0.01 secs           0.02 secs             0.03 secs
Transaction rate:             939.19 trans/sec   1139.71 trans/sec     1444.27 trans/sec
Throughput:                    73.76 MB/sec        89.51 MB/sec         113.43 MB/sec
Concurrency:                    4.92               24.77                 49.64
Successful transactions:        9251               10850                 13114
Failed transactions:               0                   0                     0
Longest transaction:            0.03                0.11                  0.14
Shortest transaction:           0.00                0.00                  0.01
```
