from ltr_search import ltr_search
import json

SEARCH_SETTING_FILENAME = 'search_settings_rnd_4.json'
ES_INDEX = 'covid_19_0619_2'
VALID_FILENAME = 'docids-rnd4.txt'
PARAM_FILENAME = 'rnd4_params.csv'
QREL_FILENAMES = ['qrels-covid_d3_j0.5-3.txt']
RESCORE_SIZE = 2000
SEARCH_SIZE = 2000
OUTPUT_SIZE = 1000

if __name__ == '__main__':
    with open(SEARCH_SETTING_FILENAME) as json_file:
        settings = json.load(json_file)
    for setting in settings:
        ltr_search(
            es_index = ES_INDEX,
            valid_filename = VALID_FILENAME,
            query_filename = setting['query_filename'],
            param_filename = PARAM_FILENAME,
            qrel_filenames = QREL_FILENAMES,
            output_filename = setting['output_filename'],
            multi_match_type = setting['multi_match_type'],
            multi_match_fields = setting['multi_match_fields'],
            use_ltr = (setting['use_ltr'] != 0),
            ltr_model = setting['ltr_model'],
            score_mode = setting['score_mode'],
            query_weight = setting['query_weight'],
            rescore_query_weight = setting['rescore_query_weight'],
            rescore_size = RESCORE_SIZE,
            search_size = SEARCH_SIZE,
            output_size = OUTPUT_SIZE,
            run_tag = setting['run_tag']
        )
        print('{} created'.format(setting['output_filename']))
