import json
import requests
from datetime import timedelta, timezone

PH_TZOBJECT = timezone(timedelta(hours=8), name='Malay Peninsula Standard Time')

PH_LOCATION_ALIAS = {
    'NATIONAL': 'the Philippines',
    'ABRA': 'Abra',
    'AGUSAN DEL NORTE': 'Agusan del Norte',
    'AGUSAN DEL SUR': 'Agusan del Sur',
    'AKLAN': 'Aklan',
    'ALBAY': 'Albay',
    'ANGELES CITY': 'Angeles City',
    'ANTIQUE': 'Antique',
    'APAYAO': 'Apayao',
    'AURORA': 'Aurora',
    'BACOLOD CITY': 'Bacolod City',
    'BAGUIO CITY': 'Baguio City',
    'BASILAN': 'Basilan',
    'BATAAN': 'Bataan',
    'BATANES': 'Batanes',
    'BATANGAS': 'Batangas',
    'BENGUET': 'Benguet',
    'BILIRAN': 'Biliran',
    'BOHOL': 'Bohol',
    'BUKIDNON': 'Bukidnon',
    'BULACAN': 'Bulacan',
    'BUTUAN CITY': 'Butuan',
    'CAGAYAN': 'Cagayan',
    'CAGAYAN DE ORO CITY': 'Cagayan de Oro',
    'CALOOCAN CITY': 'Caloocan',
    'CAMARINES NORTE': 'Camarines Norte',
    'CAMARINES SUR': 'Camarines Sur',
    'CAMIGUIN': 'Camiguin',
    'CAPIZ': 'Capiz',
    'CATANDUANES': 'Catanduanes',
    'CAVITE': 'Cavite',
    'CEBU': 'Cebu',
    'CEBU CITY': 'Cebu City',
    'CITY OF ISABELA': 'Isabela City',
    'CITY OF LAS PIÑAS': 'Las Piñas',
    'CITY OF MAKATI': 'Makati',
    'CITY OF MALABON': 'Malabon',
    'CITY OF MANDALUYONG': 'Mandaluyong',
    'CITY OF MANILA': 'Manila',
    'CITY OF MARIKINA': 'Marikina',
    'CITY OF MUNTINLUPA': 'Muntinlupa',
    'CITY OF NAVOTAS': 'Navotas',
    'CITY OF PARAÑAQUE': 'Parañaque',
    'CITY OF PASIG': 'Pasig',
    'CITY OF SAN JUAN': 'San Juan',
    'CITY OF SANTIAGO': 'Santiago, Isabela',
    'CITY OF VALENZUELA': 'Valenzuela',
    'COTABATO (NORTH COTABATO)': 'North Cotabato',
    'COTABATO CITY': 'Cotabato City',
    'DAGUPAN CITY': 'Dagupan',
    'DAVAO CITY': 'Davao City',
    'DAVAO DE ORO (COMPOSTELA VALLEY)': 'Davao de Oro',
    'DAVAO DEL NORTE': 'Davao del Norte',
    'DAVAO DEL SUR': 'Davao del Sur',
    'DAVAO OCCIDENTAL': 'Davao Occidental',
    'DAVAO ORIENTAL': 'Davao Oriental',
    'DINAGAT ISLANDS': 'the Dinagat Islands',
    'EASTERN SAMAR': 'Eastern Samar',
    'GENERAL SANTOS CITY (DADIANGAS)': 'General Santos City',
    'GUIMARAS': 'Guimaras',
    'IFUGAO': 'Ifugao',
    'ILIGAN CITY': 'Iligan',
    'ILOCOS NORTE': 'Ilocos Norte',
    'ILOCOS SUR': 'Ilocos Sur',
    'ILOILO': 'Iloilo',
    'ILOILO CITY': 'Iloilo City',
    'ISABELA': 'Isabela Province',
    'KALINGA': 'Kalinga',
    'LA UNION': 'La Union',
    'LAGUNA': 'Laguna',
    'LANAO DEL NORTE': 'Lanao del Norte',
    'LANAO DEL SUR': 'Lanao del Sur',
    'LAPU-LAPU CITY (OPON)': 'Lapu-Lapu City',
    'LEYTE': 'Leyte',
    'LUCENA CITY': 'Lucena',
    'MAGUINDANAO': 'Maguindanao',
    'MANDAUE CITY': 'Mandaue',
    'MARINDUQUE': 'Marinduque',
    'MASBATE': 'Masbate',
    'MISAMIS OCCIDENTAL': 'Misamis Occidental',
    'MISAMIS ORIENTAL': 'Misamis Oriental',
    'MOUNTAIN PROVINCE': 'Mountain Province',
    'NAGA CITY': 'Naga, Camarines Sur',
    'NEGROS OCCIDENTAL': 'Negros Occidental',
    'NEGROS ORIENTAL': 'Negros Oriental',
    'NORTHERN SAMAR': 'Northern Samar',
    'NUEVA ECIJA': 'Nueva Ecija',
    'NUEVA VIZCAYA': 'Nueva Vizcaya',
    'OCCIDENTAL MINDORO': 'Occidental Mindoro',
    'OLONGAPO CITY': 'Olongapo',
    'ORIENTAL MINDORO': 'Oriental Mindoro',
    'ORMOC CITY': 'Ormoc',
    'PALAWAN': 'Palawan',
    'PAMPANGA': 'Pampanga',
    'PANGASINAN': 'Pangasinan',
    'PASAY CITY': 'Pasay',
    'PATEROS': 'Pateros',
    'PUERTO PRINCESA CITY': 'Puerto Princesa',
    'QUEZON': 'Quezon',
    'QUEZON CITY': 'Quezon City',
    'QUIRINO': 'Quirino',
    'RIZAL': 'Rizal',
    'ROMBLON': 'Romblon',
    'SAMAR (WESTERN SAMAR)': 'Western Samar',
    'SARANGANI': 'Sarangani',
    'SIQUIJOR': 'Siquijor',
    'SORSOGON': 'Sorsogon',
    'SOUTH COTABATO': 'South Cotabato',
    'SOUTHERN LEYTE': 'Southern Leyte',
    'SULTAN KUDARAT': 'Sultan Kudarat',
    'SULU': 'Sulu',
    'SURIGAO DEL NORTE': 'Surigao del Norte',
    'SURIGAO DEL SUR': 'Surigao del Sur',
    'TACLOBAN CITY': 'Tacloban',
    'TAGUIG CITY': 'Taguig',
    'TARLAC': 'Tarlac',
    'TAWI-TAWI': 'Tawi-Tawi',
    'ZAMBALES': 'Zambales',
    'ZAMBOANGA CITY': 'Zamboanga City',
    'ZAMBOANGA DEL NORTE': 'Zamboanga del Norte',
    'ZAMBOANGA DEL SUR': 'Zamboanga del Sur',
    'ZAMBOANGA SIBUGAY': 'Zamboanga Sibugay'
}

