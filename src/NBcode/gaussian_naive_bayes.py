#!/usr/bin/env python
# Naive Bayes classifier running code, makes the following assumptions:
# missing values in mueric attributes have been filled in !
# preferably no surprises in the attrtibute data.
import naive_bayes
import read_data
import naive_bayes
import sys
if __name__=='__main__':

    numeric_attr_names = sys.argv[3].strip().split(",")
    reader = read_data.InputReader()
    X_train,Y_train  = reader.read_csv(sys.argv[1]);
    X_test,Y_test = reader.read_csv(sys.argv[2]);
    classifier = naive_bayes.NBclassifier();
    classifier.train(X_train,Y_train,numeric_attr_names);
    pred_train = classifier.predict(X_train,numeric_attr_names);
    pred_test = classifier.predict(X_test,numeric_attr_names);
    #calculate predictions on training data
    print "Status on training data"
    read_data.print_metrics(pred_train,Y_train);
    print "Status on testing data"
    read_data.print_metrics(pred_test,Y_test);
    

    
