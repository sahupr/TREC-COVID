from elasticsearch import Elasticsearch
import pandas as pd
from collections import OrderedDict

def read_valid_file(valid_filename):
    result = set()
    with open(valid_filename) as valid_file:
        for line in valid_file:
            result.add(line.strip())
    return result

def read_qrel_files(qrel_filenames):
    result = set()
    for qrel_filename in qrel_filenames:
        with open(qrel_filename) as qrel_file:
            for line in qrel_file:
                result.add(line.strip().split()[2])
    return result

def ltr_search(es_index, valid_filename, query_filename, param_filename, qrel_filenames, output_filename, multi_match_type, multi_match_fields, use_ltr, ltr_model, score_mode, query_weight, rescore_query_weight, rescore_size, search_size, output_size, run_tag):
    es = Elasticsearch(timeout=300)
    valid_cord_uids = read_valid_file(valid_filename)
    queries = pd.read_csv(query_filename).fillna('').set_index('topic_id')
    params = pd.read_csv(param_filename).fillna('').set_index('topic_id')
    qrel_cord_uids = read_qrel_files(qrel_filenames)
    with open(output_filename, 'w') as output_file:
        for topic_id in queries.index:
            if not use_ltr:
                query_json = {
                    'query': {
                        'multi_match': {
                            'query': queries.loc[topic_id, 'query'],
                            'type': multi_match_type,
                            'fields': multi_match_fields
                        }
                    }
                }
            else:
                query_json = {
                    'query': {
                        'multi_match': {
                            'query': queries.loc[topic_id, 'query'],
                            'type': multi_match_type,
                            'fields': multi_match_fields
                        }
                    },
                    'rescore': {
                        'window_size': rescore_size,
                        'query': {
                            'rescore_query': {
                                'sltr': {
                                    'params': params.loc[topic_id].to_dict(),
                                    'model': ltr_model
                                }
                            },
                            'score_mode': score_mode,
                            'query_weight': query_weight,
                            'rescore_query_weight': rescore_query_weight
                        }
                    }
                }
            response = es.search(index=es_index, body=query_json, size=search_size)
            hits = response['hits']['hits']
            result_cord_uids = [hit['_source']['cord_uid'] for hit in hits]
            result_cord_uids = [result_cord_uid for result_cord_uid in result_cord_uids if result_cord_uid in valid_cord_uids and result_cord_uid not in qrel_cord_uids]
            result_cord_uids = list(OrderedDict.fromkeys(result_cord_uids))
            result_cord_uids = result_cord_uids[:output_size]
            for (counter, result_cord_uid) in enumerate(result_cord_uids):
                output_file.write('{} Q0 {} {} {} {}\n'.format(topic_id, result_cord_uid, counter + 1, (output_size - counter) / output_size, run_tag))

if __name__ == '__main__':
    ltr_search(
        es_index = 'covid_19_0619_2',
        valid_filename = 'docids-rnd4.txt',
        query_filename = 'rnd4_run0_query.csv',
        param_filename = 'rnd4_params.csv',
        qrel_filenames = ['qrels-covid_d3_j0.5-3.txt'],
        output_filename = 'output.txt',
        multi_match_type = 'cross_fields',
        multi_match_fields = ['title', 'abstract', 'metamap_term_00_title_abstract'],
        use_ltr = True,
        ltr_model = 'model_trec_covid_rnd_4_2_ranker_0',
        score_mode = 'total',
        query_weight = 1.0,
        rescore_query_weight = 1.0,
        rescore_size = 2000,
        search_size = 2000,
        output_size = 1000,
        run_tag = 'CincyMedIR-0'
    )
