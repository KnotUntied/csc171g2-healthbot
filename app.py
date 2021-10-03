from flask import Flask, request, make_response, jsonify

from actions import ACTIONS

# from apify_client import ApifyClient

app = Flask(__name__)
log = app.logger

# client = ApifyClient()

@app.route('/', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    try:
        action = req.get('queryResult').get('action')
    except AttributeError:
        return 'json error'

    try:
        res = ACTIONS[action](req)
    except KeyError:
        log.error('Unexpected action.')

    print('Action: ' + action)
    print('Response: ' + res)

    return make_response(jsonify({'fulfillmentText': res}))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')