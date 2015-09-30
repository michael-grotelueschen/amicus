
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


# In[36]:

model = LogisticRegression()

#model.fit(x, y_true)
#probs = model.predict_proba(x)[:, 1]
#threshold = 0.5
#y_pred = probs > threshold

#print classification_report(y_true, y_pred)
#print accuracy_score(y_true, y_pred)
#print confusion_matrix(y_true, y_pred)

scores = cross_val_score(model, x, y_true, scoring='f1', cv=10)
print np.mean(scores)


# In[37]:

model = RandomForestClassifier()
#model.fit(x, y_true)

#probs = model.predict_proba(x)[:, 1]
#y_pred = probs > threshold

#print classification_report(y_true, y_pred)
#print accuracy_score(y_true, y_pred)
#print confusion_matrix(y_true, y_pred)

scores = cross_val_score(model, x, y_true, scoring='f1', cv=10)
print np.mean(scores)


# In[ ]:




# In[ ]:



