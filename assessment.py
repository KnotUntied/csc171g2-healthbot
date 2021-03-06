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
    'SAFE': 'You appear to be safe from COVID-19 for now.',
    'PUM': 'You may be classified as a Person Under Monitoring (PUM).',
    'PUI_MILD': 'You may be classified as a Person Under Investigation (PUI) with mild risks.',
    'PUI_SEVERE': 'You may be classified as a Person Under Investigation (PUI) with severe risks.'
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

def _assess_evaluate(params):
    points = 0.1
    symptoms = params.get('coronavirus_symptom')
    if symptoms:
        for symptom in symptoms:
            points += ASSESS_POINTS[symptom]
    for multiplier in list(ASSESS_MULTIPLIERS.keys()):
        if params.get(multiplier) == 'yes':
            points *= ASSESS_MULTIPLIERS[multiplier]
    if params.get('coronavirus_assess_q6') and params.get('coronavirus_assess_q6') >= 60:
        points *= ASSESS_MULTIPLIERS['coronavirus_assess_q6']

    if points >= 18:
        return ASSESS_RESPONSES['PUI_SEVERE']
    elif points >= 14:
        return ASSESS_RESPONSES['PUI_MILD']
    elif points >= 9:
        return ASSESS_RESPONSES['PUM']
    else:
        return ASSESS_RESPONSES['SAFE']

def assess_yes(req):
    (session, params) = _get_request_values(req)
    contexts = _get_contexts_cleared(req)

    assess_Q_name = _get_current_coronavirus_assess_q(session, contexts)
    if assess_Q_name:
        params[assess_Q_name] = 'yes'
        assess = _add_context(session, contexts, 'coronavirus_assess')
        assess['parameters'] = assess['parameters'] | params
        if assess_Q_name == 'coronavirus_assess_q7':
            text = _assess_evaluate(assess['parameters'])
        else:
            _assess_keys = list(ASSESS_QUESTIONS.keys())
            _next_Q = _assess_keys[_assess_keys.index(assess_Q_name) + 1]
            assess_Q = _add_context(session, contexts, _next_Q)
            text = ASSESS_QUESTIONS[_next_Q]

            assess_type = _add_context(session, contexts, ASSESS_TYPES[_next_Q])
    else:
        assess = _add_context(session, contexts, 'coronavirus_assess')
        assess['parameters'] = assess['parameters'] | params

        assess_Q = _add_context(session, contexts, 'coronavirus_assess_q1')
        text = ASSESS_QUESTIONS['coronavirus_assess_q1']

        assess_type = _add_context(session, contexts, 'coronavirus_assess_yesno')

    return {'fulfillmentText': text,
            'outputContexts': contexts}

def assess_no(req):
    (session, params) = _get_request_values(req)
    contexts = _get_contexts_cleared(req)

    assess_Q_name = _get_current_coronavirus_assess_q(session, contexts)
    if assess_Q_name:
        params[assess_Q_name] = 'no'
        assess = _add_context(session, contexts, 'coronavirus_assess')
        assess['parameters'] = assess['parameters'] | params
        if assess_Q_name == 'coronavirus_assess_q7':
            text = _assess_evaluate(assess['parameters'])
        else:
            _assess_keys = list(ASSESS_QUESTIONS.keys())
            _next_Q = _assess_keys[_assess_keys.index(assess_Q_name) + 1]
            assess_Q = _add_context(session, contexts, _next_Q)
            text = ASSESS_QUESTIONS[_next_Q]

            assess_type = _add_context(session, contexts, ASSESS_TYPES[_next_Q])
    else:
        text = 'The self-assessment has been cancelled.'

    return {'fulfillmentText': text,
            'outputContexts': contexts}

def assess_previous(req):
    (session, params) = _get_request_values(req)
    contexts = _get_contexts_cleared(req)

    assess_Q_name = _get_current_coronavirus_assess_q(session, contexts)
    if assess_Q_name != 'coronavirus_assess_q1':
        assess = _add_context(session, contexts, 'coronavirus_assess')
        _assess_keys = list(ASSESS_QUESTIONS.keys())
        if (assess_Q_name == 'coronavirus_assess_q6'
            and not assess['parameters'].get('coronavirus_symptom')
        ):
            _prev_Q = _assess_keys[_assess_keys.index(assess_Q_name) - 2]
        else:
            _prev_Q = _assess_keys[_assess_keys.index(assess_Q_name) - 1]
        assess_Q = _add_context(session, contexts, _prev_Q)
        text = ASSESS_QUESTIONS[_prev_Q]

        assess_type = _add_context(session, contexts, ASSESS_TYPES[_prev_Q])
    else:
        text = 'The self-assessment has been cancelled.'

    return {'fulfillmentText': text,
            'outputContexts': contexts}

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

        assess_age = _add_context(session, contexts, 'coronavirus_assess_age')

    assess = _add_context(session, contexts, 'coronavirus_assess')
    assess['parameters'] = assess['parameters'] | params

    return {'fulfillmentText': text,
            'outputContexts': contexts}

def assess_age(req):
    (session, params) = _get_request_values(req)
    contexts = _get_contexts_cleared(req)

    assess_Q = _add_context(session, contexts, 'coronavirus_assess_q7')
    text = ASSESS_QUESTIONS['coronavirus_assess_q7']

    assess_yesno = _add_context(session, contexts, 'coronavirus_assess_yesno')

    assess = _add_context(session, contexts, 'coronavirus_assess')
    assess['parameters'] = assess['parameters'] | params

    return {'fulfillmentText': text,
            'outputContexts': contexts}