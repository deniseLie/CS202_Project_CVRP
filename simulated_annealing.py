import sys
import itertools
import random
import math

# SIMULATED ANNEALING

### cooling_rate=0.995 
# 821774 Score
# 29932ms Total Time
# 1438ms Peak Time

### cooling_rate=0.997 
# 821287 Score
# 34378ms Total Time
# 1662ms Peak Time

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

def is_valid_route(route, Q, q):
    """Check if a route does not exceed the vehicle capacity"""
    total_demand = sum([q[i] for i in route if i != 0])  # Exclude depot (0)
    return total_demand <= Q

def initial_solution(n, Q, D, q):
    """Creates an initial greedy solution for CVRP."""
    unvisited = set(range(1, n))  # Customers (excluding depot)
    routes = []
    
    while unvisited:
        route = [0]  # Start at the depot
        load = 0
        current = 0  # Last visited location (initial depot)
        
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

def perturb_solution(routes, Q, q, D):
    """Randomly perturbs the solution by swapping customers within a route or between routes."""
    new_routes = [route[:] for route in routes]

    # Ensure capacity constraint is maintained during perturbation
    if len(new_routes) < 2:
        return new_routes
    
    r1, r2 = random.sample(new_routes, 2)
    if len(r1) > 2 and len(r2) > 2:
        idx1, idx2 = random.randint(1, len(r1) - 2), random.randint(1, len(r2) - 2)
        r1[idx1], r2[idx2] = r2[idx2], r1[idx1]

        # Check if the perturbed solution is valid
        if is_valid_route(r1, Q, q) and is_valid_route(r2, Q, q):
            return new_routes  # Return modified solution if valid
    
    return routes   # Otherwise, return original solution

def total_distance(routes, D):
    """Calculates total distance for all routes."""
    return sum(calculate_route_distance(route, D) for route in routes)

def solve_cvrp(n, Q, D, q, max_iter=5000, initial_temp=1000, cooling_rate=0.997):
    """Solves the CVRP using simulated annealing."""
    current_solution = initial_solution(n, Q, D, q)
    best_solution = current_solution[:]                     # Set best solution to initial solution
    current_distance = total_distance(current_solution, D)  
    best_distance = current_distance
    temperature = initial_temp
    
    # Iterate for max_iter steps
    for _ in range(max_iter):

        # compute total distance of perturbed solution
        new_solution = perturb_solution(current_solution, Q, q, D)  
        new_distance = total_distance(new_solution, D)
        
        if all(is_valid_route(route, Q, q) for route in new_solution):
            # Acceptance criteria : if new solution is better, if new solution worse accept with probability
                # Accept worse solution : 
                # escape local minima, higher temperature more likely accept bad solutions,
                # as temperature decreases, we become more selective about accepting bad solutions
            if new_distance < current_distance or random.random() < math.exp((current_distance - new_distance) / max(temperature, 1e-10)):
                current_solution = new_solution[:]
                current_distance = new_distance
                
                if current_distance < best_distance:
                    best_solution = current_solution[:]
                    best_distance = current_distance
        
        # Gradually reduce temperature
        temperature *= cooling_rate
    
    return best_solution

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
