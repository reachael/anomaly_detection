# Coding Summary

I used Python 3.6.1 for this coding challenge. In the Python script, I used sys, time, json, collections and math modules. All are built-in modules for Python.
There are 1 class and 10 functions in the code. They are:

*Graph()
*getNetworkTransactions()
*insertPosition()
*mergeSort()
*isValidSchema()
*updateGraph()
*buildInitialState()
*flagAnomalousPurchases()
*getMeanAndStdev()
*isAnomalous()
*main()

### Graph()

The Graph class is undirected. Inside the Graph class, there are 3 functions: add_edge(), remove_edge() and addNodeValue(). 

1. add_edge() takes 2 parameters: node1 and node2, it adds an edge between node1 and node2.

2. remove_edge() takes 2 parameters: node1 and node2, it removes an edge between node1 and node2.

3. addNodeValue() takes 5 parameters: idx, node,timeStamp,amount and trans. idx is the index for the record in the file, node is the node to be added values, timeStamp is the timestamp for the record, trans is the consecutive purchases, the values are order by timeStamp. 

In the addNodeValue() function, if a new record is coming for that node, check it with the latest timeStamp, if the timeStamp is newer, appends to the end of the node, otherwise uses the insertPosition() function to insert the record to the right place.

### getNetworkTransactions()

This function takes 4 parameters: graph,node,degree and trans. The function Breadth-first searches for all the nodes in the **graph** that are **degree** degrees in a social network of **node** (not including **node**). 
If the nodes is not empty, add it to networkNodes for further usage. Since the values stores in each node is sorted by timestamp ( see addNodeValue() function in the Graph class), I use merge sort algorithm to get the 
consecutive purchases made by a **node**'s social network. Finally, return None if there is less than 2 purchases in the social network, otherwise return a list of **trans** length or less.

### insertPosition()


### mergeSort()
### isValidSchema()
### updateGraph()
### buildInitialState()
### flagAnomalousPurchases()
### getMeanAndStdev()
### isAnomalous()
### main()

