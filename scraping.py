#importing dependencies
from bs4 import BeautifulSoup
import requests
import re
import operator 
import json
from tabulate import tabulate
import sys
from stop_words import get_stop_words

wikipedia_api_link = "https://en.wikipedia.org/w/api.php?format=json&action=query&list=search&srsearch="
wikipedia_link = "https://en.wikipedia.org/wiki/"

#input for string to be queried 
if(len(sys.argv)<2):
	print 'Enter valid string'
	exit()

query= sys.argv[1]
#input for stop word removal
if(len(sys.argv)>2):
	search_mode=True
else:
	search_mode=False

url = wikipedia_api_link+query

try:
	response = requests.get(url)
	data = json.loads(response.content.decode('utf-8'))
	#loads json from wikipedia api page and retireves the most relevant article from the top
	wikipedia_page_tag = data['query']['search'][0]['title']
	#create new link to obtain the main article 
	url = wikipedia_link+wikipedia_page_tag
	#gets list of words in the article
	page_word_list = getWordList(url)
	#tabulate and generate frequency of words in the list 
	page_word_count = createFreqTable(page_word_list)
	sorted_word_list = sorted(page_word_count.items(),key=operator.itemgetter(1),reverse=True)
	#removing stop words
	if(search_mode)	:
		sorted_word_list= remove_stop_words(sorted_word_list)

	#calculating frequency
	total_word_sum = 0
	for key,value in sorted_word_list:
		total_word_sum += value
	#get top 20 words related to the query





except Exception as e:
	raise e




