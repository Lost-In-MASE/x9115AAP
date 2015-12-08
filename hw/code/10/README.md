# IMPLEMENTATION OF GENETIC ALGORITHM
Aaditya Sriram (asriram4), Abhishek Ravi (aravi5), Parth Satra (pasatra)


## I. ABSTRACT

Genetic Algorithms and other closely related areas such as genetic programming, evolution strategies and evolutionary algorithms are subject of increasing amount of research interest. Genetic Algorithms (GA) are evolutionary algorithms which are used to solve search and optimisation problems. These algorithms are modeled after the genetic process of biological organisms where natural populations evolve according to the principles of natural selection and survival of the fittest [1]. This paper presents our implementation of GA, our understanding of the working principles of multi-objective evolutionary algorithms (MOEAs) and discusses results obtained when testing the performance of our algorithm as a MOEA.


## II. INTRODUCTION

GAs use a direct analogy to natural behaviour. They work with a population of “individuals”, each representing a possible solution to a given problem. Every individual has an associated “fitness score” which is a representation of how good a solution to the problem is. The fitness score is calculated by “fitness function”.  High fitness score signifies highly fit individuals. Such individuals are given opportunities to “reproduce” to produce new “offsprings”. These new individuals share some features taken from each “parent”. The least fit members of the population are less likely to get selected for reproduction and hence, eventually “die out”. Thus, a “generation” of new population is produced by selecting the best individuals from current generation and these new generation individuals contain a higher proportion of characteristics possessed by the good members of the previous generation. Through reproduction of highly fit individuals, good characteristics spread throughout the population, being mixed and exchanged with other good characteristics as they go. Mating of the more fit individuals ensures that the most promising areas of the search space is explored. As individuals of a population evolve over generations, they converge towards an optimal solution. GAs have a robust technique and can successfully deal with a wide range of problem areas. However, GAs are not guaranteed to find the globally optimum solution but they are good at finding a reasonably good solutions to problems, fairly quickly. 

Two processes that govern the quality of a GA are selection and reproduction processes. Selection refers to the process of selecting highly fit individuals from a population and considering them for reproducing new offsprings. A lot of work has gone over the past few decades in coming up with various strategies for selection. Some of the popular approaches are Tournament Selection, Proportional Roulette Wheel Selection, Rank-based Roulette Wheel Selection [2], Ranking Selection, Proportionate Reduction, and “Genitor” Selection [3]. We have chosen all-pair binary tournament selection as the strategy for selection process. Section III will discuss in greater detail on the selection strategy that is used in the experiments. During the reproductive phase of the GA, the individuals are selected from the population and recombined, producing offsprings that will belong to the next generation. Having selected two parents, their “chromosomes” are recombined using the techniques of Crossover and Mutation to produce the children. Section III provides a brief summary of the reproduction techniques used in our implementation of GA.

One of the important challenges of testing MOEAs is that the test problems are either too simple or too complicated. Deb, Kalyanmoy, et al. propose scalable test problems for evolutionary algorithms in [4]. We will be testing the performance of our implementation of GA on 20 repeats of DTLZ 1, 3, 5, 7 models proposed by Deb, Kalyanmoy, et al. in [4].

Apart from testing our algorithm on different models, we will be tuning our GA parameters using Differential Evolution to maximize the GA population hyper volume. The parameters that were tuned for performance were mutation probability, crossover probability and the population size.

The rest of the paper is organized as follows - Section III discusses the implementation details and some of the design choices made during the course of implementation. Section IV provides a summary of our interpretation of the results obtained when GA was tested against DTLZ 1, 3, 5, 7. Section V talks about the threats to the validity of our implementation while Section VI talks about our learnings from this implementation and our plans to better the algorithm. Section VII is references.


## III. THE PROCESS

