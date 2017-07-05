# Coding Summary

I used Python 3.6.1 for this coding challenge. In the Python scripts, I used sys, time, json, collections and math modules. All are built-in modules for Python.
There are 3 python files in the src directory. They are:

## graph.py

* [Graph()](README.md## Graph())
* [updateGraph()](README.md## updateGraph(graph, idx, data, trans))

## attribute.py

* [getNetworkTransactions()](README.md## getNetworkTransactions(graph, node, degree, trans))
* [insertPosition()](README.md## insertPosition(A, target))
* [mergeSort()](README.md## mergeSort(A, B, trans))
* [isValidSchema()](README.md## isValidSchema(data))
* [buildInitialState()](README.md## buildInitialState(graph, infile))
* [flagAnomalousPurchases()](README.md## flagAnomalousPurchases(g, streamFile, outputFile, idx, trans, degree))
* [getMeanAndStdev()](README.md## getMeanAndStdev(list))
* [isAnomalous()](README.md## isAnomalous(data, mean, sd))

## main.py

* [main()](README.md## main(args))

## Graph()

The Graph class is undirected. Inside the Graph class, there are 3 functions: addEdge(), removeEdge() and addNodeValue(). 

1. addEdge() takes 2 parameters: node1 and node2, it adds an edge between node1 and node2.

2. removeEdge() takes 2 parameters: node1 and node2, it removes an edge between node1 and node2.

3. addNodeValue() takes 5 parameters: idx, node, timeStamp, amount and trans. idx is the index for the record in the file, node is the node to be added values, timeStamp is the timestamp for the record, trans is the consecutive purchases, the values are order by timeStamp. 

In the addNodeValue() function, if a new record is coming for that node, check it with the latest timeStamp, if the timeStamp is newer, appends to the end of the node, otherwise uses the insertPosition() function to insert the record to the right place.

## updateGraph(graph, idx, data, trans)

This function takes 4 parameters: graph, idx, data and trans. It will update the `graph` based on event type of `data`. The code will crash if the event type is not among "purchase", "befriend", "unfriend".

## getNetworkTransactions(graph, node, degree, trans)

This function takes 4 parameters: graph, node, degree and trans. The function Breadth-first searches for all the nodes in the `graph` that are `degree` degrees in a social network of `node` (not including `node`). 
If the nodes is not empty, add it to networkNodes for further usage. Since the values stores in each node is sorted by timestamp ( see addNodeValue() function in the Graph class), I use merge sort algorithm to get the 
consecutive purchases made by a `node`'s social network. Finally, return None if there is less than 2 purchases in the social network, otherwise return a list of `trans` length or less.

## insertPosition(A, target)

This function takes 2 parameters: A and target. It return the position of which the value is greater than `target` and should be inserted in `A`.

## mergeSort(A, B, trans)

This function takes 3 parameters: A, B and trans. It merges `A` and `B` and return a list of `trans` length or less.

## isValidSchema(data)

The function takes one parameter: data. It checks the schema of data, the code will crash if the schema is not correct.


## buildInitialState(graph, infile)

This functions takes 2 parameters: graph and infile. It builds the initial state of the `graph` and return `degree`, `trans`, `idx`.

## flagAnomalousPurchases(g, streamFile, outputFile, idx, trans, degree)

This function takes 6 parameters: g, streamFile, outputFile, idx, trans and degree. It reads in `streamFile` and update `g`, flag anomalous purchases to `outputFile` bases on `idx, trans, degree`. It will proceed to new record
if current records cannot read in.

## getMeanAndStdev(list)

This function takes 1 parameters: list. It will return the `mean` and `sd` of the list in string format.

## isAnomalous(data, mean, sd)

This function takes 3 parameters: data, mean and sd. It will return boolean value if `data` is anomalous or not base on `mean` and `sd`.

## main(args)

This is the main function of the coding.

- It initializes the Graph.
- Builds the initial state of the Graph.
- flag anomalous purchases.