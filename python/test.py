#!/usr/bin/env python
#encoding=utf8

import time

a = [i for i in range(10000000)]

'''K = 5
final = []
t1 = time.clock()
for k in xrange(K):
    final.append([x for i, x in enumerate(a) if i % K==k])
t2 = time.clock()
print t2-t1

final = [[], [], [], [], []]
t3 = time.clock()
for i, x in enumerate(a):
    if i % K == 0:
        final[0].append(x)
    if i % K == 1:
        final[1].append(x)
    if i % K == 2:
        final[2].append(x)
    if i % K == 3:
        final[3].append(x)
    if i & K == 4:
        final[4].append(x)

t4 = time.clock()
print t4-t3'''
t1 = time.clock()
index = 0
for i in a:
    index = index + 1
t2 = time.clock()
print t2-t1

t3 = time.clock()
b = len(a)
t4 = time.clock()
print t4-t3

