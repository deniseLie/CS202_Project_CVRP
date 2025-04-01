import sys
import itertools

# 708067 Score
# 6417ms Total Time

"""
To use this file with example testcases, run: 

python clarkey_wright_savings.py < 1.in > 1.out

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
    """Solves the Capacitated Vehicle Routing Problem using the Clarke-Wright Savings Algorithm."""
    # Step 1: Compute savings values
    savings = []
    for i in range(1, n):
        for j in range(i + 1, n):
            s = D[0][i] + D[0][j] - D[i][j]  # Savings formula
            savings.append((s, i, j))
    
    # Step 2: Sort savings in descending order
    savings.sort(reverse=True, key=lambda x: x[0])
    
    # Step 3: Initialize separate routes for each customer
    routes = {i: [0, i, 0] for i in range(1, n)}
    route_loads = {i: q[i] for i in range(1, n)}
    
    # Step 4: Merge routes based on savings
    for _, i, j in savings:
        if i in routes and j in routes and routes[i] != routes[j]:
            # Check if both routes exist before merging
            if i in route_loads and j in route_loads and route_loads[i] + route_loads[j] <= Q:
                # Merge routes
                route_i = routes[i]
                route_j = routes[j]
                
                # Ensure endpoints are correct
                if route_i[-2] == i and route_j[1] == j:
                    new_route = route_i[:-1] + route_j[1:]
                elif route_i[1] == i and route_j[-2] == j:
                    new_route = route_j[:-1] + route_i[1:]
                else:
                    continue  # Skip invalid merges
                
                # Update route tracking
                for node in new_route[1:-1]:
                    routes[node] = new_route
                route_loads[i] += route_loads[j]
                del routes[j]
                route_loads.pop(j, None)  # Safely remove j from route_loads
    
    # Step 5: Extract final routes
    final_routes = list(set(tuple(r) for r in routes.values()))
    return [list(r) for r in final_routes]

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
