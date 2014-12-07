#!/usr/bin/python
'''
	This program is used to implement the Naive Bayes Algorithm for classification.
	To run the program, type the following command:
	
	python NaiveBayes.py <training_file> <test_file> 
'''
import sys
import csv
import math
label = "IsBadBuy"
num_attr_list=["WarrantyCost","MMRAcquisitionAuctionCleanPrice","MMRCurrentRetailAveragePrice","MMRAcquisitionRetailAveragePrice","VehOdo","VehicleAge","MMRCurrentRetailCleanPrice","MMRAcquisitionAuctionAveragePrice","MMRAcquisitonRetailCleanPrice","MMRCurrentAuctionAveragePrice","VehBCost","MMRCurrentAuctionCleanPrice","VehOdo_by_VehAge","r2_minus_r1_avg","r2_minus_r1_clean","r2_minus_a1_avg","r2_minus_a1_clean","r2_avg_minus_vehbc","r2_clean_minus_vehbc","vehbc_minus_a1_avg","vehbc_minus_a1_clean","warranty_by_vehbc"]


'''This function mentions the correct usage for running the program.
'''
def usage(program_name):
	return "Wrong Usage!\nCorrect Usage is:\t<python "+ program_name + "> <train_file> <test_file> <prediction_file>"


'''This function is used to find all the distinct values that each nominal attribute can take.
	 This is stored in a dictionary with keys as the attribute names and the value for a 
	 key as a list of distinct values that the attribute can take.
'''
def find_distinct_values_feature(training_data,testing_data,all_features):
	values_in_features = {}
	total_data = training_data + testing_data
	for feature in all_features:
		distinct_values = set()
		for example in total_data:
			distinct_values.add(example[feature])
		values_in_features[feature] = distinct_values
	return values_in_features
		

'''This function is used to calculate the prior probabilities of the class labels.
'''
def find_prior_probability(label_value,training_data):
	global label
	count = 0
	for example in training_data:
		if example[label] == label_value:
			count += 1
	return float(count)/float(len(training_data))

	
'''This function is basically the model that is learned in the Naive Bayes Classifier.
	 It stores the conditional probability values of each attribute_name -> value -> label
	 combination. These values are stored in a dictionary and looked up using a 
	 string lookup.
'''
def store_all_feature_value_label_cond_probabilities(training_data,values_in_features):
	global label
	value_cond_prob = {}
	labels = ['0','1']
	for feature in values_in_features:
		distinct_values = values_in_features[feature]
		total_values_feature = len(distinct_values)
		for value in distinct_values:
			for label_val in labels:
				string_lookup = str(feature) + ':' + str(value) + ':' + label_val
				counter = 0
				total_counter = 0
				for example in training_data:
					if example[label] == label_val:
						total_counter += 1
						if example[feature] == value:
							counter += 1
				if counter == 0:
					counter = 1																													#Laplacian Correction.
					total_counter += total_values_feature
				probability =  float(counter)/float(total_counter)
				value_cond_prob[string_lookup] = probability
	return value_cond_prob


def store_mean_std_dev_numeric_attributes(training_data,numeric_features,value_cond_prob):
	positive_examples = []
	negative_examples = []
	for example in training_data:
		if example[label] == "1":
			positive_examples.append(example)
		else:
			negative_examples.append(example)
	value_cond_prob = get_mean_std_dev_labelled_examples(positive_examples,numeric_features,value_cond_prob,"1")
	value_cond_prob = get_mean_std_dev_labelled_examples(negative_examples,numeric_features,value_cond_prob,"0")
	return value_cond_prob


def get_mean_std_dev_labelled_examples(labelled_data,numeric_features,value_cond_prob,lab_val):	
	total = len(labelled_data)
	for feature in numeric_features:
		summation = 0.0
		mean = 0.0
		std_dev = 0.0
		all_vals = []
		for example in labelled_data:
			summation = float(summation) + float(example[feature])
			all_vals.append(float(example[feature]))
		mean = float(summation)/float(total)
		summation = 0.0
		for value in all_vals:
			dev = float(value) - float(mean)	
			numerator = float(dev)**2
			summation = float(summation) + float(numerator)
		std_dev = float(summation)/float(total)
		std_dev = float(std_dev)**(0.5)
		value_cond_prob[feature + "_" + lab_val] = [mean,std_dev]
	return value_cond_prob


'''This function is used for training the Naive Bayes classifier and returning the corresponding 
	 conditional probability values which is the model that is learned.
'''
def train_naive_bayes_get_classifier(training_data,values_in_features,numeric_features):
	prior_positive = find_prior_probability("1",training_data)
	prior_negative = find_prior_probability("0",training_data)
	#print "Done finding prior probabilities for class labels."
	value_cond_prob = store_all_feature_value_label_cond_probabilities(training_data,values_in_features)
	value_cond_prob = store_mean_std_dev_numeric_attributes(training_data,numeric_features,value_cond_prob)
	value_cond_prob['prior_positive'] = prior_positive
	value_cond_prob['prior_negative'] = prior_negative
	#print "Done storing conditional probabilities for attribute values."
	return value_cond_prob																											#Return the model for the Naive Bayes classifier.


