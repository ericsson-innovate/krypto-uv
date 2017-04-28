from flask import Flask, abort, jsonify, make_response, render_template, request
from flask_cors import CORS, cross_origin



app = Flask(__name__)
app.config['CORS_HEADERS'] = ['Content-Type']
app.config['CORS_RESOURCES'] = {r"/*": {"origins": "*"}}
app.config['CORS_ORIGINS'] = ['*']
cors = CORS(app)


@app.route('/')
def index():
    """
    Check the status of the gateway
    :return: 
    """
    response = {
        'status': 'OK',
    }
    return jsonify(response)


@app.route('/auth', methods=['GET'])
def auth():
    print "/auth"

    response = {
        'status': 'OK',
    }
    return jsonify(response)

@app.errorhandler(400)
def bad_request(error):
    print error
    return make_response(jsonify({'error': 'Bad request'}), 400)


@app.errorhandler(404)
def not_found(error):
    print error
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app.run(debug=True)