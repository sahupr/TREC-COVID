import json
import subprocess
import pandas as pd

OUTPUT_FILENAME = 'evaluation_results_rnd_4.csv'
SEARCH_SETTING_FILENAME = 'combine_run_settings_rnd_4.json'
TREC_EVAL_FILENAME = '/home/projects/202004_TREC-COVID/trec_eval/trec_eval'
QREL_FILENAME = 'qrels-covid_d4_j3.5-4.txt' 
MEASURES = ['ndcg_cut_20', 'P_20', 'bpref', 'map', 'Rprec', 'recall_10']

if __name__ == '__main__':
    with open(SEARCH_SETTING_FILENAME) as json_file:
        settings = json.load(json_file)
    result = {'run_tag':[], 'avg':[]}
    for measure in MEASURES:
        result[measure] = []
    for setting in settings:
        result['run_tag'].append(setting['run_tag'])
        proc = subprocess.run([TREC_EVAL_FILENAME, '-m', 'all_trec', '-c', '-M1000', QREL_FILENAME, setting['output_filename']], stdout=subprocess.PIPE, encoding='utf8')
        eval_result = proc.stdout
        avg = 0
        for line in eval_result.strip().split('\n'):
            if len(line) == 0:
                continue
            tokens = line.split()
            if tokens[0] in MEASURES:
                result[tokens[0]].append(float(tokens[2]))
                avg += float(tokens[2]) / len(MEASURES)
        result['avg'].append(avg)
    pd.DataFrame(result).set_index('run_tag')[MEASURES + ['avg']].to_csv(OUTPUT_FILENAME, index=True)
