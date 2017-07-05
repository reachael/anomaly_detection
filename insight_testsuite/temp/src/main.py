import sys
from attribute import *
from graph import *
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

    print ("The initial state took "+"{0:.5f}".format(time.time()-startTime)+" seconds")
    print ("read stream_log.json file and flag anomalous purchases")
    streamFile = args[2]
    outputFile = args[3]
    # flag the anomalous purchases and store it in flagged_purchases.json
    flagAnomalousPurchases(g,streamFile,outputFile,idx,trans,degree)

    print ("total execution took "+"{0:.5f}".format(time.time()-startTime)+" seconds")

if __name__ == "__main__":
    main(sys.argv)