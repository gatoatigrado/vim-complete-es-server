from __future__ import absolute_import
from __future__ import print_function

# Fix Flask-autoloaded module path
import sys
if "/code" not in sys.path:
    sys.path.insert(0, "/code")

import flask
import re
import simplejson
from collections import namedtuple

from es_complete import es_client
from es_complete import es_query
from es_complete import es_index_data
from es_complete import text_analysis

app = flask.Flask(__name__)


AutocompleteRequest = namedtuple("AutocompleteRequest", [
    "current_line",
    "current_column",
    "lines",
    "word_being_completed"
])


SPACES_RE = re.compile(ur'[^\w\d\_]+')
def simple_buffer_complete(request):
    if request.word_being_completed:
        words = text_analysis.get_all_words("\n".join(request.lines))
        return [
            w for w in words if w.startswith(request.word_being_completed)
        ]
    else:
        return []


@app.route('/complete')
def complete():
    body = flask.request.get_json(force=True)
    request = AutocompleteRequest(**body)
    basics = simple_buffer_complete(request)
    
    result = (
        simple_buffer_complete(request)[:10] +
        es_query.elasticsearch_complete(request)
    )
    return simplejson.dumps(result)


@app.route("/index-raw", methods=["POST"])
def index_raw():
    es_index_data.index_data(flask.request.get_data())
    return "Success!"


@app.route("/clear-index", methods=["POST"])
def clear_index():
    es_client.recreate_index()
    return "Success!"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=18013, debug=True)
