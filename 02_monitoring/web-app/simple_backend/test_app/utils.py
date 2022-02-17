import random
import string

from elasticsearch import Elasticsearch

es = Elasticsearch('http://elasticsearch:9200')


def random_string(n: int = 255):
    return ''.join(random.choice(string.ascii_uppercase) for _ in range(n))


