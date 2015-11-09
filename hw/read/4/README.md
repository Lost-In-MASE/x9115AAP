### i. Paper Reviewed
Nicolas Bettenburg, Rahul Premraj, Thomas Zimmermann and Sunghun Kim; “Duplicate Bug Reports Considered Harmful ... Really?” in Software Maintenance, 2008. ICSM 2008

###ii. Keywords and Definitions  
* **ii1. Master Report:** This is a bug database that of the original bug reports. These are considered to be the bugs that didn't have any duplicates at the time they were created. This report normally should have the complete information about the bug being reported. But according to the survey in the paper many a times a lot of information from the duplicates also helps the developers. 

* **ii2. Extended Master Report:** The paper suggests a new method of dealing with duplicates. Normally the duplicates are detected and marked as closed. In this paper the authors have conducted survey of the open source projects and have concluded the many a times the duplicates also have some important imformation that helps developers to solve the bug faster. Hence along with the master report database, the system maintains additional extended master report for the detected duplicates and stores information in them that is not present in the master report. 

* **ii3. Information items:** Bugs have different information available such as stacktraces, , product, component, screenshots, attachments and so on. Information items is a quantitaive measure of value added by each of these information field. This information is finally used to check if the bug duplicate provides any additional information.

* **ii4. Natural Language Processing:** Detecting if the bug is a duplicate is itself very challenging. To do this the paper uses the technique of natural language proessing. Natural language processing is very similar to text mining. In this process the complete bug report which includes fields like title, description, steps to recreate and summary are all compared to newly reported bug and then if a certain amount of similarities are found then the 2 bugs are declared duplicate.

### iii. Brief notes 

#####iii1. Motivation
The common understanding in duplicate bug detection is to detect the duplicate bug and then to discard it. This mainly helps the developers to not waste time in dealing with bugs that they are already aware of. This paper on the other hand proposes that the duplicate bugs do help in providing additional information that might not be present in the original report. This will totally change the approach towards duplicate bugs and this information can then be used to improve the accuracy of the triaging as well. Thus, this paper aims at analyzing this information providing the findings and improvement in the bug detection algorithm accuracy. This paper compares machine learning algorithms like SVM and Bayes Net.  

#####iii2. Hypotheses
All the prior literature work assumed that the duplicate bugs are the same as original and discarded them. With the change in the approach now, the dublicates are also important and its also important to quantify the additional information provided by the duplicates. This quantifies information can then be used to improve the accuracy of detecting the new duplicates since now we have more information in complement to the original bug. Thus duplicate bug detection also adds more value in providing addtional information.

#####iii3. Data
The data for this paper is taken from bug database of the ECLIPSE Project. This is freely available as an XML export on the MSR Mining Challenge 2008. The database contains a 211843 bug reports from October 2001 to December 2007. Out of these total number of bugs, 16511 were unique bugs and 27838 were duplicate reports. The bugs had title, description, component, product, priority, affected version, operating system and target milestone. The reports can also provide screenshots, attachments and stacktraces. 


#####iii4. Future Work
The paper is based on the assumption that the information gained from the duplicate bugs always adds povitively to the original bug. However it is possible in practical sense that the additional information might be misleading and might lead to a wrong developer. Hence identifying the information to be positively influential or negatively influential will improve the accuracy even further. 

### iv. Improvements  
* iv1. One of the key assumptions made in the paper is that the additional information found in the duplicate bugs always positively helps in finding the right developer and helping in solving the problem. However it is possible that the information can be misleading and thus it is important to be able to identify whether the information positively impacts the original bug. This will improve the accuracy of prediction as well. 

* iv2. The paper only experiments with ECLIPSE data. Even though the data contains bugs from multiple sub-projects it might not be sufficient to generalize the results to other projects either open-source or closed projects. Hence the experiment should be done on multiple projects from different domains to get a better understanding of the results. 

* iv3. Here a lot of fields were available as information items for the duplicate bugs. Normally not all the bugs have so many fields. In such cases what will be the performance of this proposed technique. It would be great if authors provide more insights into what happens when there are varying number of fields available. 

### v. Connection to the Initial Paper
The previously reviewed paper [1] was build on one of the key concept proposed in this paper. This paper proposes that the duplicate bugs also provide additional information useful to developers in solving the issues. Hence the duplicates should not be discarded after detecting them but instead should be used to complement the information and use them to improve the accuracy. Hence the previously reviewed paper maintains a master list of unique bugs and attaches a secondary list of duplicate bugs to each master list record. This structure is then used to complement the information and increase the accuracy. 

### vi. References
* [1] C. Sun, D. Lo, S.-C. Khoo, and J. Jiang, “Towards more accurate retrieval of duplicate bug reports,” in Proceedings of the IEEE/ACM International Conference on Automated Software Engineering, 2011.