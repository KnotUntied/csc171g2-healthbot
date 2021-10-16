from os import getenv

from flask import Flask, request, make_response, jsonify

from actions import ACTIONS

app = Flask(__name__)
log = app.logger

@app.route('/')
@app.route('/index')
def index():
    agent_id = getenv('AGENT_ID')
    return '''
<html>
    <head>
        <meta name="viewport" content="width-device-width, initial-scale=1">
        <title>Healthbot</title>
    </head>
    <body>
        <script src="https://www.gstatic.com/dialogflow-console/fast/messenger/bootstrap.js?v=1"></script>
        <df-messenger
          expand=true
          intent="WELCOME"
          chat-title="Healthbot"
          agent-id=''' + agent_id + '''
          language-code="en"
        ></df-messenger>
    </body>
</html>'''

@app.route('/', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    try:
        action = req.get('queryResult').get('action')
    except AttributeError:
        return 400

    try:
        res = ACTIONS[action](req)
    except KeyError:
        log.error('Unexpected action.')

    print('Action: ' + action)
    print('Response:')
    print(res)

    # return make_response(jsonify({'fulfillmentText': res}))
    return make_response(jsonify(res))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')