#!/usr/bin/python
import math
import sys
MAX_DEPTH

'''Assuming that we have a list of training examples, where each example is a dict indexed by feature name.
	We also have "values_features" which is a list of all the distinct values that a feature can take (this information is there for every feature).'''
training_data = []
testing_data = []
label = "IsBadBuy"


def calc_total_entropy(data):
	global label
	count_lab_1 = 0
	total = len(data)
	for example in data:
		if example[label] == 1:
			count_lab_1 += 1
	prob_lab_1 = float(count_lab_1)/float(total)
	term_lab_1 = float(prob_lab_1) * float(math.log(float(prob_lab_1),2))
	term_lab_0 = float(1 - prob_lab_1) * float(math.log(float(1 - prob_lab_1),2))
	entropy = -1 * (float(term_lab_0) + float(term_lab_1))
	if prob_lab_1 >= 0.5:
		lab = "label1"
		conf = prob_lab_1
	else:
		lab = "label0"
		conf = prob_lab_0
	return entropy,lab,conf


def calc_gain_feature(total,training_data,feature_name,total_entropy_data):
	values_dict = {}																								#Key = feature name value -> value = [num ex for label 0,num ex for label 1,[ list of examples]]
	for example in training_data:
		attr_val = example[feature_name]
		if attr_val in values_dict:
			if example[label] == 1:
				values_dict[attr_val][0] += 1
			else:
				values_dict[attr_val][1] += 1
			values_dict[attr_val][2].append(example)
	
	entropy_attribute = 0.0
	for value in values_dict:
		value_prob_1 = float(values_dict[value][0]) /float(values_dict[value][0] + values_dict[value][1])
		value_prob_0 = float(values_dict[value][1]) /float(values_dict[value][0] + values_dict[value][1])
		entropy_attribute_val = (-1) * (value_prob_1 * math.log(value_prob_1,2) + value_prob_0 * math.log(value_prob_0,2))
		entropy_attribute += entropy_attribute_val *sum(values_dict[value][:2])/float(total)

	gain = 	float(total_entropy_data) - float(entropy_attribute)
	return gain,values_dict


def run_dt(training_data,features,depth):

	total_entropy_data,lab,conf = calc_total_entropy(training_data)

	global MAX_DEPTH
	if depth >= MAX_DEPTH:
		print " "*depth,"MAX_DEPTH","<",lab,conf,">"
		#calculate the majority label and return that
		return [lab,conf]

	# achieved complete classification
	global break_thresh
	if total_entropy_data <= break_thresh:
		print " "*depth,"CONF_CLASS","<",lab,conf,">"
		return [lab,conf]

	# if no more features to split then return the majoity label at this node	
	if not features:
		print " "*depth,"<",lab,conf,">"
		return [lab,conf]

	# otherwise continue growing the tree
	max_gain = (-1)*sys.maxint
	split_feature  = None
	split_feature_values = None
	num_examples = len(training_data)

	for feature in features:
		gain,values_dict = calc_gain_feature(num_examples,training_data,feature,total_entropy_data)
		if gain > max_gain:
			max_gain = gain
			split_feature = feature
			split_feature_values = values_dict

	#Split the current data on the different values of split_feature
	print " "*depth,"<GROW:",split_feature,">"
	node = [split_feature,{}]
	new_features = list(features)
	new_features.remove(split_feature)

	for value in split_feature_values:
		sub_tree_root = run_dt(split_feature_values[value][2],new_features,depth + 1)
		node[1][value] = sub_tree_root

	return node


def traverse(dt,test_case):
	attr_name = dt[0]
	attr_val = test_case[attr_name]
	if attr_val not in dt[1]:
		return None;
	else:
		next_node = dt[1][attr_val]
		if next_node[0]=="label1" || next_node[0]=="label0":
			return next_node[0],next_node[1]	
	  else:
			traverse(next_node,test_case);


def get_predictions(testing_data,dt):
	preds = []
	for test_case in testing_data:
		prediction = traverse(dt,test_case)
		preds.append(prediction)


if __name__ == "__main__":
	features = values_features.keys()
	dt = run_dt(training_data,features,0)
	predictions = get_predictions(testing_data,dt)
				
