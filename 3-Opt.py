import sys
import itertools

# 818364 Score
# 3134ms Total Time
# 181ms Peak Time
# 20 MiB Peak Memory

"""
To use this file with example testcases, run: 

python vrp.py < 1.in > 1.out

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

def calculate_route_distance(route, D):
    """Calculates total distance of a given route."""
    return sum(D[route[i]][route[i + 1]] for i in range(len(route) - 1))

def three_opt(route, D):
    """Performs 3-Opt optimization on a single route."""
    best_route = route[:]
    improved = True
    
    while improved:
        improved = False
        for i in range(1, len(best_route) - 3):
            for j in range(i + 1, len(best_route) - 2):
                for k in range(j + 1, len(best_route) - 1):
                    
                    # Generate possible 3-Opt swaps
                    options = [
                        best_route[:i] + best_route[i:j+1][::-1] + best_route[j+1:k+1][::-1] + best_route[k+1:],
                        best_route[:i] + best_route[j+1:k+1] + best_route[i:j+1] + best_route[k+1:],
                        best_route[:i] + best_route[j+1:k+1] + best_route[i:j+1][::-1] + best_route[k+1:],
                        best_route[:i] + best_route[i:j+1] + best_route[j+1:k+1][::-1] + best_route[k+1:]
                    ]
                    
                    # Select the best swap
                    best_option = min(options, key=lambda r: calculate_route_distance(r, D))
                    if calculate_route_distance(best_option, D) < calculate_route_distance(best_route, D):
                        best_route = best_option
                        improved = True
    
    return best_route

def solve_cvrp(n, Q, D, q):
    """Greedy CVRP solver with 3-Opt optimization."""
    unvisited = set(range(1, n))  # Customers (excluding depot)
    routes = []
    
    while unvisited:
        route = [0]  # Start at the depot
        load = 0
        current = 0  # Last visited location (initial depot)
        
        while unvisited:
            next_customer = min(
                (c for c in unvisited if load + q[c] <= Q),
                key=lambda c: D[current][c],
                default=None
            )
            
            if next_customer is None:
                break  
            
            route.append(next_customer)
            load += q[next_customer]
            current = next_customer
            unvisited.remove(next_customer)
        
        route.append(0)  # Return to depot
        optimized_route = three_opt(route, D)  # Apply 3-Opt optimization
        routes.append(optimized_route)
    
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
