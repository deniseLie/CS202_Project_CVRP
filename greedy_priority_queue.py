import sys
import itertools
import heapq

# GREEDY PRIORITY QUEUE
# 821774 Score
# 3102ms Total Time

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

def solve_cvrp(n, Q, D, q):
    """Enhanced greedy heuristic to solve the Capacitated Vehicle Routing Problem."""
    unvisited = set(range(1, n))  # Customers (excluding depot)
    routes = []
    
    while unvisited:
        route = [0]  # Start at the depot
        load = 0
        current = 0
        
        # Use a priority queue to store potential customers based on distance and feasibility
        pq = []
        for c in unvisited:
            if load + q[c] <= Q:  # Only feasible customers
                heapq.heappush(pq, (D[current][c], c))  # Push customer with distance
        
        # Greedily select the nearest customer
        while pq:
            _, next_customer = heapq.heappop(pq)
            if load + q[next_customer] <= Q:
                route.append(next_customer)
                load += q[next_customer]
                current = next_customer
                unvisited.remove(next_customer)
                
                # Rebuild priority queue for remaining unvisited customers
                pq = []
                for c in unvisited:
                    if load + q[c] <= Q:
                        heapq.heappush(pq, (D[current][c], c))
        
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
