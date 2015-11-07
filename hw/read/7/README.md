### i. Paper Reviewed
Anahita Alipour , Abram Hindle , Eleni Stroulia, A contextual approach towards more accurate duplicate bug report detection, Proceedings of the 10th Working Conference on Mining Software Repositories, May 18-19, 2013, San Francisco, CA, USA


###ii. Keywords and Definitions
* **ii1. Bug Deduplication:** The term deduplication refers generally to eliminating duplicate or redundant information. The process of bug triaging or analysing bugs to find and group duplicate bugs is called Bug Deduplication.

* **ii2. Contextual Information:** Information regarding software quality, software architecture and system development can be defined as contextual information. Context of a bug report can be identified by some of the domain specific words used in the title or description of the bugs. For example, topic words such as bluetooth, browser, USB etc., can define and thus differentiate the context of bugs.

* **ii3. Text Similarity:** Measuring the similarity between words, sentences, paragraphs and documents is referred to as Text Similarity. It forms an integral part of Information Retrieval. Three well known approaches to measure textual similarity are String-based, Corpus-based and Knowledge-based approaches.

* **ii4. Machine Learning Evaluation:** The paper discusses about various machine learning algorithms used to classify bugs as duplicates. The algorithms used are 0-R, C4.5, K-NN (K Nearest Neighbours), Logistic Regression, and Naive Bayes.


### iii. Brief notes

#####iii1. Hypothesis

Detection of duplicate bug reports is currently being done manually and hence there has been lot of research to alleviate the burden on triagers through automated duplicate bug detection. The studies have shown great progress and considerable accuracy in detection. However, there is still a lot of room for improvement. In this paper, the authors introduce a new approach for improvement in accuracy. This approach exploits domain knowledge about the software engineering process and the knowledge of the system specifically. In the paper, the authors show that the performance of bug report deduplication is increased by this approach and hence one should not ignore domain and context of software engineering and software development. The improved accuracy will save money and effort on bug triaging and duplicate bug detection, for companies.

#####iii2. Related Work

* **P. Runeson, M. Alexandersson, and O. Nyholm, “Detection of duplicate defect reports using natural language processing,” in Software Engineer- ing, 2007. ICSE 2007. 29th International Conference on. IEEE, 2007, pp. 499–510.** - In this paper, the authors have developed a prototype tool to study the effect of NLP on detecting duplicate bug reports using the defect reports of Sony Ericson Mobile Commu- nications. Their evaluations shows that about 66% of the duplicates can be found using the NLP techniques.

* **D. Poshyvanyk, A. Marcus, R. Ferenc, and T. Gyimo ́thy, “Using infor- mation retrieval based coupling measures for impact analysis,” Empirical Software Engineering, vol. 14, no. 1, pp. 5–32, 2009.** - The paper provides two different definitions for similar and duplicate bugs. The bugs are compared using some well-known string similarity algorithms and semantic similarity methods.

* **N. Bettenburg, R. Premraj, T. Zimmermann, and S. Kim, “Duplicate bug reports considered harmful really?” in Software Maintenance, 2008. ICSM 2008. IEEE International Conference on. IEEE, 2008, pp. 337– 345.** - In this study, the authors follow an approach in which the triaging is done by machine learners. The textual features of the bug reports are converted to word vectors which are then fed to SVM and Naive Bayes algorithms for automated bug triaging. The authors show that the SVM is more accurate.

* **N. Jalbert and W. Weimer, “Automated duplicate detection for bug tracking systems,” in Dependable Systems and Networks With FTCS and DCC, 2008. DSN 2008. IEEE International Conference on. IEEE, 2008, pp. 52–61.** - In this study, the authors introduced a classifier for incoming bug reports which combines the categorical features of the reports, textual similarity metrics, and graph clustering algorithms to identify duplicates.

* **X. Wang, L. Zhang, T. Xie, J. Anvik, and J. Sun, “An approach to detecting duplicate bug reports using natural language and execution information,” in Proceedings of the 30th international conference on Software engineering. ACM, 2008, pp. 461–470.** - The approach followed in this study shows some promise behind using contextual information. The authors used natural language information, combined with execution information to detect duplicate bugs. 

* **R.Lotufo,Z.Malik,andK.Czarnecki,“Modellingthehurriedbugreport reading process to summarize bug reports.”** - This is a study about how a triager reads and navigates through bugs. The authors developed a bug summarizer using this research. The quality of the summarizer has successfully been evaluated on a wide variety of developers.

#####iii3. New Results

As mentioned before, there have been several studies on detection of duplicate bugs. But most of the previous works have concentrated on textual similarities as the means to detect duplicate bugs. This is the first time that contextual information such as prior knowledge of software quality, software architecture, software development topics and so on. The studies show that there is a 11.55% improvement in accuracy over Sun et al[1]. The results thus confirm that pulling in contextual information can boost the performance of bug deduplication.

#####iii4. Informative Visualisations

The picture below shows the workflow of the methodology followed by the authors. The rectangles represent data and rounded corner rectangles represent activities.

![Workflow](https://github.com/Lost-In-MASE/x9115AAP/blob/master/hw/read/7/images/workflow.png)


### iv. Improvements

* iv1. The authors could have thrown some light on the setup used to conduct the experiments.

* iv2. The experiment was an improvisation on Sun et al's approach[1], but was conducted on a different dataset. The impact on the runtime due to measurement of contextual similarity could have been discussed.

* iv3. The critical aspect of the study is the list of topic words that help define the context of a bug. For the Android repository, there have been several studies that have tried to extract such topic words. Hence, for this experiment, a word list of contextual features was available and used. The authors could have discussed a little more in detail regarding the approaches that could be used to extract topic words from bugs(and not popular terms).

### v. Connection to the Initial Paper
This entire study was based on the first paper. Sun et al. in [1] discuss about an accurate approach for retrieving duplicate bug reports. Anahita et al. use these findings as the baseline and show that contextual information can improve the accuracy of the detection. The approaches used for information retrieval, classification and extraction are all inspired by paper 1.

### vi. References

* [1]C. Sun, D. Lo, S. Khoo, and J. Jiang, “Towards more accurate retrieval of duplicate bug reports,” in Proceedings of the 2011 26th IEEE/ACM International Conference on Automated Software Engineering. IEEE Computer Society, 2011, pp. 253–262.

