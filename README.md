#Amicus
## Overview
The Supreme Court consists of 9 judges, called justices, who decide cases brought before them by petitioners. Their opponents are called respondents. The courts’ decisions are based in part on oral arguments, during which the attorneys for both the petitioner and respondent sides of the case answer questions from the justices. It turns out that the behavior of the attorneys and justices during oral argument can predict the courts’ decisions. 

The purpose of Amicus is to predict Supreme Court decisions based on oral arguments. 

![alt text](/court.jpg)

## Result
Amicus achieves accuracy comparable to [Katz, et al., 2014](http://papers.ssrn.com/sol3/papers.cfm?abstract_id=2463244), even without features based on legal expertise. 

## Pipeline 
Amicus has 4 parts:
  - Obtain oral argument transcripts
  - Process them
  - Extract behavioral features from the text
  - Model

 ## Next steps 
