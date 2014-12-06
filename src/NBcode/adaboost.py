#This is the implementation of AdaBoost
from random import random;
from math import log
import sys

class AdaBoost:
    '''This contains the sampling version of AdaBoost suitable for use with the
    Naive Bayes classifier'''
    def __init__(self):
        self.num_iters =15  #no of iterattions to run it for
        self.data_X=[]  # the X training data for the boosted classifier
        self.data_Y=[]  # the training labels for the boosted classifier.
        self.classifiers=[]
        self.classifier_type = None; #the instance of the classifier to run

        self.weights = [] #representing the training distribution
        self.alpha_weights=[] # the calculated alpha weights in each iteration
        self.num_training_examples=0;


    def sample_data(self,sample_size):
        '''This function returns samples of size IID with replacement from the test data
         according to the weight distribution maintained for the data '''
        #always assert that the distribution sums to 1.
        samples_idx = [];
        for i in xrange(sample_size):
            rand_w = random();
            sum = 0;
            for j in xrange(self.num_training_examples):
                sum += self.weights[j];
                if sum>rand_w:
                    samples_idx += [j];
                    break;

        return samples_idx;

    def train(self,X,Y,class_type):

        self.data_X=X;
        self.data_Y=Y;
        self.classifier_type = class_type;
        self.classifiers =[];
        self.weights = [];
        self.alpha_weights = [];
        self.num_training_examples = len(X);

        #intialize
        for i in xrange(self.num_training_examples):
            self.weights.append(float(1)/self.num_training_examples);

        for i in xrange(self.num_iters):
            #print "-------- iteration ",i,"-------------"

            #train and predict 
            samples_idx = self.sample_data(self.num_training_examples);
            train_X = [self.data_X[idx] for idx in samples_idx];
            train_Y = [self.data_Y[idx] for idx in samples_idx];

            classifier = self.classifier_type();
            classifier.train(train_X,train_Y);
            train_preds = classifier.predict(self.data_X);

            #calculate the errors
            raw_error = 0;
            error = 0;
            for l in xrange(len(self.data_X)):
                if train_preds[l] != self.data_Y[l]:
                    error += self.weights[l];
                    raw_error += 1;

            alpha  = log((1-error)/error);
            raw_error = float(raw_error)/self.num_training_examples;
            #print >>sys.stderr,"The weighted errror is :",error;
            #assert(error<0.5);
            if(error>0.5): alpha = -alpha
            self.alpha_weights += [alpha];
            self.classifiers += [classifier];
            #print "alpha:",alpha
            #classifier.dump();
            #z = 2*sqrt(error(1-error));

            #recalcuate the weights
            #if the sample is correctly predicted, demote the weight
            for l in xrange(len(self.data_X)):
                if train_preds[l] == self.data_Y[l]:
                    self.weights[l] = float(self.weights[l]*error)/(1-error);

            #and now normalize across all samples
            norm = sum(self.weights);
            self.weights = [float(w)/norm for w in self.weights];

            #print the updated weights
            #print >>sys.stderr,self.weights
            #print "--------------------------------------"


    def predict(self,X):
        '''This returns the prediction as a weighted prediction of the predictions of the
        other classifiers'''
        pred_Y = [];
        count = 0;
        for x in X:
            count +=1
            #print "predicting example ",count
            sum = 0;
            for i in xrange(self.num_iters):
                [p] = self.classifiers[i].predict([x]);
                p = 1 if p=='+1' else -1;
                sum += self.alpha_weights[i]*p;
            pred = '+1' if sum>=0 else '-1';
            pred_Y += [pred];

        return pred_Y;


