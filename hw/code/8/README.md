## Comparators

### I.	Abstract
Dominance of one solution over another solution or a pool of solutions can be simply found by calculating the energy values and taking the one closest to heaven as the best solution. This sounds simple but what if we have to arrange solutions in a particular order and we have 1000’s of solutions? For each solution we generate we need to check if it is better than the existing solutions? We would end up comparing each solution quadratic number of times to the order of 2 or more. This literature talks about faster but less accurate ways to measure the dominance of a solution over others.
### II.	Background

#### Differential Evolution

Differential Evolution is a metaheuristic that does not guarantee an optimal solution but is fast enough to get acceptable solutions quickly. Differential Evolution starts with a frontier which it generates that contains a set of solutions that satisfy the constraints of the model being used in the optimizer. From this frontier we take each member of the population and choose two other and mutate them together to form a new valid solution, if the energy of this new solution is better than the older solution we replace the old item with the new one on the frontier.

#### Simulated Annealing

Simulated Annealing is a common method used for discrete solution spaces to find global maximum or minimum as the situation desires. Given a seed we randomly jump around the search space in search of a better solution, at each instant we try to find a better solution than the one at hand. With a small chance we also jump to suboptimal solutions this helps us get out of local maxima or local minima, we still keep track of the best solution we have till now. The probability of jumping to sub optimal solutions reduces with time, this is based on the cooling schedule, and the randomness reduces over time as we would have ideally covered most of the local optimal solutions in the initial random phase.

#### Max Walk Sat

Max Walk Sat is a local search algorithm that is simpler to understand than Simulated Annealing. It tries to improve the solution in one dimension at a time rather than jumping around as was the case in Simulated Annealing. What we try to achieve with Max Walk Sat is we fixate on one dimension and with some probability we jump around in search of newer dimensions. It can be seen as a method of observing the landscape and understanding it and then exploring solutions that fit the need.

### III.	Introduction
There are three main types of comparators that we will be talking about,
	Boolean Domination
	Continuous Domination
	Fast Era Assessment

More informally we have type1, type2 and type3 comparators. The type1 comparators can use either Boolean or continuous domination to establish a stand. Type1 comparators are what are at the heart of each optimizer that we use, in this case simulated annealing, max walk sat and differential evolution. Every time we generate a new solution, we use type 1 comparator to decide if this new solution should replace the existing solution. The important point to note here is that binary domination although easier to understand and implement will only work well for 2 objectives, if you have more than 2 objectives then continuous domination is a good option to consider. The type1 comparator is the most used comparator in our optimization algorithms simply because it runs for each generated solution. The Boolean comparator gives a simple yes or no solution rather than giving a degree of domination by one solution over another.

Type2 comparator is run every time we have 2 comparable eras, it is a step that can help us terminate our optimizer earlier that it would have normally by checking if enough has improved from one era to the other. Often if the change is not evident between two era’s we can be confident that the improvement that we are gaining out of it is not worth the effort we have to put in, the type2 comparator helps us with this early termination. It takes into account candidates from 2 consecutive eras and checks if the change between the two is substantial enough to warrant another era, the optimizer runs as long as the number of eras count is greater than 0. For each type2 comparison between eras, if the difference between two eras is less than a certain percentage we reduce the number of remaining eras otherwise we add few more eras indicating belief in the optimizer to be able to yield much better results given more time. The type 2 comparator we use implements the Krall’s B Stop method to find how the number of eras should be incremented or decremented and A12 is adapted from Vargha and Delaney’s A12 statistic. From the same statistic we get the idea that if the difference between two consecutive eras is less than 56% we can claim it is not significantly different.

Type 3 comparator is run just once at the end of the program and is more of a ranking algorithm that rates the finals eras that are created by each of the optimizers. Ideally different seeds are used and each algorithm is run multiple times to ensure that luck wasn’t a factor that rated one optimizer over another, with a larger dataset we can see if any optimizer consistently performs better than the other optimizers. We try to find similarities in eras and discard them and use the actual differences and use them to rank one run over another.

### IV.	The Process

Over the course of the semester we implemented various optimizers and models, the process here implements the three comparators that were introduced in the previous section. Type 1 comparator is used in place of comparing energy values to decide which of given solutions is better, internally the type 1 comparator uses continuous domination to arrive at a decision given two solutions, since this problem uses DTLZ with 10 decision and 2 objective, Boolean domination could have been used as well. When we have more than 2 objectives though, Continuous Domination is a better option. We use the type 1 comparator for each of the optimizers (Simulated Annealing, Max Walk Sat and Differential Evolution), this is implemented in the base model so we don’t have to re implement it for other models. After each new candidate is generated we add the candidate to the current era and when the size of the current era reaches 100 (10 times the number of decisions) we compare it with the previous era using a12, if the difference between the two eras as returned by a12 is greater than 0.56 we add 5 to the number of eras left to calculate else we reduce the count by 1. Our options for terminating the optimizer are either the current best value reaching the threshold (0 for minimization and 1 for maximization) or early termination by virtue of number of eras reaching 0 or running out of max tries.

