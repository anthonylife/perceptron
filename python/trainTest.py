#!/usr/bin/env python
#encoding=utf8

## Function: train and test
## Date: 2012/9/23

import numpy as np
from scipy.sparse import csr_matrix     # sparse matrix representation

def train(train_set, learn_rate, maxIter, dimensions):
    '''Input:
            train_set: have k-1 groups inside
            learn_rate: the learning rate of perceptron algorithm
            maxIter: the maximum iterations of the learning algorithm
    '''
    # Initialize all the parameters
    w = [0 for i in xrange(dimensions)] # function parameter of each dimension
    w = np.array(w)
    b = 0   # bias

    iterNum = 0
    # parameters adjustment
    while iterNum < maxIter:
        if iterNum % 50 == 0:
            print 'iter num: %d ...' % iterNum
        error_tag = False
        for i in xrange(len(train_set)):
            x = train_set[i].toarray()[0][1:]
            y = train_set[i].toarray()[0][0]
            # parameter condition
            # print y * (np.dot(w,x) + b)
            if y * (np.dot(w, x)+b) <= 0:
                w = w + learn_rate*y*x
                b = b + learn_rate*y
                error_tag = True
        # All instances are classified accurately
        if not error_tag:
            break
        iterNum = iterNum + 1

    return w, b

def test(test_set, w, b):
    # Initial
    acc_baseball = 0
    ass_baseball = 0
    num_baseball = 0
    acc_hockey = 0
    ass_hockey = 0
    num_hockey = 0

    for i in xrange(len(test_set)):
        x = test_set[i].toarray()[0][1:]
        y = test_set[i].toarray()[0][0]
        y_comp = np.dot(w, x) + b
        if y_comp < 0:
            ass_baseball = ass_baseball + 1
            if y < 0:
                num_baseball = num_baseball + 1
                acc_baseball = acc_baseball + 1
            elif y > 0:
                num_hockey = num_hockey + 1
        elif y_comp > 0:
            ass_hockey = ass_hockey + 1
            if y < 0:
                num_baseball = num_baseball + 1
            elif y > 0:
                num_hockey = num_hockey + 1
                acc_hockey = acc_hockey + 1

    P_baseball = acc_baseball * 1.0 / ass_baseball
    R_baseball = acc_baseball * 1.0 / num_baseball
    F_baseball = 2*P_baseball*R_baseball / (P_baseball+R_baseball)
    P_hockey = acc_hockey * 1.0 / ass_hockey
    R_hockey = acc_hockey * 1.0 / num_hockey
    F_hockey = 2*P_hockey*R_hockey / (P_hockey+R_hockey)

    return F_baseball, F_hockey

def sparseTransform(instance_groups, K, dimensions):
    sparseFeatures = []
    for i in xrange(K):
        for instance in instance_groups[i]:
            label = int(instance[0])
            features = [0 for j in xrange(dimensions + 1)]
            ins_dimension = map(lambda x: int(x.split(":")[0]), instance[1:])
            ins_value = map(lambda x: float(x.split(":")[1]), instance[1:])
            feature_vector = np.array(features)
            feature_vector[0] = label
            feature_vector[ins_dimension] = ins_value
            sparseFeatures.append(csr_matrix(feature_vector))
    return sparseFeatures

if __name__ == "__main__":
    # Test 'sparseTransform'
    a = [[['-1', '10:3', '20:4'], ['1', '11:4', '22:1']], [['1', '4:1'], ['-1', '2:1', '6:3']]]
    b = sparseTransform(a, 2, 40)
    '''for item in b:
        print item
        print item.toarray()[0]'''

    print train(b, 0.2, 100, 40)
