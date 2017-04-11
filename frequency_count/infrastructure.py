
import nltk
import os
import string
from nltk.tag.stanford import StanfordPOSTagger

import parse
from word_list_hacky import word_freq, sort_by_freq

STANFORD_MODELS = "/Users/kirnhans/Documents/15-591/stanford-postagger-full-2014-08-27/models/english-bidirectional-distsim.tagger"
CLASSPATH = "/Users/kirnhans/Documents/15-591/stanford-postagger-full-2014-08-27/stanford-postagger-3.4.1.jar"

corpus_directory = "corpus"
output_directory = "output"

def initStories(read_directory):
	stories = []
	outputs = os.listdir(output_directory)
	for filename in os.listdir(read_directory):
		address = read_directory + "/" + filename
		if (filename.endswith(".txt") and (filename not in outputs)):
			stories += [Story(address)]
			print filename
	for story in stories:
		print story.address
		story.freq()

class Story(object):
	'''
	'''
	def __init__(self,address):
		self.address = address
		self.f = open(address,"r")
		self.text = self.f.read()
		self.tagger = StanfordPOSTagger(STANFORD_MODELS, CLASSPATH)

	'''
	Uncommon Words
	1. Get word frequencies for words in corpus.
	2. Normalize
	3. Save this in data structure.
	'''
	def freq(self):
		(self.word_freq,self.length) = word_freq(self.text)
		self.word_freq_ordered = sort_by_freq(self.word_freq)

		output_text = self.address + "\n"
		for key in sorted(list(self.word_freq_ordered.keys())):
			output_text += key + " : " + self.word_freq_ordered[key] + "\n"
		output_text += "length: " + self.length + "\n"
		output_text += "\n"
		print output_text


#not designed to isolated words - need to input sentences into postagger
	def pos_freq(self):
		if (not self.word_freq):
			freq(self)
		self.pos_freq = dict()
		for word in self.word_freq:
			word_pos = self.tagger.tag([word]) #PROBLEM
			pos = word_pos[1]
			if pos in self.pos_freq:
				self.pos_freq[pos] += self.word_freq[word]
			else:
				self.pos_freq[pos] = self.word_freq[word]
		print self.pos_freq

# initStories("corpus")
initStories("training")