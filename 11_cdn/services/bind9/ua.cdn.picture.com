$ORIGIN .
$TTL 3600       ; 1 hour
cdn.picture.com         IN SOA  ns1.picture.com. hostmaster.picture.com. (
                                2          ; serial
                                900        ; refresh (15 minutes)
                                600        ; retry (10 minutes)
                                86400      ; expire (1 day)
                                3600       ; minimum (1 hour)
                                )
$TTL 0  ; 0 seconds
                        NS      ns1.picture.com.
                        NS      ns2.picture.com.
$TTL 3600       ; 1 hour
                        A       172.16.1.20
