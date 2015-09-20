### i. Paper Reviewed
C. Sun, D. Lo, X. Wang, J. Jiang, and S.-C. Khoo, “A discriminative model approach for accurate duplicate bug report retrieval,” in ICSE, 2010

###ii. Keywords and Definitions  
* **ii1. Bug Tracking Systems:** The systems these days are very complex and the software built for these systems are quite large and complex as well. Hence the software invariably has defects. Thus the bug tracking systems enable the users and testers to report the defects found and also track the statuses of the bug reports in a unified environment. Hence these bug tracking systems enable maintenance activities that result in more reliable systems.


* **ii2. Triaging:** Bug reporting is ad-hoc and uncoordinated process. Often same bugs can be reported more than once by different users. Triaging refers to the process of linking all the bugs referring to the same error, to its master bug and marking these bugs as duplicate of the of master.

* **ii3. IR Process:** Information retrieval aims to extract useful information from unstructured documents which mostly contain natural language data. The typical steps of information retrieval are:
**Preprocessing** - This is the first step in any data mining process where the data is cleaned and brought to a form that enables further processing. The most common activities of this stage are tokenization, stemming and stop word removal. During tokenization the character stream is broken down to words. In “stemming”, the words are reduced to their root words and in “stop-word removal” common words such as articles and prepositions, that carry very little helpful information, are removed.
**Term weighting** - It is a statistical process to obtain the importance of a particular word in a document or corpus. Term Frequency - Inverse Document Frequence (TF-IDF) is a popular approach, where TF is a local importance measure i.e., importance within a document and IDF is a global importance measure.


* **ii4. Support Vector Machine:** SVM is an approach to build a discriminative model or classifier based on a set of labeled vectors. When provided with a vector containing positive class and another vector containing negative class, SVM can build a hyperplane that can separate the positive class from the negative. Based on this model built, it can classify any unseen data.

### iii. Brief notes  
#####iii1. Motivation

Due to the uncoordinated and ad-hoc nature of the bug reporting system, many times bugs for the same defect are reported. These bugs have to be reported as the duplicate of the master bug. This classification often needs a manual inspection and the people who do this triaging are called triagers. Fixing bugs is one of the most frequent software maintenance activities. With the current pace of software development and the rate at which the bugs are getting reported, it is becoming harder and more painful for to keep up triagers. Hence there is a need for automated triaging that can alleviate the burden on triagers. A system that can filter out duplicate reports from reaching the triagers or a system that can give a list of reports that are similar to the one reported.

#####iii2. Hypotheses

All works related to duplicate bug report detection used similarity measure to compute the distance between reports where as in this paper, Sun et al. have used a discriminative model building approach. The classifiers in previous works returned a boolean flag “Duplicate” or “New” for each new report submitted where as the approach chosen in this paper ranked candidate duplicate bug reports are returned based on the probability measure. A bucket-based retrieval is chosen in this study rather than report-based retrieval. The latter approach can return reports that refer to same defects in the list of candidate duplicate bugs, causing redundant effort for the triager.


#####iii3. Data
Data for the project has been taken from the bug repositories of 3 large open source projects that capture different domain, different language used for code and different users. The data sets used are - 
* 12,732 bug reports reported to OpenOffice in the year 2008
* 44,653 bug reports reported to Eclipse in the year 2008
* 47,704 bug reports reported to Mozilla for Firefox since 2002, up to 2008.


#####iii4. Important Visualizations:

* **Figure-1** depicts the overall framework built to retrieve duplicate bug reports.

![Figure-1](https://github.com/Lost-In-MASE/x9115AAP/blob/master/hw/read/2/images/fig1.png)

* **Figure-2** shows the bucket data structure used to store the bug reports. Every bucket contains a master bug report and its duplicate bug reports associated with it. If a new bug report is a duplicate of existing master bug report, it is added to the respective bucket but if a new bug report is not a duplicate, a new bucket is created.

![Figure-2](https://github.com/Lost-In-MASE/x9115AAP/blob/master/hw/read/2/images/fig2.png)

* **Figure-3** is a visual depiction of the process followed for training the discriminative model to classify duplicate bug reports.

![Figure-3](https://github.com/Lost-In-MASE/x9115AAP/blob/master/hw/read/2/images/fig3.png)

### iv. Improvements  
* iv1. The study uses only summary and description fields to find similarity between bug reports. There are lots of other fields associated with a bug report, such as the product, module, comments / conversations, version; that can be used to improve the accuracy of the model.

* iv2. When talking about the experimental setup, the authors justify the run time of their approach but do not mention the configuration of the machines on which experiments were run. It would have been useful to any party which is planning to consider the approach mentioned in this paper as a viable to approach to solve duplicate bug report detection problem.

* iv3. The approach discussed in the paper outperforms existing approaches by a relative improvement of close to 25% on Firefox dataset and an improvement of 43% on Eclipse dataset. However, it would have been insightful if the authors also discussed the reasons behind such differences in number.


### v. Connection to the Initial Paper
The previously reviewed paper [1], is written by the same authors of the current paper. The previous paper discusses an approach that is an improvement over the approach of the current paper. There, BM25F is used for textual similarity (instead of discriminative model / SVM) and REP is used for retrieval. The results of the previously reviewed paper are more accurate than the current one and the run time is significantly lesser.

### v. References
* [1] C. Sun, D. Lo, S.-C. Khoo, and J. Jiang, “Towards more accurate retrieval of duplicate bug reports,” in Proceedings of the IEEE/ACM International Conference on Automated Software Engineering, 2011.