from flask import Flask, jsonify, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from waitress import serve
from error import InvalidUsage
from pre_trained_dt import LDAModel

app = Flask(__name__)
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

def has_args(iterable, args):
    """Verify that all args are in the iterable."""
    try:
        return all(x in iterable for x in args)

    except TypeError:
        return False


@app.route('/', methods=['GET'])
@limiter.exempt
def ping():
    return 'Running'


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.route('/getLDAPreds', methods=['GET'])
def get_information():
    print(request.json)
    if not has_args(request.json, ['file_url']):
      raise InvalidUsage('Missing Image URL')

    lda = LDAModel()
    outputs = lda.getLDAPreds("0.txt")

    # temporarily returning string
    return str(outputs)

if __name__ == '__main__':
    app.debug = True
    app.run(threaded=True)