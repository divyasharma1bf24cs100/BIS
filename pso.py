
import numpy as np

cities = np.array([
    [0, 0],
    [2, 3],
    [5, 2],
    [6, 6],
    [8, 3]
])

n = len(cities)

def distance(a, b):
    return np.linalg.norm(cities[a] - cities[b])

def get_route(position):
    order = np.argsort(position)
    return [0] + (order + 1).tolist() + [0]

def fitness(position):
    route = get_route(position)
    total = 0

    for i in range(len(route) - 1):
        total += distance(route[i], route[i + 1])

    return total

particles = 30
iterations = 100
w = 0.7
c1 = 1.5
c2 = 1.5

dimensions = n - 1

positions = np.random.rand(particles, dimensions)
velocities = np.random.rand(particles, dimensions) * 0.1

pbest = positions.copy()
pbest_scores = np.array([fitness(p) for p in positions])

best_index = np.argmin(pbest_scores)
gbest = pbest[best_index].copy()
gbest_score = pbest_scores[best_index]

for iteration in range(iterations):

    for i in range(particles):

        r1 = np.random.rand(dimensions)
        r2 = np.random.rand(dimensions)

        velocities[i] = (
            w * velocities[i]
            + c1 * r1 * (pbest[i] - positions[i])
            + c2 * r2 * (gbest - positions[i])
        )

        positions[i] += velocities[i]

        score = fitness(positions[i])

        if score < pbest_scores[i]:
            pbest[i] = positions[i].copy()
            pbest_scores[i] = score

    best_index = np.argmin(pbest_scores)

    if pbest_scores[best_index] < gbest_score:
        gbest = pbest[best_index].copy()
        gbest_score = pbest_scores[best_index]

best_route = get_route(gbest)

print("Best Route:", " -> ".join(map(str, best_route)))
print("Shortest Distance:", round(gbest_score, 2))