def _get_from_scraper(key, alias, location='NATIONAL'):
    if location == 'NATIONAL':
        data = requests.get(
            'https://raw.githubusercontent.com/KnotUntied/ph-covid19-cases-scraper/master/data/national.json')
        value = data.json().get(key)
    else:
        data = requests.get(
            'https://raw.githubusercontent.com/KnotUntied/ph-covid19-cases-scraper/master/data/local.json')
        value = data.json().get(location).get(key)

    print(f'{key}: {value:,}')

    if value is not None:
        if location in PH_LOCATION_ALIAS:
            text = f'According to the DOH, the number of {alias} in {PH_LOCATION_ALIAS.get(location)} is {value:,}.'
        else:
            text = 'We were unable to identify this location.'
    else:
        text = ('We were unable to retrieve data from the DOH. '
                    'You may also check their COVID-19 dashboard at https://doh.gov.ph/covid19tracker.')

    return {'fulfillmentText': text}

def _get_param_location(req):
    try:
        params = req.get('queryResult').get('parameters')
    except AttributeError:
        return 'json error'

    location = params.get('ph_locations') or 'NATIONAL'
    return location

def active_cases(req):
    location = _get_param_location(req)
    return _get_from_scraper('Active Cases', 'active cases of COVID-19', location)

def confirmed_cases(req):
    location = _get_param_location(req)
    return _get_from_scraper('Total Cases', 'confirmed cases of COVID-19', location)

