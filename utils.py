# -*- coding: utf-8 -*-
"""
Created on Fri Apr  7 17:15:29 2023

@author: m_bar
"""

import numpy as npl

class Graph(object):
    
    def __init__(self,edges,nodes):
        self.N= nodes
        self.edges = edges.copy()
        self.colours = [None for i in range(self.N)]
        self.neighbours = [set([]) for i in range(self.N)]
        self.make_neighbours()
        self.degree = [len(self.neighbours[i]) for i in range(self.N)]
        
        
    def make_neighbours(self):
        for e in self.edges:
            self.neighbours[e[0]].add(e[1])
            self.neighbours[e[1]].add(e[0])
            
    def trivial_colour(self):
        self.colours = [i for i in range(self.N)]
        self.colour_count = max(self.colours) + 1
        
def read_input(file_location):
    f = open(file_location, 'r')
    input_data = f.read()
    lines = input_data.split('\n')

    first_line = lines[0].split()
    node_count = int(first_line[0])
    edge_count = int(first_line[1])

    edges = []
    for i in range(1, edge_count + 1):
        line = lines[i]
        parts = line.split()
        edges.append((int(parts[0]), int(parts[1])))

    # build a trivial solution
    # every node has its own color
    
    g = Graph(edges,node_count)
    return g