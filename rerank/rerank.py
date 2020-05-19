QREL_FILENAMES = ['qrels-rnd1.txt']
VALID_DOCID_FILENAME = 'docids-rnd1.txt'
RUN_FILENAME = '02_retrieval_run2.csv'
RERANKED_RUN_FILENAME = '02_retrieval_run2_reranked.txt'
RERANKED_NUM_DOCS_PER_TOPIC = 1000
RUN_TAG = 'CincyMedIR-2'

if __name__ == '__main__':
	qrel_map = {}
	for qrel_filename in QREL_FILENAMES:
		with open(qrel_filename, 'r') as qrel_file:
			for line in qrel_file:
				tokens = line.rstrip().split()
				topicid = int(tokens[0])
				docid = tokens[2]
				rel = int(tokens[3])
				qrel_map[(topicid, docid)] = rel
	valid_docids = set()
	with open(VALID_DOCID_FILENAME, 'r') as valid_docid_file:
		for line in valid_docid_file:
			docid = line.rstrip()
			valid_docids.add(docid)
	rankings = {}
	with open(RUN_FILENAME, 'r') as run_file:
		for line in run_file:
			tokens = line.rstrip().split('\t')
			topicid = int(tokens[0])
			docid = tokens[2]
			score = float(tokens[4])
			if docid not in valid_docids:
				print('Warning: Invalid docid:', docid)
			if topicid not in rankings:
				rankings[topicid] = []
			rankings[topicid].append((docid, score))
	for topicid in rankings:
		rankings[topicid] = [doc[0] for doc in sorted(rankings[topicid], key=lambda doc: -doc[1])]
	set_rankings = {topicid:set(rankings[topicid]) for topicid in rankings}
	for topicid, docid in qrel_map:
		if docid in valid_docids and docid not in set_rankings[topicid]:
			rankings[topicid].append(docid)
			set_rankings[topicid].add(docid)
	reranked_rankings = {}
	for topicid in rankings:
		qrel_docs = []
		for rank, docid in enumerate(rankings[topicid]):
			if (topicid, docid) in qrel_map:
				qrel_docs.append((docid, rank, qrel_map[(topicid, docid)]))
		qrel_docs = [doc[0] for doc in sorted(qrel_docs, key=lambda doc: (doc[2], -doc[1]))]
		reranked_rankings[topicid] = []
		for docid in rankings[topicid]:
			if (topicid, docid) in qrel_map:
				reranked_rankings[topicid].append(qrel_docs.pop())
			else:
				reranked_rankings[topicid].append(docid)
	with open(RERANKED_RUN_FILENAME, 'w') as reranked_run_file:
		for topicid in reranked_rankings:
			for rank, docid in enumerate(reranked_rankings[topicid]):
				if rank >= RERANKED_NUM_DOCS_PER_TOPIC:
					break
				reranked_run_file.write('{}\tQ0\t{}\t{}\t{}\t{}\n'.format(topicid, docid, rank + 1, (RERANKED_NUM_DOCS_PER_TOPIC - rank) / RERANKED_NUM_DOCS_PER_TOPIC, RUN_TAG))
