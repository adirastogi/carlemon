'''Implements the functions to read data and print the metrics '''
import csv;

def print_metrics(predictions,Y):
    '''prints the 4 metrics'''
    true_pos =0;
    true_neg =0;
    false_pos =0;
    false_neg =0;
    assert(len(predictions)==len(Y))
    for p,y in zip(predictions,Y):
        if p==y:
            if p=='+1': true_pos +=1;
            else: true_neg +=1;
        else:
            if p=='+1': false_pos +=1;
            else: false_neg +=1;

    print "%d %d %d %d"%(true_pos,false_neg,false_pos,true_neg);

    print "Acc:",float(true_neg+true_pos)/(true_neg+true_pos+false_neg+false_pos)
    print "Error:",float(false_neg+false_pos)/(true_neg+true_pos+false_neg+false_pos)
    recall  = float(true_pos)/(true_pos+false_neg)
    print "Sentivity/Recall:",recall
    print "Specificity:",float(true_neg)/(true_neg+false_pos)
    precision = float(true_pos)/(true_pos+false_pos)
    print "Precision:", precision
    print "F-score " , 2*precision*recall/(precision+recall)
    print "F-0.5 score ", 1.25*precision*recall/(0.25*precision+recall)
    print "F2 sore ", 5*precision*recall/(4*precision+recall)
    print "\n"


class InputReader:
    '''This class reads the input given in the requested libSVM format(categorical)
        and builds the data dictionary'''
    def __init__(self):
        pass;

    def read_input(self,filename):
        '''This function reads a file specified in a libSVM format
        and returns a list of dict of attr-val pairs for X and a label vector for Y'''
        Y = [];
        X = [];
        count = 0;
        with open(filename, 'r') as fhandle:
            for line in fhandle:
                line = line.strip().split();
                count +=1;
                # do not want to process empty lines
                if not line : continue;
                # build the dict and extract the label
                x = {}
                for t in line[1:]:
                    [attr_idx,attr_val] = t.split(':');
                    #attr_idx = int(attr_idx);
                    #attr_val = int(attr_val);
                    x[attr_idx] = attr_val;
                label = line[0];
                X += [x];
                Y += [label];

        return X,Y;

    def read_csv(self,filename):
        X= []
        Y = []  
        with open(filename,'r') as csvfile:
            reader = csv.DictReader(csvfile);
            for row in reader:
                x ={}
                for k in row.keys():
                    if k=='IsBadBuy':
                        label = '+1' if row[k]=='1' else '-1';
                    else:
                        x[k] =  row[k]
                X+=[x];
                Y += [label];

        return X,Y




                
        

