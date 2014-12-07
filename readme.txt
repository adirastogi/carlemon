Steps For Pre-Processing Data:
________________________________

Please look into the "./etl/" directory for all the scripts used for preprocessing the data.
The main script used for pre-processing the data is: process_data.py

To run "process_data.py", type the following command:

	python process_data.py <CSV file_name>

Where <file_name> is the CSV file that you want to preprocess.

________________________________
Functionality of process_data.py:
________________________________
1. Find the mode of all nominal attributes in the data.
2. Find the mean of all numeric attributes in the data.
3. Fill missing values of numeric attributes with the mean of that attribute.
4. Fill missing values of nominal attributes with the mode of that attribute.
5. Add more numeric attributes (as explained in the report) which seem to be important indicators.

________________________________
Weka Steps:
________________________________
1. Load the total data (training set plus test set) into Weka.
2. Remove the attributes which were observed to be redundant (explained in the report).
3. Convert all the attributes to the correct data types (some nominal attributes are 
	 interpreted to be nominal).
4. Bin all the numeric attributes using Weka GUI -> Filter --> Unsupervised --> Attribute --> Discretize.

________________________________


Steps for Running the Classification Algorithm:
________________________________

I]	Naive Bayes:

		Please look into the "./src/" directory for source codes of all the classifiers implemented.
	 	The main classifier (one with the best score) is : "./src/NBCode/NaiveBayes.py"

		To run "NaiveBayes.py", type the following command:

		python NaiveBayes.py <train_file> <test_file> <Output prediction_file>


________________________________
Steps for running Naive Bayes:
________________________________
1. NaiveBayes.py should be run by providing the train,test and output prediction file names.
2. NaiveBayes.py will output the predictions in the prediction file provided via command line.
3. The program also outputs the metrics (true positives,negatives,etc. for the training data).
4. <Output Prediction File> should be named "result.txt" to be compatible with processing of the 
	 bash script "process_result.sh". 
5. The header "IsBadBuy" should be added to the top line of "result.txt".
6. This bash script appends the refids from "ref_ids.txt" to the prediction.
7. This generates 'prediction.txt" which is suitable for Kaggle submission.



II]	Gaussian Naive Bayes:

		Please look into the "./src/" directory for source codes of all the classifiers implemented.
	 	The program is located at: "./src/NBCode/GaussianNaiveBayes.py"

		To run "GaussianNaiveBayes.py", type the following command:

		python GaussianNaiveBayes.py <train_file> <test_file> <Output prediction_file>


________________________________
Steps for running Gaussian Naive Bayes:
________________________________
1. GaussianNaiveBayes.py should be run by providing the train,test and output prediction file names.
2. GaussianNaiveBayes.py will output the predictions in the prediction file provided via command line.
3. The program also outputs the metrics (true positives,negatives,etc. for the training data).
4. <Output Prediction File> should be named "result.txt" to be compatible with processing of the 
	 bash script "process_result.sh". 
5. The header "IsBadBuy" should be added to the top line of "result.txt".
6. This bash script appends the refids from "ref_ids.txt" to the prediction.
7. This generates 'prediction.txt" which is suitable for Kaggle submission.



III] Boosted Decision Trees:
		
		Please look into the "./src/" directory for source codes of all the classifiers implemented.
		Add the "./src/" and all its subdirectories to your "PYTHONPATH" environment variable.
	 	The program is located at: "./src/BoostedDT/boosted_dt.py"

		To run "boosted_dt.py", type the following command:

		python boosted_dt.py <train_file> <test_file> 


________________________________
Implementation Details:
________________________________
1. On running, it will produce the predictions file containing the labels for IsBadBuy.
