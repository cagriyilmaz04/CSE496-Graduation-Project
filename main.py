import tkinter as tk
import math
import random
import itertools

def mu_coloring(graph, mu):
    colors = {}
    for vertex in sorted(graph, key=lambda x: mu[x]):
        available_colors = set(range(mu[vertex] + 1))
        used_colors = {colors[neigh] for neigh in graph[vertex] if neigh in colors}
        for color in sorted(available_colors):
            if color not in used_colors:
                colors[vertex] = color
                break
    return colors

def exhaustive_mu_coloring(graph, mu):
    nodes = list(graph.keys())
    best_coloring = None

    # Tüm olası renklendirmeleri dener
    for num_colors in range(1, len(nodes) + 1):
        for colors in itertools.product(range(num_colors), repeat=len(nodes)):
            valid = True
            for u, v in itertools.combinations(nodes, 2):
                if v in graph[u] and colors[nodes.index(u)] == colors[nodes.index(v)]:
                    valid = False
                    break
            if valid:
                best_coloring = {nodes[i]: colors[i] for i in range(len(nodes))}
                return best_coloring
    return best_coloring

def color_palette():
    return ["#F0A3FF", "#0075DC", "#993F00", "#4C005C", "#191919", "#005C31", "#2BCE48", "#FFCC99",
            "#808080", "#94FFB5", "#8F7C00", "#9DCC00", "#C20088", "#003380", "#FFA405", "#FFA8BB",
            "#426600", "#FF0010", "#5EF1F2", "#00998F", "#E0FF66", "#740AFF", "#990000", "#FFFF80",
            "#FFFF00", "#FF5005"]

def draw_graph(canvas, graph, colors, node_color=None, edge_color='black', text_color='white', padding=50):
    canvas.delete("all")
    radius = 20
    positions = {}
    width = int(canvas['width'])
    height = int(canvas['height'])
    center_x, center_y = width // 2, height // 2
    circle_distance = min(center_x, center_y) - padding  # Padding değeri eklendi
    edge_width = 2
    text_offset = 10

    num_vertices = len(graph)
    angle = 2 * math.pi / num_vertices
    palette = color_palette()

    for i in range(num_vertices):
        x = center_x + circle_distance * math.cos(i * angle)
        y = center_y + circle_distance * math.sin(i * angle)
        positions[i] = (x, y)
        color = palette[colors[i] % len(palette)] if node_color is None else node_color
        canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill=color, outline='black')
        canvas.create_text(x, y - radius - text_offset, text=str(i), fill=text_color, font=('Arial', 12, 'bold'))

    for v in graph:
        for u in graph[v]:
            if v < u:  # Her kenarı bir kere çizmek için
                canvas.create_line(
                    positions[v][0], positions[v][1],
                    positions[u][0], positions[u][1],
                    fill=edge_color, width=edge_width
                )

def generate_random_graph(num_vertices):
    graph = {i: [] for i in range(num_vertices)}
    edges = set()
    for node in range(num_vertices):
        while True:
            neighbor = random.randint(0, num_vertices - 1)
            if node != neighbor and (node, neighbor) not in edges and (neighbor, node) not in edges:
                graph[node].append(neighbor)
                graph[neighbor].append(node)
                edges.add((node, neighbor))
                break

    for _ in range(num_vertices):  # Ekstra rastgele bağlantılar ekle
        u = random.randint(0, num_vertices - 1)
        v = random.randint(0, num_vertices - 1)
        if u != v and (u, v) not in edges and (v, u) not in edges:
            graph[u].append(v)
            graph[v].append(u)
            edges.add((u, v))

    return graph

def generate_random_mu(graph):
    mu = {vertex: random.randint(1, len(graph) // 2) for vertex in graph}
    return mu

def show_greedy_coloring():
    num_vertices = random.randint(5, 10)
    graph = generate_random_graph(num_vertices)
    mu = generate_random_mu(graph)
    colors = mu_coloring(graph, mu)
    draw_graph(canvas, graph, colors)

def show_exhaustive_coloring():
    num_vertices = random.randint(5, 10)
    graph = generate_random_graph(num_vertices)
    mu = generate_random_mu(graph)
    colors = exhaustive_mu_coloring(graph, mu)
    draw_graph(canvas, graph, colors)

root = tk.Tk()
root.title("Graph Coloring")

root.configure(bg='gray')

canvas = tk.Canvas(root, width=400, height=400, bg='gray')
canvas.pack(expand=True, fill='both')

greedy_button = tk.Button(root, text="Greedy Renklendir", command=show_greedy_coloring)
greedy_button.pack()

exhaustive_button = tk.Button(root, text="Exhaustive Search Renklendir", command=show_exhaustive_coloring)
exhaustive_button.pack()

root.mainloop()
