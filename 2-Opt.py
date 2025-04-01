import sys
import itertools

# GREEDY 2-OPT
# 817664 Score
# 3003ms Total Time

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

def two_opt(route, D):
    """Performs 2-Opt optimization on a single route."""
    best_route = route[:]
    improved = True
    
    while improved:
        improved = False

        # iterate through pairs of edges in route
        for i in range(1, len(best_route) - 2):
            for j in range(i + 1, len(best_route) - 1):
                
                # swap two edges
                new_route = best_route[:i] + best_route[i:j+1][::-1] + best_route[j+1:]

                # keep the best route, if new route is shorter
                if calculate_route_distance(new_route, D) < calculate_route_distance(best_route, D):
                    best_route = new_route
                    improved = True
    
    return best_route

def calculate_route_distance(route, D):
    """Calculates total distance of a given route."""
    return sum(D[route[i]][route[i + 1]] for i in range(len(route) - 1))

def solve_cvrp(n, Q, D, q):
    """Greedy CVRP solver with 2-Opt optimization."""
    unvisited = set(range(1, n))  # Customers (excluding depot)
    routes = []
    
    while unvisited:
        route = [0]  # Start at the depot
        load = 0
        current = 0  # Last visited location (initial depot)
        
        # Find nearest feasible customer who fits within the vehicle capacity (Q)
        while unvisited:
            next_customer = min(
                (c for c in unvisited if load + q[c] <= Q),
                key=lambda c: D[current][c],
                default=None
            )
            
            # No feasible customers left for this route
            if next_customer is None:
                break  
                
            # Add customer to route
            route.append(next_customer)
            load += q[next_customer]
            current = next_customer
            unvisited.remove(next_customer)
        
        route.append(0)  # Return to depot
        optimized_route = two_opt(route, D)  # Apply 2-Opt optimization
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
