#!/usr/bin/env python
import sys
'''This script wil convert the model/submodel features into categorical attrs'''

def convert_features(filename,attr_table,attr_idx):
    with open(filename,'r') as filename:
        for line in filename:
            line = line.strip().split(',');
            if line[0]=='RefId':
                new_line = line[:attr_idx] + attr_table + ['others'] +  line[attr_idx+1:];
            else:
                new_line = line[:attr_idx];
                attr_value = line[attr_idx];
                attr_tokens = set(attr_value.split());
                found = False;
                for token in attr_table:
                    if token in attr_tokens: 
                        found = True;
                        new_line += ['yes'];
                    else: 
                        new_line += ['no'];
                if found:
                    new_line += ['no'] 
                else :
                    new_line += ['yes']
                new_line += line[attr_idx+1:]
            print ','.join(new_line);
                
if __name__=="__main__":
    attr_filename = sys.argv[1]
    attr_idx = int(sys.argv[2]) 
    data_filename = sys.argv[3]
    attr_table = []
    with open(attr_filename,'r') as attr_file:
        for line in attr_file:
            attr_table += [line.strip().split()[0]];
    convert_features(data_filename,attr_table,attr_idx);
