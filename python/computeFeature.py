#!/usr/bin/env python
#encoding=utf8

import sys
import math

def computeTfidf(token_table, all_tokens, word_map):
    final_feature_table = []
    num_docs = len(all_tokens)

    for i, tokens in enumerate(all_tokens):
        final_feature_table.append([tokens[0]])
        token_set = set(tokens[1:])
        for token in token_set:
            if token_table.has_key(token):
                token_doc = token_table[token]
                if not token_doc.has_key(str(i)):
                    print 'doc id error.'
                    sys.exit(1)
                tf = token_doc[str(i)] / 1.0    # unigram: length 1
                #print tf
                term_num_docs = len(token_doc)
                idf = math.log(float(1+num_docs) / (1+term_num_docs))

                tfidf = tf * idf
                feature_s = word_map[token] + ':' + str(tfidf)
                final_feature_table[i] = final_feature_table[i] + [feature_s]
    return final_feature_table

if __name__ == "__main__":
    # Test
    token_table = {'num':{'0':3, '1':2}, 'ha':{'0':1, '1': 1}}
    word_map = {'num':'1', 'ha':'2'}
    all_tokens = [['-1', 'num', 'num', 'ha', 'num'], ['1', 'ha', 'num', 'num'], ['1', 'ewr', 'asdf']]
    final_feature_table = computeTfidf(token_table, all_tokens, word_map)
    print final_feature_table
