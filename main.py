import random

import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()

G.add_nodes_from(range(5))

G.add_edges_from([
    (0, 1),
    (0, 2),
    (1, 3),
    (1, 4),
    (2, 3),
    (2, 4),
    (3, 4),
])

COLOR_NAMES = ["red", "green", "blue", "yellow", "orange", "purple", "cyan", "magenta"]
colorCount = 1
colorCountMax = 4
conflicts = 0
iterationCount = 100
conflict_history = []


def colourGraph(graph, colorsAvailable):
    colors = {}
    for node in graph.nodes():
        color = random.randint(0, colorsAvailable - 1)
        colors[node] = color
    return colors

coloring_result = {}
is_valid = False
while colorCount <= colorCountMax:
    print("Color count: ", colorCount)
    for iteration in range(iterationCount):
        print("Iteration: ", iteration)
        coloring_result = colourGraph(G, colorCount)

        conflicts = sum(
            coloring_result[u] == coloring_result[v]
            for u, v in G.edges()
        )
        conflict_history.append(conflicts)

        is_valid = conflicts == 0
        if is_valid:
            print("Correct coloring found with color count: ", colorCount)
            break
        print(is_valid)
    if (is_valid): break
    colorCount += 1

color_list = []
for vertex, color in sorted(coloring_result.items()):
    name = COLOR_NAMES[color]
    color_list.append(name)


print(f"\nColoring valid: {is_valid}")
print(f"Coloring conflicts: {conflicts}")


nx.draw_networkx(G, pos=nx.spring_layout(G), node_color=color_list, with_labels=True)
plt.show()
plt.figure()
plt.plot(conflict_history)
plt.xlabel("Iteration")
plt.ylabel("Conflicts")
plt.title("Conflicts over time")
plt.show()