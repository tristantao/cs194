import pandas
import os
import csv
DATA_PATH = "/Users/t-rex-Box/Desktop/work/cs194/hw1/data/" # Make this the /path/to/the/data

AMAZON_DICT_FULL = {}
AMAZON_DICT_SMALL = {}
GOOGLE_DICT_FULL = {}
GOOGLE_DICT_SMALL = {}

def load(dir_root, csv_name, target_dict):
    with open(os.path.join(dir_root, csv_name), 'rb') as f:
        reader = csv.reader(f)
        next(reader, None) #ignore header
        for row in reader:
            target_dict[row[0]] = " ".join(row[1:])

load(DATA_PATH, 'Amazon.csv', AMAZON_DICT_FULL)
load(DATA_PATH, 'Amazon_small.csv', AMAZON_DICT_SMALL)
load(DATA_PATH, 'Google.csv', GOOGLE_DICT_FULL)
load(DATA_PATH, 'Google_small.csv', GOOGLE_DICT_SMALL)

print len(AMAZON_DICT_FULL)
print len(AMAZON_DICT_SMALL)
print len(GOOGLE_DICT_FULL)
print len(GOOGLE_DICT_SMALL)


import re

quickbrownfox = "A quick brown fox jumps over the lazy dog."
split_regex = r'\W+'

# TODO Implement this
def simple_tokenize(string):
    tokens = re.split(split_regex, string)
    processed_tokens = [x.lower() for x in tokens if x != ""]
    return processed_tokens

print simple_tokenize(quickbrownfox) # Should give ['a', 'quick', 'brown', ... ]

