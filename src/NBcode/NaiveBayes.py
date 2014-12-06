'''Implements the Naive Bayes classifier'''
import naive_bayes
import read_data
import sys;


if __name__=='__main__':
    ireader = read_data.InputReader();
    X_train,Y_train = ireader.read_input(sys.argv[1]);
    X_test,Y_test = ireader.read_input(sys.argv[2]);
    classifier = naive_bayes.NBclassifier();
    classifier.train(X_train,Y_train);
    #calculate predictions on training data
    pred_train = classifier.predict(X_train);
    read_data.print_metrics(pred_train,Y_train)
    #calculate predictions on test data
    pred_test = classifier.predict(X_test)
    read_data.print_metrics(pred_test,Y_test)


