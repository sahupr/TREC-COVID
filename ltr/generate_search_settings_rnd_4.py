import json

SEARCH_SETTING_FILENAME = 'search_settings_rnd_4.json'
OUTPUT_FILENAME_FORMAT_1 = 'run_files/run_{}.txt'
OUTPUT_FILENAME_FORMAT_2 = 'run_files/run_{}_{}_{}.txt'
RUN_TAG_FORMAT_1 = 'CincyMedIR-{}'
RUN_TAG_FORMAT_2 = 'CincyMedIR-{}-{}-{}'
DEFAULT_LTR_MODEL = 'model_trec_covid_rnd_4_2_ranker_0'
DEFAULT_SCORE_MODE = 'total'
DEFAULT_QUERY_WEIGHT = 1.0
DEFAULT_RESCORE_QUERY_WEIGHT = 1.0
SETTINGS_LEVEL_1 = [
    {
        'id_1': 1,
        'id_2': 2,
        'query_filename': 'queries_rnd_4_text.csv',
        'multi_match_fields': ['title', 'abstract', 'metamap_term_00_title_abstract'],
        'multi_match_type': 'cross_fields'
    },
    {
        'id_1': 3,
        'id_2': 4,
        'query_filename': 'queries_rnd_4_metamap_00_id.csv',
        'multi_match_fields': ['metamap_00_id_title_abstract'],
        'multi_match_type': 'cross_fields'
    },
    {
        'id_1': 5,
        'id_2': 6,
        'query_filename': 'queries_rnd_4_metamap_01_id.csv',
        'multi_match_fields': ['metamap_01_id_title_abstract'],
        'multi_match_type': 'cross_fields'
    },
    {
        'id_1': 7,
        'id_2': 8,
        'query_filename': 'queries_rnd_4_metamap_10_id.csv',
        'multi_match_fields': ['metamap_10_id_title_abstract'],
        'multi_match_type': 'cross_fields'
    },
    {
        'id_1': 9,
        'id_2': 10,
        'query_filename': 'queries_rnd_4_metamap_11_id.csv',
        'multi_match_fields': ['metamap_11_id_title_abstract'],
        'multi_match_type': 'cross_fields'
    }
]
SETTINGS_LEVEL_2 = [
    {
        'id': 1,
        'score_mode': 'total',
        'query_weight': 1.0,
        'rescore_query_weight': 1.0
    },
    {
        'id': 2,
        'score_mode': 'total',
        'query_weight': 0.0,
        'rescore_query_weight': 1.0
    },
    {
        'id': 3,
        'score_mode': 'total',
        'query_weight': 0.2,
        'rescore_query_weight': 0.8
    },
    {
        'id': 4,
        'score_mode': 'total',
        'query_weight': 0.4,
        'rescore_query_weight': 0.6
    },
    {
        'id': 5,
        'score_mode': 'multiply',
        'query_weight': 1.0,
        'rescore_query_weight': 1.0
    }
]
SETTINGS_LEVEL_3 = [
    {
        'id': 0,
        'ltr_model': 'model_trec_covid_rnd_4_2_ranker_0'
    },
    {
        'id': 1,
        'ltr_model': 'model_trec_covid_rnd_4_2_ranker_1'
    },
    {
        'id': 2,
        'ltr_model': 'model_trec_covid_rnd_4_2_ranker_2'
    },
    {
        'id': 3,
        'ltr_model': 'model_trec_covid_rnd_4_2_ranker_3'
    },
    {
        'id': 4,
        'ltr_model': 'model_trec_covid_rnd_4_2_ranker_4'
    },
    {
        'id': 5,
        'ltr_model': 'model_trec_covid_rnd_4_2_ranker_5'
    },
    {
        'id': 6,
        'ltr_model': 'model_trec_covid_rnd_4_2_ranker_6'
    },
    {
        'id': 7,
        'ltr_model': 'model_trec_covid_rnd_4_2_ranker_7'
    },
    {
        'id': 8,
        'ltr_model': 'model_trec_covid_rnd_4_2_ranker_8'
    },
    {
        'id': 9,
        'ltr_model': 'model_trec_covid_rnd_4_2_ranker_9'
    },
]

if __name__ == '__main__':
    result = []
    for setting_level_1 in SETTINGS_LEVEL_1:
        final_setting = {
            'output_filename': OUTPUT_FILENAME_FORMAT_1.format(setting_level_1['id_1']),
            'query_filename': setting_level_1['query_filename'],
            'multi_match_fields': setting_level_1['multi_match_fields'],
            'multi_match_type': setting_level_1['multi_match_type'],
            'use_ltr': 0,
            'ltr_model': DEFAULT_LTR_MODEL,
            'score_mode': DEFAULT_SCORE_MODE,
            'query_weight': DEFAULT_QUERY_WEIGHT,
            'rescore_query_weight': DEFAULT_RESCORE_QUERY_WEIGHT,
            'run_tag': RUN_TAG_FORMAT_1.format(setting_level_1['id_1'])
        }
        result.append(final_setting)
        for setting_level_2 in SETTINGS_LEVEL_2:
            for setting_level_3 in SETTINGS_LEVEL_3:
                final_setting = {
                    'output_filename': OUTPUT_FILENAME_FORMAT_2.format(setting_level_1['id_2'], setting_level_2['id'], setting_level_3['id']),
                    'query_filename': setting_level_1['query_filename'],
                    'multi_match_fields': setting_level_1['multi_match_fields'],
                    'multi_match_type': setting_level_1['multi_match_type'],
                    'use_ltr': 1,
                    'ltr_model': setting_level_3['ltr_model'],
                    'score_mode': setting_level_2['score_mode'],
                    'query_weight': setting_level_2['query_weight'],
                    'rescore_query_weight': setting_level_2['rescore_query_weight'],
                    'run_tag': RUN_TAG_FORMAT_2.format(setting_level_1['id_2'], setting_level_2['id'], setting_level_3['id'])
                }
                result.append(final_setting)
    with open(SEARCH_SETTING_FILENAME, 'w') as json_file:
        json_file.write(json.dumps(result, indent=4) + '\n')
