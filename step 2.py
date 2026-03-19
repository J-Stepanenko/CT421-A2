import random
import networkx as nx
import matplotlib.pyplot as plt

G = nx.erdos_renyi_graph(10, 0.7, seed=42)

COLOR_NAMES = ["red", "green", "blue", "yellow", "orange", "purple", "cyan", "magenta"]
colorCount = 1
colorCountMax = 8
pop_size = 10
generations = 20
mutation_rate = 0.1
conflict_history = []


def random_individual(num_nodes, k):
    return [random.randint(0, k - 1) for _ in range(num_nodes)]

# Positive values mean conflicts
def fitness(individual, edges):
    return sum(1 for u, v in edges if individual[u] == individual[v])

def tournament_select(population, fitnesses, tournament_size=3):
    candidates = random.sample(list(zip(population, fitnesses)), tournament_size)
    return min(candidates, key=lambda x: x[1])[0]

def crossover(parent1, parent2):
    point = random.randint(1, len(parent1) - 1)
    return parent1[:point] + parent2[point:], parent2[:point] + parent1[point:]

def mutate(individual, k):
    return [
        random.randint(0, k - 1) if random.random() < mutation_rate else gene
        for gene in individual
    ]

edges = list(G.edges())
num_nodes = G.number_of_nodes()
is_valid = False
best_individual = None

while colorCount <= colorCountMax:
    print("Color count: ", colorCount)
    population = [random_individual(num_nodes, colorCount) for _ in range(pop_size)]

    for gen in range(generations):
        fitnesses = [fitness(idx, edges) for idx in population]
        best_fitness = min(fitnesses)
        conflict_history.append(best_fitness)
        print("Generation: ", gen, " Best conflicts: ", best_fitness)

        if best_fitness == 0:
            best_individual = population[fitnesses.index(0)]
            is_valid = True
            print("Correct coloring found with color count: ", colorCount)
            break

        new_population = []
        best_idx = fitnesses.index(best_fitness)
        new_population.append(population[best_idx])

        while len(new_population) < pop_size:
            p1 = tournament_select(population, fitnesses)
            p2 = tournament_select(population, fitnesses)
            c1, c2 = crossover(p1, p2)
            c1 = mutate(c1, colorCount)
            c2 = mutate(c2, colorCount)
            new_population.append(c1)
            if len(new_population) < pop_size:
                new_population.append(c2)

        population = new_population

    if is_valid:
        break
    colorCount += 1

if best_individual is None:
    fitnesses = [fitness(ind, edges) for ind in population]
    best_individual = population[fitnesses.index(min(fitnesses))]

coloring_result = {node: best_individual[node] for node in G.nodes()}
conflicts = fitness(best_individual, edges)
color_list = [COLOR_NAMES[coloring_result[node]] for node in sorted(coloring_result)]

print(f"\nColoring valid: {is_valid}")
print(f"Coloring conflicts: {conflicts}")

nx.draw_networkx(G, pos=nx.spring_layout(G), node_color=color_list, with_labels=True)
plt.show()

plt.figure()
plt.plot(conflict_history)
for i in range(1, len(conflict_history) // generations + 1):
    plt.axvline(x=i * generations, color="gray", linestyle=":", linewidth=0.8,
                label=f"colour count={i+1}")
plt.xlabel("Generation")
plt.ylabel("Best Conflicts")
plt.title("GA Graph Colouring - Conflicts over time")
plt.legend()
plt.show()