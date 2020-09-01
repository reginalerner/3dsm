import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from itertools import combinations


class Edge:
    def __init__(self, _from, _to, _weight):
        '''
        Structure fields:
            _from -- outgoing vertex
            _to -- incoming vertex
            _weight -- edges weight \in {1, 2, 3},
            _weight = 1 is for the best preference
        '''
        self._from =  _from
        self._to  = _to
        self._weight = _weight
        
    def  __eq__(self, other):
        '''
        Edge equality operator
        '''
        return (self._from == other._from and
                         self._to == other._to) 
        
        
class PreferenceGraph:
    def __init__(self, basic_graph_index, rest_edges_code):
        '''
        Parameters:
          basic_graph_index (int in {1, ..., 6}) -- one of 6 variants of basic 
              graph G''
          rest_edges_code (str) -- str of length 9 with information about rest 
              edges for each vertex (5 ** 9 variants)
          
        Structure fields:
          edges -- adjacency list 
              (list of length 9 with all the outgoing edges for each vertex)
        '''
        self.edges = [[] for _ in range(9)]
        self.add_basic_edges(basic_graph_index)
        self.add_other_edges(rest_edges_code)
        
    def show_edges(self):
        '''
        Prints all edges, for debug
        '''
        for i in range(9):
            for e in self.edges[i]:
                print('(from: {}, to: {}, weight: {})'.format(
                  str(e._from), str(e._to), str(e._weight)))
                print('\n')        

    def draw_edges(self):
        '''
        Graph visualization
        '''
        plt.figure(figsize=(16, 8))
        G = nx.DiGraph()
        G.add_nodes_from(range(9))
        for i in range(9):
            for e in self.edges[i]:
                G.add_edge(e._from, e._to, weight=e._weight)
        pos = nx.spring_layout(G)
        edge_labels=dict([((u, v,), d['weight'])
                 for u, v, d in G.edges(data=True)])
        get_color = lambda n: 'r' if n % 3 == 0 else (
            'g' if n % 3 == 1 else 'b')
        nx.draw_networkx_nodes(G, pos, node_size = 500,
                              node_color=[get_color(i) for i in range(9)])
        nx.draw_networkx_labels(G, pos)
        nx.draw_networkx_edges(G, pos, arrows=True)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
        plt.show()
                
        
    def add_edge(self, _from, _to, _weight):
        '''
        Adds an edge to graph's adjacency list
        '''
        self.edges[_from].append(Edge(_from, _to, _weight))
        
        
    def add_basic_edges(self, basic_graph_index):
        '''
        Parameters:
            basic_graph_index (int in {0, 1, 2, 3, 4, 5})
        Builds graph's basic subgraph G'' of given index
        (adds edges of weight=1)
        '''
        if basic_graph_index == 0:
            '''
            Cycle of length 9
            '''
            for i in range(9):
                self.add_edge(i % 9, (i + 1) % 9, 1)
        elif basic_graph_index == 1:
            '''
            Cycle of length 6 with tail of length 3
            '''
            for i in range(6):
                self.add_edge(i % 6, (i + 1) % 6, 1)
            self.add_edge(6, 7, 1)
            self.add_edge(7, 8, 1)
            self.add_edge(8, 0, 1)    
        elif basic_graph_index == 2:
            '''
            Cycle of length 6, tails of length 2 and 1 near each other
            '''
            for i in range(6):
                self.add_edge(i % 6, (i + 1) % 6, 1)
            self.add_edge(6, 1, 1)
            self.add_edge(7, 8, 1)
            self.add_edge(8, 0, 1)
        elif basic_graph_index == 3:
            '''
            Cycle of length 6, tails of length 2 and 1 through one vertex
            '''
            for i in range(6):
                self.add_edge(i % 6, (i + 1) % 6, 1)
            self.add_edge(6, 4, 1)
            self.add_edge(7, 8, 1)
            self.add_edge(8, 0, 1)
        elif basic_graph_index == 4:
            '''
            Cycle of length 6, three tails of length 1 near each other
            '''
            for i in range(6):
                self.add_edge(i % 6, (i + 1) % 6, 1)
            self.add_edge(6, 1, 1)
            self.add_edge(7, 2, 1)
            self.add_edge(8, 0, 1)
        elif basic_graph_index == 5:
            '''
            Cycle of length 6, three tails of length 1 through one vertex
            '''
            for i in range(6):
                self.add_edge(i % 6, (i + 1) % 6, 1)
            self.add_edge(6, 4, 1)
            self.add_edge(7, 2, 1)
            self.add_edge(8, 0, 1)
            
    def add_other_edges(self, rest_edges_code):
        '''
        Parameters:
            rest_edges_code (str of length(9)) -- info about non-basic edges 
              for each vertex
            rest_edges_code[i] in {'0', ..., '4'}
              '0' -- no more outgoing edges
              '1', '2' -- one more outgoing edge of weight 2, 
                          2 cases where it can lead to
              '3', '4' -- two edges of weight 2 and 3,
                          2 cases of how to distribute them among 
                          two possible vertexes
        '''
        for i in range(9):
            neighbours = {(i + 1) % 9, (i + 4) % 9, (i + 7) % 9}
            neighbours.remove(self.edges[i][0]._to) 
            ''' 
            List of 2 vertexes, 
            to which the edges of weight 2 and 3 can lead
            '''
            neighbours = list(neighbours)

            if rest_edges_code[i] == '0':
                continue
            if rest_edges_code[i] == '1':
                self.edges[i].append(Edge(i, neighbours[0], 2))
            if rest_edges_code[i] == '2':
                self.edges[i].append(Edge(i, neighbours[1], 2))
            if rest_edges_code[i] == '3':
                self.edges[i].append(Edge(i, neighbours[0], 2))
                self.edges[i].append(Edge(i, neighbours[1], 3))
            if rest_edges_code[i] == '4':
                self.edges[i].append(Edge(i, neighbours[0], 3))
                self.edges[i].append(Edge(i, neighbours[1], 2))
    
    def check_triplets_comb(self, comb):
        '''
        Parameters:
            comb -- combination of 1, 2 or 3 triplets of man, women and dog

        Checks if all the triplets in the given combination are families in graph
          (= graph has all the necessery edges)
        If it has, returns the list 'weights' of lenth 9,
            weights[i] -- weigth of the outgoing edge from vertex i 
              in combination    
        If it has not, returns []  
        '''
        weights = [4] * 9
        for triplet in comb:
            man = [it for it in triplet if it % 3 == 0][0]
            woman = [it for it in triplet if it % 3 == 1][0]
            dog = [it for it in triplet if it % 3 == 2][0]
            
            edges1 = list(filter(
                lambda e: e._from == man and e._to == woman, self.edges[man]))
            edges2 = list(filter(
                lambda e: e._from == woman and e._to == dog, self.edges[woman]))
            edges3 = list(filter(
                lambda e: e._from == dog and e._to == man, self.edges[dog]))
            if not (len(edges1) == 1 and len(edges2) == 1 
                    and len(edges3) == 1):
                return []
            else:
                weights[edges1[0]._from] = edges1[0]._weight
                weights[edges2[0]._from] = edges2[0]._weight
                weights[edges3[0]._from] = edges3[0]._weight
        return weights
    
    
    def find_blocking_for_comb(self, comb):
        '''
        Parameters:
            comb -- combination of 1, 2 or 3 triplets of man, women and dog

        Checks if this combination is possible in graph 
          via check_triplets_comb method and get edges' weights if it is.
        Then goes over all possible triplets,
          checks if there is a blocking one among them.
        Returns True if there is and False otherwise
        '''
        weights = self.check_triplets_comb(comb)
        if weights == []:
            return None
        triplets = np.array(
            np.meshgrid([0, 3, 6], [1, 4, 7], [2, 8, 5])).T.reshape(-1, 3)
        for triplet in triplets:
            man = [it for it in triplet if it % 3 == 0][0]
            woman = [it for it in triplet if it % 3 == 1][0]
            dog = [it for it in triplet if it % 3 == 2][0]
            
            edges1 = list(filter(
                lambda e: e._from == man and e._to == woman, self.edges[man])) 
            edges2 = list(filter(
                lambda e: e._from == woman and e._to == dog, self.edges[woman]))
            edges3 = list(filter(
                lambda e: e._from == dog and e._to == man, self.edges[dog]))
            if not (len(edges1) == 1 and len(edges2) == 1 
                    and len(edges3) == 1):
                continue
            if weights[edges1[0]._from] > edges1[0]._weight \
            and weights[edges2[0]._from] > edges2[0]._weight \
            and weights[edges3[0]._from] > edges3[0]._weight:
                return True
        return False
