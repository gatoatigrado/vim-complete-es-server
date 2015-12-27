"""
Queries ElasticSearch for completions
"""
from __future__ import absolute_import
from __future__ import print_function

from es_complete.es_client import es
from es_complete import text_analysis


def get_context_words(request):
    i = request.current_line + 1
    context_lines = request.lines[max(0, i - 1):i]
    return [
        w.lower()
        for w in text_analysis.get_all_words("\n".join(context_lines))
    ]


def uniq(results):
    seen = set()
    for r in results:
        if r not in seen:
            seen.add(r)
            yield r


def elasticsearch_complete(request):
    context_words = get_context_words(request)
    prefix_match = {
        "term": {"prefix_term": request.word_being_completed.lower()}
    }
    context_query = {
        "terms": {"context": context_words}
    }
    query = {"bool": {"should": (
        ([prefix_match] if request.word_being_completed else []) +
        ([context_query] if context_words else [])
    )}}
    results = es.search(
        index="completions",
        body={
            "query": query,
            "_source": ["term"]
        }
    )
    results = list(uniq(
        hit['_source']['term'] for hit in results['hits']['hits']
    ))

    # for demostration purposes
    import sys
    import simplejson
    print("ES completions: {}   -->   {}".format(
        simplejson.dumps(query),
        simplejson.dumps(results)
    ), file=sys.stderr)

    return results
