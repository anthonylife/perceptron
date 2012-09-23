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
from python.trainTest import train, test, sparseTransform


## Path Setting
# File path setting
final_feature_file = "./features/feature.full"

## Value Setting
# K-cross validation
K = 5
# Setting parameters of perceptron algorithm
learn_rate = 0.25
maxIter = 1000

# Features readed from files
final_feature_table = []
for line in open(final_feature_file):
    line = line.strip('\n')
    final_feature_table.append(line.split(' '))

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
    print 'Iter %d: %f, %f' % (k, F_1, F_2)
    F_baseball += F_1
    F_hockey += F_2

# procedure 5.4
F_baseball = F_baseball / K
F_hockey = F_hockey / K
print 'Finish procedure 5.'

## Output the final result
print 'The F-score of class "Baseball" %f ...\n' % (F_baseball)
print 'The F-score of class "Hockey" %f ...\n' % (F_hockey)

