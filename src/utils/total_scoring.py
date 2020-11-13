from ..app.data import get_data
from math import abs, pow

def calculate_total_score(report):
    goal_len = get_data('scoring_settings/goal_speech_length')
    good_expressions = get_data('scoring_settings/good_expressions').split(', ')
    
    speech_len = report['single_data']['speech_length']
    disfluencies = report['single_data']['disfluency_count']
    expressions = report['stream_data']['expression_stream']['stream']
    expressions = [x['expression'] for x in expressions]

    len_score = abs(speech_len - goal_len)/goal_len
    expr_score = sum(x in expressions for x in good_expressions) / len(expressions)
    disf_score = 100*(1-pow(disfluencies,2)/(pow(disfluencies,2)+100))
    total_score = (len_score + expr_score + disf_score) / 3
    return total_score