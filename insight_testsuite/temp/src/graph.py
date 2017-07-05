from collections import defaultdict

# Build the undirected graph data structure
class Graph(object):
    def __init__(self):
        self._connectedNode = defaultdict(set)
        self._nodeValue = defaultdict(list)

    def addEdge(self, node1,node2):
        #Add edge to graph
        self._connectedNode[node1].add(node2)
        self._connectedNode[node2].add(node1)

    def removeEdge(self, node1,node2):
        #Remove edge from graph
        self._connectedNode[node1].remove(node2)
        self._connectedNode[node2].remove(node1)

    def addNodeValue(self,idx, node,timeStamp,amount,trans):
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

# update graph for each category
def updateGraph(graph,idx,data,trans):
    if data["event_type"] == "purchase":
        graph.addNodeValue(idx, data["id"], data["timestamp"],float(data["amount"]),trans)
    elif data["event_type"]== "befriend":
        graph.addEdge(data["id1"],data["id2"])
    elif data["event_type"]== "unfriend":
        graph.removeEdge(data["id1"],data["id2"])
        # remove isolated nodes from the dictionary
        if not graph._connectedNode[data["id1"]]:
            del graph._connectedNode[data["id1"]]
        if not graph._connectedNode[data["id2"]]:
            del graph._connectedNode[data["id2"]]
    else:
        raise ValueError ("Category is not valid!")