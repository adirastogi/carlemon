#This is the implementation of the Naive Bayes classifier with laplace and gaussian smoothing
from random import shuffle;
import math


class NBclassifier:

    def __init__(self):
        self.p_y = {}                   #this stores the class labels and their counts
        self.p_X_y = {}                 #this stores the mapping of attr_id -> {attr_val,yval} combinations
        self.count_distinct_x_y = {};   #this storess the mapping of distinct counts of each attr_id,class_label pair
        self.num_train_examples=0;      #this stores the number of training examples.
        pass


    def train(self,X,Y,numeric_attrs):
        #reset the model everytime you train
        assert(len(X)==len(Y))
        self.num_train_examples = len(Y);
        self.p_X_y.clear()
        self.p_y.clear()

        #count the frequencies of the class labels
        for y in Y:
            if y not in self.p_y: self.p_y[y] = 1
            else:                 self.p_y[y] += 1

        #build the dict of all the X|Y freq combinations.
        for i in xrange(self.num_train_examples):
            x = X[i];
            y = Y[i];
            for attr_idx in x.keys():
                #Handle numeric attribute
                if attr_idx in numeric_attrs:
                    if attr_idx not in self.p_X_y: self.p_X_y[attr_idx] = {};
                    p_x_y = self.p_X_y[attr_idx];
                    if y in p_x_y:  p_x_y[y] += [float(x[attr_idx])];
                    else:           p_x_y[y] =  [float(x[attr_idx])];
                else: 
                    #Handle nominal attribute
                    if attr_idx not in self.p_X_y: self.p_X_y[attr_idx]={};
                    p_x_y = self.p_X_y[attr_idx];
                    if (x[attr_idx],y) in p_x_y: p_x_y[(x[attr_idx],y)] += 1;
                    else                       : p_x_y[(x[attr_idx],y)] = 1;

        #count the number of distinct values of each attribute x conditioned on each y(required for smooting of nominal attrs)
        # for numeric attribute ,calculate their mean and variance for use in gaussian dist
        for attr_idx,p_x_y in self.p_X_y.items():
            #Handle numeric attribute
            if attr_idx in numeric_attrs:
                    p_x_y = self.p_X_y[attr_idx];
                    mean = 0;
                    stdev = 0;
                    for y in self.p_y.keys():
                        #print attr_idx, y
                        sumval =sum( p_x_y[y])
                        numvals = len(p_x_y[y]);
                        mean = float(sumval)/numvals;
                        var = sum([(v-mean)*(v-mean) for v in p_x_y[y]])
                        var = float(var)/numvals
                        # dont need the other values anymore
                        #print mean,var
                        p_x_y[y] = (mean,var);
            # Handle nominal attribute
            else:
                for y in self.p_y.keys():
                    # count the number of times this attribute occurs as None as well for this class and update that
                    # information as well
                    count_attr_null_for_class = self.p_y[y]-sum([count for (attr_val,yval),count in p_x_y.items() if yval==y]);
                    assert(count_attr_null_for_class>=0);
                    p_x_y[(None,y)]=count_attr_null_for_class;
                    count_distinct = len(set([attr_val for attr_val,yval in p_x_y.keys() if yval==y]));
                    self.count_distinct_x_y[(attr_idx,y)] = count_distinct;

        return;

    def predict(self,X,numeric_attrs):
        #stores the predicted labels
        Y_pred = [];
        #list of training attrs
        train_attrs = self.p_X_y.keys();
        #predict for each test example
        for x in X:
            max_prob=0;
            #the class label 0 will never be observed and signifies fail
            pred_label = '0';
            test_attrs = x.keys();
            # take the union of the attribute list in training and test
            attr_list = set(test_attrs) | set(train_attrs);
            #print "predicting example ",x,"\n";
            # test each class label to see if it gives max_prob
            for y in self.p_y.keys():
                count_y = self.p_y[y];
                prob = float(count_y)/(self.num_train_examples)
                #print"P(",y,")=",prob
                for attr_idx in attr_list:
                    #attribute seen in training data
                    if attr_idx in self.p_X_y:
                        if attr_idx in x : attr_val = x[attr_idx];
                        else             : attr_val = None;
                        p_x_y = self.p_X_y[attr_idx];
                        #If the attribute is numeric
                        if attr_idx in numeric_attrs:
                            mean,var = p_x_y[y];
                            exp_term = math.pow(float(float(x[attr_idx])-mean),2)/var
                            attr_prob = (1/math.sqrt(2*math.pi*var))*(math.exp(-0.5*exp_term))
                            #If the attribute is nominal
                        else:
                            if (attr_val,y) in p_x_y:
                                attr_prob = float(p_x_y[(attr_val,y)]+1)/(count_y+self.count_distinct_x_y[attr_idx,y]);
                                #debug
                                #print "P(%s=%s|%s)=%.3f"%(attr_idx,attr_val,y,attr_prob);
                            else:
                                attr_prob = float(1)/(count_y+self.count_distinct_x_y[(attr_idx,y)]+1);
                                #debug
                                #print "P(%s=*%s|%s)=%.3f"%(attr_idx,attr_val,y,attr_prob);
                    #attribute not seen in training data
                    else:
                        #If the attribute is numeric
                        if attr_idx in numeric_attrs:
                            attr_prob = 1; #ignore the attribute
                            #If the attribute is nominal
                        else:
                            attr_prob = float(1)/(count_y+2);
                            #debug
                            attr_val = x[attr_idx];
                            #print "P(*%s=%s|%s)=%.3f"%(attr_idx,attr_val,y,attr_prob);
                            #debug
                    prob = prob*attr_prob;
                #debug
                #print ;

                if prob > max_prob:
                    max_prob = prob;
                    pred_label = y;

            # set the class label as the maximum observed over all the labels.
            Y_pred += [pred_label];
            #debug
            #print "predicted label ",pred_label," with probability ",max_prob
            #print "---------------"
        #return the vector of predictions
        assert(len(X)==len(Y_pred));
        return Y_pred;


    def cross_validate(self,X,Y,nfolds=5):
        assert(len(X)==len(Y));
        #randomize the data first
        data = zip(X[:],Y);
        shuffle(data);
        [X_rand,Y_rand] = zip(*data);
        fold_size = len(X)/nfolds;
        acc = 0;
        for k in xrange(nfolds):
            test_X = X_rand[fold_size*k:fold_size*(k+1)];
            test_Y = Y_rand[fold_size*k:fold_size*(k+1)];
            train_X = X_rand[:fold_size*k] + X_rand[fold_size*(k+1):];
            train_Y = Y_rand[:fold_size*k] + Y_rand[fold_size*(k+1):];
            self.train(train_X,train_Y);
            predictions = self.predict(test_X);
            assert(len(predictions)==len(test_Y));
            acc += float(sum([1 for (py,y) in zip(predictions,test_Y) if py==y ]))/fold_size;
        acc /= nfolds;
        print "Average accuracy on %d folds : %.4f"%(nfolds,acc);


    def dump(self):
        print "Total examples trained on: ",self.num_train_examples;
        for y,count in self.p_y.items():
            print "#%s:%d"%(y,count);
        for attr_idx in self.p_X_y.keys():
            print "Attribute ",attr_idx;
            for (attr_val,label),count in self.p_X_y[attr_idx].items():
                print "\t%s:%s:%s=%d"%(attr_idx,attr_val,label,count);


























