import sys
import itertools
import heapq

# BRANCH AND BOUND 


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

class Node:
    """Represents a state in the branch-and-bound search."""
    def __init__(self, routes, cost, remaining_customers):
        self.routes = routes  # List of routes (each route is a list of customers)
        self.cost = cost  # Total cost of all routes
        self.remaining_customers = remaining_customers  # Customers yet to be visited

    def __lt__(self, other):
        return self.cost < other.cost  # For priority queue to sort by cost (ascending)

def calculate_route_cost(route, D):
    """Calculate the cost (distance) of a given route."""
    cost = 0
    for i in range(len(route) - 1):
        cost += D[route[i]][route[i + 1]]
    return cost

def lower_bound(node, D):
    """Estimate the lower bound of the cost of the current node."""
    bound = node.cost
    remaining_customers = node.remaining_customers
    
    # Add minimum outgoing cost for each remaining customer
    for customer in remaining_customers:
        bound += min(D[customer])
    
    return bound

def solve_cvrp(n, Q, D, q):
    """Solves the Capacitated Vehicle Routing Problem using Branch and Bound."""
    root = Node([ [0] ], 0, set(range(1, n)))  # Start with a single route from depot
    
    pq = []
    heapq.heappush(pq, root)
    
    best_cost = float('inf')
    best_routes = None
    
    while pq:
        node = heapq.heappop(pq)
        
        if node.cost >= best_cost:
            continue
        
        if not node.remaining_customers:
            if node.cost < best_cost:
                best_cost = node.cost
                best_routes = node.routes
            continue
        
        # Try assigning each remaining customer to an existing route or a new one
        for customer in list(node.remaining_customers):
            for i, route in enumerate(node.routes):
                new_route = route[:-1] + [customer] + [0]  # Insert before depot return
                new_cost = node.cost - calculate_route_cost(route, D) + calculate_route_cost(new_route, D)
                
                if sum(q[c] for c in new_route if c != 0) <= Q:
                    new_routes = node.routes[:]
                    new_routes[i] = new_route
                    new_remaining_customers = node.remaining_customers - {customer}
                    bound = lower_bound(Node(new_routes, new_cost, new_remaining_customers), D)
                    
                    if bound < best_cost:
                        heapq.heappush(pq, Node(new_routes, new_cost, new_remaining_customers))
            
            # Start a new route if necessary
            new_routes = node.routes + [[0, customer, 0]]
            new_cost = node.cost + D[0][customer] + D[customer][0]
            new_remaining_customers = node.remaining_customers - {customer}
            bound = lower_bound(Node(new_routes, new_cost, new_remaining_customers), D)
            
            if bound < best_cost:
                heapq.heappush(pq, Node(new_routes, new_cost, new_remaining_customers))
    
    return best_routes

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
