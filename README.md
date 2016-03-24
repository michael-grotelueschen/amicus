#Amicus
### Overview
The Supreme Court consists of nine justices who decide cases brought before them by petitioners. The petitioners' opponents in a case are called respondents. The court's decisions are based in part on oral arguments, during which the attorneys for both the petitioners and respondents answer questions from the justices. 

The purpose of Amicus is to predict Supreme Court decisions based on the behavior of attorneys and justices during oral arguments. 

![alt text](/court.jpg)

### Result
Amicus achieves accuracy comparable to a control model based on legal information developed by expert legal analysts ([Katz, et al., 2014](http://papers.ssrn.com/sol3/papers.cfm?abstract_id=2463244)) even without features based on legal expertise. Instead, the features are law-agnostic textual details like laughter, pauses, or interruptions found in oral argument transcripts.

### Pipeline 
Amicus has 4 parts:
  - Obtain oral argument transcripts
  - Process them
  - Extract behavioral features from the text
  - Model

Supreme Court oral argument transcripts are public and freely available at ([supremecourt.gov](http://www.supremecourt.gov)) I crawled the site and downloaded more than 700 transcripts in PDF format. Then, I used Apache Tika to extract raw text data from the PDFs. Next I wrote a few python scripts to clean the raw text and process it into a format to make analysis as easy as possible. (There are many examples of the format in [txts_whitelist](https://github.com/michael-grotelueschen/amicus/tree/master/txts_whitelist). Next, I came up with behavioral features like laughter, pauses, interruptions, or mentions of other cases and collected them from the text. These and other features are collected separately for justices, petitioner attorneys, and respondent attorneys. Finally, I used these features in a logistic regression model.

### Future Steps
  - Make data pipeline more robust
  - Explore interaction terms
  - Explore more data sources