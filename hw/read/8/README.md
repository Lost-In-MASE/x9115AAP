### i. Paper Reviewed
Aggarwal, Karan, et al. "Detecting duplicate bug reports with software engineering domain knowledge." Software Analysis, Evolution and Reengineering (SANER), 2015 IEEE 22nd International Conference on. IEEE, 2015.

###ii. Keywords and Definitions
* **ii1. Software Literature Context:** The term refers to extracting words from software engineering literature, that can be used as contextual features that help understand the context of a bug report. This can be used in automated bug triaging.

* **ii2. Latent Dirichlet Alllocation (LDA):** LDA is a probabilistic, generative model for discovering latent semantic topics in large collections of text data[1]. Mining an entire corpus of text documents can expose sets of words that frequently co-occur within documents. These sets of words may be intuitively interpreted as topics and each discovered topic is characterized by its own particular distribution over words which act as the building blocks of the short descriptions. LDA is an algorithm that specifically aims to find these short descriptions for members in a data collection.

* **ii3. Bug-Report Preprocessing:** Preprocessing is important step of data mining. Some of the bug common steps followed in bug report preprocessing are - removal of bug reports that lack sufficient information such as bug ID, removal of stop words from title and bug description, prune large clusters of similar bugs as they may introduce a strong bias in prediction and so on.

* **ii4. Issue Tracking Systems:** They form an integral part of quality assurance processes for modern day software projects. These systems typically record issues (popularly known as bugs) that developers, testers and other users enounter in a software system. These systems serve as repositories of bug reports, stack traces and feature requests.

### iii. Brief notes###

#####iii1. Motivational statements

Automated bug tracking has gained importance in the field of software engineering over the past few years because the of rapid pace with which the bugs are being reported each day. There are several challenges with detection of duplicate bugs. Since bug reporting distributed random process, reporting of duplicate bugs cannot be controlled at source. Moreover, bug reports are written in in natural-language text and hence the same issue can potentially be described in several ways. This makes it hard to identify duplicates. Vocabulary used by developers who report issue may be much different when compared to that of an end user. It would require an expert in the field to be a triager and detect duplicate bug reports. Thus recognizing duplicate reports is an important problem that, if solved, would enable developers to fix bugs faster, and prevent them from wasting time by addressing the same bug multiple times.

#####iii2. Data

This paper uses four different bug datasets from open-source projects, Android, Open Office, Mozilla, and Eclipse containing approximately 37000, 42000, 72000 and 29000 bug reports respectively. For the study, the authors have also extracted conextual words from various sources such as Pressman’s "Software Engineering: A Practitioner’s Approach"[2], Murphy's "The Busy Coder’s Guide to Android Development"[3], Eclipse Documentation, Open Office Documentation, Mozilla Documentation, LDA topic words used by Alipour et al. in [5] and Random English Words for baseline results.

#####iii3. New Results

Alipour et al. first introduced the concept of using contextual words to improve the accuracy of bug de-duplication, in [5]. But Alipour et al. used Labelled LDA approach to extract contextual features. This procedure took 60 person-hours to create topic words. However, in this paper, the authors propose "software literature conext method", where the conextual words are extracted from a generic software-literature. This approach shows a significant improvement in time with a slight decrease in accuracy of prediction. The extraction of contextual words in the current approach took only half a person-hour. The general software-engineering features extracted from a textbook published in 2001, performed only marginally worse, showing the robustness of the software-literature context method.

The figure below shows the results for Eclipse bugs and Open Office bugs, in comparison with results obtained by following the procedure mentioned in [5].
![Results](https://github.com/Lost-In-MASE/x9115AAP/blob/master/hw/read/8/images/results.png)

#####iii4. Informative Visualisations

The picture below shows the workflow of the methodology followed by the authors. The rectangles represent data and rounded corner rectangles represent activities.
![Workflow](https://github.com/Lost-In-MASE/x9115AAP/blob/master/hw/read/8/images/workflow.png)

### iv. Improvements

* iv1. The authors could have thrown some light on the setup used to conduct the experiments.

* iv2. The authors could discussed in detail about how to extract quality contexts from multiple textbooks and source of documentations and efficient representations of such contexts.

* iv3. The accuracy of contextual information from software literature was almost equal to that of contextual information extracted from random english words. This brings up the question of generic software enngineering is a good enough source for extractng contextual information or should domain specific literature be considered?

### v. Connection to the Initial Paper

The authors follow the procedures for proposed by Sun et al.[5], the first paper reviewed, for measuring textual similarity between duplicate bug reports. They also adopted the concept of "buckets" introduced in [5]. The current paper is an improvement on [4].

### vi. References

* [1]Hu, Diane J. "Latent dirichlet allocation for text, images, and music." University of California, San Diego. Retrieved April 26 (2009): 2013.
* [2]R. S. Pressman and W. S. Jawadekar, “Software engineering,” New York 1992, 1987.
* [3]M. L. Murphy, The Busy Coder’s Guide to Advanced Android Development. CommonsWare, LLC, 2009.
* [4]C. Sun, D. Lo, S. Khoo, and J. Jiang, “Towards more accurate retrieval of duplicate bug reports,” in Proceedings of the 2011 26th IEEE/ACM International Conference on Automated Software Engineering. IEEE Computer Society, 2011, pp. 253–262.
* [5]Anahita Alipour , Abram Hindle , Eleni Stroulia, A contextual approach towards more accurate duplicate bug report detection, Proceedings of the 10th Working Conference on Mining Software Repositories, May 18-19, 2013, San Francisco, CA, USA
