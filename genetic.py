import sys
import random
import math

#  GENETIC 

# 

"""
To use this file with example testcases, run: 

python vrp.py < 1.in > 1.out

This reads input from 1.in and prints output to 1.out. 
"""

# 1. Initialize population: Generate a random initial population of solutions.
# 2. Evaluate fitness: Calculate the fitness of each solution in the population.
# 3. Select parents: Use tournament selection to choose two parents.
# 4. Apply crossover: Perform crossover to produce a child solution.
# 5. Apply mutation: Occasionally apply mutation to introduce diversity.
# 6. Replace population: Create a new population by selecting parents, applying crossover, and mutation.
# 7. Repeat for a set number of generations.
# 8. Return the best solution found.

# Crossover is used to combine solutions and inherit good traits from both parents.
# Mutation is used to introduce diversity and avoid getting stuck in local optima.
# Selection ensures that better solutions are more likely to propagate to future generations.
# Fitness drives the search towards better solutions by minimizing the total travel distance.

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

def total_distance(routes, D):
    """Calculates total distance for all routes."""
    return sum(calculate_route_distance(route, D) for route in routes)

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

# def crossover(parent1, parent2):
#     """Perform a one-point crossover between two parent solutions. Recombination"""
    
#     child = [None] * len(parent1)
#     crossover_point = random.randint(1, len(parent1) - 2)   # random crossover point chosen along the route
    
#     # Copy part of parent1
#     for i in range(crossover_point):
#         child[i] = parent1[i]
    
#     # first part of one parent’s route is taken and combined with the second part of the other parent’s route
#     # Copy part of parent2, making sure that no customer is repeated
#     # combine the strengths of both parents and hopefully create a better solution
#     parent2_customers = [i for i in parent2 if i not in child]
#     child[crossover_point:] = parent2_customers[:len(parent1) - crossover_point]
    
#     return child

def crossover(parent1, parent2, Q, q):
    """Perform crossover, ensuring the child solution is valid."""
    for _ in range(5):  # Try up to 5 times to get a valid child
        crossover_point = random.randint(1, len(parent1) - 2)
        
        # Create a child solution by combining parent routes
        child_routes = parent1[:crossover_point] + parent2[crossover_point:]

        # Ensure valid routes (not just a flat list of nodes)
        valid_routes = []
        for route in child_routes:
            if is_valid_route(route, Q, q):
                valid_routes.append(route)
        
        if valid_routes:
            return valid_routes  # Return a valid set of routes
    
    return parent1  # If no valid solution found, return parent1


# def mutate(solution, Q, q):
#     """Apply mutation to a solution by swapping two customers within a route."""
#     route = random.choice(solution)  # Choose a random route
#     if len(route) > 3:  # Ensure there are at least two customers to swap
#         i, j = sorted(random.sample(range(1, len(route) - 1), 2))  # Pick two indices
#         route[i], route[j] = route[j], route[i]
    
#     return solution

def mutate(solution, Q, q):
    """Apply mutation only if the new solution remains valid."""
    for _ in range(5):
        route = random.choice(solution)
        if len(route) > 3:
            i, j = sorted(random.sample(range(1, len(route) - 1), 2))
            route[i], route[j] = route[j], route[i]

            if all(is_valid_route(route, Q, q) for route in solution):
                return solution
    return solution

def fitness(solution, D, Q, q):
    """Calculate fitness based on the total distance of the routes."""

    # solution is valid (doesn't exceed vehicle capacity). fitness = total distance
    if all(is_valid_route(route, Q, q) for route in solution):
        return total_distance(solution, D)
    else:
        return float('inf')  # Return a high cost for invalid solutions

def selection(population, D, Q, q):
    """Select two parents using tournament selection."""
    tournament_size = 5
    parents = []

    # two best individuals are selected as parents for crossover
    # tournament selection - find solution with better fitness hv higher change being selected 
    # while there're some randomness to avoid premature
    for _ in range(2):
        tournament = random.sample(population, tournament_size)
        tournament_fitness = [(ind, fitness(ind, D, Q, q)) for ind in tournament]
        parents.append(min(tournament_fitness, key=lambda x: x[1])[0])
    return parents

def repair_solution(solution, Q, q):
    """Ensure all routes satisfy vehicle capacity constraints by redistributing excess load."""
    new_solution = []
    excess_customers = []
    
    for route in solution:
        load = sum(q[i] for i in route if i != 0)
        if load <= Q:
            new_solution.append(route)
        else:
            valid_route = [0]  # Start at depot
            current_load = 0
            
            for customer in route[1:-1]:  # Exclude depot at start & end
                if current_load + q[customer] <= Q:
                    valid_route.append(customer)
                    current_load += q[customer]
                else:
                    excess_customers.append(customer)  # Store excess customers
            
            valid_route.append(0)  # Return to depot
            new_solution.append(valid_route)
    
    # Try to distribute excess customers to existing routes
    for customer in excess_customers:
        for route in new_solution:
            current_load = sum(q[i] for i in route if i != 0)
            if current_load + q[customer] <= Q:
                route.insert(-1, customer)  # Add before returning to depot
                break
        else:
            # If no existing route can take it, create a new route
            new_solution.append([0, customer, 0])

    return new_solution

# generations = fixed number of generations
# crossover_prob = likelihood that crossover will occur
# mutation_prob = likelihood that mutation will occur in a child solution 
#               (lower focus refining solutions, higher increases exploration)
def solve_cvrp(n, Q, D, q, population_size=100, generations=1000, mutation_prob=0.1, crossover_prob=0.7):
    """Solve CVRP using a Genetic Algorithm."""
    # Initialize population with random solutions
    population = []

    # Ensure the population only contains valid solutions
    while len(population) < population_size:
        candidate = initial_solution(n, Q, D, q)
        if candidate:
            population.append(candidate)
    
    best_solution = None
    best_distance = float('inf')
    
    for _ in range(generations):
        # Evaluate the fitness of all solutions
        population_fitness = [(ind, fitness(ind, D, Q, q)) for ind in population]
        
        # Get the best solution in the current generation
        # current_best_solution = min(population_fitness, key=lambda x: x[1])[0]
        # current_best_distance = fitness(current_best_solution, D, Q, q)
        current_best_solution, current_best_distance = min(population_fitness, key=lambda x: x[1])
        
        if current_best_distance < best_distance:
            best_solution = current_best_solution
            best_distance = current_best_distance
        
        # Selection: Select parents
        parents = selection(population, D, Q, q)
        
        # Create the next generation through crossover and mutation
        next_generation = []
        
        while len(next_generation) < population_size:
            
            # Perform crossover to create a new child
            if random.random() < crossover_prob:
                child = crossover(parents[0], parents[1], Q, q)
            else:
                # If no crossover, just duplicate one of the parents
                child = parents[0]
            
            # Apply mutation with probability mutation_prob
            if random.random() < mutation_prob:
                child = mutate(child, Q, q)
            
            if all(is_valid_route(route, Q, q) for route in child):
                next_generation.append(child)
        
        # Prevent empty population
        if next_generation:
            population = next_generation
    
    return best_solution # Only return the best valid solution

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

