import argparse
from math import sqrt
import itertools
import sys

parser = argparse.ArgumentParser()
parser.add_argument('-f', action='store', dest='file_name', default='input.txt', required=False, help="input file location")

def read_from_file(file):
	lines = open(file).readlines()
	return [line[1:].strip().split(' ') for line in lines]

def write_to_file(file, line):
	with open(file + ".tour", "a") as output:
		output.write(" ".join(line))
		output.write('\n')

def calculate_distance(p1, p2):
	return sqrt((int(p2[0]) - int(p1[0])) ** 2 + (int(p2[1]) - int(p1[1])) ** 2)

def generate_distance_matrix(coordinates):
	matrix = []
	for a in coordinates:
		row = []
		for b in coordinates:
			row.append(calculate_distance(a,b))
		matrix.append(row)
	return matrix

class MST():
 
    def __init__(self, vertices):
        self.V = vertices
        self.graph = [[0 for column in range(vertices)] 
                      for row in range(vertices)]
 
    # A utility function to print the constructed MST stored in parent[]
    def returnMST(self, parent):
        MST = []
        for i in range(1,self.V):
        	edge = (parent[i], i, self.graph[i][parent[i]])
        	MST.append(edge)
            # print parent[i],"-",i,"\t",self.graph[i][ parent[i] ]
        return MST
 
    # A utility function to find the vertex with minimum distance value, from
    # the set of vertices not yet included in shortest path tree
    def minKey(self, key, mstSet):
 
        # Initilaize min value
        min = sys.maxint
 
        for v in range(self.V):
            if key[v] < min and mstSet[v] == False:
                min = key[v]
                min_index = v
 
        return min_index
 
    # Function to construct and print MST for a graph represented using
    # adjacency matrix representation
    def primMST(self):
 
        #Key values used to pick minimum weight edge in cut
        key = [sys.maxint] * self.V
        parent = [None] * self.V # Array to store constructed MST
        key[0] = 0   # Make key 0 so that this vertex is picked as first vertex
        mstSet = [False] * self.V
 
        parent[0] = -1  # First node is always the root of
 
        for cout in range(self.V):
 
            # Pick the minimum distance vertex from the set of vertices not
            # yet processed. u is always equal to src in first iteration
            u = self.minKey(key, mstSet)
 
            # Put the minimum distance vertex in the shortest path tree
            mstSet[u] = True
 
            # Update dist value of the adjacent vertices of the picked vertex
            # only if the current distance is greater than new distance and
            # the vertex in not in the shotest path tree
            for v in range(self.V):
                # graph[u][v] is non zero only for adjacent vertices of m
                # mstSet[v] is false for vertices not yet included in MST
                # Update the key only if graph[u][v] is smaller than key[v]
                if self.graph[u][v] > 0 and mstSet[v] == False and\
                   key[v] > self.graph[u][v]:
                        key[v] = self.graph[u][v]
                        parent[v] = u
 
        return self.returnMST(parent)


def _odd_vertices_of_MST(M, number_of_nodes):
	"""Returns the vertices having Odd degree in the Minimum Spanning Tree(MST).
	"""
	odd_vertices = [0 for i in range(number_of_nodes)]
	for u,v,d in M:
		odd_vertices[u] = odd_vertices[u] + 1
		odd_vertices[v] = odd_vertices[v] + 1
	odd_vertices = [vertex for vertex, degree in enumerate(odd_vertices) if degree % 2 == 1]
	return odd_vertices

def bipartite_Graph(M, bipartite_set, odd_vertices):
	"""
	"""
	bipartite_graphs = []
	vertex_sets = []
	for vertex_set1 in bipartite_set:
		vertex_set1 = list(sorted(vertex_set1))
		vertex_set2 = []
		for vertex in odd_vertices:
			if vertex not in vertex_set1:
				vertex_set2.append(vertex)
		matrix = [[-1000000 for j in range(len(vertex_set2))] for i in range(len(vertex_set1))]
		for i in range(len(vertex_set1)):
			for j in range(len(vertex_set2)):
				if vertex_set1[i] < vertex_set2[j]:
					matrix[i][j] = M[vertex_set1[i]][vertex_set2[j]]
				else:
					matrix[i][j] = M[vertex_set2[j]][vertex_set1[i]]
		bipartite_graphs.append(matrix)
		vertex_sets.append([vertex_set1,vertex_set2])
	return [bipartite_graphs, vertex_sets]

def main():
    user_args = parser.parse_args()
    array_of_lines = read_from_file(user_args.file_name)
    mst = MST(len(array_of_lines))
    mst.graph = generate_distance_matrix(array_of_lines)
    triples = mst.primMST()
    print triples
    odd_vertices = _odd_vertices_of_MST(triples, len(array_of_lines))
    print odd_vertices
    bipartite_set = [set(i) for i in itertools.combinations(set(odd_vertices), len(odd_vertices)/2)]
    print bipartite_set
    bipartite_graphs = bipartite_Graph(mst.graph, bipartite_set, odd_vertices)
    print bipartite_graphs
    # print held_karp(generate_distance_matrix(array_of_lines))


if __name__ == "__main__":
    main()
