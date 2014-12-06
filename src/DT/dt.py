#!/usr/bin/python
import math
import sys
import csv
MAX_DEPTH = 3
BREAK_THRES = 0.95
#0.468 corresponds to 90% confidence.

class DTclassifier:
    def  __init__(self):
        self.tree_root = None
    
    # calls the DT predictor after converting from the labels to the ones
    # required by DT, the predictions so calculated are going to be passed to read_data API write_predictions that converts them to output labels. It uses the following mapping 
    #+1--->IsbadBuy=1
    #-1-->IsBadBuy=0
    #The dt returns the prediction
    #1-->isBadBuy=1
    #0-->isBadBuy=0
    # so 1 (dt) --> +1(pred) and 0(dt)---> -1(pred)
    def predict(self,X_test):
        if self.tree_root:
            predictions,conf=get_predictions(X_test,self.tree_root)
            prediction = ["+1" if p==1 else "-1"  for p in predictions]
            return prediction;

    def train(self,X_train,Y_train):
        print "Inside DT training"
        features = X_train[0].keys()
        features.remove(label)
        self.tree_root=run_dt(X_train,features,0)


'''Assuming that we have a list of training examples, where each example is a dict indexed by feature name.
	We also have "values_features" which is a list of all the distinct values that a feature can take (this information is there for every feature).'''
training_data = []
testing_data = []
label = "IsBadBuy"
'''
label0 -> IsBadBuy == 0
label1 -> IsBadBuy == 1
'''

def calc_total_entropy(data):
	global label
	count_lab_1 = 0
	total = len(data)
	for example in data:
		if example[label] == "1":
			count_lab_1 += 1
	prob_lab_1 = float(count_lab_1)/float(total)
	if prob_lab_1 == 0.0:
		lab = "label0"
		conf = 1
		return 0,lab,conf
	elif prob_lab_1 == 1.0:
		lab = "label1"
		conf = 1
		return 0,lab,conf
	term_lab_1 = float(prob_lab_1) * float(math.log(float(prob_lab_1),2))
	term_lab_0 = float(1 - prob_lab_1) * float(math.log(float(1 - prob_lab_1),2))
	entropy = -1 * (float(term_lab_0) + float(term_lab_1))
	if prob_lab_1 >= 0.5:
		lab = "label1"
		conf = prob_lab_1
	else:
		lab = "label0"
		conf = 1 - prob_lab_1
	return entropy,lab,conf


def calc_gain_feature(total,training_data,feature_name,total_entropy_data):
	values_dict = {}																								#Key = feature name value -> value = [num ex for label 1,num ex for label 0,[ list of examples]]
	values_values = []
	for example in training_data:
		attr_val = example[feature_name]
		if attr_val in values_dict:
			values_values = values_dict[attr_val]
		else:
			values_dict[attr_val] = [0,0,[]]
			values_values = values_dict[attr_val]

		if example[label] == "1":
			values_values[0] += 1
		else:
			values_values[1] += 1
		values_values[2].append(example)
	
	entropy_attribute = 0.0
	for value in values_dict:
		value_prob_1 = float(values_dict[value][0]) /float(values_dict[value][0] + values_dict[value][1])
		value_prob_0 = float(values_dict[value][1]) /float(values_dict[value][0] + values_dict[value][1])
		if value_prob_0 == 0.0 or value_prob_0 == 1.0:
			continue
		entropy_attribute_val = (-1) * (value_prob_1 * math.log(value_prob_1,2) + value_prob_0 * math.log(value_prob_0,2))
		entropy_attribute += entropy_attribute_val *sum(values_dict[value][:2])/float(total)

	gain = 	float(total_entropy_data) - float(entropy_attribute)
	return gain,values_dict


