import psycopg2
import pandas as pd
import time

df = pd.read_csv('books.csv')

def test_shard():
    with psycopg2.connect(dbname='mybooks', user='postgres', password='postgres', host='localhost', port=5433) as conn:
        conn.autocommit = True
        with conn.cursor() as cursor:
            id = 1
            while id < 1000000:
                for index, row in df.iterrows():
                    ins = f"INSERT INTO books_view (id, category_id, author, title, year) VALUES ({id},{row['category']},'{row['author_name']}','{row['book_title']}',{row['publish_date']});"
                    cursor.execute(ins)

                    id = id+1
                    if(id>=1000000):
                        break



def test_one_node():
    with psycopg2.connect(dbname='mybooks2', user='postgres', password='postgres', host='localhost', port=5433) as conn:
        conn.autocommit = True
        with conn.cursor() as cursor:
            id = 1
            while id < 1000000:
                for index, row in df.iterrows():
                    ins = f"INSERT INTO books (id, category_id, author, title, year) VALUES ({id},{row['category']},'{row['author_name']}','{row['book_title']}',{row['publish_date']});"
                    cursor.execute(ins)

                    id = id+1
                    if(id>=1000000):
                        break

def test(func):
    start_time = time.time()
    func()
    return (time.time() - start_time)

t = test(test_shard)
print('Write with sharding =', t, 'sec')

t = test(test_one_node)
print('Write without sharding =', t, 'sec')
