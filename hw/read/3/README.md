### i. Paper Reviewed
Ashish Sureka and Pankaj Jalote, “Detecting Duplicate Bug Report Using Character N-Gram-Based Features” in 2010 Asia Pacific Software Engineering Conference.

###ii. Keywords and Definitions  
* **ii1. Bug Report Analysis:** A bug report is expected to contain enough information for a developer to fix the bug and not too much information such that the problem sounds more complicated than what it actually is. Bug report analysis can be used to fetch legible information from a stack trace or a bug report filed by users.


* **ii2. Duplicate Bug Detection:** As software grows, the number of features and number of users may grow along. An unfortunate side effect is the bug numbers increasing. A lot of times diffferent reports may actually be pointing to the same issue but may be picked up by different teams leading to time wastage. Duplicate bug detection tries to match similar bugs together to help triagers to finish work efficiently.

* **ii3. Text Classification:** Text classification is the process of taking some text and categorizing it into a set of predefined tags. Text classification can be done in different ways, documents can be classified into either single tags (at most) or multiple tags. SVMs are popular when it comes to text classification.


* **ii4. Software Engineering Task Automation:** The process of automating tasks that form part of the routine software engineering process such as code deployment, automated builds and infrastructure setup. Another important task with this paper in context is bug merging, this is a pretty intensive task for the triager.

### iii. Brief notes  
#####iii1. Motivation

Software matures with time, and one of the key factors that help mature the program are the bug reports. These bugs are reported via bug trackers and before the bugs are sent over to developers to work on a fix, they are triaged. Triaging is the process followed by a triager who is someone with knowledge of the system and the people involved in its development, they process the reports to make sure there is enough information to be able to find the issue and fix. They also make sure that new tasks are merged with duplicate tasks already in the system. Duplicate tasks can lead to problems in terms of efficiency where the same bug can be worked upon by multiple teams just because they had more than one report associated with them. When the rate of inbound reports is high, manual work on bug duplicate detection becomes a really hard job and fails. This paper aims at devising a scalable method for merging duplicate bugs.

#####iii2. Hypotheses

All works prior to this literature performed bug duplicate detection using word-level analysis of reports while the approach mentioned here works on a character level representation. The argument behind this approach is that characters can give an idea of key linguistic features. Character level approach also provides language independence which could help make sense of noisy text and prevent the system from relying on tokenization, stop-word removal and other language specific data pre processing techniques.


#####iii3. Data
Data for the project has been taken from the bug repositories of eclipse which is available as XML for experiments and research purposes. 213,000 bug for the eclipse project were downloaded from the publicly available of the Mining Software Repositories Mining Challenge website. The speciality of this dataset is that they were pre-annotated, that is bugs were tagged as duplicates by the triager who worked on them.

### iii4. Visualizations

* **Figure-1** Overall system architecture for similarity detection

![Figure-1](https://github.com/Lost-In-MASE/x9115AAP/blob/master/hw/read/3/images/hlsa.PNG)

* **Figure-2** Graph showing the percentage of reports that had a score greater than 50 based on title similarity, title similarity was the main metric in finding duplicate reports in this study.

![Figure-2](https://github.com/Lost-In-MASE/x9115AAP/blob/master/hw/read/3/images/tts.PNG)

* **Figure-3** Histogram showing the top-N results for bug reports based on Title-Title, Title-Description and Description-Title similarity metric.

![Figure-3](https://github.com/Lost-In-MASE/x9115AAP/blob/master/hw/read/3/images/recra.PNG)

### iv. Improvements  
* iv1. The study uses only the title of bug reports and performs character level n-grams between reports, there are times when completely different titles can have similar description.

* iv2. Studies have often used eclipse datasets to perform their studies and many perform really well on the eclipse data, it could be accounted to better bug reporting techniques, the same studies also don't perform as well on other datasets. Using a single dataset to prove a study seems to me that they are being over optimistic with limited positive results.

* iv3. The authors use the dataset of the experiment in this case being significantly larger than the previous experiments as an improvement over prior studies. This however doesn't consider the diversity factor that was present in the dataset of previous studies such as multiple data sources that ranged across different types of applications.

### v. Connection to the Initial Paper
The previously reviewed paper [1], is an improvement over this paper. In fact this paper was a baseline study used in [1] to show how their method is a major improvement over character level n-gram approach.

### vi. References
* [1] C. Sun, D. Lo, S.-C. Khoo, and J. Jiang, “Towards more accurate retrieval of duplicate bug reports,” in Proceedings of the IEEE/ACM International Conference on Automated Software Engineering, 2011.