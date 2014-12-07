#!/usr/bin/python
#
#
# This program is used for feature engineering and data preprocessing.
import sys
from pca_logistic_regression import *

data_dir = "../data/input_files/"
#total_data_file = data_dir + "sample_total_data.csv"
#total_data_file = data_dir + "model_submodel_removed_total_data.csv"
total_data_file = "../data/training.csv"
#class_label_file = data_dir + "sample_class_labels.txt"
class_label_file = data_dir + "class_labels.txt"
result_file = "result.txt"
preprocessed_training_set_file = data_dir + "preprocessed_training.csv"
vectorized_training_data = "vectorized_data.txt"
delimiter  = ','

def store_examples(example_file):
	lines = example_file.readlines()	
	features = lines[0].strip().split(delimiter)	
	example_set = []
	for example in lines[1:]:
		example_feature_values = example.strip().split(delimiter)
		record_in_example = {}
		i = 0
		for feature in features:
			record_in_example[feature] = example_feature_values[i]
			i += 1
		example_set.append(record_in_example)
	return features,example_set


def fill_missing_values(mode_nominal_attributes,mean_numeric_attributes,example_set):
	new_example_set = []
	for example in example_set:
		for feature in example:
			if example[feature] == "NULL" or example[feature] == "" or example[feature] == " ":
				if feature not in mean_numeric_attributes:							#Nominal Attribute
					example[feature] = mode_nominal_attributes[feature]		
				else:
					example[feature] = mean_numeric_attributes[feature]
		new_example_set.append(example)
	example_set = new_example_set
	return example_set

	
def find_max_freq_value(value_freq):
	max_val = -1
	value_name = ""
	for key in value_freq:
		if value_freq[key] > max_val:
			max_val = value_freq[key]
			value_name = key
	return value_name


def find_all_values_mode_nominal_attribute(feature,training_set):
	values = set()
	value_freq = {}
	for example in training_set:
		example_value = example[feature]
		if example_value != "NULL" and example_value != "" and example_value != " ":
			values.add(example_value)
			if example_value in value_freq:
				frequency = value_freq[example_value]
				value_freq[example_value] = frequency + 1
			else:
				value_freq[example_value] = 1
	return values, find_max_freq_value(value_freq)


def find_average_numeric_attribute(attribute,training_set):
	sum_value = 0
	num_non_missing = 0
	for example in training_set:
		if example[attribute] != "NULL" and example[attribute] != "" and example[attribute] != " ":
			num_non_missing += 1
			sum_value += float(example[attribute])
	return float(sum_value)/float(num_non_missing)


def store_numeric_features(features):
	numeric_features = []
	numeric_features.append("VehicleAge")
	numeric_features.append("VehOdo")
	numeric_features.append("VehBCost")
	numeric_features.append("WarrantyCost")
	for feature in features:
		if feature[-5:] == "Price":
			numeric_features.append(feature)
	return numeric_features


def store_min_max_bin_width_numeric_attribute(feature,training_set):
	min_max_bin_width = []
	min_val = sys.maxint
	max_val = -1 * min_val
	for example in training_set:
		if example[feature] != "NULL" and example[feature] != "" and example[feature] != " ":
			if float(example[feature]) < min_val:
				min_val = float(example[feature])
			if float(example[feature]) > max_val:
				max_val = float(example[feature])
	min_max_bin_width.append(min_val)
	min_max_bin_width.append(max_val)
	if feature == "VehicleAge":
		min_max_bin_width.append(1)
	if feature == "VehOdo":
		min_max_bin_width.append(1000)
	if feature[-5:] == "Price" or feature == "VehBCost" or feature == "WarrantyCost":
		min_max_bin_width.append(1000)
	return min_max_bin_width
	

