import sys
import time
import json
from collections import defaultdict
from math import floor, sqrt

# Build the undirected graph data structure
class Graph(object):
    def __init__(self):
        self._connectedNode = defaultdict(set)
        self._nodeValue = defaultdict(list)

    def add_edge(self, node1,node2):
        #Add edge to graph
        self._connectedNode[node1].add(node2)
        self._connectedNode[node2].add(node1)

    def remove_edge(self, node1,node2):
        #Remove edge from graph
        self._connectedNode[node1].remove(node2)
        self._connectedNode[node2].remove(node1)

    def add_nodeValue(self,idx, node,timeStamp,amount,trans):
        # Add new purchase to a user, queue data structure
        # each field corresponds to index, timeStamp, amount, sorted by time and idx
        if len(self._nodeValue[node])==0 or timeStamp >= self._nodeValue[node][-1][1]:
            self._nodeValue[node].append((idx, timeStamp,amount))
        else:
            pos = insertPosition(self._nodeValue[node],((idx, timeStamp,amount)))
            self._nodeValue[node].insert(pos,(idx, timeStamp,amount))
        # Remove outdated purchase if there is over T purchases for a user
        while len(self._nodeValue[node]) > trans:
            # sort by timeStamp then index
            self._nodeValue[node].pop(0)


# Get the latest T purchases
def getNetworkTransactions(graph,node,degree,trans):
    # queue data structure to store nodes for each layer
    queue = set()
    queue.add(node)
    # network store all the nodes for D degree network excluding the user
    networkNodes = []
    # label the nodes that have been visited, Hashset data structure, o(1) for searching
    visited = set()
    visited.add(node)
    d = 0
    # BFS search for graph
    while d < degree:
        temp=set()
        while queue:
            currentNode = queue.pop()
            # get connected nodes for current node
            for n in graph._connectedNode[currentNode]:
                # check if visited or not
                if n not in visited:
                    visited.add(n)
                    temp.add(n)
                    # add the node if it is not empty
                    if len(graph._nodeValue[n])!=0:
                        networkNodes.append(n)
        queue = temp
        d+=1
    # store latest T purchase
    purchases = graph._nodeValue[networkNodes.pop()]
    for node in networkNodes:
        # get all purchases for D degree network
        purchases = mergeSort(purchases,graph._nodeValue[node],trans)

    length = len(purchases)
    if length < 2:
        return None
    else:
        return [k for i,j,k in purchases]

# binary search to get the inserted position, return the first position > target
def insertPosition(A, target):
    if len(A) == 0:
        return 0
    left, right = 0, len(A) - 1
    while left <= right:
        mid = int((left + right) / 2)
        if A[mid][1] <= target[1]:
            left = mid+1
        else:
            right = mid-1
    return left

# merge two sorted list,return trans largest number
def mergeSort(A,B,trans):
    m = len(A); n = len(B)
    tmp = [None for _ in range(m+n)]
    i = 0; j = 0; k = 0
    while i < m and j < n:
        if A[i][1] < B[j][1]:
            tmp[k] = A[i];i += 1
        elif B[j][1] < A[i][1]:
            tmp[k] = B[j];j += 1
        else:
            if A[i][0] < B[j][0]:
                tmp[k] = A[i];i += 1
            else:
                tmp[k] = B[j];j += 1
        k += 1
    if i == m:
        while k < m + n:
            tmp[k] = B[j]
            k += 1; j += 1
    else:
        while k < m + n:
            tmp[k] = A[i]
            k += 1; i += 1

    return tmp if m+n<=trans else tmp[m+n-trans:]

# check the schema of the data
def isValidSchema(data):
    if all(key in data for key in ["event_type","timestamp","id","amount"])\
    or all (key in data for key in ["event_type","timestamp","id1","id2"]):
        return True
    else:
        raise ValueError ("Invalid schema!")

