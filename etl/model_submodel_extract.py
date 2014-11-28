#!/usr/bin/env python
'''Script to extract the model and submodel information and print their counts'''
import sys
def unique_tokens(filename):
    '''Prints the unique tokens in the model/submodel data'''
    tokendict = {}
    with open(filename,'r') as handle:
        for line in handle:
            tokens  = line.strip().split();
            tokens = tokens[1:]
            for tok in tokens:
                if tok in tokendict: tokendict[tok] +=1;
                else:                tokendict[tok] = 1;

    #print all the unique tokens and their counts in descending order'
    tokens = sorted(tokendict.items(),key=lambda x: x[1],reverse=True);
    for tok in tokens:
        print tok;

if __name__=='__main__':
    unique_tokens(sys.argv[1]); 
