import sys
from itertools import permutations

# BRUTE FORCE 


"""
To use this file with example testcases, run: 

python branch_and_bound.py < 1.in > branch1.out

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
    """Solves the Capacitated Vehicle Routing Problem using Branch and Bound."""
    best_routes = None
    best_cost = float('inf')
    
    def calculate_cost(route):
        cost = 0
        for i in range(len(route) - 1):
            cost += D[route[i]][route[i + 1]]
        return cost
    
    def is_valid(route):
        total_load = sum(q[i] for i in route if i != 0 and i < len(q))
        return total_load <= Q
    
    # Generate all possible routes (brute force for small n)
    customers = list(range(1, n))
    for perm in permutations(customers):
        route = [0] + list(perm) + [0]  # Start and end at depot
        if is_valid(route):
            cost = calculate_cost(route)
            if cost < best_cost:
                best_cost = cost
                best_routes = [route]
    
    return best_routes if best_routes else [[0]]  # Return at least a default route

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
