import sys
import itertools

# GREEDY 
# 821774 score time
# 2956ms Total Time

# 821774 score time
# 2846ms Total Time
# 166ms Peak Time
# 20 MiB Peak Memory

"""
To use this file with example testcases, run: 

python greedy_cvrp.py < 1.in > 1.out

This reads input from 1.in and prints output to 1.out. 
"""

def read_input():
    """Reads input from stdin and returns number of locations, vehicle capacity, distance matrix, and demand vector."""
    n = int(sys.stdin.readline().strip())   # Number of locations (including depot)
    Q = int(sys.stdin.readline().strip())   # Vehicle capacity
    
    D = []
    for _ in range(n):
        D.append(list(map(int, sys.stdin.readline().strip().split())))  # Distance matrix
    
    q = list(map(int, sys.stdin.readline().strip().split()))    # Demand vector
    
    return n, Q, D, q

def solve_cvrp(n, Q, D, q):
    """TODO: Solve the Capacitated Vehicle Routing Problem and return a list of routes."""
    unvisited = set(range(1, n))  # Customers (excluding depot)
    routes = []
    
    while unvisited:
        route = [0]  # Start at the depot
        load = 0
        current = 0
        
        while unvisited:
            # Find the nearest feasible customer
            next_customer = min(
                (c for c in unvisited if load + q[c] <= Q), # Feasible customers
                key=lambda c: D[current][c],                # Choose the nearest customer
                default=None                    # If no customer can be served, return None
            )
            
            if next_customer is None:
                break       # No more feasible customers, return to depot
            
            route.append(next_customer)     
            load += q[next_customer]
            current = next_customer
            unvisited.remove(next_customer)
        
        route.append(0)  # Return to depot
        routes.append(route)
    
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
