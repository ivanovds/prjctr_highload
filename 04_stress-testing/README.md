# Lesson 4
## Stress testing using siege tool
Simple api prepared for stress testing. <br>
[dogpile](https://dogpilecache.sqlalchemy.org/en/latest/) is used for avoiding cache stampede (or dog-piling).

### Setup:

* clone the git repository
* change SECRET_KEY in config.py
* Create DB "projector_db"
* Install siege <br>
[How to install siege on Ubuntu](https://linuxhint.com/install-siege-ubuntu/)
* Run Flask API:
```
cd flask_api
export FLASK_APP=main  
flask run
```
* Run siege tool <br>
[User guide](https://www.tecmint.com/load-testing-web-servers-with-siege-benchmarking-tool/) 
```
siege --concurrent=25 --verbose --time=15s http://127.0.0.1:5000/headers
siege --concurrent=25 --verbose --time=15s http://127.0.0.1:5000/random_row
```

To use more than 255 threads:
```
cd ~/.siege
sudo nano siege.conf
```

change limit parameter:
limit = 1500

```
siege -R siege.conf --concurrent=500 --verbose --time=30s http://127.0.0.1:5000/headers
```



## Stress testing results:

### Concurrency = 25
```
Transactions:		        5823 hits
Availability:		      100.00 %
Elapsed time:		       14.64 secs
Data transferred:	        0.38 MB
Response time:		        0.06 secs
Transaction rate:	      397.75 trans/sec
Throughput:		        0.03 MB/sec
Concurrency:		       24.91
Successful transactions:        5823
Failed transactions:	           0
Longest transaction:	        0.10
Shortest transaction:	        0.03

```

### Concurrency = 50
```
Transactions:		        5364 hits
Availability:		      100.00 %
Elapsed time:		       14.74 secs
Data transferred:	        0.35 MB
Response time:		        0.14 secs
Transaction rate:	      363.91 trans/sec
Throughput:		        0.02 MB/sec
Concurrency:		       49.71
Successful transactions:        5364
Failed transactions:	           0
Longest transaction:	        0.27
Shortest transaction:	        0.02

```

### Concurrency = 255
```
Transactions:		       14839 hits
Availability:		      100.00 %
Elapsed time:		       59.63 secs
Data transferred:	        0.98 MB
Response time:		        0.53 secs
Transaction rate:	      248.85 trans/sec
Throughput:		        0.02 MB/sec
Concurrency:		      132.13
Successful transactions:       14839
Failed transactions:	           0
Longest transaction:	        0.31
Shortest transaction:	        0.04

```

### Concurrency = 500
```
Transactions:		        4730 hits
Availability:		      100.00 %
Elapsed time:		       14.41 secs
Data transferred:	        0.31 MB
Response time:		        1.20 secs
Transaction rate:	      328.24 trans/sec
Throughput:		        0.02 MB/sec
Concurrency:		      392.68
Successful transactions:        4730
Failed transactions:	           0
Longest transaction:	       13.66
Shortest transaction:	        0.51
```


### Concurrency = 700
```
Transactions:		        9802 hits
Availability:		       99.67 %
Elapsed time:		       29.97 secs
Data transferred:	        0.65 MB
Response time:		        1.22 secs
Transaction rate:	      327.06 trans/sec
Throughput:		        0.02 MB/sec
Concurrency:		      400.58
Successful transactions:        9802
Failed transactions:	          32
Longest transaction:	       29.38
Shortest transaction:	        0.00
```

So we got failed transactions only with concurrent=700. Real maximum concurrency in this case is 400.  