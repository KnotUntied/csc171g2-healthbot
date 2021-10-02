import json
import requests
from datetime import datetime as dt
from datetime import timedelta, timezone

from dateutil.parser import isoparse

from flask import Flask, request, make_response, jsonify

# from apify_client import ApifyClient

app = Flask(__name__)
log = app.logger

# client = ApifyClient()

PH_TZOBJECT = timezone(timedelta(hours=8), name="Malay Peninsula Standard Time")

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


def _get_from_apify(val, name, period='total'):
    data = requests.get(
        'https://api.apify.com/v2/key-value-stores/lFItbkoNDXKeSWBBA/records/LATEST?disableRedirect=true'
    )

    data_json = data.json()
    data_value = data_json.get(val)
    # data_updated = data_json.get('lastUpdatedAtApify')
    # data_updated_iso = isoparse(data_updated)
    # data_updated_tz = data_updated_iso.astimezone(PH_TZOBJECT)

    if data_value:
        if period == 'current':
            response = f'According to the DOH, the current number of {name} for COVID-19 is {data_value:,}.'
        else:
            response = f'According to the DOH, the total number of {name} for COVID-19 is {data_value:,}.'
    else:
        response = 'We were unable to retrieve data from the DOH. Please try again.'

    return response


def confirmed_cases(req):
    return _get_from_apify('infected', 'confirmed cases')

def deaths(req):
    return _get_from_apify('deceased', 'deaths')

def recovered(req):
    return _get_from_apify('recovered', 'recoveries')

def active_cases(req):
    return _get_from_apify('activeCases', 'active cases', 'current')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')