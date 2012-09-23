#!/usr/bin/env python
#encoding=utf8

## Function: Extract text from mails, remove unrelated symbol.
## Method: Rule-based
## Date: 2012/9/22

import re
import sys
import time
import nltk

def extractTokens(inputFile):
    final_tokens = []
    cache_line = ''

    for i, line in enumerate(open(inputFile)):
        line = line.strip('\n')
        # header line
        #print line
        if i == 0 or i == 1:
            if line.find('Subject: Re: ') != -1:
                line = line.replace('Subject: Re: ', '')
            elif line.find('Subject: ') != -1:
                line = line.replace('Subject: ', '')
            else:
                line = ''
        # cache the 4th line to decide whether it belongs the main text or not
        elif i == 3:
            cache_line = line
            continue
        else:
            # not include forward text
            if not line.startswith('>'):
                if i== 4:
                    line = cache_line + ' ' + line
            else:
                line = ''
        tokens = nltk.word_tokenize(line)
        # Erase punctuation and other uncorrelated symbols
        p = re.compile(r'[^a-zA-Z\']')
        for token in tokens:
            token = token.lower()
            syms = p.findall(token)
            for sym in syms:
                token = token.replace(sym, '')
            p1 = re.compile(r'[a-z]{1,}.*')
            m = p1.match(token)
            if m and token != '' and len(token) != 1:
                final_tokens = final_tokens + [token]

    return final_tokens


def output(outputFile, tokens):
    return ''

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print 'usage: <InputFile> [<OutputFile>]'
        sys.exit(1)
    result = extractTokens(sys.argv[1])
    print result
