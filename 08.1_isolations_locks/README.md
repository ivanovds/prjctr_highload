# Isolations & locks

## 1) PostgreSQL
### Install PostgreSQL

### Create DB and table with some data:
```
sudo -u postgres psql
CREATE DATABASE isolation;
\c isolation;

CREATE TABLE my_table (
    f1 int,
    f2 int
);

INSERT INTO my_table (f1, f2)
VALUES (1, 0);
```

### READ COMMITTED Isolation Level
PostgreSQL does not support "read uncommitted":
[In PostgreSQL READ UNCOMMITTED is treated as READ COMMITTED.](https://www.postgresql.org/docs/current/sql-set-transaction.html)
So "Lost Update" and "Dirty Read" is not reproducible. 

#### - Trying to reproduce Dirty Read:

session1:
```
isolation=# select * from my_table; 
 f1 | f2 
----+----
  1 |  0
(3 rows)

isolation=# BEGIN TRANSACTION ISOLATION LEVEL READ COMMITTED;                  
BEGIN

isolation=*# UPDATE my_table SET f2=f2+1 WHERE f1=1;
UPDATE 1

isolation=*# select * from my_table; 
 f1 | f2 
----+----
  1 |  1
(3 rows)

```
session2:
```
isolation=# select * from my_table; 
 f1 | f2 
----+----
  1 |  0
(3 rows)
```

**So this isolation level prevents Dirty Read.**

#### - Trying to reproduce Non-Repeatable Read:
session2:
```
isolation=# BEGIN TRANSACTION ISOLATION LEVEL READ COMMITTED;
BEGIN

isolation=*# SELECT f2 FROM my_table WHERE f1=1;
 f2 
----
  0
(1 row)
```
session1:
```
isolation=# begin;
BEGIN

isolation=*# UPDATE my_table SET f2=f2+3 WHERE f1=1;
UPDATE 1

isolation=*# end;
COMMIT
```
session2:
```
isolation=*# SELECT f2 FROM my_table WHERE f1=1;
 f2 
----
  3
(1 row)

isolation=*# end;
COMMIT
```
**Managed to reproduce Non-Repeatable Read on 'read committed' isolation level.**


### REPEATABLE READ Isolation Level

#### - Trying to reproduce Non-Repeatable Read:
session2:
```
isolation=# BEGIN TRANSACTION ISOLATION LEVEL REPEATABLE READ;
BEGIN

isolation=*# SELECT f2 FROM my_table WHERE f1=1;
 f2 
----
  0
(1 row)
```
session1:
```
isolation=# begin;
BEGIN

isolation=*# UPDATE my_table SET f2=f2+3 WHERE f1=1;
UPDATE 1

isolation=*# end;
COMMIT
```
session2:
```
isolation=*# SELECT f2 FROM my_table WHERE f1=1;
 f2 
----
  0
(1 row)
```
**So this isolation level prevents Dirty Read.**


#### - Trying to reproduce Phantom Reads:

session2:
```
isolation=# BEGIN TRANSACTION ISOLATION LEVEL REPEATABLE READ;
BEGIN

isolation=*# SELECT SUM(f2) FROM my_table;
 sum 
-----
  78
(1 row)
```
session1:
```
isolation=# INSERT INTO my_table (f1,f2) VALUES (15,20);
INSERT 0 1
```
session2:
```
isolation=*# SELECT SUM(f2) FROM my_table;
 sum 
-----
  78
(1 row)

isolation=*# end;
COMMIT

isolation=# SELECT SUM(f2) FROM my_table;
 sum 
-----
 98
(1 row)
```

And the same situation on "SERIALIZABLE" level. 
So in PostgreSQL "REPEATABLE READ" and "SERIALIZABLE" isolation levels prevent Phantom Reads.



## 2) Percona + InnoDB

### Install Percona Server for MySQL
[Installation guide for Debian and Ubuntu](https://www.percona.com/doc/percona-server/5.7/installation/apt_repo.html)

### Create DB and table with some data:
```
mysql -u root -p
CREATE DATABASE isolation;
\u isolation

CREATE TABLE my_table (
    f1 int,
    f2 int
);

INSERT INTO my_table (f1, f2)
VALUES (1, 0);

SET autocommit=0;
SET GLOBAL innodb_status_output=ON;
SET GLOBAL innodb_status_output_locks=ON;
```

### "SERIALIZABLE" Isolation Level
```
set global transaction_isolation='SERIALIZABLE';
```

- Trying to reproduce Dirty Read:

session1:
```
mysql> select * from my_table; 
+------+------+
| f1   | f2   |
+------+------+
|    1 |    0 |
+------+------+
1 row in set (0,00 sec)

mysql> begin;
Query OK, 0 rows affected (0,00 sec)

mysql> UPDATE my_table SET f2=f2+1 WHERE f1=1;
Query OK, 1 row affected (0,00 sec)
Rows matched: 1  Changed: 1  Warnings: 0
```

session2 (dirty read):
```
mysql> select * from my_table; 
+------+------+
| f1   | f2   |
+------+------+
|    1 |    1 |
+------+------+
1 row in set (0,00 sec)
```
session1:
```
mysql> rollback work;
Query OK, 0 rows affected (0,01 sec)

mysql> select * from my_table; 
+------+------+
| f1   | f2   |
+------+------+
|    1 |    0 |
+------+------+
1 row in set (0,00 sec)
```

I don`t know why I managed to reproduce Dirty Read on SERIALIZABLE isolation level...



SET TRANSACTION SESSION ISOLATION LEVEL SERIALIZABLE;
```
mysql> SELECT @@GLOBAL.transaction_isolation;
+--------------------------------+
| @@GLOBAL.transaction_isolation |
+--------------------------------+
| SERIALIZABLE                   |
+--------------------------------+
1 row in set (0,00 sec)

mysql> SELECT @@SESSION.transaction_isolation;
+---------------------------------+
| @@SESSION.transaction_isolation |
+---------------------------------+
| READ-UNCOMMITTED                |
+---------------------------------+
1 row in set (0,00 sec)
```