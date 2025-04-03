import sys
import itertools

# Hybrid Clarke-Wright + Local Search for CVRP

# 706157 Score
# 6494ms Total Time

"""
To use this file with example testcases, run: 

python clarkey_local_search.py < 1.in > 1.out

This reads input from 1.in and prints output to 1.out. 
"""

def read_input():
    n = int(sys.stdin.readline().strip())  # Number of locations (including depot)
    Q = int(sys.stdin.readline().strip())  # Vehicle capacity
    
    D = []
    for _ in range(n):
        D.append(list(map(int, sys.stdin.readline().strip().split())))
    
    q = list(map(int, sys.stdin.readline().strip().split()))  # Demand vector
    
    return n, Q, D, q

def clarke_wright_savings(n, Q, D, q):
    savings = []
    for i in range(1, n):
        for j in range(i + 1, n):
            s = D[0][i] + D[0][j] - D[i][j]  # Savings formula
            savings.append((s, i, j))
    
    savings.sort(reverse=True, key=lambda x: x[0])
    
    routes = {i: [0, i, 0] for i in range(1, n)}
    route_loads = {i: q[i] for i in range(1, n)}
    
    for _, i, j in savings:
        if i in routes and j in routes and routes[i] != routes[j]:
            if i in route_loads and j in route_loads and route_loads[i] + route_loads[j] <= Q:
                route_i = routes[i]
                route_j = routes[j]
                
                if route_i[-2] == i and route_j[1] == j:
                    new_route = route_i[:-1] + route_j[1:]
                elif route_i[1] == i and route_j[-2] == j:
                    new_route = route_j[:-1] + route_i[1:]
                else:
                    continue
                
                for node in new_route[1:-1]:
                    routes[node] = new_route
                route_loads[i] += route_loads[j]
                del routes[j]
                route_loads.pop(j, None)
    
    final_routes = list(set(tuple(r) for r in routes.values()))
    return [list(r) for r in final_routes]

def two_opt(route, D):
    improved = True
    while improved:
        improved = False
        for i in range(1, len(route) - 2):
            for j in range(i + 1, len(route) - 1):
                if D[route[i - 1]][route[i]] + D[route[j]][route[j + 1]] > D[route[i - 1]][route[j]] + D[route[i]][route[j + 1]]:
                    route[i:j + 1] = reversed(route[i:j + 1])
                    improved = True
    return route

def local_search(routes, D, q, Q):
    for route in routes:
        route[:] = two_opt(route, D)
    return routes

def check(routes, n, Q, D, q):
    node_visited = []
    for route in routes:
        total_demand = sum(q[i] for i in route if i != 0)
        if total_demand > Q:
            return False
        node_visited += route
    return len(set(node_visited)) == len(q)

def main():
    n, Q, D, q = read_input()
    routes = clarke_wright_savings(n, Q, D, q)
    routes = local_search(routes, D, q, Q)
    
    if check(routes, n, Q, D, q):
        for route in routes:
            print(" ".join(map(str, route)))

if __name__ == "__main__":
    main()
