import pandas as pd
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

from sklearn.cross_validation import cross_val_score, KFold
from sklearn.metrics import accuracy_score, \
                            precision_score, \
                            recall_score, \
                            classification_report, \
                            confusion_matrix

get_ipython().magic(u'matplotlib inline')

with open('amicus/debug_files/ok_case_names') as f:
    case_text = f.readlines()
approved_cases = [case.split('.')[0] for case in case_text[7:]]

df = pd.read_csv('amicus/scdb/SCDB_2015_01_caseCentered_Citation.csv')
columns_of_interest = ['docket', \
                       'dateArgument', \
                       'caseIssuesId', \
                       'certReason', \
                       'naturalCourt', \
                       'chief', \
                       'issueArea', \
                       'jurisdiction', \
                       'partyWinning']

df_subset = df[df['docket'].isin(approved_cases)][columns_of_interest]
df_scdb = df_subset[df_subset.notnull().all(axis=1)]

df_scdb['argument_month'] = df_scdb['dateArgument'].apply(lambda d: int(d.split('/')[0]))

df_transcripts = pd.read_csv('amicus/debug_files/data.csv')
df_transcripts.pop('decision')

df_final = pd.merge(df_scdb, df_transcripts, on='docket')

x = df_final[['argument_month']].values
x = np.hstack((x, pd.get_dummies(df_final['certReason']).values))
x = np.hstack((x, pd.get_dummies(df_final['naturalCourt']).values))
x = np.hstack((x, pd.get_dummies(df_final['chief']).values))
x = np.hstack((x, pd.get_dummies(df_final['issueArea']).values))
x = np.hstack((x, pd.get_dummies(df_final['jurisdiction']).values))

x = np.hstack((x, pd.get_dummies(df_final['petitioner_interruption_count']).values))
x = np.hstack((x, pd.get_dummies(df_final['respondent_interruption_count']).values))
              
y_true = df_final['partyWinning'].values



#############################################################################
df = pd.read_csv('amicus/code/feature_matrix.csv')
feature_names = df.columns[1:-1]

y_true = df['decision'].values
x = df.drop(['docket', 'decision'], axis=1).values


lr_model_1 = LogisticRegression()
lr_model_1.fit(x, y_true)

scores = cross_val_score(lr_model_1, x, y_true, scoring='accuracy', cv=10)
print scores
print np.mean(scores)

accuracy_scores = []
for train, test in KFold(df.shape[0], 10):
    x_train, x_test, y_train, y_test = x[train], x[test], y_true[train], y_true[test]

    # Added regularization term
    lr_model_2 = LogisticRegression(penalty='l1', C=0.00599484)
    lr_model_2.fit(x_train, y_train)
    probs = lr_model.predict_proba(x_test)[:, 1]

    threshold = 0.3
    y_pred = probs > threshold
    accuracy_scores.append(accuracy_score(y_test, y_pred))

print
print scores
print np.mean(accuracy_scores)



x_const = add_constant(x, prepend=True)
logit_model = Logit(y_true, x_const).fit()
#logit_model = Logit(y_true, x_const).fit_regularized(method='l1', alpha=0.00599484)
logit_model.summary()



# significant features:
#
# 1  : num_petitioner_lawyers
# 2  : num_respondent_lawyers (possibly significant?)
# 4  : p_interruption_count
# 5  : p_word_count
# 19 : p_justice_question_count
# 23 : p_justice_I_count
# 27 : r_word_count
# 29 : r_pauses



lrcv = LogisticRegressionCV(penalty='l1', solver='liblinear')
lrcv.fit(x, y_true, )

lrcv.C_

print lrcv.coef_
import pylab as py
%matplotlib inline
py.plot(sorted(lrcv.coef_[0]))