def store_feature_info(features,example_set):
	all_possible_values_nominal_attributes = {}
	mode_nominal_attributes = {}
	mean_numeric_attributes = {}
	numeric_attributes_min_max_bin = {}
	numeric_features = store_numeric_features(features)
	for feature in features:
		if feature not in numeric_features:																	#Nominal Attribute
			all_possible_values_nominal_attributes[feature],mode_nominal_attributes[feature] = find_all_values_mode_nominal_attribute(feature,example_set)
		else:																																#Numeric Attribute
			mean_numeric_attributes[feature] = str(find_average_numeric_attribute(feature,example_set))			
			numeric_attributes_min_max_bin[feature] = store_min_max_bin_width_numeric_attribute(feature,example_set)
	return all_possible_values_nominal_attributes,mode_nominal_attributes,mean_numeric_attributes,numeric_attributes_min_max_bin

def normalize_numeric_attributes(numeric_attributes_min_max_bin,example_set):
	new_example_set = []
	for example in example_set:
		for feature in example:
			if feature in numeric_attributes_min_max_bin:			#Numeric Data
				example[feature] = float(example[feature])
				example[feature] = float(example[feature] - numeric_attributes_min_max_bin[feature][0])/float(numeric_attributes_min_max_bin[feature][1] - numeric_attributes_min_max_bin[feature][0])
		new_example_set.append(example)
	example_set = new_example_set
	return example_set


def convert_numeric_to_nominal_binning(numeric_attributes_min_max_bin,example_set):
	all_possible_values_numeric_binned_attributes = {}
	mode_numeric_binned_attributes = {}
	new_example_set = []
	for example in example_set:
		for feature in numeric_attributes_min_max_bin:
			actual_value = example[feature]
			distance_from_min = float(actual_value) - numeric_attributes_min_max_bin[feature][0]
			bin_number = int(distance_from_min / numeric_attributes_min_max_bin[feature][2])
			example[feature] = str(bin_number)
		new_example_set.append(example)
	example_set = new_example_set
	for feature in numeric_attributes_min_max_bin:
		all_possible_values_numeric_binned_attributes[feature],mode_numeric_binned_attributes[feature] = find_all_values_mode_nominal_attribute(feature,example_set)
	return example_set,all_possible_values_numeric_binned_attributes


'''
def convert_to_binary_features(training_set,all_possible_values_nominal_attributes):
	modified_training_set = []
	training_example = {}
	for example in training_set:
		for feature in example:
			values  = all_possible_values_nominal_attributes[feature]
			for value in values:
				new_feature = feature + "_" + value
				if example[feature] == value:
					training_example[new_feature] = "1"
				else:
					training_example[new_feature] = "0"
		modified_training_set.append(training_example)
	return modified_training_set
'''

def create_csv(training_set):
	ppr_train_file = open(preprocessed_training_set_file,'w')
	feature_list = training_set[0].keys()
	for feature in feature_list:
		if feature_list.index(feature) == len(feature_list) - 1:
			ppr_train_file.write(feature)
		else:
			ppr_train_file.write(feature + ",")			
	ppr_train_file.write("\n")
	for example in training_set:
		for feature in feature_list:
			if feature_list.index(feature) == len(feature_list) - 1:
				ppr_train_file.write(example[feature])
			else:
				ppr_train_file.write(example[feature] + ",")
		ppr_train_file.write("\n")
	ppr_train_file.close()


def separate_numeric_nominal(example_set,numeric_attribute_names):
	example_set_nominal_data = []
	example_set_numeric_data = []
	for example in example_set:
		example_nominal_features = {}
		example_numeric_features = {}
		for feature in example:
			if feature in numeric_attribute_names:
				example_numeric_features[feature] = example[feature]
			else:
				example_nominal_features[feature] = example[feature]
		example_set_nominal_data.append(example_nominal_features)
		example_set_numeric_data.append(example_numeric_features)
	return example_set_nominal_data,example_set_numeric_data

