
import random
# Symptoms: Fever, Cough, Headache
patient = [1, 1, 0]

population = [
    [random.randint(0, 1) for i in range(3)]
    for j in range(6)
]

def fitness(chromosome):
    return sum(
        chromosome[i] == patient[i]
        for i in range(3)
    )

for generation in range(10):

    population.sort(key=fitness, reverse=True)

    parent1 = population[0]
    parent2 = population[1]

    child = parent1[:2] + parent2[2:]

    if random.random() < 0.2:
        i = random.randint(0, 2)
        child[i] = 1 - child[i]

    population[-1] = child

population.sort(key=fitness, reverse=True)
best = population[0]

print("Patient Symptoms:", patient)
print("Best Chromosome:", best)
print("Fitness:", fitness(best))

if fitness(best) == 3:
    print("Disease pattern matched")
else:
    print("Disease pattern not fully matched")
