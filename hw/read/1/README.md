### i. Paper Reviewed
C. Sun, D. Lo, S.-C. Khoo, and J. Jiang, “Towards more accurate retrieval of duplicate bug reports,” in Proceedings of the IEEE/ACM International Conference on Automated Software Engineering, 2011.

###ii. Keywords and Definitions  
* **ii1. Duplicate Bug Report:** Tester and user report bugs and bug reporting is a distributed process. Sometimes the same bug can be reported by different testers and end-users. A master bug has to identified and the rest become the duplicate of the master bug.

* **ii2. Information Retrieval:** It is a ranking function that ranks the matching results according to their relevance to a given search query.

* **ii3. BM25F:** It is an effective textual similarity based information retrieval model for structured documents.

* **ii4. Gradient Descent:** It is an optimization algorithm that is used to find the local minimum of a function. Given a function that is defined by a set of parameters, gradient descent starts with an initial set of parameter values and it iteratively moves towards a set of parameter values that minimize the function.

### iii. Brief notes  
#####iii1. Motivational statements 

Every software organization has a bug tracking system where testers and users submit multiple bugs. It is possible that multiple reports for the same bug has been reported and these bugs are referred to as duplicates. In such situations it is important to prevent assigning the same problem or defect to multiple developers. Hence the bugs have to be triaged to be classified as duplicate. Most organizations these days have triagers who manually look into every bug filed to detect bug report duplication. This process is not scalable, especially in today’s world where the product development lifecycle is so short, it is important to automate the duplicate bug report detection and improve its accuracy as much as possible.

#####iii2. Data

The data required for experimentation and validation was obtained from the bug repositories of three large open source projects - OpenOffice, Mozilla and Eclipse. Since the projects are very different from one another in terms of purposes, users and implementation languages; they help in generalizing the conclusions of the experiments.

#####iii3. Related Work
* **P. Runeson, M. Alexandersson, and O. Nyholm, “Detection of Duplicate Defect Reports Using Natural Language Processing,” in proceedings of the International Conference on Software Engineering, 2007.** - This was one of the earliest works in detection of duplicate bug reports. Standard tokenization, stemming and stop word removal was performed on natural text and the bag of tokens were modeled as a feature vector. The feature value was calculated based on the formula 1 + log2(TF(word)) where TF is the term frequency. This feature vector generated for each bug report was used to measure the similarity.

* **X. Wang, L. Zhang, T. Xie, J. Anvik, and J. Sun, “An Approach to Detecting Duplicate Bug Reports using Natural Language and Execu- tion Information,” in proceedings of the International Conference on Software Engineering, 2008.** - Wang et al. also use the concept of feature vectors but here the term frequency TF and Inverse Document Frequency IDF are considered. Cosine similarity measure is used to find top-k reports similar to the candidate bug report.

* **C. Sun, D. Lo, X. Wang, J. Jiang, and S.-C. Khoo, “A discriminative model approach for accurate duplicate bug report retrieval,” in ICSE, 2010, pp. 45–56.** - Sun et al. propose the use of Support Vector machines to train a model that can compute the probability of two reports being duplicate. This probability is used to rank the bug reports based on similarity. 

* **A. Sureka and P. Jalote, “Detecting duplicate bug report using character n-gram-based features,” in Proceedings of the 2010 Asia Pacific Software Engineering Conference, 2010, pp. 366–374.** - The approach suggested by Sureka and Jalote does not consider the word tokens as features in a feature vector, but considers n-grams.

#####iii4. New Results

* BM25Fext performs constantly better than BM25F. BM25Fext gains a relative improvement of 4%– 11% on OpenOffice, 7%–13% on Mozilla, 3%–6% on Eclipse and 3%–5% on Large Eclipse datasets (over BM25F)

* The new retrieval function outperforms SVM 14–27% in OpenOffice dataset, 10–26% in Mozilla dataset and 12–22% in Eclipse dataset.

* The recall rate of Suleka and Jarote at 10 was 21%, 20 was 25% and at 2000 was 68 percent. Where as for Sun et al., recall rate at 1 is 37% and at 20 is 71%.

* The REP has also improved the running time of the experiment when compared to SVM used for retrieval.
(https://github.com/Lost-In-MASE/x9115AAP/tree/master/hw/read/1/images/Running_time.png)

### iv. Improvements  
* iv1. The logging these days is so advanced that traces can actually point to the exact location of the error. Parsing just the error logs / messages (not the entire log) can improve the accuracy of duplicate bug detection, significantly. 

* iv2. The run-time of REP retrieval is drastically less when compared to SVM. An explanation regarding choice of REP instead of SVM in the first place and a comment on why REP is so much faster when compared to SVM could have been provided.

* iv3. A comment on best practices to follow in bug reporting, to see a significant improvement of accuracy in automated duplicate bug report detection would have helped.


### v. References  

* [Gradient Descent Linear Regression] (http://spin.atomicobject.com/2014/06/24/gradient-descent-linear-regression/)

* Stephen Robertson, Hugo Zaragoza and Michael Taylor “Simple BM25 Extension to Multiple Weighted Fields”.
