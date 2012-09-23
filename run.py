#!/usr/bin/env python
#encoding=utf8

## Function: Perform all the procudures in order.
## Procedure: 1.Extract main text from mails and create word tokens;
##            2.Get the stem of words and remove stop words;
##            3.Word Feature Selection by gini index and frequency
##            4.Compute TF-IDF and output feature file
##            5. 5-fold cross validation
##              5.1 partition
##              5.2 train
##              5.3 test
##              5.4 average and get F-score
## Date: 2012/9/23

import os
from python.extractText import extractTokens
from python.wordProcess import loadStopwords, filterWords
from python.featureSelection import mkTable, wordSelection
from python.computeFeature import computeTfidf
from python.partition import partitionData
from python.trainTest import train, test, sparseTransform


## Path Setting
# File path setting
Stopword_file = './dictionary/stopwords'
final_feature_file = './features/feature.full'
word_map_file = './features/word.map'
doc_map_file = './features/doc.map'
instance_group_file = './features/feature'
# Source file root path
Baseball_dir = "./baseball/"
Hockey_dir = "./hockey/"
# Feature file root path
Feature_dir = "./features/"

## Value Setting
# Word Lest frequency setting
word_freq = 5
# Least gini index setting
gini_index = 0.2
# K-cross validation
K = 5
# Setting parameters of perceptron algorithm
learn_rate = 0.25
maxIter = 1000

#----Start Running-----
# Get source files' lists
baseball_files = map(lambda x: Baseball_dir + x, os.listdir(Baseball_dir))
hockey_files = map(lambda x: Hockey_dir + x, os.listdir(Hockey_dir))

# Procedure 1 and 2
print 'Start procedure 1 and 2: Extract Main text and pre-processing text data ...'
all_tokens = []
#lm = WordNetLemmatizer()
id_sep = len(os.listdir(Baseball_dir))

stopwordDic = loadStopwords(Stopword_file)
for i, baseball_file in enumerate(baseball_files):
    tokens = extractTokens(baseball_file)
    tokens = filterWords(stopwordDic, tokens)
    all_tokens.append(['-1'] + tokens)

for i, hockey_file in enumerate(hockey_files):
    tokens = extractTokens(hockey_file)
    tokens = filterWords(stopwordDic, tokens)
    all_tokens.append(['1'] + tokens)
print 'Finish procedure 1 and 2.'

# Procedure 3
print 'Start procedure 3: Word feature selection ...'
token_table = mkTable(all_tokens)
token_table = wordSelection(token_table, id_sep, word_freq, gini_index)
print 'Finish procedure 3.'

# Procedure 4
print 'Start procedure 4: Compute tf-idf value ...'
word_map = {}   # word id mapping
wfd = open(word_map_file, 'w')
for i, word in enumerate(token_table.keys()):
    word_map[word] = str(i+1)
    wfd.write(word + ' ' + str(i+1) + '\n')
wfd.close()

dimensions = len(word_map)  # dimensions of features

final_feature_table = computeTfidf(token_table, all_tokens, word_map)
wfd = open(final_feature_file, 'w')
for final_feature in final_feature_table:
    wfd.write(' '.join(final_feature) + '\n')
wfd.close()
print 'Finish procedure 4.'

## Procedure 5
print 'Start procedure 5: Train and test ...'
F_baseball = 0.0
F_hockey = 0.0
# procedure 5.1
instance_groups = partitionData(final_feature_table, K)
for k in xrange(K):     # Output partitioned instances
    wfd = open(instance_group_file + '.' + str(k+1), 'w')
    lines = map(lambda x: ' '.join(x), instance_groups[k])
    wfd.write('\n'.join(lines))
    wfd.close()

# procedure 5.2 + 5.3
for k in xrange(K):
    train_set = [group for i, group in enumerate(instance_groups) if i != k]
    train_set = sparseTransform(train_set, K-1, dimensions)
    test_set = instance_groups[k]
    test_set = sparseTransform([test_set], 1, dimensions)
    # Train
    [w, b] = train(train_set, learn_rate, maxIter, dimensions)
    # Test
    [F_1, F_2] = test(test_set, w, b)
    print 'Iter %d: %f, %f' % (k+1, F_1, F_2)
    F_baseball += F_1
    F_hockey += F_2

# procedure 5.4
F_baseball = F_baseball / K
F_hockey = F_hockey / K
print 'Finish procedure 5.'

## Output the final result
print 'The F-score of class "Baseball" %f ...\n' % (F_baseball)
print 'The F-score of class "Hockey" %f ...\n' % (F_hockey)
