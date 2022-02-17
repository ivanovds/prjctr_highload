import pandas as pd

# dataset taken from https://www.kaggle.com/brosen255/goodreads-books
df = pd.read_csv('good_reads_final.csv')
df = df.drop(columns=['author_average_rating', 'author_gender', 'author_genres', 'author_id', 'author_page_url', 'author_rating_count', 'author_review_count', 'birthplace', 'book_average_rating', 'book_fullurl', 'genre_2', 'num_ratings', 'num_reviews', 'pages', 'score', 'book_id'])

df['publish_date'] = df['publish_date'].apply(lambda x: int(str(x)[-4:]) if str(x)[-4:].strip().isdigit() else 0)
df['author_name'] = df['author_name'].apply(lambda x: str(x).replace('\n', '').replace('\'', '`').strip())
df['book_title'] = df['book_title'].apply(lambda x: str(x).replace('\n', '').replace('\'', '`').strip())

g = df['genre_1'].unique()
range = int(len(g)/3)
g1 = g[0:range]
g2 = g[range:range*2]
def trans(x):
    if x in g1:
        return 1
    if x in g2:
        return 2
    return 3
df['genre_1'] = df['genre_1'].apply(trans)
df = df.rename(columns={'genre_1': 'category'})

# print(df.to_string()) 

df.to_csv("books.csv")


