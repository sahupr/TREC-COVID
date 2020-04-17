import xml.etree.ElementTree as ET
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re



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
	tokens = filter(lambda token: re.search('[a-zA-Z]', token), tokens)
	tokens = filter(lambda token: token not in stop_words, tokens)
	tokens = list(map(lemmatizer.lemmatize, tokens))
	return tokens



# Return a list of queries, each query is a dictionary with the following key:
# 'number': topic number
# 'query': tokenized words in <query> tag
# 'question': tokenized words in <question> tag
# 'narrative': tokenized words in <narrative> tag
def get_queries(xml_filename):
	tree = ET.parse(xml_filename)
	topics = tree.getroot()
	queries = []
	for topic in topics:
		metadata = {'number':topic.attrib['number']}
		for topic_metadata in topic:
			metadata[topic_metadata.tag] = tokenize(topic_metadata.text)
		queries.append(metadata)
	return queries



if __name__ == '__main__':
	queries = get_queries('topics-rnd1.xml')
	for query in queries:
		for metadata in query:
			print(metadata, ':', query[metadata])
		print()