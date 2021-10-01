import json
import requests
from datetime import datetime as dt

from dateutil.parser import isoparse

from flask import Flask, request, make_response, jsonify

from apify_client import ApifyClient

app = Flask(__name__)
log = app.logger

client = ApifyClient()


@app.route('/', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    try:
        action = req.get('queryResult').get('action')
    except AttributeError:
        return 'json error'

    if action == 'coronavirus.confirmed_cases':
        res = confirmed_cases(req)
    else:
        log.error('Unexpected action.')

    print('Action: ' + action)
    print('Response: ' + res)

    return make_response(jsonify({'fulfillmentText': res}))


def confirmed_cases(req):
    # data = requests.get(
    #     'https://api.apify.com/v2/key-value-stores/lFItbkoNDXKeSWBBA/records/LATEST?disableRedirect=true'
    # )

    # data_json = data.json()
    # data_confirmed = data_json.get('infected')
    # data_updated = data_json.get('lastUpdatedAtApify')
    # data_updated_iso = isoparse(data_updated)
    # data_updated_tz = data_updated_iso.astimezone

    # if data_confirmed:
    #     response = f'According to the DOH, there have been {data_confirmed} confirmed cases as of {}'
    # else:
    #     response = 'We were unable to retrieve data from the DOH. Please try again.'

    # return response
    return 'Hello World!'


# def _call_apify_api():
#     return requests.get(
#         'http://api.worldweatheronline.com/premium/v1/weather.ashx'
#     )


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')