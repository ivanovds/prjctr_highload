# How to install and run the application

1. Clone the repository
2. Run `docker-compose up -d --build` in the project folder

# How to test replication
1. Login to the postgres-b container with help the command `docker-compose exec postgres-b bash`
2. Login to postgres server with help the command `psql --username user --dbname=mydb`
3. Sead source data with help the query
```
INSERT INTO products_source_data(id, category_id, brand_id, title, description)
SELECT generate_series(1, 1000100)    AS id,
       floor(random() * 2 + 1)      category_id,
       floor(random() * 100 + 1) as brand_id,
       md5(random()::text)       AS title,
       md5(random()::text)       AS description;
```
4. Test insert of 1 000 000 records with queries
```
/* the table without sharding */
INSERT INTO products_without_sharding SELECT * FROM products_source_data WHERE id <= 1000000; /* execution time - 4 s 565 ms */

/* the table with sharding */
INSERT INTO products SELECT * FROM products_source_data WHERE id <= 1000000;  /* execution time - 34 s 705 ms */
```
5. Test insert of 100 records with queries
```
/* the table without sharding */
INSERT INTO products_without_sharding SELECT * FROM products_source_data WHERE id > 1000000; /* execution time - 3 ms */

/* the table with sharding */
INSERT INTO products SELECT * FROM products_source_data WHERE id > 1000000; /* execution time - 8 ms */
```
