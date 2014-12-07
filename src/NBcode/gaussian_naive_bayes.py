#!/usr/bin/env python
# Naive Bayes classifier running code, makes the following assumptions:
# missing values in mueric attributes have been filled in !
# preferably no surprises in the attrtibute data.
import naive_bayes
import read_data
import naive_bayes
import sys
if __name__=='__main__':
    
    disable_numeric = True;

    if disable_numeric==True:
        numeric_attr_names = []
    else:
        numeric_attr_names = [
        'WarrantyCost',
        'MMRAcquisitionAuctionCleanPrice',
        'MMRCurrentRetailAveragePrice',
        'MMRAcquisitionRetailAveragePrice',
        'VehOdo',
        'VehicleAge',
        'MMRCurrentRetailCleanPrice',
        'MMRAcquisitionAuctionAveragePrice',
        'MMRAcquisitonRetailCleanPrice',
        'MMRCurrentAuctionAveragePrice',
        'VehBCost',
        'MMRCurrentAuctionCleanPrice',
        'VehOdo_by_VehAge',
        'r2_minus_r1_avg',
        'r2_minus_r1_clean',
        'r2_minus_a1_avg',
        'r2_minus_a1_clean',
        'r2_avg_minus_vehbc',
        'r2_clean_minus_vehbc',
        'vehbc_minus_a1_avg',
        'vehbc_minus_a1_clean',
        'warranty_by_vehbc'
        ]

    reader = read_data.InputReader()
    X_train,Y_train  = reader.read_csv(sys.argv[1]);
    X_test = reader.read_csv_test(sys.argv[2]);
    classifier = naive_bayes.NBclassifier();
    classifier.train(X_train,Y_train,numeric_attr_names);
    #classifier.dump()
    pred_train = classifier.predict(X_train,numeric_attr_names);
    pred_test = classifier.predict(X_test,numeric_attr_names);
    #calculate predictions on training data
    print "Status on training data"
    read_data.print_metrics(pred_train,Y_train);
    print "Writing the new predictions in file predictions.txt"
    reader.write_predictions("result.txt",pred_test)
    

    
