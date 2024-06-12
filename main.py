import tkinter as tk
from tkinter import Canvas, messagebox
from tkinter import ttk
import random
import time
from itertools import product
import math
import threading

lock = threading.Lock()

def create_random_graph(num_nodes, edge_prob):
    graph = {i: [] for i in range(num_nodes)}
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            if random.random() < edge_prob:
                graph[i].append(j)
                graph[j].append(i)

    for i in range(num_nodes):
        if not graph[i]:
            j = random.choice([x for x in range(num_nodes) if x != i])
            graph[i].append(j)
            graph[j].append(i)

    return graph


def create_graph_from_input(graph_input):
    graph = {}
    lines = graph_input.strip().split("\n")
    for line in lines:
        parts = line.split()
        node = int(parts[0])
        neighbors = list(map(int, parts[1:]))
        graph[node] = neighbors
    return graph


def create_mu(graph):
    return {node: random.randint(1, len(graph)) for node in graph}


def is_mu_colorable(graph, mu, coloring):
    for node in graph:
        if coloring.get(node, 0) > mu[node]:
            return False
        for neighbor in graph[node]:
            if neighbor in coloring and coloring[node] == coloring[neighbor]:
                return False
    return True


def exhaustive_mu_coloring(graph, mu):
    nodes = list(graph.keys())
    max_colors = max(mu.values())
    all_colorings = product(range(1, max_colors + 1), repeat=len(nodes))
    for colors in all_colorings:
        coloring = {nodes[i]: colors[i] for i in range(len(nodes))}
        if is_mu_colorable(graph, mu, coloring):
            return coloring
    return None


def greedy_mu_coloring(graph, mu):
    nodes = sorted(graph, key=lambda x: len(graph[x]), reverse=True)
    coloring = {}
    for node in nodes:
        available_colors = set(range(1, mu[node] + 1))
        used_colors = {coloring.get(neighbor) for neighbor in graph[node] if neighbor in coloring}
        for color in available_colors:
            if color not in used_colors:
                coloring[node] = color
                break
    if len(coloring) == len(graph) and is_mu_colorable(graph, mu, coloring):
        return coloring
    return None


def draw_graph(canvas, graph, coloring, mu, width=600, height=600):
    canvas.delete("all")
    num_nodes = len(graph)
    angle_step = 2 * math.pi / num_nodes
    radius = 200
    center_x = width // 2
    center_y = height // 2

    node_positions = {}
    for i in range(num_nodes):
        angle = i * angle_step
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)
        node_positions[i] = (x, y)

    for node, neighbors in graph.items():
        x1, y1 = node_positions[node]
        for neighbor in neighbors:
            x2, y2 = node_positions[neighbor]
            canvas.create_line(x1, y1, x2, y2, fill="black")

    color_array = [
        "#FF5733", "#33FF57", "#3357FF", "#F333FF", "#57FF33", "#5733FF", "#FF3357", "#33FFF3",
        "#F3FF33", "#FF33F3", "#33F3FF", "#F33357", "#5733F3", "#57F333", "#33FF33", "#FF5733",
        "#FFA500", "#800080", "#00FFFF", "#0000FF", "#FF00FF", "#FFFF00", "#00FF00", "#FF0000",
        "#C0C0C0", "#808080", "#800000", "#808000", "#008000", "#008080", "#000080"
    ]

    if coloring:
        for node, (x, y) in node_positions.items():
            if node in coloring:
                color_index = (coloring[node] - 1) % len(color_array)
                color = color_array[color_index]
                canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill=color, outline="black")
                canvas.create_text(x, y, text=f"{color_index + 1}\nµ={mu[node]}", font=("Helvetica", 10))
            else:
                canvas.create_text(x, y, text="X", fill="red", font=("Helvetica", 10))
    else:
        canvas.create_text(center_x, center_y, text="Graph is not µ-colorable", fill="red", font=("Helvetica", 16))


