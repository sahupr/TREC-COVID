import xml.etree.ElementTree as ET
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re



# Reprocess a list of tokens (that is not properly handled by nltk.tokenize) and return a list of processed tokens. Do the following:
# Split every token of words connected by slashes into separate tokens (eg. ['weather/climate'] -> ['weather', 'climate'])
# Join every token starting with a contraction with its previous token (eg. ['virus', "'s"] -> ["virus's"])
def process_tokens(tokens):
	slash_split_tokens = []
	contraction_join_tokens = []
	for token in tokens:
		slash_split_tokens.extend(token.split('/'))
	slash_split_tokens = list(filter(lambda token: len(token) > 0, slash_split_tokens))
	for token in slash_split_tokens:
		if token[0] == "'" and len(contraction_join_tokens) > 0:
			contraction_join_tokens[-1] = contraction_join_tokens[-1] + token
		else:
			contraction_join_tokens.append(token)
	return contraction_join_tokens



# Tokenize a text into a list of words. Do the following:
# Split all words (to lowercase) and punctuation into a list of tokens
# Remove all punctuation tokens (strings that do not contain any letter)
# Remove all stop words
# Lemmatize all remaining tokens
def tokenize(text):
	tokens = []
	stop_words = set(stopwords.words('english'))
	lemmatizer = WordNetLemmatizer()
	for sent in sent_tokenize(text):
		for word in word_tokenize(text):
			tokens.append(word.lower())
	tokens = list(filter(lambda token: re.search('[a-zA-Z]', token), tokens))
	tokens = process_tokens(tokens)
	tokens = list(filter(lambda token: token not in stop_words, tokens))
	tokens = list(map(lemmatizer.lemmatize, tokens))
	return tokens



# Return a dictionary of queries of form {topic_id:[query,question,narrative]} where:
# topic_id is attribute number in tag <topic>
# query is processed string of text in tag <query>
# question is processed string of text in tag <question>
# narrative is processed string of text in tag <narrative>
def get_queries(xml_filename):
	tree = ET.parse(xml_filename)
	topics = tree.getroot()
	queries = {}
	for topic in topics:
		metadata = []
		for topic_metadata in topic:
			metadata.append(' '.join(tokenize(topic_metadata.text)))
		queries[topic.attrib['number']] = metadata
	return queries



if __name__ == '__main__':
	queries = get_queries('topics-rnd1.xml')
	for topic_id in queries:
		print('topic id:', topic_id)
		print('query:', queries[topic_id][0])
		print('question:', queries[topic_id][1])
		print('narrative:', queries[topic_id][2])
		print()
