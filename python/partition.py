#!/usr/bin/env python
#encoding=utf8

from random import shuffle

def partitionData(ins_features, K):
    '''Input:
            ins_features: the feature list of instances
            K: k cross validation
    '''
    instance_groups = []
    shuffle(ins_features)
    for k in xrange(K):
        instance_groups.append([x for i, x in enumerate(ins_features) if i%K == k])

    return instance_groups

if __name__ == "__main__":
    ins_features = [['1', '11:2'], ['-1', '3:4'], ['1', '11:2'], ['-1', '3:4']]
    a = partitionData(ins_features, 2)
    print a
