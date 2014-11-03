#!/usr/bin/python

import nltk,json,pprint
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.tokenize import WordPunctTokenizer
from collections import Counter


tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
stops = set(stopwords.words('english'))
file = open("/home/mwilcher/enron.json", "r")
corpusFile = open("/home/mwilcher/eee/outfile.txt","w")

punct='`\'\-,()\.;<>:?&%$!^='

docOpen=0
docFailed=0

for line in file:
	try:
		docOpen+=1
		email=json.loads(line)
		
		#print json.dumps(email, indent=4, sort_keys=True)
		payload=email["payload"]
		message_id=email['headers']['Message-ID']
		Subject=email['headers']['Subject']
		docWords=[]
		tokens = [word for sent in sent_tokenize(payload) for word in word_tokenize(sent)]
		docWords= filter(lambda word: word not in punct, tokens)
		docWordsLower = [x.lower() for x in docWords ]
		docWordsFilters = filter(lambda word: word not in stops,docWordsLower)
		c = Counter(docWordsFilters)
		for word in docWordsFilters:
			corpusFile.write('%s\t%s\t%d\n' % (message_id,word, c[word]))	
			
	except ValueError:
		print 'Decoding JSON has failed'
		docFailed+=1


	
