from __future__ import absolute_import
from __future__ import print_function

from elasticsearch import Elasticsearch


es = Elasticsearch("http://elasticsearch:9200/")


# ensure the index exists on startup
es.indices.create(index='completions', ignore=400)


def recreate_index():
    es.indices.delete(index='completions')
    es.indices.create(index='completions')
