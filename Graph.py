import numpy as np

class Graph:
    def __init__(self, edges_file, cluster_file):
        self.adj_mat = []
        self.adj_set = {}
        self.cluster_list = []
        self.cluster_file = cluster_file
        self.edges_file = edges_file
        self.create_adjacency_set_and_mat(edges_file, cluster_file)

    class Node:
        def __init__(self, name):
            self.name = name
            self.num_of_neighbors = 0
            self.neighbors_set = set()
            self.idx = 0

    class Cluster:
        def __init__(self, cluster_number, num_of_members, members_set, cluster_neighbors):
            self.cluster_number = 0
            self.num_of_members = 0
            self.members_set = set()
            self.cluster_neighbors = set()

    # Creates a set of <Node> with the node's neighbors set
    def create_adjacency_set_and_mat(self, edges_file, cluster_file):
        temp_node_dict = {}
        temp_node_list = []
        temp_adj_mat = []
        with open(cluster_file, 'r') as node_file:
            for line in node_file:
                node_name = line.split()[0]
                temp_node_list.append(node_name)
                temp_node_dict[node_name] = self.Node(node_name)
        node_file.close()

        # Add index in the adjacency matrix for each node and create adj_mat with everything disconnected
        temp_node_list = sorted(temp_node_list)
        for node in temp_node_dict.values():
            node.idx = temp_node_list.index(node.name)
            temp_adj_mat.append([0 for i in range(len(temp_node_list))])

        with open(edges_file, 'r') as edges_file:
            for line in edges_file:
                splitted_line = line.split()
                node_name = splitted_line[0]
                neighbor_name = splitted_line[1]
                temp_node_dict[node_name].neighbors_set.add(temp_node_dict[neighbor_name])
        edges_file.close()

        self.adj_set = temp_node_dict.values()
        for node in self.adj_set:
            node.num_of_neighbors = len(node.neighbors_set)
            for neighbor in node.neighbors_set:
                temp_adj_mat[node.idx][neighbor.idx] = 1

        self.adj_mat = temp_adj_mat

    def zero_one(self, x):
        if x > 0:
            return 1
        if x == 0:
            return 0

    def create_our_weights(self,depth):
        new_weighted_mat = np.matrix(self.adj_mat.copy())
        mat_list = [new_weighted_mat]
        zero_one_vect = np.vectorize(self.zero_one)
        for i in range(depth):
            temp_mat = np.matmul(new_weighted_mat, mat_list[i]).tolist()
            for k in range(len(temp_mat)):
                for j in range(len(temp_mat)):
                    if temp_mat[k][j] > 0:
                        temp_mat[k][j] = 1

            temp_mat = np.matrix(temp_mat)
            temp_mat = temp_mat/(i+2)
            print(temp_mat.tolist())
            mat_list.append(temp_mat)
            print(f"{(1+i)*100/depth}% done...")

        for mat in mat_list[1:]:
            new_weighted_mat = np.add(new_weighted_mat, mat)
        return new_weighted_mat.tolist()
