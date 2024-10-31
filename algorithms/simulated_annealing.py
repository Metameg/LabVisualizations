import networkx as nx
import random
import math

class SA:
    def __init__(self, G, T, a):
        self.G = G
        self.source = 0
        self.target = max(G.nodes)
        self.all_paths = list(nx.all_simple_edge_paths(G, source=self.source, target=self.target, cutoff=9))
        self.visited_paths = set()
        self.T = T  # Initial temperature
        self.a = a
        self.max_inflow = 0 

        # Save initial state params ( for reset function)
        self.init_graph = G  # Save the original graph to reset later
        self.init_temp = T
        self.init_max_inflow = 0 
        self.init_visited_paths = set()

    def _init_G(self):
        # Set all flow values in graph to 0
        for u, v in self.G.edges():
            self.G[u][v]['flow'] = 0

    def _select_path(self):
        # select a random path from the list of paths from source to sink
        path = random.choice(self.all_paths)

        return path

    def _get_min_capacity(self, path):
        # get the minimum capacity of the path
        min_capacity = math.inf
        for edge in path:
            if self.G[edge[0]][edge[1]]['capacity'] < min_capacity:
                min_capacity = self.G[edge[0]][edge[1]]['capacity']

        return min_capacity

    def _heuristic(self, G):
        '''The heuristic calculates the inflow into the sink node
        of the given graph
        '''

        sink = max(G.nodes)
        total_inflow = 0

        # Calculate the total flow into the sink node
        for predecessor in G.predecessors(sink):
            total_inflow += G[predecessor][sink]['flow']

        return total_inflow

    def _zero_out_flow(self, G, path):
        for edge in path:
            G[edge[0]][edge[1]]['flow'] = 0

    def _enforce_conservation(self, G, curr_path):

        '''This will make sure each edge in a path that also contains an edge in the
         currently selected path will be 0'd out before updating the flow values
         in the current path. By zeroing out all edges in a path that is jointed
         with the current path, we guarantee that conservation will be maintained
         for the new flow values of the current path.
        '''

        # Iterate over a shallow copy of visited_paths
        # (since visited_paths will be changed as we iterate)
        for v_path in list(self.visited_paths):
            # Create sets of edges for both paths
            curr_path_edges = set(curr_path)
            v_path_edges = set(v_path)

            # Check for intersection
            if not curr_path_edges.isdisjoint(v_path_edges):
                # Zero out all edges if there is an edge intersection
                # print(f"erasing: {v_path}")
                self._zero_out_flow(G, v_path)
                self.visited_paths.remove(v_path)



    def _successor(self):
        '''This will determine the edge flows of a new graph at each iteration of the
        simulated annealing algorithm
        '''
        # copy G so we don't update the existing graph
        temp_G = self.G.copy()

        # Randomly select a path
        curr_path = self._select_path()
        min_capacity = self._get_min_capacity(curr_path)

        # Select random flow value for this path
        flow = random.randint(1, min_capacity)

        # Before updating flow values, make sure conservation will be maintained
        self._enforce_conservation(temp_G, curr_path)
        # Add this path to visited
        self.visited_paths.add(tuple(curr_path))


        # Set each edge to the flow value
        for edge in curr_path:
            temp_G[edge[0]][edge[1]]['flow'] = flow

        return temp_G, self._heuristic(temp_G)

    def step(self):
        ''' Perform a single iteration of the simulated annealing algorithm. '''
        if self.T < 0.01:  # Stop if temperature is very low
            return 0, self.max_inflow, self.G, 0
        
        # Temperature dissipation
        self.T = self.T*(1-self.a)
        print("temperature:", self.T)
        visited_paths_state = self.visited_paths.copy()

        # Store new graph and inflow value from the successor function
        curr_G, curr_inflow = self._successor()

        # Acceptance condition
        if curr_inflow < self.max_inflow:
            E = curr_inflow - self.max_inflow
            acceptance_threshold = math.exp(E / self.T)
            p = random.uniform(0, 1)
            if p < acceptance_threshold:
                self.max_inflow = curr_inflow
                self.G = curr_G
            else:
                self.visited_paths = visited_paths_state
        else:
            self.max_inflow = curr_inflow
            self.G = curr_G

        return curr_inflow, self.max_inflow, self.G, self.T

    def simulated_annealing(self, T, a):
        self._init_G()
        max_inflow = 0

        # Loop until T is approx. 0 since T will never actually hit 0.
        while T > 0.01:
            # Temperature dissapates on each iteration
            T = T*(1-a)
            visited_paths_state = self.visited_paths.copy()

            # Store the new graph and its inflow value according to successor function
            curr_G, curr_inflow = self._successor()

            # If the new inflow is worse than the current max, accept it anyway
            # with a certain probability
            if curr_inflow < max_inflow:
                E = curr_inflow - max_inflow
                acceptance_threshold = math.exp(E / T)
                p = random.uniform(0, 1)

                if p < acceptance_threshold:
                    max_inflow = curr_inflow
                    self.G = curr_G   # update graph
                else:
                    self.visited_paths = visited_paths_state

            # If the new inflow is better, always accept it
            else:
                max_inflow = curr_inflow
                self.G = curr_G  # update graph

        return max_inflow, self.G
    
    def reset(self):
        self.G = self.init_G
        self.T = self.init_temp
        self.max_inflow = self.init_max_inflow
        self.visited_paths = self.init_visited_paths