def calc_gaussian_prob(value,mean,std_dev):
	diff = float(value) - float(mean)
	diff_sq = float(diff)**2
	variance = float(std_dev)**2
	diff_sq = (-1) * float(diff_sq)/float(2.0*variance)
	exp_term = float(math.exp(diff_sq))
	
	denom = float(2.0 * math.pi  * variance)
	denom = float(denom**(0.5))

	return float(exp_term)/float(denom)


'''This function is used to return the predictions of the classifier on testing data.
'''
def get_predictions_from_model(value_cond_prob,testing_data,nominal_features,numeric_features):
	predictions = []
	for example in testing_data:
		predicted_label = "0"
		features_prob_product_positive = 1.0
		features_prob_product_negative = 1.0
		for feature in nominal_features:
			string_lookup = str(feature) + ':' + str(example[feature]) + ':1'
			features_prob_product_positive = float(features_prob_product_positive) * float(value_cond_prob[string_lookup])

			string_lookup = str(feature) + ':' + str(example[feature]) + ':0'
			features_prob_product_negative = float(features_prob_product_negative) * float(value_cond_prob[string_lookup])

		for num_feature in numeric_features:
			string_lookup = str(num_feature) + "_" + "1"
			mean,std_dev = value_cond_prob[string_lookup]
			features_prob_product_positive = float(features_prob_product_positive) * float(calc_gaussian_prob(example[num_feature],mean,std_dev))
		
			string_lookup = str(num_feature) + "_" + "0"
			mean,std_dev = value_cond_prob[string_lookup]
			features_prob_product_negative = float(features_prob_product_negative) * float(calc_gaussian_prob(example[num_feature],mean,std_dev))
			
		if (float(features_prob_product_positive * value_cond_prob['prior_positive']) >= float(features_prob_product_negative * value_cond_prob['prior_negative'])):
			predicted_label = "1"
		predictions.append(predicted_label)
	return predictions


'''This function is used to evaluate the accuracy/quality of the classifier on the test data
	 and for printing the metrics like the true positives, negatives, etc.
'''
def print_metrics(testing_data,predictions):
	global label
	true_positives = 0
	false_negatives = 0
	false_positives = 0
	true_negatives = 0
	num_examples = len(testing_data)
	for example_num in range(0,num_examples):
		predicted_label = predictions[example_num]
		if testing_data[example_num][label] == "1":
			if predicted_label == "1":
				true_positives += 1
			elif predicted_label == "0":
				false_negatives += 1
		elif testing_data[example_num][label] == "0":
			if predicted_label == "1":
				false_positives += 1
			elif predicted_label == "0":
				true_negatives += 1
	print true_positives,"\t",false_negatives,"\t",false_positives,"\t",true_negatives


def read_csv(fhandle):
	data = []
	reader = csv.DictReader(fhandle)
	data = [row for row in reader]
	return data

def csv_process(train_file,test_file):
	global label
	global num_attr_list
	training_data = read_csv(train_file)
	testing_data = read_csv(test_file)
	all_features = training_data[0].keys()
	all_features.remove(label)
	max_index = len(all_features)
	numeric_features = num_attr_list
	for feature in numeric_features:
		all_features.remove(feature)
	values_in_features = find_distinct_values_feature(training_data,testing_data,all_features)
	return training_data,testing_data,values_in_features,max_index,numeric_features
	

if __name__ == "__main__":
	if(len(sys.argv)) != 4:
		print usage("GaussianNaiveBayes.py")
		sys.exit(1)
	else:
		train_file_name = sys.argv[1]
		test_file_name = sys.argv[2]
		pred_file_name = sys.argv[3]
		train_file = open(train_file_name,"r")
		test_file = open(test_file_name,"r")
		training_data,testing_data,values_in_features,max_index,numeric_features = csv_process(train_file,test_file)
		train_file.close()
		test_file.close()

		value_cond_prob = train_naive_bayes_get_classifier(training_data,values_in_features,numeric_features)
		nominal_features = values_in_features.keys()
		predictions = get_predictions_from_model(value_cond_prob,training_data,nominal_features,numeric_features)
		print_metrics(training_data,predictions)
		predictions = get_predictions_from_model(value_cond_prob,testing_data,nominal_features,numeric_features)
		pred_file = open(pred_file_name,"w")
		for pred in predictions:
			pred_file.write(str(pred) + "\n")
		pred_file.close()
