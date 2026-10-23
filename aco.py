#TSP
import random

roads = {
    "A": {"B": 4, "C": 2},
    "B": {"A": 4, "C": 1, "D": 5},
    "C": {"A": 2, "B": 1, "D": 8, "E": 10},
    "D": {"B": 5, "C": 8, "E": 2},
    "E": {"C": 10, "D": 2}
}

cities = list(roads.keys())

ants = 10
iterations = 50
alpha = 1       # Pheromone importance
beta = 2        # Distance importance 
evaporation = 0.5
Q = 100

pheromone = {}

for city in cities:
    for next_city in roads[city]:
        pheromone[(city, next_city)] = 1.0

def route_distance(route):
    total = 0

    for i in range(len(route) - 1):
        total += roads[route[i]][route[i + 1]]

    return total

def choose_city(current, unvisited):
    probabilities = []

    for city in unvisited:
        p = pheromone[(current, city)] ** alpha
        d = (1 / roads[current][city]) ** beta
        probabilities.append(p * d)

    total = sum(probabilities)
    probabilities = [p / total for p in probabilities]

    return random.choices(
        unvisited, weights=probabilities, k=1
    )[0]

source = input("Enter source city (A, B, C, D, E): ").upper()
destination = input("Enter destination city (A, B, C, D, E): ").upper()

if source not in roads or destination not in roads:
    print("Invalid city!")
elif source == destination:
    print("Source and destination are the same.")
else:
    best_route = None
    best_distance = float("inf")

    for iteration in range(iterations):
        all_routes = []

        for ant in range(ants):
            route = [source]
            current = source
            unvisited = [c for c in cities if c != source]

            while current != destination:
                possible = [
                    c for c in unvisited
                    if c in roads[current]
                ]

                if not possible:
                    break

                next_city = choose_city(current, possible)
                route.append(next_city)
                unvisited.remove(next_city)
                current = next_city

            if current == destination:
                dist = route_distance(route)
                all_routes.append((route, dist))

                if dist < best_distance:
                    best_route = route.copy()
                    best_distance = dist

        # Evaporate pheromones
        for edge in pheromone:
            pheromone[edge] *= (1 - evaporation)

        # Deposit pheromones on successful routes
        for route, dist in all_routes:
            deposit = Q / dist

            for i in range(len(route) - 1):
                edge = (route[i], route[i + 1])
                reverse_edge = (route[i + 1], route[i])

                pheromone[edge] += deposit
                pheromone[reverse_edge] += deposit

    if best_route:
        print("Best route:", " -> ".join(best_route))
        print("Total distance:", best_distance)
    else:
        print("No route found between these cities.")
