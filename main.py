import random

import networkx as nx
import matplotlib.pyplot as plt

G = nx.erdos_renyi_graph(10, 0.7, seed=42)

COLOR_NAMES = ["red", "green", "blue", "yellow", "orange", "purple", "cyan", "magenta"]
colorCount = 1
colorCountMax = 8
conflicts = 0
iterationCount = 1000
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
for i in range(1, len(conflict_history) // iterationCount + 1):
    plt.axvline(x=i * iterationCount, color="gray", linestyle=":", linewidth=0.8,
                label=f"colour count={i+1}")
plt.xlabel("Iteration")
plt.ylabel("Conflicts")
plt.title("Conflicts over time")
plt.legend()
plt.show()