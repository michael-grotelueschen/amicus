
# coding: utf-8

# In[31]:

import pandas as pd
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

from sklearn.cross_validation import cross_val_score
from sklearn.metrics import accuracy_score,                            precision_score,                            recall_score,                            classification_report,                            confusion_matrix                
get_ipython().magic(u'matplotlib inline')


# In[32]:

with open('amicus/debug_files/ok_case_names') as f:
    case_text = f.readlines()
approved_cases = [case.split('.')[0] for case in case_text[7:]]

df = pd.read_csv('amicus/scdb/SCDB_2015_01_caseCentered_Citation.csv')
columns_of_interest = ['docket',                       'dateArgument',                       'caseIssuesId',                       'certReason',                       'naturalCourt',                       'chief',                       'issueArea',                       'jurisdiction',                       'partyWinning']

df_subset = df[df['docket'].isin(approved_cases)][columns_of_interest]
df_scdb = df_subset[df_subset.notnull().all(axis=1)]


# In[33]:

df_scdb['argument_month'] = df_scdb['dateArgument'].apply(lambda d: int(d.split('/')[0]))


# In[34]:

df_transcripts = pd.read_csv('amicus/debug_files/data.csv')
df_transcripts.pop('decision')

df_final = pd.merge(df_scdb, df_transcripts, on='docket')
("")


# In[35]:

x = df_final[['argument_month']].values
x = np.hstack((x, pd.get_dummies(df_final['certReason']).values))
x = np.hstack((x, pd.get_dummies(df_final['naturalCourt']).values))
x = np.hstack((x, pd.get_dummies(df_final['chief']).values))
x = np.hstack((x, pd.get_dummies(df_final['issueArea']).values))
x = np.hstack((x, pd.get_dummies(df_final['jurisdiction']).values))

x = np.hstack((x, pd.get_dummies(df_final['petitioner_interruption_count']).values))
x = np.hstack((x, pd.get_dummies(df_final['respondent_interruption_count']).values))
              
y_true = df_final['partyWinning'].values












import pandas as pd
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

from sklearn.cross_validation import cross_val_score
from sklearn.metrics import accuracy_score,                            precision_score,                            recall_score,                            classification_report,                            confusion_matrix
get_ipython().magic(u'matplotlib inline')


# In[193]:

df_transcripts = pd.read_csv('amicus/code/test_file.csv')
dockets = df_transcripts['docket'].tolist()

ok_cases_train_set = []
with open('amicus/code/ok_cases_train_set') as f:
    for line in f:
        case = line.replace('\n', '')
        ok_cases_train_set.append(case)
        
ok_cases_test_set = []
with open('amicus/code/ok_cases_test_set') as f:
    for line in f:
        case = line.replace('\n', '')
        ok_cases_test_set.append(case)

train_set_mask = [True if d in ok_cases_train_set else False for d in dockets]
test_set_mask = [True if d in ok_cases_test_set else False for d in dockets]


# In[194]:

df_train_set = df_transcripts[train_set_mask]
df_test_set = df_transcripts[test_set_mask]


# In[195]:

y_true_train = df_train_set['decision'].values
df_train_set.pop('decision')
df_train_set.pop('docket')
x_train = df_train_set.values

y_true_test = df_test_set['decision'].values
df_test_set.pop('decision')
df_test_set.pop('docket')
x_test = df_test_set.values


# In[210]:

lr_model = LogisticRegression()
lr_model.fit(x_train, y_true_train)
lr_model.get_params()

probs = lr_model.predict_proba(x_test)[:, 1]
threshold = 0.7
y_pred = probs > threshold

print classification_report(y_true_test, y_pred)
print accuracy_score(y_true_test, y_pred)
print confusion_matrix(y_true_test, y_pred)

#scores = cross_val_score(lr_model, x, y_true, scoring='f1', cv=10)
#print scores
#print np.mean(scores)


# In[197]:

rf_model = RandomForestClassifier()
rf_model.fit(x_train, y_true_train)

probs = rf_model.predict_proba(x_test)[:, 1]
threshold = 0.5
y_pred = probs > threshold

print classification_report(y_true_test, y_pred)
print accuracy_score(y_true_test, y_pred)
print confusion_matrix(y_true_test, y_pred)

#scores = cross_val_score(rf_model, x, y_true, scoring='f1', cv=10)
#print scores
#print np.mean(scores)