import pandas as pd

with open('amicus/debug_files/ok_case_names') as f:
    case_text = f.readlines()
cases = [case.split('.')[0] for case in case_text[7:]]

df = pd.read_csv('amicus/scdb/SCDB_2015_01_caseCentered_Citation.csv')
print '\n'.join(df.columns)

columns_of_interest = ['dateArgument',\
                       'caseIssuesId',\
                       'certReason',\
                       'naturalCourt',\
                       'chief',\
                       'issueArea',\
                       'partyWinning']