csv_file = "./training_wo_null.csv"
def write_to_csv(example_set):
	op_fd = open(csv_file,"w")
	value = sorted(example_set[0].items(),key=lambda x:x[0])		
	value = [v for v,x in value]
	op_fd.write(','.join(value) + "\n")
	for example in example_set:
		value = sorted(example.items(),key=lambda x:x[0])		
		value = [x for v,x in value]
		op_fd.write(','.join(value) + "\n")
	op_fd.close()
	

def pre_process(features,example_set):
	features.remove("RefId")
	features.remove("WheelType")
	features.remove("PurchDate")
	features.remove("Model")
	features.remove("AUCGUART")
	features.remove("PRIMEUNIT")
	features.remove("Transmission")
	features.remove("IsOnlineSale")
	features.remove("VNZIP1")
	new_example_set = []
	for example in example_set:
		example.pop("RefId")
		example.pop("WheelType")
		example.pop("PurchDate")
		example.pop("Model")
		example.pop("AUCGUART")
		example.pop("PRIMEUNIT")
		example.pop("Transmission")	
		example.pop("IsOnlineSale")
		example.pop("VNZIP1")
		new_example_set.append(example)
	example_set = new_example_set
	
	all_possible_values_nominal_attributes,mode_nominal_attributes,mean_numeric_attributes,numeric_attributes_min_max_bin = store_feature_info(features,example_set)
	print "Done Storing Feature Info."

	print "Done Removing Redundant Features."
	example_set =  fill_missing_values(mode_nominal_attributes,mean_numeric_attributes,example_set)
	#TODO remove
	write_to_csv(example_set)
	sys.exit(1)
	print "Done Filling Missing Values."
	
	example_set = normalize_numeric_attributes(numeric_attributes_min_max_bin,example_set)
	example_set_nominal_data,example_set_numeric_data = separate_numeric_nominal(example_set,numeric_attributes_min_max_bin.keys())

	vec_data_file = open(vectorized_training_data,"w")
	vector_data = vectorize_data(example_set_nominal_data,vec_data_file)	
	vec_data_file.close()
	return vector_data_nominal,example_set_numeric_data
	print "Done vectorizing data."
	'''
	example_set = convert_to_binary_features(example_set,all_possible_values_nominal_attributes)
	print "Done Converting All Features to Binary Feature Vectors."
	create_csv(example_set)
	print "Done Creating The CSV File for Preprocessed Data."
	'''

	'''
	vec_data_file = open(vectorized_training_data,"w")
	vector_data = vectorize_data(example_set,vec_data_file)	
	vec_data_file.close()
	print "Done vectorizing data."
	return vector_data
	'''

	'''
	trans_data = pca_on_vectorized(vector_data,138)
	print "Done running PCA on the vectorized data."
	return trans_data
	'''
	
	
if __name__ == "__main__":
	total_data_fd = open(total_data_file,"r")
	features, total_set = store_examples(total_data_fd)
	print "Done Storing Examples."
	total_data_fd.close()	
	total_trans_data_nominal,total_trans_data_numeric = pre_process(features,total_set)
	#total_trans_data contains each example as a vector.
	
	class_labels_fd = open(class_label_file,"r")
	train_labels = class_labels_fd.readlines()[1:]
	train_labels = [float(x.strip()) for x in train_labels]
	class_labels_fd.close()

	num_training_data = len(train_labels) 
	train_data_nominal = total_trans_data_nominal[:num_training_data]
	train_data_numeric = total_trans_data_numeric[:num_training_data]
	test_data_nominal = total_trans_data_nominal[num_training_data:]
	test_data_numeric = total_trans_data_numeric[num_training_data:]

	naive_bayes_nominal_model = train_naive_bayes_nominal(train_data_nominal,train_labels)

	#TODO
	predicted_labels = run_logistic_regression(train_data,test_data,train_labels)
	
	result_file_fd = open(result_file,"w")
	result_file_fd.write("IsBadBuy\n")
	for prediction in predicted_labels:
		result_file_fd.write(str(prediction) + "\n")
	result_file_fd.close()
	
