"""
Populates the ElasticSearch index.
"""
from __future__ import absolute_import
from __future__ import print_function

from es_complete.es_client import es
from es_complete import text_analysis


def index_data(data):
    words = [
        w for w in text_analysis.get_all_words(data) if len(w) > 1
    ]

    for i in xrange(len(words)):
        context = [w.lower() for w in words[max(0, i - 4):i]]
        word = words[i]
        word_lower = word.lower()
        prefixes = [word_lower[:j] for j in xrange(1, len(word) + 1)]
        doc = {
            'term': word,
            'context': context,
            'prefix_term': prefixes
        }
        es.index(
            index='completions',
            doc_type='completion',
            body=doc,
            id=hash(repr(doc))
        )
