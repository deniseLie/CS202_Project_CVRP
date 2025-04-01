import sys
import itertools

# 821774 score
# 2513ms TotalTime
# 146ms Peak Time

"""
To use this file with example testcases, run: 

python nearest_neighbor.py < 1.in > 1.out

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
    routes = [[0]]

    unvisited = set(range(1, n))

    while unvisited:
        
        route = [0] # Start a new route from the depot
        capacity = Q
        current = 0

        # Find nearest unvisited
        while unvisited: 
            nearest = None
            nearest_dist = float('inf')

            for customer in unvisited: 
                if q[customer] <= capacity and D[current][customer] < nearest_dist:
                    nearest = customer
                    nearest_dist = D[current][customer]
            
            # No more customers can fit, return to depot
            if nearest is None:
                break

            # Visit nearest customer
            route.append(nearest)
            capacity -= q[nearest]
            unvisited.remove(nearest)
            current = nearest
        
        route.append(0) # return to depot
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
