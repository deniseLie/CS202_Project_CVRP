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
    def __init__(self, route, cost, load, remaining_customers):
        self.route = route  # Current route (list of customers)
        self.cost = cost  # Total cost of the route so far
        self.load = load  # Total load (demand) of the current route
        self.remaining_customers = remaining_customers  # Customers yet to be visited

    def __lt__(self, other):
        return self.cost < other.cost  # For priority queue to sort by cost (ascending)

def calculate_cost(route, D):
    """Calculate the cost (distance) of a given route."""
    cost = 0
    for i in range(len(route) - 1):
        cost += D[route[i]][route[i + 1]]
    return cost

def lower_bound(node, D, q, Q):
    """Estimate the lower bound of the cost of the current node."""
    # If the load is too high, it's an invalid route
    if node.load > Q:
        return float('inf')
    
    # Heuristic lower bound (we use the nearest neighbor method for simplicity)
    bound = node.cost
    remaining_customers = node.remaining_customers
    current = node.route[-1]
    
    while remaining_customers:
        # Find the nearest customer
        min_dist = float('inf')
        next_customer = None
        for customer in remaining_customers:
            if D[current][customer] < min_dist:
                min_dist = D[current][customer]
                next_customer = customer
        bound += min_dist
        current = next_customer
        remaining_customers.remove(next_customer)
    
    return bound

def solve_cvrp(n, Q, D, q):
    """Solves the Capacitated Vehicle Routing Problem using Branch and Bound."""
    # Start with the root node (depot, no customers visited, cost 0)
    root = Node([0], 0, 0, set(range(1, n)))  # Start at the depot, no load, all customers remaining
    
    # Priority queue for exploring the search space (min-heap based on cost)
    pq = []
    heapq.heappush(pq, root)
    
    best_cost = float('inf')
    best_routes = None
    
    while pq:
        node = heapq.heappop(pq)
        
        # If this node's cost is already worse than the best found, prune it
        if node.cost >= best_cost:
            continue
        
        # If all customers have been visited, return to depot and check the solution
        if not node.remaining_customers:
            route_cost = node.cost + D[node.route[-1]][0]  # Return to depot
            if route_cost < best_cost:
                best_cost = route_cost
                best_routes = [node.route + [0]]  # Store the best route
            continue
        
        # Branching: try visiting each remaining customer
        for customer in list(node.remaining_customers):
            new_route = node.route + [customer]
            new_cost = node.cost + D[node.route[-1]][customer]
            new_load = node.load + q[customer]
            new_remaining_customers = node.remaining_customers.copy()
            new_remaining_customers.remove(customer)
            
            # If the load exceeds capacity, prune this branch
            if new_load > Q:
                continue
            
            # Calculate the lower bound of the new node
            bound = lower_bound(Node(new_route, new_cost, new_load, new_remaining_customers), D, q, Q)
            
            # If the bound is better than the best cost found so far, add the node to the queue
            if bound < best_cost:
                heapq.heappush(pq, Node(new_route, new_cost, new_load, new_remaining_customers))
    
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