We run the above steps for all 3 optimizers using the DTLZ model and the optimizers return the last computed era. We run each of the optimizers 20 times to generate a list of eras and we label them with a label specifying the corresponding optimizer. This list of list of solutions is then sent to rdiv which is part of the sk.py library and we get a ranking of the optimizer’s performance over the 20 runs each.

### V.	THREATS TO VALIDITY
Most optimization algorithms use exploration and exploitation to find a globally optimal solution. Exploration refers to a technique used to investigate new and unknown areas in the search space, and exploitation refers to a technique that makes use of previously visited points to find better points. A good search algorithm must find a tradeoff between the two. A purely random search is good at exploration, where as a purely hill climbing method is good at exploitation/ The combination of the two techniques is required to achieve a global optimal solution but it is very difficult to strike the best balance between the two. Early termination may hamper the process of finding optimal solutions, but it is a trade off between speed and accuracy that has to be made.

### VI.	Results

##### Early Terminations

|Optimizer|Early Terminations|
|:-:|:-:|
|DE|15|
|SA|9|
|MWS|3|

##### This data is not normalized for energy values

	rank ,         name ,    med   ,  iqr 
	----------------------------------------------------
   	1 ,         DE16 ,    6.34  ,  0.92 (*-             |              ), 6.34,  6.34,  7.26
   	1 ,          DE5 ,    6.85  ,  0.36 ( -*            |              ), 6.49,  6.85,  6.85
   	2 ,          DE9 ,    7.07  ,  0.37 (  *            |              ), 7.07,  7.07,  7.45
   	2 ,         DE20 ,    7.22  ,  1.24 (  *--          |              ), 7.22,  7.22,  8.46
   	2 ,         DE15 ,    7.22  ,  0.31 (  *            |              ), 7.04,  7.22,  7.35
   	2 ,          DE4 ,    7.28  ,  0.77 (  *            |              ), 6.95,  7.28,  7.72
   	2 ,         DE14 ,    7.43  ,  0.34 (  -*           |              ), 7.17,  7.43,  7.51
   	3 ,          DE8 ,    7.51  ,  0.25 (   *           |              ), 7.51,  7.51,  7.76
   	3 ,          DE2 ,    7.57  ,  0.15 (   *           |              ), 7.48,  7.57,  7.63
   	4 ,          DE1 ,    7.67  ,  0.07 (   *           |              ), 7.67,  7.67,  7.74
   	5 ,          DE7 ,    7.88  ,  0.19 (    *          |              ), 7.88,  7.88,  8.06
   	6 ,         DE19 ,    8.10  ,  0.22 (    *          |              ), 8.10,  8.10,  8.32
   	6 ,         DE11 ,    8.17  ,  0.73 (   -*          |              ), 7.71,  8.17,  8.44
   	6 ,          DE6 ,    8.23  ,  0.20 (    -*         |              ), 8.09,  8.23,  8.28
   	6 ,         DE10 ,    8.28  ,  0.47 (    -*         |              ), 7.93,  8.28,  8.40
   	7 ,         DE18 ,    8.51  ,  0.11 (     *         |              ), 8.40,  8.51,  8.51
   	7 ,          DE3 ,    8.51  ,  0.12 (     *         |              ), 8.51,  8.51,  8.63
   	8 ,         DE13 ,    8.75  ,  0.26 (     -*        |              ), 8.56,  8.75,  8.82
   	8 ,         DE12 ,    8.90  ,  0.76 (    --*        |              ), 8.23,  8.90,  8.98
   	9 ,         DE17 ,    9.32  ,  0.23 (      -*       |              ), 9.12,  9.32,  9.35
  	10 ,          SA6 ,    12.47  ,  1.67 (            -*-|              ), 11.97,  12.47,  13.63
  	10 ,          SA3 ,    12.60  ,  2.07 (            --*|              ), 11.83,  12.60,  13.90
  	10 ,          SA5 ,    12.72  ,  2.41 (            --*|-             ), 11.63,  12.72,  14.04
  	10 ,         SA14 ,    12.74  ,  2.13 (            --*|              ), 11.72,  12.74,  13.86
  	10 ,          SA7 ,    12.75  ,  2.31 (           ---*|              ), 11.47,  12.75,  13.78
  	10 ,         SA18 ,    12.80  ,  2.17 (            --*|              ), 11.72,  12.80,  13.89
  	10 ,         SA15 ,    12.82  ,  2.26 (            --*|-             ), 11.84,  12.82,  14.10
  	10 ,         SA10 ,    12.86  ,  2.21 (            --*|-             ), 11.90,  12.86,  14.11
  	10 ,         SA16 ,    12.87  ,  2.43 (            --*|-             ), 11.71,  12.87,  14.14
  	10 ,          SA2 ,    12.90  ,  2.22 (            --*|-             ), 11.86,  12.90,  14.08
  	10 ,          SA9 ,    12.98  ,  2.23 (             --*-             ), 12.04,  12.98,  14.27
  	10 ,          SA1 ,    12.98  ,  2.51 (            ---*-             ), 11.84,  12.98,  14.35
  	10 ,         SA20 ,    13.02  ,  2.66 (           ----*-             ), 11.52,  13.02,  14.17
  	10 ,         SA17 ,    13.03  ,  2.36 (            ---*-             ), 11.70,  13.03,  14.06
  	10 ,          SA8 ,    13.06  ,  2.47 (            ---*-             ), 11.59,  13.06,  14.06
  	10 ,         SA19 ,    13.11  ,  2.40 (           ----*              ), 11.50,  13.11,  13.90
  	10 ,         SA11 ,    13.15  ,  2.78 (           ----*-             ), 11.50,  13.15,  14.28
  	10 ,         SA13 ,    13.17  ,  2.27 (            ---*-             ), 11.87,  13.17,  14.14
  	10 ,         SA12 ,    13.26  ,  1.98 (             --*-             ), 12.13,  13.26,  14.11
  	10 ,          SA4 ,    13.30  ,  2.01 (             --*-             ), 12.13,  13.30,  14.14
  	11 ,        MWS15 ,    15.87  ,  2.07 (               |   --*-       ), 14.98,  15.90,  17.04
  	11 ,         MWS2 ,    15.89  ,  2.10 (               |   --*-       ), 14.86,  15.90,  16.96
  	11 ,         MWS4 ,    15.92  ,  1.99 (               |   --*--      ), 15.23,  15.94,  17.22
  	11 ,        MWS18 ,    15.97  ,  2.56 (               |  ---*--      ), 14.80,  15.99,  17.36
  	11 ,        MWS19 ,    16.00  ,  1.61 (               |   --*-       ), 15.25,  16.02,  16.86
  	11 ,         MWS5 ,    16.05  ,  2.32 (               |  ---*-       ), 14.84,  16.08,  17.16
  	11 ,        MWS10 ,    16.07  ,  2.10 (               |   --*-       ), 14.97,  16.08,  17.07
  	11 ,        MWS20 ,    16.10  ,  2.50 (               |   --*--      ), 14.93,  16.10,  17.43
  	11 ,         MWS8 ,    16.11  ,  1.72 (               |   --*-       ), 15.31,  16.11,  17.03
  	11 ,        MWS11 ,    16.17  ,  2.07 (               |   --*-       ), 15.11,  16.18,  17.19
  	11 ,        MWS16 ,    16.18  ,  2.29 (               |   --*-       ), 14.89,  16.19,  17.18
  	11 ,        MWS12 ,    16.26  ,  2.47 (               |   --*--      ), 15.11,  16.26,  17.58
  	11 ,         MWS3 ,    16.26  ,  2.39 (               |   ---*-      ), 14.93,  16.28,  17.33
  	11 ,         MWS7 ,    16.30  ,  2.11 (               |   ---*-      ), 15.24,  16.30,  17.35
  	11 ,         MWS6 ,    16.30  ,  1.96 (               |   ---*       ), 15.06,  16.30,  17.02
  	12 ,        MWS17 ,    16.40  ,  2.54 (               |   ---*-      ), 15.12,  16.41,  17.66
  	12 ,        MWS14 ,    16.46  ,  2.27 (               |   ---*-      ), 14.96,  16.50,  17.23
  	12 ,         MWS1 ,    16.46  ,  2.28 (               |   ---*-      ), 15.09,  16.47,  17.37
  	12 ,        MWS13 ,    16.57  ,  2.22 (               |    --*-      ), 15.40,  16.58,  17.62
  	12 ,         MWS9 ,    16.68  ,  2.31 (               |   ---*-      ), 15.17,  16.71,  17.48

### VII. Future Work

If the code ran any faster we could run this over all the models and optimizers we have implemented throughout the course and compare all results to see how well one optimizer for a specific model stacks up against the other options. It was observed a few times that the normalization produced values larger than 1 or less than 0 very early in the exploration phase, this led to premature termination, the one workaround for this was to run the code multiple times and hoping we get enough data before a threshold is breached. There should be a better baseline method that is more fault tolerant or can dynamically change bounds based on how long the optimizer has run.