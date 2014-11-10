#!/usr/bin/env python
from sklearn.feature_extraction import DictVectorizer;
from sklearn.decomposition import PCA;
from sklearn.linear_model import LogisticRegression;
import numpy as np;
def extract_class_labels(data_list):
    '''Takes in data as a list of attribute-name:value tuples
    and extracts the class label and writes it to a file'''
    class_labels_vector = []
    for row in data_list:
        if 'IsBadBuy' in row:
            class_labels += [int(row['IsBadBuy'])];
            del row['IsBadBuy'];
    return class_labels_vector;

def vectorize_data(data_list):
    '''Takes in the data as a list of attribute-name:value tuples
    and converts it into vectorized form for processing by scikit
    prints the feature mapping in filename.'''
    
    vec=DictVectorizer();
    vector_data = vec.fit_transform(data_list).toarray();
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
            print >> file, vector.inverse_transform(row),"\n";

    return vector_data;

def pca_on_vectorized(vector_data,num_comp):
    '''This function will run PCA on the vectorized data'''
    pca = PCA(n_components=num_comp,class_wight='auto');
    trans_data = pca.fit_transform(vector_data);
    return trans_data;

def run_logistic_regression(vector_train_data,vector_test_data,train_class_labelstest_class_labels):
    '''This function will run logistic regression on the data in the vector_data
    variable and using the class_label vector'''
    assert(len(vector_train_data)==len(train_class_labels));
    assert(len(vector_test_data)==len(test_class_labels));
    logr = LogisticRegression(penalty='l2');
    logr.fit(vector_train_data,train_class_labels);
    predicted_labels = logr.predict(vector_test_data);
    acc = logr.score(vector_test_data,test_class_labels);
    return acc,predicted_labels;
    

