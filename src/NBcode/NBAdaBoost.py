'''Implements the AdaBoosted NaiveBayes classifier'''
import naive_bayes
import adaboost
import read_data
import sys

if __name__=='__main__':

    ireader = read_data.InputReader();
    X_train,Y_train = ireader.read_input(sys.argv[1]);
    X_test,Y_test = ireader.read_input(sys.argv[2]);
    abclassifier = adaboost.AdaBoost();
    abclassifier.train(X_train,Y_train,naive_bayes.NBclassifier);
    #calculate predictions on training data
    pred_train = abclassifier.predict(X_train);
    read_data.print_metrics(pred_train,Y_train)
    #calculate predictions on test data
    pred_test = abclassifier.predict(X_test)
    read_data.print_metrics(pred_test,Y_test)

