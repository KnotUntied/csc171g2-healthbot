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


# Request contexts are lowercased
ASSESS_QUESTIONS = {
    'coronavirus_assess_q1': 'Q1: Have you recently travelled to or resided in a country with local transmission of COVID-19?',
    'coronavirus_assess_q2': 'Q2: Have you recently travelled to or resided in an area under enhanced community quarantine (ECQ)?',
    'coronavirus_assess_q3': ('Q3: Were you exposed to a confirmed COVID-19 case through any of the following situations?\n'
            'A. Staying in a closed environment (such as classroom, household, workspace, or gathering)\n'
            'B. Travelling in close proximity to a confirmed case\n'
            'C. Giving direct care to a COVID-19 patient without proper personal protective equipment'),
    'coronavirus_assess_q4': ('Q4: Which of the following symptoms do you have right now?\n'
            'You may also answer "all" or "none."\n'
            '1. Fever - temperatures higher than 38°C for more than 48 hours\n'
            '2. Cough - with/without phlegm\n'
            '3. Shortness of breath\n'
            '4. Diarrhea and/or vomiting\n'
            '5. Sore throat\n'
            '6. Nasal congestion - runny and/or stuffy nose\n'
            '7. Muscle pain and/or fatigue'),
    'coronavirus_assess_q5': 'Q4b: Did any of your symptoms appear from the past 14 days?',
    'coronavirus_assess_q6': 'Q5: How old are you in years?',
    'coronavirus_assess_q7': ('Q6: Do you have any of the following medical conditions?\n'
            '1. Diabetes\n'
            '2. Hypertension\n'
            '3. Cancer, with ongoing chemotherapy or radiation therapy\n'
            '4. Heart disease (such as congestive heart failure or coronary artery disease)\n'
            '5. Lupus, scleroderma, dermatomyositis or another connective tissue disease\n'
            '6. Condition or medication (such as steroids) that suppresses the immune system\n'
            '7. Chronic lung disease (such as asthma, chronic obstructive pulmonary disease or tuberculosis)')
}
ASSESS_TYPES = {
    'coronavirus_assess_q1': 'coronavirus_assess_yesno',
    'coronavirus_assess_q2': 'coronavirus_assess_yesno',
    'coronavirus_assess_q3': 'coronavirus_assess_yesno',
    'coronavirus_assess_q4': 'coronavirus_assess_symptoms',
    'coronavirus_assess_q5': 'coronavirus_assess_yesno',
    'coronavirus_assess_q6': 'coronavirus_assess_age',
    'coronavirus_assess_q7': 'coronavirus_assess_yesno'
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
    'coronavirus_assess_q1': 1.15,
    'coronavirus_assess_q2': 1.25,
    'coronavirus_assess_q3': 1.5,
    'coronavirus_assess_q5': 1.5,
    'coronavirus_assess_q6': 1.35,
    'coronavirus_assess_q7': 1.3
}
ASSESS_RESPONSES = {
    'SAFE': 'a',
    'PUM': 'b',
    'PUI_MILD': 'c',
    'PUI_SEVERE': 'd'
}

def _get_request_values(req):
    session = req.get('session')
    params = req.get('queryResult').get('parameters')
    return (session, params)

def _get_contexts_cleared(req):
    contexts = req.get('queryResult').get('outputContexts')
    for context in contexts:
        context['lifespanCount'] = 0
    return contexts

def _get_current_coronavirus_assess_q(session, contexts):
    context_prefix = session + '/contexts/'
    questions = list(ASSESS_QUESTIONS)
    for c in contexts:
        if c['name'].removeprefix(context_prefix) in questions:
            return c['name'].removeprefix(context_prefix)
    else:
        return None

def _add_context(session, contexts, context_name):
    new_context_name = session + '/contexts/' + context_name
    for c in contexts:
        if c['name'] == new_context_name:
            c['lifespanCount'] = 5
            return c
    else:
        new_context = {
            'name': new_context_name,
            'lifespanCount': 5
        }
        contexts.append(new_context)
        return new_context