stopwords = [] # Load from file
with open(os.path.join(DATA_PATH, "stopwords.txt"), 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
        stopwords += (row)
#print stopwords

# TODO Implement this
def tokenize(string):
    tokens = re.split(split_regex, string)
    processed_tokens = [x.lower() for x in tokens if x != "" and x.lower() not in stopwords]
    return processed_tokens

print tokenize(quickbrownfox) # Should give ['quick', 'brown', ... ]


# TODO Compute these (dict() or DataFrame OK)
amazon_rec2tok = {}
google_rec2tok = {}
total_tokens = 0 # TODO Fix me

for key, val in AMAZON_DICT_SMALL.items():
	token = tokenize(val)
	amazon_rec2tok[key] = token
	total_tokens += len(token)

for key, val in GOOGLE_DICT_SMALL.items():
	google_rec2tok[key] = tokenize(val)
	total_tokens += len(tokenize(val))

#print amazon_rec2tok
print 'There are %s tokens in the combined data sets' % total_tokens

sorted_amazon = sorted(amazon_rec2tok.iteritems(), key=lambda (k, v): len(v), reverse=True)
biggest_record = sorted_amazon[0][0] # TODO Fix me
print 'The Amazon record with ID "%s" has the most tokens' % biggest_record

print len(sorted_amazon[0][1])
print len(sorted_amazon[1][1])
print len(sorted_amazon[100][0])


# TODO Implement this
def tf(tokens):
	tf_count_hash = {}
	total = float(len(tokens))
	for t in tokens:
		tf_count_hash[t] = tf_count_hash.get(t, 0) + 1
	tf_count_hash.update((x, y/total) for x, y in tf_count_hash.items())
	return tf_count_hash
print tf(tokenize(quickbrownfox)) # Should give { 'quick': 0.1666 ... }


# TODO Implement this
def find_idfs(corpus):
    #corpus: dict of id:[tokens]
    #return dic token: weights
    idf_hash = {}
    size = float(len(corpus))
    token_hash = {}
    for tokens in corpus.values(): #{id:[tokens]}
        dup_check = set()
        for token in tokens: #for each token in [tokens], update the token count only ONCE per document.
            if token not in dup_check:
                token_hash[token] = token_hash.get(token, 0) + 1
                dup_check.add(token) #no longer counted for again.
    token_hash.update((x, size/y) for x, y in token_hash.items())
    return token_hash


combined = dict(amazon_rec2tok.items() + google_rec2tok.items())
idfs_small = find_idfs(combined)
unique_tokens = len(idfs_small) # Fix me
print (idfs_small)
#print len(amazon_rec2tok)
#print len(google_rec2tok)
#print len(combined)
#print token_hash

print "There are %s unique tokens in the small data sets." % unique_tokens

# Plotting goes here
#

# TODO Implement this
def tfidf(tokens, idfs):
    tokens_tf_hash = tf(tokens)
    tokens_tfidf_hash = {}
    for token in tokens:
        tokens_tfidf_hash[token] = idfs[token] * tokens_tf_hash[token]
    return tokens_tfidf_hash

rec_b000hkgj8k_weights = tfidf(amazon_rec2tok['b000hkgj8k'], idfs_small) # Fix me

print "Amazon record 'b000hkgj8k' has tokens and weights:\n%s" % rec_b000hkgj8k_weights

import math

# Optional utility
def dotprod(a, b):
    sum_product = 0.0
    for key in a.keys():
        sum_product += (a.get(key, 0) * b.get(key, 0)) #if the other document doens't have this single token, it'll be 0 anyways.
    return sum_product

# Optional utility
def norm(a):
    return math.sqrt(dotprod(a, a))

# Optional freebie
def cossim(a, b):
    return dotprod(a, b) / norm(a) / norm(b)

test_vec1 = {'foo': 2, 'bar': 3, 'baz': 5 }
test_vec2 = {'foo': 1, 'bar': 0, 'baz': 20 }
print dotprod(test_vec1, test_vec2), norm(test_vec1) # Should be 102 6.16441400297

# TODO Implement this
def cosine_similarity(string1, string2, idfs):
    tokens_a = tokenize(string1)
    tokens_b = tokenize(string2)
    vector_a = tfidf(tokens_a, idfs)
    vector_b = tfidf(tokens_b, idfs)
    #print vector_a
    #print vector_b
    return cossim(vector_a, vector_b)

print cosine_similarity("Adobe Photoshop",
                        "Adobe Illustrator",
                        idfs_small) # Should be 0.0577243382163

# TODO Compute similarities
similarities = {}
for amazon_key, amazon_val in AMAZON_DICT_SMALL.items():
    for google_key, google_val in GOOGLE_DICT_SMALL.items():
        #print google_val
        similarities[(amazon_key, google_key)] = cosine_similarity(amazon_val, google_val, idfs_small)

print 'Requested similarity is %s.' % similarities[('b000o24l3q',
  'http://www.google.com/base/feeds/snippets/17242822440574356561')]


gold_standard = [] # Load this if not already loaded
#loading in (amazon, google) format
with open(os.path.join(DATA_PATH, "Amazon_Google_perfectMapping.csv"), 'rb') as f:
    reader = csv.reader(f)
    next(reader, None) #ignore header
    for row in reader:
        gold_standard.append(tuple(row))

true_dups = 0 # Fix me
false_dups = 0
total_sim_dups = 0.0
total_sim_non = 0.0

for amazon_id, amazon_val in AMAZON_DICT_SMALL.items():
    for google_id, google_val in GOOGLE_DICT_SMALL.items():
        if (amazon_id, google_id) in gold_standard: #dup
            true_dups += 1
            total_sim_dups += cosine_similarity(amazon_val, google_val, idfs_small)
        else: #non dup
            false_dups += 1
            total_sim_non += cosine_similarity(amazon_val, google_val, idfs_small)


avg_sim_dups = total_sim_dups / true_dups # Fix me
avg_sim_non = total_sim_non / false_dups # Fix me

print "There are %s true duplicates." % true_dups
print "The average similarity of true duplicates is %s." % avg_sim_dups
print "And for non duplicates, it is %s." % avg_sim_non






