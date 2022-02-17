from db import test_db
from utils import calculate_time, print_table

cursor = test_db.cursor()

select_exact_sql = 'SELECT * FROM test_db.users_table_with_idx WHERE {} = "2020-01-01";'
select_range_sql = 'SELECT * FROM test_db.users_table_with_idx WHERE "2020-01-01" < {} < "2020-01-02";'


@calculate_time
def select_from_db(sql):
    cursor.execute(sql)
    cursor.fetchall()


print_table(
    ['Action', 'Duration'],
    [['SELECT EXACT without index', select_from_db(select_exact_sql.format('date_joined'))],
     ['SELECT EXACT with btree index', select_from_db(select_exact_sql.format('birth_date'))]])

print_table(
    ['Action', 'Duration'],
    [['SELECT RANGE without index', select_from_db(select_range_sql.format('date_joined'))],
     ['SELECT RANGE with btree index', select_from_db(select_range_sql.format('birth_date'))]])