# update graph for each category
def updateGraph(graph,idx,data,trans):
    if data["event_type"] == "purchase":
        graph.add_nodeValue(idx, data["id"], data["timestamp"],float(data["amount"]),trans)
    elif data["event_type"]== "befriend":
        graph.add_edge(data["id1"],data["id2"])
    elif data["event_type"]== "unfriend":
        graph.remove_edge(data["id1"],data["id2"])
        # remove isolated nodes from the dictionary
        if not graph._connectedNode[data["id1"]]:
            del graph._connectedNode[data["id1"]]
        if not graph._connectedNode[data["id2"]]:
            del graph._connectedNode[data["id2"]]
    else:
        raise ValueError ("Category is not valid!")


# read input file and build initial state
def buildInitialState(graph,infile):
    idx = 0
    # initialize D and T
    degree=None
    trans=None
    context = open(infile,"r").read()
    for item in context.strip().split("\n"):
        if item.strip():
            try:
                data=json.loads(item)
                if idx==0:
                    degree = int(data["D"])
                    trans = int(data["T"])
                else:
                    if isValidSchema(data):
                        updateGraph(graph,idx,data,trans)
                idx+=1
            except KeyError:
                continue

    return idx, degree, trans

# flag the anomalous purchases and store it in flagged_purchases.json
def flagAnomalousPurchases(g,streamFile,outputFile,idx,trans,degree):
    # open output file
    output = open(outputFile,"a")
    # open stream_log.json
    with open (streamFile,"r") as input:
        for item in input:
            if item.strip():
                try:
                    data=json.loads(item)
                    # check if the data is conformed to the schema
                    if isValidSchema(data):
                        # update the social network and purchase history of users
                        updateGraph(g,idx,data,trans)
                        idx+=1
                        # check the event type
                        if data["event_type"]=="purchase":
                            # return None if there are less 2 purchases
                            transHistory = getNetworkTransactions(g,data["id"],degree,trans)
                            if transHistory:
                                mean, sd = getMeanAndStdev(transHistory)
                                # check if the purchase is anomalous
                                if isAnomalous(data["amount"],mean,sd):
                                    #save flagged purchase
                                    string = '{"event_type": "%s", "timestamp": "%s", "id": "%s", "amount": "%s", "mean": "%s", "sd": "%s"}'\
                                    % (data["event_type"],data["timestamp"],data["id"],data["amount"],mean,sd)
                                    output.write(string+"\n")
                except KeyError:
                    # proceed next row if data cannot be read in
                    continue
    # close output file
    output.close()


# get mean and standard deviation for purchases
def getMeanAndStdev(list):
    if len(list)==0:
        raise ValueError ("Empty list!")
    m = sum(list)/float(len(list))
    mean = "{0:.2f}".format(floor(m * 100) / 100)
    sqDiff = [(x-float(mean))**2 for x in list]
    d = sqrt(sum(sqDiff)/len(list))
    sd = "{0:.2f}".format(floor(d * 100) / 100)
    return mean,sd

# criteria for anomalous, input is string format
def isAnomalous(data, mean, sd):
    return float(data) > float(mean)+3*float(sd)

# this is the main function
def main(args):
    # check if there is enough arguments
    if len(args)!=4:
        raise ValueError("Please provide input files and out file")
    startTime = time.time()
    inputFile = args[1]
    # initialize the network
    g = Graph()
    # get index, D and T from the batch_log.json
    idx, degree,trans = buildInitialState(g,inputFile)
    # check if degree meets requirement
    if degree < 1:
        raise ValueError ("Least degree is 1!")
    # check if transactions meets requirement
    if trans < 2:
        raise ValueError ("Least consecutive purchases is 2!")
    print ("The initial state took "+"{0:.5f}".format(time.time()-startTime)+" seconds")
    print ("read stream_log.json file and flag anomalous purchases")
    streamFile = args[2]
    outputFile = args[3]
    # flag the anomalous purchases and store it in flagged_purchases.json
    flagAnomalousPurchases(g,streamFile,outputFile,idx,trans,degree)

    print ("total execution took "+"{0:.5f}".format(time.time()-startTime)+" seconds")

if __name__ == "__main__":
    main(sys.argv)

