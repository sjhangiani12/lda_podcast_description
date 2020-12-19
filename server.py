from flask import Flask, jsonify, request
from waitress import serve
from error import InvalidUsage
from pre_trained_dt import LDAModel
from transcribe import makeTranscript
import time

app = Flask(__name__)

script_name = "script.txt"

def has_args(iterable, args):
    """Verify that all args are in the iterable."""
    try:
        return all(x in iterable for x in args)

    except TypeError:
        return False


@app.route('/', methods=['GET'])
def ping():
    return 'Running'


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.route('/getLDAPreds', methods=['POST'])
def get_information():
    print(request.json['file_url'])
    if not has_args(request.json, ['file_url']):
      raise InvalidUsage('Missing Image URL')

    job_name = str(time.strftime("%Y%m%d-%H%M%S"))

    # take s3 file and transcribe
    transcription = makeTranscript(job_name,request.json['file_url'],'mp3')

    lda = LDAModel()
    # take transcription and make predicition
    outputs = lda.getLDAPreds(transcription)

    # temporarily returning string
    return str(outputs)

if __name__ == '__main__':
    app.debug = True
    app.run(threaded=True)