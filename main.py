from Graph import Graph
from GraphUtils import *
test = Graph("../test/edges.txt", "../test/clusters.txt")

print(test.create_our_weights(5))