We implemented the GA in python and it is largely based on the algorithm suggested by David Beasley et al. [1]. The pseudocode is given is Figure 1. It is possible that a potential solution to a problem may be represented as a set of parameters. This is true in terms of genetic terms as well. The set of parameters represented by a particular chromosome is referred to as genotype. Hence, every “individual” is represented with a set of decisions and the number of decisions is decided by the model we are trying to optimize. The DTLZ models are also designed in such a way that the number of decisions and objectives can be dynamically configured. The “BaseModel” class defines the general outline of a model which consists of member variables and methods. The “eval” method uses the objective functions of the model and returns a single numerical value that represents the “figure of merit” of a solution. This method is thus the fitness function for our GA. The fitness function is used to measure the fitness of an individual in the population and this is required by the selection procedure. Since the number of decisions and objectives are controlled by the BaseModel, our algorithm is thus generic enough to handle different decision and objective combination. 

![GA](https://github.com/Lost-In-MASE/x9115AAP/blob/master/hw/code/9/images/ga_basic.png)

The selection strategy addresses on which of the individuals in the current generation will be used to reproduce offspring in hopes that next generation will have even higher fitness. The selection operator is carefully formulated to ensure that highly fit individuals of the population have a greater probability of being selected for mating, but that worse members of the population still have a small probability of being selected. This is important to ensure that the search process is global and does not simply converge to the nearest local optimum. Tournament selection is probably the most popular selection method in genetic algorithm due to its efficiency and simple implementation [2][3]. In our algorithm we have used a flavor of tournament selection called the all-pair binary tournament selection to select individuals from the population to insert into a “mating pool”. In binary tournament, we select two individuals at random and compare the fitness scores using "boolean domination". Boolean domination considers an individual dominant if it is better on at least one objective but not worse for any other objectives. Such dominant individuals are placed in the mating pool. To ensure that the most dominant individual gets more share in reproduction process, we put every dominant individual as many times in the mating pool, as they dominate other individuals. Thus if an individual dominates ten other individuals, this individual will have ten clones in the mating pool. The drawback of this approach is that it requires n^2 comparisons and thus greatly affects the run time algorithm. We have also tried the approach of including dominant individuals only once in the mating pool and reduce the number of comparisons by trying to return from the inner "for" loop as quickly as possible. This approach has shown vastly improved run time with acceptable results.

![CROSSOVER](https://github.com/Lost-In-MASE/x9115AAP/blob/master/hw/code/9/images/crossover.png)

The reproductive phase of the GA is where individuals are selected from the population and recombined to produce offsprings which will form the next generation. Having selected two parents, their chromosomes are recombined using the mechanisms of crossover and mutation. For crossover, we use an approach called “single point crossover”. Here, we take two individuals and cut their decisions at some randomly chosen position, to produce two "head" segments and two "tail" segments. The tail segments are then swapped over to produce two new full length chromosomes, see Figure 2 for pictorial representation. The two offsprings each inherit some genes from each parent. Crossover is not applied to all pairs of individuals selected for mating. A random choice is made where the likelihood of crossover being applied is decided by a threshold 0.85. A typical value for threshold is between 0.6 and 1 [1]. If crossover is not applied, offsprings are produced simply by duplicating the parents. This gives each individual a chance of passing on its genes without the disruption of crossover. Mutation is applied to each child individually after crossover. Each decision of an individual is altered with a small probability of 0.05. The traditional view is that crossover is the more important of the two techniques for rapidly exploring a search space while mutation provides a small amount of random search that helps ensure that no point in the search space is left unexplored [1].

After a hundred generations our algorithm begins to monitor the progress of the population to determine the case of early termination. The population is given a bonus of another 100 generations but each time the population does not show an improvement, the number of generations left to reproduce reduces by 1. Thus if the population does not show any improvement, it can last for another 100 generations. However, if there is a difference of 0.5 or greater in the aggregated objective scores of all individuals, the population is given 10 more generations to progress.

Once the GA terminates, in order to evaluate the efficiency of the algorithm, we compute the hypervolume indicator. The population of the final generation is assumed to be the pareto frontier. We start comparing the candidates in this set with the rest of the population, that belong to previous generation. If the candidates of the final generation dominate the candidates of other generation, they are allowed to stay in the pareto frontier. But if the result is the other way around, then the candidates are replaced. If a pareto frontier individual is unable to dominate another randomly picked individual, then the latter is added to the pareto frontier. This way we build the pareto frontier required to evaluate our implementation. We also clean up the pareto frontier by making sure that there are no candidates in the pareto frontier that are dominated by other members of the frontier.

The hypervolume returned by GA is used to determine if one tuning of the GA parameters works better than another, we employ DE in this tuning process to modify the values of crossover probability, mutation probability and population size as we try to maximize the hyper volume. Once the DE terminates we use the new tuned parameters to generate our GA process, another call is made to GA with the default un tuned parameters. This is done for each combination for every model, that is we have 12 different runs for each model with varying number of decisions and objectives. Once this data is generated, as we did in code 9 and 10 we pass on the final era list of population to type 3 comparator to generate ranks for the runs. In this case higher the hyper volume the better, so we expect runs performing well to be on the right side of the median. 

## IV. RESULTS

How to compare Pareto sets lies at the heart of research in multi-objective optimization. A measure that has been the subject of much recent study in evolutionary multi-objective optimization is the Hypervolume Indicator (Hv). It measures the volume of the dominated portion of the objective space and is of exceptional interest. Thus we chose to report the efficiency of our algorithm in terms of Hv. For each model, decision and objective combination, the GA is run for 10 times and the hv for each of these runs is recorded. We finally compute the mean value for Hv and the standard deviation observed.

**DTLZ1**

|Objectives\Decisions|10|20|40|
|:---:|---|---|---|
|2|Mean = 0.995164<br/>SD = 0.000418|Mean = 0.995661<br/>SD = 0.001073|Mean = 0.997755<br/>SD = 0.000787|
|4|Mean = 0.995025<br/>SD = 1.11e-16|Mean = 0.995564<br/>SD = 0.000934|Mean = 0.997587<br/>SD = 0.000666|
|6|Mean = 0.995711<br/>SD = 0.001349|Mean = 0.995863<br/>SD = 0.001208|Mean = 0.997711<br/>SD = 0.001007|
|8|Mean = 0.995945<br/>SD = 0.001145|Mean = 0.996240<br/>SD = 0.001337|Mean = 0.997361<br/>SD = 0.000837|

**DTLZ3**

|Objectives\Decisions|10|20|40|
|:---:|---|---|---|
|2|Mean = 0.995025<br/>SD = 1.11e-16|Mean = 0.996175<br/>SD = 0.001117|Mean = 0.997354<br/>SD = 0.000697|
|4|Mean = 0.995274<br/>SD = 0.000746|Mean = 0.996454<br/>SD = 0.001165|Mean = 0.997760<br/>SD = 0.000924|
|6|Mean = 0.995204<br/>SD = 0.000434|Mean = 0.995374<br/>SD = 0.000726|Mean = 0.997244<br/>SD = 0.000547|
|8|Mean = 0.995522<br/>SD = 0.000995|Mean = 0.995786<br/>SD = 0.001068|Mean = 0.997604<br/>SD = 0.000650|

**DTLZ5**

|Objectives\Decisions|10|20|40|
|:---:|---|---|---|
|2|Mean = 0.995274<br/>SD = 0.000746|Mean = 0.995741<br/>SD = 0.000963|Mean = 0.997400<br/>SD = 0.000815|
|4|Mean = 0.995776<br/>SD = 0.001137|Mean = 0.995550<br/>SD = 0.000773|Mean = 0.997280<br/>SD = 0.000778|
|6|Mean = 0.995050<br/>SD = 7.46e-05|Mean = 0.996299<br/>SD = 0.001378|Mean = 0.997431<br/>SD = 0.000945|
|8|Mean = 0.995254<br/>SD = 0.000502|Mean = 0.995826<br/>SD = 0.001129|Mean = 0.997483<br/>SD = 0.000549|


## V. THREATS TO VALIDITY

Most optimisation algorithms use exploration and exploitation to find a globally optimal solution. Exploration refers to a technique used to investigate new and unknown areas in the search space, and exploitation refers to a technique that makes use of previously visited points to find better points. A good search algorithm must find a tradeoff between the two. A purely random search is good at exploration, where as a purely hillclimbing method is good at exploitation/ The combination of the two techniques is required to achieve a global optimal solution but it is very difficult to strike the best balance between the two. We have sometimes seen the problem of “slow convergence” on some models as well as the problem of “early convergence” on some other models as well. We found that by changing the mutation probability we could control the convergence rate. In our algorithm, the mutation rate is a constant throughout the run of the program and the rate is independent of the kind of distribution and how well the search is progressing.

We use “boolean domination”, or commonly known as bdom,  when comparing the individuals of a population. It is possible that sometimes a generation can contain individuals that do not dominate any other individual. In such a scenario it is hard to select fittest individuals in the population.

Aggregation methods combine the objectives into a scalar function that is used for fitness calculation. On the other hand, defining the goal function in this way requires profound domain knowledge that is often not available. We have used a pure aggregation method which is a sum of all the objective scores. This may not be the best aggregation in every case.


## VI. CONCLUSION & FUTURE WORK

Implementing the Genetic Algorithm has given us deep insights into general properties and characteristics Multi-objective evolutionary algorithms. Through this activity we have been introduced to various research surrounding this topic. We have also become aware of the common challenges faced during the implementation and debugging phases and have been able to learn about the ways to overcome these challenges. Our algorithm is a humble attempt to implement the popular MOEA, Genetic Algorithm. There are quite a few improvements that we plan to do on top of our current work. Some of them are discussed below.

We mentioned about the problems of slow convergence and early convergence in the previous section. [1][2][5] papers suggest that mutation probability must depend on an attribute called “Selection Pressure”. The selection pressure is determined by how much the search has been progressed. For example, in the early stages of GA, the pressure to find the fittest individuals is not very high, hence we can afford to mutate more in order to explore the search space. But if we have spent enough time exploring and haven't really gotten anywhere, then the pressure is high to find fittest candidates. We will thus refrain from mutation and exploration. This is something that we plan to add to our algorithm.

Since boolean domination has its own drawbacks (as discussed previously), we plan to integrate continuous domination as a part of the select procedure. We also to improve the aggregation method by trying out different strategies such as weighted-sum approach and target vector optimization[5]. There also a lot of improvement to be done in improving the time taken for the selection procedure by applying some heuristics to the process.

## VII. REFERENCES
* [1] Beasley, David, R. R. Martin, and D. R. Bull. "An overview of genetic algorithms: Part 1. Fundamentals." University computing 15 (1993): 58-58.
* [2] Noraini, Mohd Razali, and John Geraghty. "Genetic algorithm performance with different selection strategies in solving TSP." (2011).
* [3] Goldberg, David E., and Kalyanmoy Deb. "A comparative analysis of selection schemes used in genetic algorithms." Foundations of genetic algorithms 1 (1991): 69-93.
* [4] Deb, Kalyanmoy, Lothar Thiele, Marco Laumanns, and Eckart Zitzler. Scalable test problems for evolutionary multiobjective optimization. Springer London, 2005.
* [5] Zitzler, Eckart, and Lothar Thiele. "Multiobjective evolutionary algorithms: a comparative case study and the strength Pareto approach." evolutionary computation, IEEE transactions on 3.4 (1999): 257-271.


  rank ,         name ,    med   ,  iqr 
  ----------------------------------------------------
  1  , DTLZ7_40_6_untuned ,    1.09  ,  0.04 (-*             |              ), 1.09,  1.09,  1.12
  1  , DTLZ7_40_8_untuned ,    1.10  ,  0.04 (-*             |              ), 1.08,  1.10,  1.12
  2  , DTLZ7_40_4_untuned ,    1.13  ,  0.02 (  *            |              ), 1.12,  1.13,  1.14
  2  , DTLZ5_20_8_untuned ,    1.13  ,  0.00 (  *            |              ), 1.13,  1.13,  1.13
  3  , DTLZ3_10_6_untuned ,    1.15  ,  0.00 (   *           |              ), 1.15,  1.15,  1.15
  4  , DTLZ7_10_6_untuned ,    1.17  ,  0.01 (   *           |              ), 1.16,  1.17,  1.17
  4  , DTLZ1_10_6_untuned ,    1.17  ,  0.00 (    *          |              ), 1.17,  1.17,  1.17
  4  , DTLZ7_10_8_untuned ,    1.17  ,  0.03 (   -*          |              ), 1.17,  1.17,  1.19
  4  , DTLZ7_10_4_untuned ,    1.17  ,  0.03 (   -*          |              ), 1.16,  1.17,  1.19
  4  , DTLZ3_10_4_untuned ,    1.18  ,  0.00 (    *          |              ), 1.18,  1.18,  1.18
  5  , DTLZ1_10_8_untuned ,    1.20  ,  0.00 (     *         |              ), 1.20,  1.20,  1.20
  5  , DTLZ3_10_6_tuned   ,    1.20  ,  0.00 (     *         |              ), 1.20,  1.20,  1.20
  5  , DTLZ3_10_2_untuned ,    1.20  ,  0.00 (     *         |              ), 1.20,  1.20,  1.20
  5  , DTLZ7_40_2_untuned ,    1.20  ,  0.03 (    -*         |              ), 1.19,  1.20,  1.22
  5  , DTLZ3_20_2_untuned ,    1.20  ,  0.00 (     *         |              ), 1.20,  1.20,  1.20
  5  , DTLZ3_10_4_tuned   ,    1.21  ,  0.00 (     *         |              ), 1.21,  1.21,  1.21
  5  , DTLZ3_40_2_untuned ,    1.21  ,  0.00 (     *         |              ), 1.21,  1.21,  1.21
  5  , DTLZ3_10_8_untuned ,    1.21  ,  0.00 (     *         |              ), 1.21,  1.21,  1.21
  5  , DTLZ3_40_8_untuned ,    1.21  ,  0.00 (     *         |              ), 1.21,  1.21,  1.21
  5  , DTLZ7_10_4_tuned   ,    1.22  ,  0.02 (     *         |              ), 1.21,  1.22,  1.23
  5  , DTLZ3_20_4_untuned ,    1.22  ,  0.00 (     *         |              ), 1.22,  1.22,  1.22
  5  , DTLZ1_10_6_tuned   ,    1.22  ,  0.00 (     *         |              ), 1.22,  1.22,  1.22
  5  , DTLZ3_20_8_untuned ,    1.22  ,  0.00 (     *         |              ), 1.22,  1.22,  1.22
  5  , DTLZ7_10_8_tuned   ,    1.23  ,  0.02 (     -*        |              ), 1.21,  1.23,  1.23
  5  , DTLZ7_10_6_tuned   ,    1.23  ,  0.02 (     -*        |              ), 1.21,  1.23,  1.23
  5  , DTLZ1_20_2_untuned ,    1.23  ,  0.00 (      *        |              ), 1.23,  1.23,  1.23
  5  , DTLZ3_40_6_untuned ,    1.23  ,  0.00 (      *        |              ), 1.23,  1.23,  1.23
  5  , DTLZ3_10_8_tuned   ,    1.23  ,  0.00 (      *        |              ), 1.23,  1.23,  1.23
  5  , DTLZ1_10_8_tuned   ,    1.23  ,  0.00 (      *        |              ), 1.23,  1.23,  1.23
  5  , DTLZ7_20_8_untuned ,    1.23  ,  0.02 (     -*        |              ), 1.21,  1.23,  1.23
  5  , DTLZ3_10_2_tuned   ,    1.23  ,  0.00 (      *        |              ), 1.23,  1.23,  1.23
  5  , DTLZ7_20_4_untuned ,    1.23  ,  0.09 (     -*--      |              ), 1.22,  1.23,  1.31
  5  , DTLZ1_10_2_untuned ,    1.23  ,  0.00 (      *        |              ), 1.23,  1.23,  1.23
  5  , DTLZ1_10_4_untuned ,    1.23  ,  0.00 (      *        |              ), 1.23,  1.23,  1.23
  5  , DTLZ5_10_2_untuned ,    1.24  ,  0.00 (      *        |              ), 1.24,  1.24,  1.24
  5  , DTLZ5_10_4_untuned ,    1.24  ,  0.00 (      *        |              ), 1.24,  1.24,  1.24
  5  , DTLZ1_40_8_untuned ,    1.24  ,  0.00 (      *        |              ), 1.24,  1.24,  1.24
  5  , DTLZ1_40_4_untuned ,    1.24  ,  0.00 (      *        |              ), 1.24,  1.24,  1.24
  5  , DTLZ3_20_6_untuned ,    1.25  ,  0.00 (      *        |              ), 1.25,  1.25,  1.25
  5  , DTLZ1_20_4_untuned ,    1.25  ,  0.00 (      *        |              ), 1.25,  1.25,  1.25
  5  , DTLZ5_40_6_untuned ,    1.25  ,  0.00 (      *        |              ), 1.25,  1.25,  1.25
  5  , DTLZ1_20_6_untuned ,    1.25  ,  0.00 (       *       |              ), 1.25,  1.25,  1.25
  5  , DTLZ1_10_4_tuned   ,    1.25  ,  0.00 (       *       |              ), 1.25,  1.25,  1.25
  5  , DTLZ1_40_2_untuned ,    1.25  ,  0.00 (       *       |              ), 1.25,  1.25,  1.25
  5  , DTLZ7_20_6_untuned ,    1.26  ,  0.05 (     --*       |              ), 1.21,  1.26,  1.26
  5  , DTLZ7_10_2_untuned ,    1.26  ,  0.03 (      -*       |              ), 1.23,  1.26,  1.26
  5  , DTLZ1_10_2_tuned   ,    1.26  ,  0.00 (       *       |              ), 1.26,  1.26,  1.26
  5  , DTLZ5_10_4_tuned   ,    1.27  ,  0.00 (       *       |              ), 1.27,  1.27,  1.27
  5  , DTLZ5_40_8_untuned ,    1.27  ,  0.00 (       *       |              ), 1.27,  1.27,  1.27
  5  , DTLZ5_20_6_untuned ,    1.27  ,  0.00 (       *       |              ), 1.27,  1.27,  1.27
  5  , DTLZ7_10_2_tuned   ,    1.27  ,  0.00 (       *       |              ), 1.27,  1.27,  1.27
  5  , DTLZ1_40_6_untuned ,    1.28  ,  0.00 (       *       |              ), 1.28,  1.28,  1.28
  5  , DTLZ3_40_4_untuned ,    1.28  ,  0.00 (       *       |              ), 1.28,  1.28,  1.28
  5  , DTLZ1_20_8_untuned ,    1.28  ,  0.00 (        *      |              ), 1.28,  1.28,  1.28
  5  , DTLZ5_40_4_untuned ,    1.28  ,  0.00 (        *      |              ), 1.28,  1.28,  1.28
  5  , DTLZ5_10_2_tuned   ,    1.28  ,  0.00 (        *      |              ), 1.28,  1.28,  1.28
  5  , DTLZ5_10_6_untuned ,    1.29  ,  0.00 (        *      |              ), 1.29,  1.29,  1.29
  5  , DTLZ5_40_2_untuned ,    1.30  ,  0.00 (        *      |              ), 1.30,  1.30,  1.30
  6  , DTLZ7_20_2_untuned ,    1.31  ,  0.06 (         *-    |              ), 1.31,  1.31,  1.37
  6  , DTLZ5_10_8_untuned ,    1.31  ,  0.00 (         *     |              ), 1.31,  1.31,  1.31
  7  , DTLZ5_20_4_untuned ,    1.33  ,  0.00 (          *    |              ), 1.33,  1.33,  1.33
  7  , DTLZ5_10_8_tuned   ,    1.34  ,  0.00 (          *    |              ), 1.34,  1.34,  1.34
  7  , DTLZ5_10_6_tuned   ,    1.35  ,  0.00 (          *    |              ), 1.35,  1.35,  1.35
  7  , DTLZ3_20_2_tuned   ,    1.35  ,  0.00 (          *    |              ), 1.35,  1.35,  1.35
  7  , DTLZ3_20_4_tuned   ,    1.35  ,  0.00 (          *    |              ), 1.35,  1.35,  1.35
  8  , DTLZ5_20_2_untuned ,    1.38  ,  0.00 (           *   |              ), 1.38,  1.38,  1.38
  8  , DTLZ1_20_4_tuned   ,    1.38  ,  0.00 (            *  |              ), 1.38,  1.38,  1.38
  8  , DTLZ1_20_2_tuned   ,    1.39  ,  0.00 (            *  |              ), 1.39,  1.39,  1.39
  8  , DTLZ3_20_8_tuned   ,    1.39  ,  0.00 (            *  |              ), 1.39,  1.39,  1.39
  8  , DTLZ3_20_6_tuned   ,    1.40  ,  0.00 (            *  |              ), 1.40,  1.40,  1.40
  9  , DTLZ1_20_6_tuned   ,    1.41  ,  0.00 (             * |              ), 1.41,  1.41,  1.41
  10 , DTLZ5_20_8_tuned   ,    1.42  ,  0.00 (             * |              ), 1.42,  1.42,  1.42
  11 , DTLZ1_20_8_tuned   ,    1.45  ,  0.00 (              *|              ), 1.45,  1.45,  1.45
  12 , DTLZ7_20_6_tuned   ,    1.46  ,  0.04 (              -*              ), 1.44,  1.46,  1.48
  13 , DTLZ7_20_4_tuned   ,    1.47  ,  0.04 (              -*              ), 1.44,  1.47,  1.49
  13 , DTLZ7_20_8_tuned   ,    1.48  ,  0.03 (               *              ), 1.47,  1.48,  1.50
  14 , DTLZ1_40_8_tuned   ,    1.50  ,  0.00 (               |*             ), 1.50,  1.50,  1.50
  15 , DTLZ3_40_8_tuned   ,    1.51  ,  0.00 (               |*             ), 1.51,  1.51,  1.51
  16 , DTLZ3_40_4_tuned   ,    1.52  ,  0.00 (               | *            ), 1.52,  1.52,  1.52
  16 , DTLZ3_40_6_tuned   ,    1.53  ,  0.00 (               | *            ), 1.53,  1.53,  1.53
  16 , DTLZ3_40_2_tuned   ,    1.53  ,  0.00 (               | *            ), 1.53,  1.53,  1.53
  17 , DTLZ7_40_8_tuned   ,    1.55  ,  0.08 (               | -*-          ), 1.53,  1.55,  1.60
  17 , DTLZ1_40_2_tuned   ,    1.56  ,  0.00 (               |  *           ), 1.56,  1.56,  1.56
  17 , DTLZ5_20_6_tuned   ,    1.56  ,  0.00 (               |  *           ), 1.56,  1.56,  1.56
  17 , DTLZ1_40_4_tuned   ,    1.56  ,  0.00 (               |  *           ), 1.56,  1.56,  1.56
  18 , DTLZ1_40_6_tuned   ,    1.57  ,  0.00 (               |   *          ), 1.57,  1.57,  1.57
  19 , DTLZ5_20_4_tuned   ,    1.59  ,  0.00 (               |    *         ), 1.59,  1.59,  1.59
  20 , DTLZ5_20_2_tuned   ,    1.61  ,  0.00 (               |    *         ), 1.61,  1.61,  1.61
  20 , DTLZ7_40_6_tuned   ,    1.61  ,  0.07 (               |   -*-        ), 1.57,  1.61,  1.65
  21 , DTLZ7_20_2_tuned   ,    1.62  ,  0.03 (               |    -*        ), 1.60,  1.62,  1.63
  22 , DTLZ7_40_4_tuned   ,    1.70  ,  0.07 (               |      --*     ), 1.66,  1.70,  1.74
  23 , DTLZ5_40_6_tuned   ,    1.74  ,  0.00 (               |         *    ), 1.74,  1.74,  1.74
  23 , DTLZ5_40_8_tuned   ,    1.79  ,  0.00 (               |           *  ), 1.79,  1.79,  1.79
  24 , DTLZ5_40_4_tuned   ,    1.83  ,  0.00 (               |             *), 1.83,  1.83,  1.83
  24 , DTLZ7_40_2_tuned   ,    1.83  ,  0.05 (               |           --*), 1.80,  1.83,  1.85
  25 , DTLZ5_40_2_tuned   ,    1.85  ,  0.00 (               |             *), 1.85,  1.85,  1.85