# highload-homework-19

**Horizontal Sharding**

- Create 3 docker containers: postgresql-b, postgresql-b1, postgresql-b2
- Setup horizontal sharding as it's described in this lesson
- Insert 1 000 000 rows into books
- Measure performance
- Do the same without sharding
- Compare performance

## Installation 
Clone repository

```
cd highload-homework-19
docker-compose up
cat shard-magic.sql | docker exec -i highload-homework-19_postgres-b_1 psql postgresql://postgres:postgres@postgres-b:5432/postgres
```

## Test performance

Testing performance using the script `test_insert.py`

```
$ python test_insert.py
Write with sharding = 1324.4388916492462 sec
Write without sharding = 833.7225177288055 sec
```
