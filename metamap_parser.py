import subprocess
import pandas as pd



def get_metamap(raw_query_filename):
	queries = pd.read_csv(raw_query_filename)
	dict_metamap = {'topic_id':queries['topic_id'].to_list(), 'metamap_terms':[]}
	for query in queries['query']:
		file = open('tmp.txt', 'w')
		file.write(query)
		file.close()
		subprocess.call(['./metamaplite.sh', 'tmp.txt'])
		file = open('tmp.mmi', 'r')
		terms = []
		for line in file:
			terms.append(line.split('|')[3])
		file.close()
		dict_metamap['metamap_terms'].append(', '.join(terms))
	return pd.DataFrame(dict_metamap)



if __name__ == '__main__':
	metamap = get_metamap('raw_query.csv')
	metamap.to_csv('metamap_query.csv', index=False, header=True)
