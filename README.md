#Amicus
### Overview
The Supreme Court consists of nine justices who decide cases brought before them by petitioners. The petitioners' opponents in a case are called respondents. The court's decisions are based in part on oral arguments, during which the attorneys for both the petitioners and respondents answer questions from the justices. It turns out that the behavior of the attorneys and justices during oral argument can predict the court's decisions. 

The purpose of Amicus is to predict Supreme Court decisions based on oral arguments. 

![alt text](/court.jpg)

### Result
Amicus achieves accuracy comparable to [Katz, et al., 2014](http://papers.ssrn.com/sol3/papers.cfm?abstract_id=2463244), even without features based on legal expertise. 

### Pipeline 
Amicus has 4 parts:
  - Obtain oral argument transcripts
  - Process them
  - Extract behavioral features from the text
  - Model

### Future Steps
  - Make data pipeline more robust
  - Explore interaction terms
  - Explore more data sources