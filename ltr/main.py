import pandas as pd
import requests
import json
import subprocess

ELASTICSEARCH_DOMAIN = 'http://localhost:9200'
FEATURESET_NAME = 'featureset_trec_covid_2'
FEATURESET_FILENAME = 'featureset.csv'
INDEX_NAME = 'covid_19_0716'
QREL_FILENAME = 'qrels-covid_d4_j0.5-4.txt'
PARAM_FILENAME = 'rnd5_params.csv'
JUDGMENT_FILENAME = 'judgment_trec_covid_rnd_5.txt'
MODEL_NAME_TEMPLATE = 'model_trec_covid_rnd_5_ranker_{}'
MODEL_FILENAME_TEMPLATE = 'model_files/model_trec_covid_rnd_5_ranker_{}.txt'
RANKLIB_JAR = 'RankLibPlus-0.1.0.jar'
RANKERS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

def get_featureset(featureset_name, featureset_filename):
    df = pd.read_csv(featureset_filename)
    result = {'featureset':{'name':featureset_name, 'features':[]}}
    for (query, index) in zip(df['query'], df['index']):
        result['featureset']['features'].append({
            'name': '{}_match_{}'.format(query, index),
            'params': [query],
            'template': {'match':{index:'{{{{{}}}}}'.format(query)}}
        })
    return result

def put_featureset(featureset, elasticsearch_domain):
    response = requests.delete('{}/_ltr/_featureset/{}'.format(elasticsearch_domain, featureset['featureset']['name']))
    response = requests.post('{}/_ltr/_featureset/{}'.format(elasticsearch_domain, featureset['featureset']['name']), json=featureset)

def read_qrel(qrel_filename):
    result = {}
    with open(qrel_filename) as qrel_file:
        for line in qrel_file:
            tokens = line.split()
            topic_id = int(tokens[0])
            cord_uid = tokens[2]
            rel = int(tokens[3])
            if topic_id not in result:
                result[topic_id] = []
            result[topic_id].append((cord_uid, rel))
    return result

def create_judgment(qrel_data, params, elasticsearch_domain, featureset_name, index_name, judgment_filename):
    print('creating judgment file ...')
    with open(judgment_filename, 'w') as judgment_file:
        for topic_id in qrel_data:
            print('topic {}'.format(topic_id))
            query_json = {
                'query': {
                    'bool': {
                        'filter': [
                            {
                                'terms': {
                                    'cord_uid': [doc[0] for doc in qrel_data[topic_id]]
                                }
                            },
                            {
                                'sltr': {
                                    '_name': 'logged_featureset',
                                    'featureset': featureset_name,
                                    'params': params.loc[topic_id].to_dict()
                                }
                            }
                        ]
                    }
                },
                'ext': {
                    'ltr_log': {
                        'log_specs': {
                            'name': 'log_entry',
                            'named_query': 'logged_featureset'
                        }
                    }
                }
            }
            response = requests.post('{}/{}/_search'.format(elasticsearch_domain, index_name), json=query_json, params={'size':10000})
            hits = response.json()['hits']['hits']
            judgment = {}
            for hit in hits:
                cord_uid = hit['_source']['cord_uid']
                values = [feature['value'] if 'value' in feature else 0 for feature in hit['fields']['_ltrlog'][0]['log_entry']]
                if cord_uid not in judgment:
                    judgment[cord_uid] = values
                else:
                    judgment[cord_uid] = [max(x, y) for (x, y) in zip(judgment[cord_uid], values)]
            for (cord_uid, rel) in qrel_data[topic_id]:
                if cord_uid in judgment:
                    value_str = ' '.join(['{}:{}'.format(idx + 1, value) for (idx, value) in enumerate(judgment[cord_uid])])
                    judgment_file.write('{} qid:{} {}\n'.format(rel, topic_id, value_str))

def train_models(ranklib_jar, rankers, judgment_filename, model_filename_template):
    for ranker in rankers:
        print('creating model file {}'.format(model_filename_template).format(ranker))
        subprocess.run(['java', '-jar', ranklib_jar, '-ranker', str(ranker), '-train', judgment_filename, '-tvs', '0.8', '-save', model_filename_template.format(ranker)])

def upload_models(elasticsearch_domain, featureset_name, rankers, model_name_template, model_filename_template):
    for ranker in rankers:
        response = requests.delete('{}/_ltr/_model/{}'.format(elasticsearch_domain, model_name_template).format(ranker))
        with open(model_filename_template.format(ranker)) as model_file:
            model_data = model_file.read()
        upload_json = {
            'model': {
                'name': model_name_template.format(ranker),
                'model': {
                    'type': 'model/ranklib',
                    'definition': model_data
                }
            }
        }
        response = requests.post('{}/_ltr/_featureset/{}/_createmodel'.format(elasticsearch_domain, featureset_name), json=upload_json)
        print(response.text)

if __name__ == '__main__':
    featureset = get_featureset(FEATURESET_NAME, FEATURESET_FILENAME)
    put_featureset(featureset, ELASTICSEARCH_DOMAIN)
    qrel_data = read_qrel(QREL_FILENAME)
    params = pd.read_csv(PARAM_FILENAME).set_index('topic_id').fillna('')
    create_judgment(qrel_data, params, ELASTICSEARCH_DOMAIN, FEATURESET_NAME, INDEX_NAME, JUDGMENT_FILENAME)
    train_models(RANKLIB_JAR, RANKERS, JUDGMENT_FILENAME, MODEL_FILENAME_TEMPLATE)
    upload_models(ELASTICSEARCH_DOMAIN, FEATURESET_NAME, RANKERS, MODEL_NAME_TEMPLATE, MODEL_FILENAME_TEMPLATE)