def run_exhaustive_search(graph, mu_function_exhaustive):
    with lock:
        start_time = time.perf_counter()
        exhaustive_coloring = exhaustive_mu_coloring(graph, mu_function_exhaustive)
        exhaustive_time = time.perf_counter() - start_time

        if exhaustive_coloring:
            result_text_exhaustive.set(f"Exhaustive Search\n{exhaustive_coloring}\nTime: {exhaustive_time:.2f} seconds")
            draw_graph(canvas_exhaustive, graph, exhaustive_coloring, mu_function_exhaustive)
        else:
            result_text_exhaustive.set(f"Exhaustive Search: Not µ-colorable\nTime: {exhaustive_time:.2f} seconds")
            draw_graph(canvas_exhaustive, graph, None, mu_function_exhaustive)

        progress_exhaustive.stop()
        progress_exhaustive.pack_forget()


def run_coloring_algorithms():
    with lock:
        graph_input = text_input.get("1.0", tk.END).strip()

        if graph_input:
            try:
                graph = create_graph_from_input(graph_input)
            except Exception as e:
                messagebox.showerror("Input Error", f"Invalid graph input format.\n{e}")
                return
        else:
            num_nodes = random.randint(5, 7)
            edge_prob = 0.5
            graph = create_random_graph(num_nodes, edge_prob)

        mu_function_exhaustive = create_mu(graph)
        mu_function_greedy = create_mu(graph)

        start_time = time.perf_counter()
        greedy_coloring = greedy_mu_coloring(graph, mu_function_greedy)
        greedy_time = (time.perf_counter() - start_time) * 1000  # Convert to milliseconds

        if greedy_coloring:
            result_text_greedy.set(f"Greedy Algorithm\n{greedy_coloring}\nTime: {greedy_time:.2f} milliseconds")
            draw_graph(canvas_greedy, graph, greedy_coloring, mu_function_greedy)
        else:
            result_text_greedy.set(f"Greedy Algorithm: Not µ-colorable\nTime: {greedy_time:.2f} milliseconds")
            draw_graph(canvas_greedy, graph, None, mu_function_greedy)

        edges = [(i, j) for i in graph for j in graph[i] if i < j]
        graph_info.set(f"Number of nodes: {len(graph)}\n"
                       f"Edges: {edges}\n"
                       f"Exhaustive µ function: {mu_function_exhaustive}\n"
                       f"Greedy µ function: {mu_function_greedy}\n")

        progress_exhaustive.pack()
        progress_greedy.pack()
        progress_exhaustive.start(10)
        progress_greedy.start(10)

        # Run exhaustive search in a separate thread
        exhaustive_thread = threading.Thread(target=run_exhaustive_search, args=(graph, mu_function_exhaustive))
        exhaustive_thread.start()

        progress_greedy.stop()
        progress_greedy.pack_forget()


root = tk.Tk()
root.title("µ-Coloring Graph")

frame_greedy = tk.Frame(root)
frame_greedy.pack(side=tk.LEFT)

frame_exhaustive = tk.Frame(root)
frame_exhaustive.pack(side=tk.RIGHT)

canvas_greedy = Canvas(frame_greedy, width=600, height=600)
canvas_greedy.pack()

canvas_exhaustive = Canvas(frame_exhaustive, width=600, height=600)
canvas_exhaustive.pack()

progress_greedy = ttk.Progressbar(frame_greedy, orient="horizontal", mode="indeterminate")
progress_greedy.pack()

progress_exhaustive = ttk.Progressbar(frame_exhaustive, orient="horizontal", mode="indeterminate")
progress_exhaustive.pack()

result_text_greedy = tk.StringVar()
result_label_greedy = tk.Label(frame_greedy, textvariable=result_text_greedy, wraplength=300, justify="center")
result_label_greedy.pack()

result_text_exhaustive = tk.StringVar()
result_label_exhaustive = tk.Label(frame_exhaustive, textvariable=result_text_exhaustive, wraplength=300,
                                   justify="center")
result_label_exhaustive.pack()

graph_info = tk.StringVar()
graph_info_label = tk.Label(root, textvariable=graph_info, wraplength=650, justify="left")
graph_info_label.pack(pady=20)  # Adding padding to move the label down

text_input = tk.Text(root, height=10, width=50)
text_input.pack(pady=10)
text_input.insert(tk.END, "0 1 2\n1 0 2\n2 0 1")  # Example graph input

run_button = tk.Button(root, text="Generate Graph and Perform µ-Coloring", command=run_coloring_algorithms)
run_button.pack()

root.mainloop()
