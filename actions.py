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
            'https://raw.githubusercontent.com/KnotUntied/ph-covid19-cases-scraper/master/data/national.json'
        )
    else:
        data = requests.get(
            'https://raw.githubusercontent.com/KnotUntied/ph-covid19-cases-scraper/master/data/local.json'
        )

    value = data.json().get(key)

    if value:
        if location in PH_LOCATION_ALIAS:
            response = f'According to the DOH, the number of {alias} in {PH_LOCATION_ALIAS.get(location)} is {value:,}.'
        else:
            response = 'We were unable to identify this location.'
    else:
        response = ('We were unable to retrieve data from the DOH. '
                    'You may also check their COVID-19 dashboard at https://doh.gov.ph/covid19tracker.')

    return response

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

ACTIONS = {
    'coronavirus.active_cases': active_cases,
    'coronavirus.confirmed_cases': confirmed_cases,
    'coronavirus.deaths': deaths,
    'coronavirus.new_cases': new_cases,
    'coronavirus.recovered': recovered
}