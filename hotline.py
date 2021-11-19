COVID_HOTLINES = {
    "BUKIDNON" : "0926-927-9916 (Globe),0947-641-0230 (Smart)",
    "CAGAYAN DE ORO CITY" : "0926-927-9908 (Globe),0947-641-0230 (Smart)",
    "CALOOCAN CITY" : "0916-797-6365 ",
    "CAMIGUIN" : "0926-927-9908 (Globe),0947-641-0230 (Smart)",
    "COTOBATO CITY" : "(083) 552-3174,(083) 228-8098",
    "DAVAO CITY" : "(082) 244-3855",
    "GENERAL SANTOS CITY" : "0951-088-8801 (Sun),0951-088-8802 (Sun),0951-088-8803 (Sun)",
    "ILIGAN CITY" : "0926-927-9908 (Globe),0947-641-0230 (Smart)",
    "LANAO DEL NORTE" : "0926-927-9913 (Globe),0947-641-0230 (Smart)",
    "LAS PIÑAS CITY" : "(02) 8552-7964,(02) 8776-7268,(02) 8994-5782,0915-648-1735 (Globe),0928-462-7034 (Smart)",
    "MAKATI CITY" : "168,(02) 8236-5790",
    "MALABON" : "(02) 8921-6009,0942-372-9891",
    "MANDALUYONG CITY" : "(02) 8533-2225,0916-255-8130 (Globe),0961-571-6959 (Smart)",
    "MANILA" : "(02) 8527-5174",
    "MARIKINA" : "161",
    "METRO MANILA CENTER FOR HEALTH DEVELOPMENT" : "(02) 535-1488,(02) 8165-6274",
    "MISAMIS OCCIDENTAL" : "0926-927-9913 (Globe),0947-641-0230 (Smart)",
    "MISAMIS ORIENTAL" : "0926-927-9806 (Globe),0947-641-0230 (Smart)",
    "MUNTINLUPA" : "(02) 8925-4351",
    "NAVOTAS" : "(02) 8281-1111",
    "NORTH COTABATO" : "0907-366-0078 (Smart)",
    "PARAÑAQUE CITY" : "911,(02) 8820-7783",
    "PASAY CITY" : "(02) 8551-2026,0956-778-6524 (Globe),0908-993-7024 (Smart)",
    "PASIG CITY" : "(02) 8643-0000",
    "PATEROS" : "(02) 8642-5159",
    "PHILIPPINE NATIONAL POLICE" : "117",
    "QUEZON CITY" : "122,(02) 8927-8827,(02) 8988-4242 local 8407 and 8416",
    "RESEARCH INSTITUTE TROPICAL MEDICINE": "(02) 8807-2631,(02) 8807-2632,(02) 8807-2637",
    "SAN JUAN CITY" : "(02) 7238-4333",
    "TAGUIG CITY" : "(02) 8789-3200,0966-419-4510",
    "VALENCIA CITY" : "0936-746-3831 (Globe)",
    "VALENZUELA" : "(02) 8352-5000"
}

def hotline(req):
    try:
        params = req.get('queryResult').get('parameters')
    except AttributeError:
        return 'json error'

    location = params.get('ph_hotline')
    if location in COVID_HOTLINES:
        hotlines = COVID_HOTLINES[location].split(",")
        if len(hotlines) == 1:
            text = f"{location.capitalize()}: {COVID_HOTLINES[location]}"
        else:
            text = "{}:".format(location.capitalize())
            for hotline in hotlines:
                text += "\n-{}".format(hotline)
    else:
        text = "Hotline not found in this location!"
    return {'fulfillmentText': text}