def run_dt(training_data,features,depth):
	total_entropy_data,lab,conf = calc_total_entropy(training_data)
	#print "\n","\t\t" *depth,"total entropy of data:\t",total_entropy_data,"\tlabel\t",lab,"\tconf\t",conf

	global MAX_DEPTH
	if depth >= MAX_DEPTH:
		print "\t\t"*depth,"MAX_DEPTH","<",lab,conf,">"
		#calculate the majority label and return that
		return [lab,conf]
	
	# achieved complete classification
	global BREAK_THRESH
	if conf >= BREAK_THRES:
		print "\t\t"*depth,"CONF_CLASS","<",lab,conf,">"
		return [lab,conf]
	
	# if no more features to split then return the majority label at this node	
	if not features:
		print "\t\t"*depth,"<",lab,conf,">"
		return [lab,conf]

	# otherwise continue growing the tree
	max_gain = (-1)*sys.maxint
	split_feature  = None
	split_feature_values = None
	num_examples = len(training_data)

	for feature in features:
		gain,values_dict = calc_gain_feature(num_examples,training_data,feature,total_entropy_data)
		#print "\t\t"*depth, "gain of feature\t",feature,"\tgain=\t",gain
		if gain > max_gain:
			max_gain = gain
			split_feature = feature
			split_feature_values = values_dict
	
	#Split the current data on the different values of split_feature
	print "\t\t"*depth,"<GROW:",split_feature,">"
	node = [split_feature,{},lab,conf]
	new_features = list(features)
	new_features.remove(split_feature)
	
	for value in split_feature_values:
		#print ""
		print "\t\t"*depth, "<Split_Feature:\t",split_feature,":",value
		sub_tree_root = run_dt(split_feature_values[value][2],new_features,depth + 1)						#Run DT code on the conditioned training examples
		node[1][value] = sub_tree_root

	return node
'''
final node returned will be:
	node[feature_name, {value1:<node>},majority_label,confidence]
At the leaves:
	node[feature_name, {value: [label,confidence]},majority_label,confidence]
'''

def traverse(dt,test_case):
	attr_name = dt[0]
	attr_val = test_case[attr_name]
	#print >> sys.stderr, attr_name,"\t",attr_val
	if attr_val not in dt[1]:																																	#Return majority label of conditioned data.
		#print >> sys.stderr, "Not FOUND"
		return dt[2],dt[3];
	else:
		#print >> sys.stderr,"Matched against\t",dt[1][attr_val][0]
		next_node = dt[1][attr_val]
		if next_node[0]=="label1" or next_node[0]=="label0":
			return next_node[0],next_node[1]	
		else:
			return traverse(next_node,test_case);


def get_predictions(testing_data,dt):
	preds = []
	confs = []
	for test_case in testing_data:
		prediction,conf = traverse(dt,test_case)
		#print >> sys.stderr, prediction
		#print >> sys.stderr,"--------------------"
		if prediction == "label1":
			p = 1
		else:
			p = 0
		preds.append(p)
		confs.append(conf)
	return preds,confs

def read_csv(file_name):
	training_data = []
	with open(file_name,"r") as fhandle:
		reader = csv.DictReader(fhandle)
		training_data = [row for row in reader]
	return training_data


def usage():
	return "<python\tdt.py\t<training_data_file>\t<testing_data_file>\t<prediction_file>"


def check_predictions(predictions,test_data):	
	num_examples = len(test_data)
	accuracy = 0.0
	for i in range(0,num_examples):
		if (predictions[i] == int(test_data[i][label])):
			accuracy += 1
	return float(accuracy)/float(num_examples)

if __name__ == "__main__":
	if len(sys.argv) != 4:
		print usage()
		sys.exit(1)
	training_data = read_csv(sys.argv[1])
	features = training_data[0].keys()
	features.remove(label)
	dt = run_dt(training_data,features,0)
	testing_data = read_csv(sys.argv[2])
	predictions,confs = get_predictions(testing_data,dt)
	pred_output_file = open(sys.argv[3],"w")
	for p,c in zip(predictions,confs):
		pred_output_file.write(str(p)+"\t"+str(c)+"\n")
	pred_output_file.close()
	#accuracy = check_predictions(predictions,training_data)
	#print "Accuracy is:\t",accuracy
				
