from DT import dt,dt_gr
from NBcode import adaboost,read_data
import sys
if __name__=="__main__":
    #sys.argv = ["progname","../../origin_data/numeric_binned/training_no_mv_new_attrs_binned.csv","../../origin_data/numeric_binned/test_no_mv_new_attrs_binned.csv"];
    ireader = read_data.InputReader();
    # returns the training data with the class label still inside X_train
    X_train,Y_train = ireader.read_csv_dt(sys.argv[1]);
    X_test = ireader.read_csv_test(sys.argv[2]);
    classifier = adaboost.AdaBoost();
    print "Starting training"
    classifier.train(X_train,Y_train,dt_gr.DTclassifierInfoGain);
    print "Printing predictions on training data"
    pred_train = classifier.predict(X_train);
    print "Printing metrics"
    read_data.print_metrics(pred_train,Y_train)
    print "Printing predictions on test data"
    pred_test = classifier.predict(X_test)
    ireader.write_predictions("prediction.txt",pred_test)
     

