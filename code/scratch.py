import pandas as pd

with open('amicus/debug_files/ok_case_names') as f:
    case_text = f.readlines()
approved_cases = [case.split('.')[0] for case in case_text[7:]]

df = pd.read_csv('amicus/scdb/SCDB_2015_01_caseCentered_Citation.csv')
print '\n'.join(df.columns)


# In the SCDB the docket column is called 'docket'
columns_of_interest = ['docket',\
                       'dateArgument',\
                       'caseIssuesId',\
                       'certReason',\
                       'naturalCourt',\
                       'chief',\
                       'issueArea',\
                       'jurisdiction',\
                       'partyWinning']

df_subset = df[df['docket'].isin(approved_cases)][columns_of_interest]

test = df_subset[df_subset.isnull().any(axis=1)]
df_final = df_subset[df_subset.notnull().all(axis=1)]

df_final['argument_month'] = df_final['dateArgument'].apply(lambda d: int(d.split('/')[0]))

















import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.cross_validation import cross_val_score

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score,                             precision_score,                             recall_score,                             classification_report,                             confusion_matrix
                

get_ipython().magic(u'matplotlib inline')

with open('amicus/debug_files/ok_case_names') as f:
    case_text = f.readlines()
approved_cases = [case.split('.')[0] for case in case_text[7:]]

df_int = pd.read_csv('amicus/debug_files/data.csv')
df_int.pop('decision')

df = pd.read_csv('amicus/scdb/SCDB_2015_01_caseCentered_Citation.csv')
print '\n'.join(df.columns)

columns_of_interest = ['docket',                       'dateArgument',                       'caseIssuesId',                       'certReason',                       'naturalCourt',                       'chief',                       'issueArea',                       'jurisdiction',                       'partyWinning']

df_subset = df[df['docket'].isin(approved_cases)][columns_of_interest]

df_subset

df_subset.isnull().sum()

test = df_subset[df_subset.isnull().any(axis=1)]
df_final = df_subset[df_subset.notnull().all(axis=1)]

df_final.head()

df_final['argument_month'] = df_final['dateArgument'].apply(lambda d: int(d.split('/')[0]))

print '\n'.join(df_final.columns)

plt.figure(figsize=(10, 10))
df_final['certReason'].hist(bins=13)
plt.xticks(range(1, 15))
("")

df_final['naturalCourt'].value_counts()

df_final['chief'].value_counts()

plt.figure(figsize=(10, 10))
df_final['issueArea'].hist(bins=15)
plt.xticks(range(1, 15))
("")

plt.figure(figsize=(10, 10))
df_final['jurisdiction'].hist(bins=2)
("")

plt.figure(figsize=(10, 10))
df_final['argument_month'].hist()
("")

print '\n'.join(df_final.columns)

a = pd.merge(df_final, df_int, on='docket')

x = a[['argument_month']].values
x = np.hstack((x, pd.get_dummies(a['certReason']).values))
x = np.hstack((x, pd.get_dummies(a['naturalCourt']).values))
x = np.hstack((x, pd.get_dummies(a['chief']).values))
x = np.hstack((x, pd.get_dummies(a['issueArea']).values))
x = np.hstack((x, pd.get_dummies(a['jurisdiction']).values))

x = np.hstack((x, pd.get_dummies(a['petitioner_interruption_count']).values))
x = np.hstack((x, pd.get_dummies(a['respondent_interruption_count']).values))
              
y_true = a['partyWinning'].values


model = LogisticRegression()

#model.fit(x, y_true)
#probs = model.predict_proba(x)[:, 1]
#threshold = 0.5
#y_pred = probs > threshold

#print classification_report(y_true, y_pred)
#print accuracy_score(y_true, y_pred)
#print confusion_matrix(y_true, y_pred)

print
scores = cross_val_score(model, x, y_true, scoring='accuracy', cv=10)
print scores
print np.mean(scores)

model = RandomForestClassifier()
#model.fit(x, y_true)

#probs = model.predict_proba(x)[:, 1]
#y_pred = probs > threshold

#print classification_report(y_true, y_pred)
#print accuracy_score(y_true, y_pred)
#print confusion_matrix(y_true, y_pred)

print
scores = cross_val_score(model, x, y_true, scoring='accuracy', cv=10)
print scores
print np.mean(scores)