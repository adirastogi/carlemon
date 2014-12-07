#!/usr/bin/env python
from sklearn.feature_extraction import DictVectorizer;
from sklearn.decomposition import PCA;
from sklearn.linear_model import LogisticRegression;
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier
import numpy as np;
import sys
def extract_class_labels(data_list):
    '''Takes in data as a list of attribute-name:value tuples
    and extracts the class label and writes it to a file'''
    class_labels_vector = []
    for row in data_list:
        if 'IsBadBuy' in row:
            class_labels_vector += [int(row['IsBadBuy'])];
            del row['IsBadBuy'];
    return class_labels_vector;


def get_decision_tree_classifier(train_data,train_labels):
    dt = DecisionTreeClassifier()
    dt_result = dt.fit(train_data,train_labels)
    return dt_result

def get_labels_decision_tree_classifier(dt_result,test_data):
    predicted_labels = dt_result.predict(test_data)
    return predicted_labels
    

def vectorize_data(data_list,vec_data_fd):
    '''Takes in the data as a list of attribute-name:value tuples
    and converts it into vectorized form for processing by scikit
    prints the feature mapping in filename.'''
    vec=DictVectorizer();
    vec.fit(data_list)
    print len(vec.get_feature_names())
    vector_data = vec.transform(data_list).toarray()

    one_hot_names = vec.get_feature_names();
    #print the feature mappings
    feature_indices = range(0,len(one_hot_names));
    one_hot_mapping = zip(one_hot_names,feature_indices);
    with open('one_hot_encoding.txt','w') as file:
        for (idx,one_hot_name) in one_hot_mapping:
            print >> file, "%s-->%d\n"%(idx,one_hot_name);
		
    # print the one-hot encoding  for each tuple.
    with open('vector_mappings.txt','w') as file:
        for row in vector_data:
            print >> file, vec.inverse_transform(row),"\n";
    sys.exit(1)
    for row in vector_data:
        row = [str(x) for x in row]
        row = ",".join(row)
        vec_data_fd.write(row)
        vec_data_fd.write("\n\n")
    return vector_data;

def pca_on_vectorized(vector_data,num_comp):
    '''This function will run PCA on the vectorized data'''
    pca = PCA(n_components=num_comp);
    trans_data = pca.fit_transform(vector_data);
    print "\n\n\nThe number of components is:\t",pca.n_components,"\n"
    print "The percentage explained variance is:\t",pca.explained_variance_ratio_,"\n"
    return trans_data;

def run_logistic_regression(vector_train_data,vector_test_data,train_class_labels):
    '''This function will run logistic regression on the data in the vector_data
    variable and using the class_label vector'''
    assert(len(vector_train_data)==len(train_class_labels));
    logr = LogisticRegression(penalty='l2',class_weight='auto');
    logr.fit(vector_train_data,train_class_labels);
    predicted_labels = logr.predict(vector_test_data);
    return predicted_labels;