def deaths(req):
    location = _get_param_location(req)
    return _get_from_scraper('Deaths', 'deaths from COVID-19', location)

def new_cases(req):
    location = _get_param_location(req)
    return _get_from_scraper('New Cases', 'new cases of COVID-19', location)

def recovered(req):
    location = _get_param_location(req)
    return _get_from_scraper('Recoveries', 'recoveries from COVID-19', location)


ASSESS_QUESTIONS = {
    'Q1': 'Have you recently travelled to or resided in a country with local transmission of COVID-19?',
    'Q2': 'Have you recently travelled to or resided in an area under enhanced community quarantine (ECQ)?',
    'Q3': ('Were you exposed to a confirmed COVID-19 case through any of the following situations?\n'
            'A. Staying in a closed environment (such as classroom, household, workspace, or gathering)\n'
            'B. Travelling in close proximity to a confirmed case\n'
            'C. Giving direct care to a COVID-19 patient without proper personal protective equipment'),
    'Q4': ('Which of the following symptoms do you have right now?\n'
            'You may also answer "all" or "none."\n'
            '1. Fever - temperatures higher than 38°C for more than 48 hours\n'
            '2. Cough - with/without phlegm\n'
            '3. Shortness of breath\n'
            '4. Diarrhea and/or vomiting\n'
            '5. Sore throat\n'
            '6. Nasal congestion - runny and/or stuffy nose\n'
            '7. Muscle pain and/or fatigue'),
    'Q5': 'Did any of your symptoms appear from the past 14 days?',
    'Q6': 'How old are you in years?',
    'Q7': ('Do you have any of the following medical conditions?\n'
            '1. Diabetes\n'
            '2. Hypertension\n'
            '3. Cancer, with ongoing chemotherapy or radiation therapy\n'
            '4. Heart disease (such as congestive heart failure or coronary artery disease)\n'
            '5. Lupus, scleroderma, dermatomyositis or another connective tissue disease\n'
            '6. Condition or medication (such as steroids) that suppresses the immune system\n'
            '7. Chronic lung disease (such as asthma, chronic obstructive pulmonary disease or tuberculosis)')
}
ASSESS_POINTS = {
    'fever':               0.6,
    'cough':               0.55,
    'shortness of breath': 0.6,
    'diarrhea':            0.6,
    'sore throat':         0.55,
    'nasal congestion':    0.55,
    'muscle pain':         0.6
}
ASSESS_MULTIPLIERS = {
    'Q1': 1.15,
    'Q2': 1.25,
    'Q3': 1.5,
    'Q5': 1.5,
    'Q6': 1.35,
    'Q7': 1.3
}
ASSESS_RESPONSES = {
    'SAFE': 'a',
    'PUM': 'b',
    'PUI_MILD': 'c',
    'PUI_SEVERE': 'd'
}

def _get_request_values(req):
    session = req.get('session')
    params = req.get('queryResult').get('params')
    return (session, params)

def assess_yes(req):
    # "outputContexts": [
    #   {
    #     "name": "projects/${PROJECT_ID}/agent/sessions/${SESSION_ID}/contexts/context name",
    #     "lifespanCount": 5,
    #     "parameters": {
    #       "param": "param value"
    #     }
    #   }
    # ],
    (session, params) = _get_request_values(req)
    sample_output_context = {
        'name': session + '/contexts/bar',
        'lifespanCount': 5,
        'parameters': params
    }
    return {'fulfillmentText': 'foo',
            'outputContexts': [sample_output_context]}

def assess_no(req):
    pass

def assess_previous(req):
    pass

def assess_symptoms(req):
    pass

ACTIONS = {
    'coronavirus.active_cases': active_cases,
    'coronavirus.confirmed_cases': confirmed_cases,
    'coronavirus.deaths': deaths,
    'coronavirus.new_cases': new_cases,
    'coronavirus.recovered': recovered,

    'coronavirus.assess_yes': assess_yes,
    'coronavirus.assess_no': assess_no,
    'coronavirus.assess_previous': assess_previous,
    'coronavirus.assess_symptoms': assess_symptoms
}