def assess_yes(req):
    (session, params) = _get_request_values(req)
    contexts = _get_contexts_cleared(req)

    assess_Q_name = _get_current_coronavirus_assess_q(session, contexts)
    if assess_Q_name:
        params[assess_Q_name] = 'yes'
        if assess_Q_name == 'coronavirus_assess_q7':
            text = 'Test complete.'
        else:
            _assess_keys = list(ASSESS_QUESTIONS.keys())
            _next_Q = _assess_keys[_assess_keys.index(assess_Q_name) + 1]
            assess_Q = _add_context(session, contexts, _next_Q)
            text = ASSESS_QUESTIONS[_next_Q]

            assess_type = _add_context(session, contexts, ASSESS_TYPES[_next_Q])

            assess = _add_context(session, contexts, 'coronavirus_assess')
            assess['parameters'] = assess['parameters'] | params
    else:
        assess_Q = _add_context(session, contexts, 'coronavirus_assess_q1')
        text = ASSESS_QUESTIONS['coronavirus_assess_q1']

        params['coronavirus_assess_q1'] = 'yes'
        assess_type = _add_context(session, contexts, 'coronavirus_assess_yesno')

        assess = _add_context(session, contexts, 'coronavirus_assess')
        assess['parameters'] = assess['parameters'] | params

    return {'fulfillmentText': text,
            'outputContexts': contexts}

def assess_no(req):
    (session, params) = _get_request_values(req)
    contexts = _get_contexts_cleared(req)

    assess_Q_name = _get_current_coronavirus_assess_q(session, contexts)
    if assess_Q_name:
        params[assess_Q_name] = 'no'
        if assess_Q_name == 'coronavirus_assess_q7':
            text = 'Test complete.'
        else:
            _assess_keys = list(ASSESS_QUESTIONS.keys())
            _next_Q = _assess_keys[_assess_keys.index(assess_Q_name) + 1]
            assess_Q = _add_context(session, contexts, _next_Q)
            text = ASSESS_QUESTIONS[_next_Q]

            assess_type = _add_context(session, contexts, ASSESS_TYPES[_next_Q])

            assess = _add_context(session, contexts, 'coronavirus_assess')
            assess['parameters'] = assess['parameters'] | params
    else:
        text = 'The self-assessment has been cancelled.'

    return {'fulfillmentText': text,
            'outputContexts': contexts}

def assess_previous(req):
    pass

def assess_symptoms(req):
    (session, params) = _get_request_values(req)
    contexts = _get_contexts_cleared(req)

    if params.get('all'):
        params['coronavirus_symptom'] = list(ASSESS_POINTS.keys())

        assess_Q = _add_context(session, contexts, 'coronavirus_assess_q5')
        text = ASSESS_QUESTIONS['coronavirus_assess_q5']

        assess_yesno = _add_context(session, contexts, 'coronavirus_assess_yesno')
    elif params.get('coronavirus_symptom'):
        assess_Q = _add_context(session, contexts, 'coronavirus_assess_q5')
        text = ASSESS_QUESTIONS['coronavirus_assess_q5']

        assess_yesno = _add_context(session, contexts, 'coronavirus_assess_yesno')
    else:
        assess_Q = _add_context(session, contexts, 'coronavirus_assess_q6')
        text = ASSESS_QUESTIONS['coronavirus_assess_q6']

    assess = _add_context(session, contexts, 'coronavirus_assess')
    assess['parameters'] = assess['parameters'] | params

    return {'fulfillmentText': text,
            'outputContexts': contexts}

# def assess_age(req):
#     pass

ACTIONS = {
    'coronavirus.active_cases': active_cases,
    'coronavirus.confirmed_cases': confirmed_cases,
    'coronavirus.deaths': deaths,
    'coronavirus.new_cases': new_cases,
    'coronavirus.recovered': recovered,

    'coronavirus.assess_yes': assess_yes,
    'coronavirus.assess_no': assess_no,
    'coronavirus.assess_previous': assess_previous,
    'coronavirus.assess_symptoms': assess_symptoms,
    # 'coronavirus.assess_age': assess_age
}