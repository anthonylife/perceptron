#!/usr/bin/env python
#encoding=utf8

## Function: Select word features
## Method: frequence and gini index
## Date: 2012/9/23

def mkTable(all_tokens):
    ''' make hash table for all words,
        inverted index.
    '''
    token_table = {}
    for i, tokens in enumerate(all_tokens):
        for token in tokens[1:]:
            if token_table.has_key(token):
                if token_table[token].has_key(str(i)):   # i: doc id
                    token_table[token][str(i)] = token_table[token][str(i)] + 1
                else:
                    token_table[token][str(i)] = 1
            else:
                token_table[token] = {}
                token_table[token][str(i)] = 1
    return token_table


def wordSelection(token_table, id_sep, pre_freq, pre_gini):
    '''Input: token_table -> inverted index table of words;
              id_sep -> the boundary of document id of the two classes.
              pre_freq -> the least time of occuring in documents the selected word should meet
              pre_gini -> the threshold of gini index
    '''
    for token in token_table.keys():
        # Filter words by the time of occuring in documents
        if len(token_table[token]) < pre_freq:
            token_table.pop(token)

        # Compute the gini index and filtering
        else:
            gini = computeGini(token_table[token], id_sep)
            if gini < pre_gini:
                token_table.pop(token)
    return token_table


def computeGini(token_doc, id_sep):
    f_num = 0
    s_num = 0

    for doc_id in token_doc.keys():
        if int(doc_id) < id_sep:
            f_num = f_num + token_doc[doc_id]
        else:
            s_num = s_num + token_doc[doc_id]


    f_p = f_num*1.0/(f_num+s_num)
    s_p = s_num*1.0/(f_num+s_num)
    gini = f_p ** 2 + s_p ** 2

    return gini

if __name__ == "__main__":
    # Test
    test_sample = [['-1', 'he', 'save', 'opportunity', 'chance', 'save'], ['1', 'he', 'fly', 'sky']]
    id_sep = 1
    pre_freq = 2
    pre_gini = 0.6
    token_table = mkTable(test_sample)
    print token_table
    token_table = wordSelection(token_table, id_sep, pre_freq, pre_gini)
    print token_table
