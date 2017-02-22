#importing dependencies
from bs4 import BeautifulSoup
import requests
import re
import operator 
import json
from tabulate import tabulate
import sys
from stop_words import get_stop_words

#get the words
def getWordList(url):
    word_list = []
    #raw data
    source_code = requests.get(url)
    #convert to text
    plain_text = source_code.text
    #lxml format
    soup = BeautifulSoup(plain_text,'lxml')

    #find the words in paragraph tag
    for text in soup.findAll('p'):
        if text.text is None:
            continue
        #content
        content = text.text
        #lowercase and split into an array
        words = content.lower().split()

        #for each word
        for word in words:
            #remove non-chars
            cleaned_word = clean_word(word)
            #if there is still something there
            if len(cleaned_word) > 0:
                #add it to our word list
                word_list.append(cleaned_word)

    return word_list


#clean word with regex
def clean_word(word):
    cleaned_word = re.sub('[^A-Za-z]+', '', word)
    return cleaned_word


def createFreqTable(word_list):
    #word count
    word_count = {}
    for word in word_list:
        #index is the word
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1

    return word_count

#remove stop words
def remove_stop_words(frequency_list):
    stop_words = get_stop_words('en')

    temp_list = []
    for key,value in frequency_list:
        if key not in stop_words:
            temp_list.append([key, value])

    return temp_list

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
	#print sorted_word_list
	#removing stop words
	if(search_mode)	:
		sorted_word_list= remove_stop_words(sorted_word_list)

	print sorted_word_list
	#calculating frequency
	total_word_sum = 0
	for key,value in sorted_word_list:
		total_word_sum = total_word_sum + value
	#get top 20 words related to the query
	if(len(sorted_word_list)>20):
		sorted_word_list=sorted_word_list[:20]


	#creating final list 
	final_list = []
	for key,value in sorted_word_list:
		per_value=float(value*100)/total_word_sum
		final_list.append([key,value,round(per_value,4)])

	#print headers
	print_header = ['Word','Frequency','Freq%' ]
	#print table
	print(tabulate(final_list, headers=print_header, tablefmt='orgtbl'))

except Exception as e:
	print ("server did not respond")




