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
Most optimization algorithms use exploration and exploitation to find a globally optimal solution. Exploration refers to a technique used to investigate new and unknown areas in the search space, and exploitation refers to a technique that makes use of previously visited points to find better points. A good search algorithm must find a tradeoff between the two. A purely random search is good at exploration, where as a purely hill climbing method is good at exploitation/ The combination of the two techniques is required to achieve a global optimal solution but it is very difficult to strike the best balance between the two.
### VI.	Results
![result_sk](https://github.com/Lost-In-MASE/x9115AAP/raw/master/hw/code/8/images/sn.PNG)

