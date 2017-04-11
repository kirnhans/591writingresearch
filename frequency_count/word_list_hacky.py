import string
from autocorrect import spell
import enchant

'''Get a dictionary with numbers as keys and the words occurring that many times as values'''
def sort_by_freq(freq_dict):
	freq_list = dict()
	for key in freq_dict:
		occurence = freq_dict[key]
		if occurence in freq_list:
			freq_list[occurence] += [key]
		else:
			freq_list[occurence] = [key]
	return freq_list

'''Get a dictionary with each word (key) associated with its raw frequency (value), total number of words'''
def word_freq(text):
	words = word_list(text)
	freq = dict()
	for word in words:
		if word in freq:
			freq[word]+=1
		else:
			freq[word]=1
	return freq,len(words)

'''Get the words into a list'''
def word_list(text):
	text_no_punc=text.translate(None, string.punctuation)
	word_list = text_no_punc.split()
	for i in xrange(len(word_list)):
		word_list[i] = spell(word_list[i]) #autocorrect spellings
		lowered = word_list[i].lower() #lower case words for accurate word counts
		if (lowered!="i" and is_word(lowered)): #except we don't change proper nouns or 'I'
			word_list[i] = lowered
	return word_list

def is_word(string):
	dictionary = enchant.Dict("en_US")
	return dictionary.check(string)