# -*- coding: utf-8 -*-
"""
Created on Fri Apr  7 17:15:29 2023

@author: m_bar
"""

import numpy as np
import random

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
        
    def colour_order(self,order,initialise=True):
        if initialise: # remove all colours found
            self.colours = [None for i in range(self.N)]
        ur_vert = order[0]
        self.colours[ur_vert] = 0
        for i in range(1,self.N):
            this_vert = order[i]
            col_taken = set()
            for neigh in self.neighbours[this_vert]:
                if self.colours[neigh] is not None:
                    col_taken.add(self.colours[neigh])
            if len(col_taken):
                col_choose = min(set(range(max(col_taken)+2)).difference(col_taken))
            else:
                col_choose = 0
            self.colours[this_vert] = col_choose
            
    def greedy_1(self):
        order_degree = argsort(self.degree, True)
        self.colour_order(order_degree)
        
    def greedy_n(self, n):
        random.seed(123)
        self.greedy_1()
        best = self.colours.copy()
        best_score = len(set(best))
        for i in range(n):
            colist = list(set(best))
            random.shuffle(colist)
            new_order = []
            col_dic = {i:[[],[]] for i in colist}
            for vert in range(self.N):
                col = self.colours[vert]
                deg = self.degree[vert]
                col_dic[col][0].append(vert)
                col_dic[col][1].append(deg)
            for col in col_dic:
                sub_order = argsort(col_dic[col][1], True)
                for o in sub_order:
                    new_order.append(col_dic[col][0][o])
            self.colour_order(new_order)
            cand = self.colours
            cand_score = len(set(cand))
            if cand_score <= best_score:
                if cand_score < best_score:
                    print('better score of', cand_score, 'at iteration', i)#
                best = cand.copy()
                best_score = cand_score
        self.colours = best.copy()
                                  
            
        
        
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

def argsort(seq, reverse=False):
    return sorted(range(len(seq)), key=seq.__getitem__, reverse=reverse)


"""
Algorithms
My simple algorithm works not so good but quick enough. It got 38/60 for the assignment, but I cannot find a graph which is simple enough to verity my algorithm will fail on it.

This is what my algorithm did: 

sort all the node to descending order of it's degree to list N

 for node in list N, collect it's connected vertex's color to array C (use -1 to represent uncolored)

    2.1. from 0 to node_count - 1, color the node with first available color c which is not in array C; 

3. repeat step 2 until all the nodes were colored.
********sol number 2*******
I am a bit shocked. With this particular version of greedy algorithm, I got 57/60 with just one submission.

It's all about how to shuffle the nodes. First apply an algorithm to the nodes so you have a solution to start with. Then group the nodes by colors. Then randomly pick one group, order the subset by degree in descending order. Pick another group, sort it and append the sorted list to the previous one. Finally feed the nodes to your greedy algorithm. Repeat the procedures on the new solutions for a couple thousand times. I did 3000.

It's just greedy, no fancy tricks in permutation. Unbelievable.

"""