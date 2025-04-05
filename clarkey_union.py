import sys
import itertools

# CLARKEY UNION
# 847929 Score
# 7412ms Total Time
# 453ms Peak Time
# 75.5 MiB Peak Memory

class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n)) # Parent tracking
        self.size = [1] * n          # Size tracking for balancing
        self.route_load = {}         # Keeps track of load per route

    def find(self, u):
        if self.parent[u] != u:
            self.parent[u] = self.find(self.parent[u]) # Path compression
        return self.parent[u]

    def union(self, u, v, Q, q):

        # Find - Locate  root representative of a customer’s route
        # Uses path compression to speed up future lookups
        root_u = self.find(u)
        root_v = self.find(v)

        if root_u != root_v:
            new_load = self.route_load.get(root_u, 0) + self.route_load.get(root_v, 0)
            
            # Check capacity constraint
            # Union - Merge two routes, use union by size to keep structure balanced
            # in constant time 
            if new_load <= Q:
                if self.size[root_u] > self.size[root_v]:
                    self.parent[root_v] = root_u
                    self.size[root_u] += self.size[root_v]
                    self.route_load[root_u] = new_load
                else:
                    self.parent[root_u] = root_v
                    self.size[root_v] += self.size[root_u]
                    self.route_load[root_v] = new_load
                return True  # Merge successful
        return False  # Merge not possible

def read_input():
    """Reads input from stdin and returns number of locations, vehicle capacity, distance matrix, and demand vector."""
    n = int(sys.stdin.readline().strip())   # Number of locations (including depot)
    Q = int(sys.stdin.readline().strip())   # Vehicle capacity
    
    D = []
    for _ in range(n):
        D.append(list(map(int, sys.stdin.readline().strip().split())))  # Distance matrix
    
    q = list(map(int, sys.stdin.readline().strip().split()))    # Demand vector
    
    return n, Q, D, q

# Clarke-Wright Savings (Route Initialization & Merging) 
# Sorts the savings in descending order so we process the best merges first
# O(n^2) + O(n^2 logn)
def compute_savings(n, D):
    savings = []
    for i in range(1, n):
        for j in range(i + 1, n):
            s = D[0][i] + D[0][j] - D[i][j]  # Savings formula
            savings.append((s, i, j))
    
    savings.sort(reverse=True, key=lambda x: x[0]) 
    return savings

def solve_cvrp(n, Q, D, q):
    savings_list = compute_savings(n, D)
    uf = UnionFind(n)
    
    # Each customer starts in their own route
    routes = {i: [0, i, 0] for i in range(1, n)}  # Initial routes
    for i in range(1, n):
        uf.route_load[i] = q[i]  # Initialize the route load with customer demands

    # Track how many separate routes exist
    num_routes = len(routes) 
    for _, i, j in savings_list:
        if num_routes == 1:  # Stop early if all merged
            break

        if i in routes and j in routes and uf.union(i, j, Q, q):
            num_routes -= 1  # Decrease number of separate routes

            route_i, route_j = routes[i], routes[j]
            
            # Merge the routes properly
            if route_i[-2] == i and route_j[1] == j:
                new_route = route_i[:-1] + route_j[1:]
            elif route_i[1] == i and route_j[-2] == j:
                new_route = route_j[:-1] + route_i[1:]
            else:
                continue  # Skip invalid merges

            # Update the route dictionary
            for node in new_route[1:-1]:
                routes[node] = new_route
            del routes[j]  # Remove merged route
    
    return list(set(tuple(r) for r in routes.values()))

def two_opt(route, D): # O(n^2)
    improved = True
    while improved:
        improved = False
        for i in range(1, len(route) - 2):
            for j in range(i + 1, len(route) - 1):
                if D[route[i - 1]][route[i]] + D[route[j]][route[j + 1]] > D[route[i - 1]][route[j]] + D[route[i]][route[j + 1]]:
                    route[i:j + 1] = reversed(route[i:j + 1]) # Reverse segment
                    improved = True
    return route

def local_search(routes, D, q, Q):
    for route in routes:
        route[:] = two_opt(route, D)
    return routes

def check(routes, n, Q, D, q):
    node_visited = []
    for route in routes:
        total_demand = sum([q[i] for i in route if i != 0])
        if not (total_demand <= Q):
            return False
        node_visited += route

    if len(set(node_visited)) != len(q):
        return False

    return True

def main():
    n, Q, D, q = read_input()
    routes = solve_cvrp(n, Q, D, q)

    if check(routes, n, Q, D, q): 
        for route in routes:
            print(" ".join(map(str, route)))

if __name__ == "__main__":
    main()

