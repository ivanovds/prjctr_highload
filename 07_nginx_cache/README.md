# Nginx cache
Web server with nginx proxy for static files caching.

Example of configuration for nginx for caching static files. Realized functionality:
 - Cache after second request
 - Drop (bypass) cache for particular request 

### Requirements:
 - [docker](https://docs.docker.com/get-docker/) >20.10.7
 - [docker-compose](https://docs.docker.com/compose/install/) >2.1.0
 
### Run on Linux
Firstly, need to clone the git repository. Then run a web server simply executing `run.sh` file:
```shell
sh run.sh
```

### Checking caching results
#### Cache response after second request only 
 - first two requests would return `X-Proxy-Cache: MISS`, which mean that response wasn't cached:
                                          
    ```
    ~$ curl -I http://127.0.0.1:8080/static/bicycle.jpg
    HTTP/1.1 200 OK
    Server: nginx/1.21.4
    Date: Tue, 23 Nov 2021 06:32:38 GMT
    Content-Type: image/png
    Content-Length: 17680
    Connection: keep-alive
    last-modified: Sun, 21 Nov 2021 21:20:05 GMT
    etag: d1c25ce3e4775fabd10d9f32e97c7176
    X-Proxy-Cache: MISS
   ```

 - third request would be with `X-Proxy-Cache` header status `HIT`, which mean that response was cached:

    ```
    ~$ curl -I http://127.0.0.1:8080/static/bicycle.jpg
    HTTP/1.1 200 OK
    Server: nginx/1.21.4
    Date: Tue, 23 Nov 2021 06:32:40 GMT
    Content-Type: image/png
    Content-Length: 17680
    Connection: keep-alive
    last-modified: Sun, 21 Nov 2021 21:20:05 GMT
    etag: d1c25ce3e4775fabd10d9f32e97c7176
    X-Proxy-Cache: HIT
    ```                                     
 
#### Bypassing cache for single file (request)
 - For force cache update `cachepurge` header with value `true` can be used (`X-Proxy-Cache: BYPASS`): 

    ```
    ~$ curl -I http://127.0.0.1:8080/static/car.jpg -H "cachepurge: true"
    HTTP/1.1 200 OK
    Server: nginx/1.21.4
    Date: Tue, 23 Nov 2021 06:32:50 GMT
    Content-Type: image/png
    Content-Length: 22111
    Connection: keep-alive
    last-modified: Sun, 21 Nov 2021 21:21:47 GMT
    etag: 9fb76f7647e2e8d4e0fe24b8d5974c78
    X-Proxy-Cache: BYPASS
    ```     
