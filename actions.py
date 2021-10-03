import json
import requests
# from datetime import datetime as dt
from datetime import timedelta, timezone

# from dateutil.parser import isoparse

PH_TZOBJECT = timezone(timedelta(hours=8), name="Malay Peninsula Standard Time")

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


ACTIONS = {
    'coronavirus.confirmed_cases': confirmed_cases,
    'coronavirus.deaths': deaths,
    'coronavirus.recovered': recovered,
    'coronavirus.active_cases': active_cases
}