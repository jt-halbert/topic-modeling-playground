#!/usr/bin/python

import nltk,json,pprint
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.tokenize import WordPunctTokenizer
from collections import Counter


tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
stops = set(stopwords.words('english'))
file = open("/data/datasets/enron.json", "r")
corpusFile = open("/home/jthalbert/github/topic-modeling-playground/eee/AllWords.txt","w")
BOW_File = open("/home/jthalbert/github/topic-modeling-playground/eee/bagOfWords.txt","w")


punct='`\'\-,()\.;<>:?&%$!^=@{}#*[]'

docOpen=0
docFailed=0
corpusTermsAll={}

for line in file:
	try:
		email=json.loads(line)
		docOpen+=1
		#print json.dumps(email, indent=4, sort_keys=True)
		payload=email["payload"]
		message_id=email['headers']['Message-ID']
		Subject=email['headers']['Subject']
		docWords=[]

		#payload to tokens
		tokens = [word for sent in sent_tokenize(payload) for word in word_tokenize(sent)]
		docWords= filter(lambda word: word not in punct, tokens)
		docWordsLower = [x.lower() for x in docWords ]
		docWordsFilters = filter(lambda word: word not in stops,docWordsLower)

		c = Counter(docWordsFilters)
		for word in set(docWordsFilters):
			BOW_File.write('%s\t%s\t%d\n' % (message_id,word, c[word]))
			if word in corpusTermsAll:
				corpusTermsAll[word]=corpusTermsAll[word] + c[word]
			else:
				corpusTermsAll[word]=c[word]

	except ValueError:
		print 'Decoding JSON has failed'
		docFailed+=1


BOW_File.close()
for word in corpusTermsAll:
	corpusFile.write('%s\t%d\n' % (word,corpusTermsAll[word]))


