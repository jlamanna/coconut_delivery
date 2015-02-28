## Coconut Delivery

A swallow has an assignment to deliver a coconut to a possibly-insane king. To save energy for the fight, the swallow will take advantage of jet streams that will lower his flying energy consumption. Before the flight, the delivery service gave the swallow an input file in the following format:

1. First line contains only 1 integer, which is the constant energy it takes to fly 1 mile WITHOUT jet streams.

2. Every subsequent line contains 3 space-separated integers: the start mile marker of the jet stream, the end mile marker of the jet stream, and lastly an integer denoting the overall energy needed to fly that jet stream’s distance.

For instance, the line “3 7 12″ means it takes 12 energy units to fly the 4 miles between mile-markers 3 and 7. Jet streams can overlap, but the swallow cannot be on more than one jet stream at a time, and it cannot fly partial jet streams.

For simplicity, consider the end mile marker of the farthest jet stream as the end of the flight.

Write a python program that takes in an input file [flight_paths](flight_paths.txt) to plan out the optimal sequence of jet streams the swallow should fly on to minimize his energy consumption throughout the entire flight. All integers in the input file are non-negative. As output, print out the mininum total energy and a list of tuples denoting the jet streams’ endpoints.

For example, given this [sample](sample_paths.txt), the minimum total energy needed to fly all 24 miles is 352 energy units, and the optimal sequence of jet streams is [(0,5), (6,11), (14,17), (19,24)].

---

### Solution Notes ###

The Coconut Delivery problem can be characterized as a single pair, shortest path problem on a directed, acyclic graph.
This problem can be solved in several different ways using graph algorithms. 
The current source contains an implementation using a simple BFS-like traversal and also using Dijkstra's algorithm.  
Another algorithm to solve this problem is A\*.

The program can be executed as follows:

	./coconut_delivery.py [paths file]

If "paths file" is omitted, the program will try to load flight\_paths in the
current directory.
