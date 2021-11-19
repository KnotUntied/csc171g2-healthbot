import assessment
import hotline
import stats

ACTIONS = {
    'coronavirus.active_cases': stats.active_cases,
    'coronavirus.confirmed_cases': stats.confirmed_cases,
    'coronavirus.deaths': stats.deaths,
    'coronavirus.new_cases': stats.new_cases,
    'coronavirus.recovered': stats.recovered,

    'coronavirus.assess_yes': assessment.assess_yes,
    'coronavirus.assess_no': assessment.assess_no,
    'coronavirus.assess_previous': assessment.assess_previous,
    'coronavirus.assess_symptoms': assessment.assess_symptoms,
    'coronavirus.assess_age': assessment.assess_age,

    'coronavirus.hotline': hotline.get_hotline
}