#!/usr/bin/python
import sys
import csv


def find_max_freq_value(value_freq):
	max_val = -1
	value_name = ""
	for key in value_freq:
		if value_freq[key] > max_val:
			max_val = value_freq[key]
			value_name = key
	return value_name


def find_average_numeric_attribute(attribute,example_set):
	sum_value = 0
	num_non_missing = 0
	for example in example_set:
		if example[attribute] != "NULL" and example[attribute] != "" and example[attribute] != " ":
			num_non_missing += 1
			sum_value += float(example[attribute])
	return float(sum_value)/float(num_non_missing)


def find_mode_nominal_attribute(feature,example_set):
	value_freq = {}
	for example in example_set:
		example_value = example[feature]
		if example_value != "NULL" and example_value != "" and example_value != " ":
			if example_value in value_freq:
				frequency = value_freq[example_value]
				value_freq[example_value] = frequency + 1
			else:
				value_freq[example_value] = 1
	return find_max_freq_value(value_freq)


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


def store_feature_info(features,example_set):
	mode_nominal_attributes = {}
	mean_numeric_attributes = {}
	numeric_features = store_numeric_features(features)
	for feature in features:
		if feature not in numeric_features:																	#Nominal Attribute
			mode_nominal_attributes[feature] = find_mode_nominal_attribute(feature,example_set)
		else:																																#Numeric Attribute
			mean_numeric_attributes[feature] = str(find_average_numeric_attribute(feature,example_set))			
	return mode_nominal_attributes,mean_numeric_attributes


def fill_missing_values(mode_nominal_attributes,mean_numeric_attributes,example_set):
	for example in example_set:
		for feature in example:
			if example[feature] == "NULL" or example[feature] == "" or example[feature] == " ":
				if feature not in mean_numeric_attributes:							#Nominal Attribute
					example[feature] = mode_nominal_attributes[feature]		
				else:
					example[feature] = mean_numeric_attributes[feature]
	print "Done replacing missing values with mean and mode of numeric and nominal data respectively."
	return example_set


def process(features,data):
	mode_nominal_attributes,mean_numeric_attributes= store_feature_info(features,data)
	print "Done Storing Feature Info."
	return fill_missing_values(mode_nominal_attributes,mean_numeric_attributes,data),mean_numeric_attributes


def add_attributes(data_wo_missing_vals,mean_numeric_attributes,fields):
	fields.append("VehOdo_by_VehAge")
	fields.append("r2_minus_r1_avg")
	fields.append("r2_minus_r1_clean")
	fields.append("r2_minus_a1_avg")
	fields.append("r2_minus_a1_clean")
	fields.append("r2_avg_minus_vehbc")
	fields.append("r2_clean_minus_vehbc")
	fields.append("vehbc_minus_a1_avg")
	fields.append("vehbc_minus_a1_clean")
	fields.append("warranty_by_vehbc")

	for example in data_wo_missing_vals:
		age = float(example["VehicleAge"])
		if age != 0:
			example["VehOdo_by_VehAge"] = float(example["VehOdo"])/float(age)
		else:
			example["VehOdo_by_VehAge"] = float(example["VehOdo"])/float(0.5)
		example["r2_minus_r1_avg"] = float(example["MMRCurrentRetailAveragePrice"]) - float(example["MMRAcquisitionRetailAveragePrice"])
		example["r2_minus_r1_clean"] = float(example["MMRCurrentRetailCleanPrice"]) - float(example["MMRAcquisitonRetailCleanPrice"])
		example["r2_minus_a1_avg"] = float(example["MMRCurrentRetailAveragePrice"]) - float(example["MMRAcquisitionAuctionAveragePrice"])
		example["r2_minus_a1_clean"] = float(example["MMRCurrentRetailCleanPrice"]) - float(example["MMRAcquisitionAuctionCleanPrice"])
		example["r2_avg_minus_vehbc"] = float(example["MMRCurrentRetailAveragePrice"]) - float(example["VehBCost"])
		example["r2_clean_minus_vehbc"] = float(example["MMRCurrentRetailCleanPrice"]) - float(example["VehBCost"])
		example["vehbc_minus_a1_avg"] = float(example["VehBCost"]) - float(example["MMRAcquisitionAuctionAveragePrice"])
		example["vehbc_minus_a1_clean"] = float(example["VehBCost"]) - float(example["MMRAcquisitionAuctionCleanPrice"])

		vehbc = float(example["VehBCost"])
		if vehbc != 0:
			example["warranty_by_vehbc"] = float(example["WarrantyCost"])/float(example["VehBCost"])		
		else:
			example["warranty_by_vehbc"] = float(example["WarrantyCost"])/float(mean_numeric_attributes["VehBCost"])

	return data_wo_missing_vals,fields
		

if __name__ == "__main__":
	data = []
	file_name = sys.argv[1]
	with open(file_name,"r") as fd:
		reader = csv.DictReader(fd)
		data = [row for row in reader]
	fields = data[0].keys()
	data_wo_missing_vals,mean_numeric_attributes = process(fields,data)
	data_wo_missing_vals_new_attrs,fields = add_attributes(data_wo_missing_vals,mean_numeric_attributes,fields)
	print "Done adding new features to the data points"
	
	with open(file_name[0:-4] + "_no_missing_vals_new_attrs.csv","w") as processed_file:
		writer = csv.DictWriter(processed_file,fields)
		writer.writeheader()
		for example in data:
			writer.writerow(example)
