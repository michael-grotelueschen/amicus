import pandas as pd
import numpy as np
import cPickle
import matplotlib.pyplot as plt

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

from sklearn.cross_validation import cross_val_score
from sklearn.metrics import accuracy_score, \
                            precision_score, \
                            recall_score, \
                            classification_report, \
                            confusion_matrix

def get_train_set_and_test_set_dataframes():
    """Return a train set dataframe and a test set dataframe
    from the feature matrix.
    """
    df_transcripts = pd.read_csv('feature_matrix.csv')
    dockets = df_transcripts['docket'].tolist()

    ok_cases_train_set = []
    with open('ok_cases_train_set') as f:
        for line in f:
            case = line.replace('\n', '')
            ok_cases_train_set.append(case)
            
    ok_cases_test_set = []
    with open('ok_cases_test_set') as f:
        for line in f:
            case = line.replace('\n', '')
            ok_cases_test_set.append(case)

    train_set_mask = [True if d in ok_cases_train_set else False for d in dockets]
    test_set_mask = [True if d in ok_cases_test_set else False for d in dockets]

    df_train_set = df_transcripts[train_set_mask]
    df_test_set = df_transcripts[test_set_mask]

    return df_train_set, df_test_set

def exlore_models():
    """This is a placeholder function explore modeling."""
    df_train_set, df_test_set = get_train_set_and_test_set_dataframes()

    y_true_train = df_train_set['decision'].values
    x_train = df_train_set.drop(['docket', 'decision'], axis=1).values

    y_true_test = df_test_set['decision'].values
    x_test = df_test_set.drop(['docket', 'decision'], axis=1).values

    #lr_model = LogisticRegression()
    #lr_model.fit(x_train, y_true_train)
    #probs = lr_model.predict_proba(x_test)[:, 1]
    #threshold = 0.7
    #y_pred = probs > threshold

    #print classification_report(y_true_test, y_pred)
    #print accuracy_score(y_true_test, y_pred)
    #print confusion_matrix(y_true_test, y_pred)
    #scores = cross_val_score(lr_model, x, y_true, scoring='f1', cv=10)
    #print scores
    #print np.mean(scores)

    #rf_model = RandomForestClassifier()
    #rf_model.fit(x_train, y_true_train)
    #probs = rf_model.predict_proba(x_test)[:, 1]
    #threshold = 0.5
    #y_pred = probs > threshold

    #print classification_report(y_true_test, y_pred)
    #print accuracy_score(y_true_test, y_pred)
    #print confusion_matrix(y_true_test, y_pred)
    #scores = cross_val_score(rf_model, x, y_true, scoring='f1', cv=10)
    #print scores
    #print np.mean(scores)

def get_predictions():
    """Get predictions for a particular model."""
    df_train_set, df_test_set = get_train_set_and_test_set_dataframes()

    y_true_train = df_train_set['decision'].values
    x_train = df_train_set.drop(['docket', 'decision'], axis=1).values

    y_true_test = df_test_set['decision'].values
    x_test = df_test_set.drop(['docket', 'decision'], axis=1).values

    lr_model = LogisticRegression()
    lr_model.fit(x_train, y_true_train)
    probs = lr_model.predict_proba(x_test)[:, 1]
    threshold = 0.7
    y_pred = probs > threshold

    predictions = []
    for docket, prediction in zip(df_test_set['docket'].tolist(), y_pred):
        if prediction == True:
            winning_side = 'petitioner'
        else:
            winning_side = 'respondent'
        predictions.append(docket + ':' + winning_side)
    return '\n'.join(predictions)

if __name__ == "__main__":
    predictions = get_predictions()
    with open('predictions', 'w') as f:
        f.write(predictions)