import tkinter as tk
import networkx as nx
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import random
import itertools


class GraphColoringApp:
    def __init__(self, master):
        self.master = master
        master.title("μ-Coloring Uygulaması")

        self.graph_frame = tk.Frame(master)
        self.graph_frame.pack(side=tk.LEFT)


        self.greedy_button = tk.Button(master, text="Greedy Renklendir", command=self.apply_greedy_coloring)
        self.greedy_button.pack(side=tk.TOP)

        self.exhaustive_button = tk.Button(master, text="Exhaustive Search Renklendir",
                                           command=self.apply_exhaustive_coloring)
        self.exhaustive_button.pack(side=tk.TOP)

        self.info_label = tk.Label(master, text="")
        self.info_label.pack(side=tk.BOTTOM)


        self.random_graph()


        self.fig, self.ax = plt.subplots(figsize=(5, 5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
        self.canvas.get_tk_widget().pack()

        self.draw_graph()

    def random_graph(self):
        num_vertices = random.randint(5, 10)
        self.G = nx.Graph()
        self.G.add_nodes_from(range(num_vertices))


        edges = set()
        for node in self.G.nodes():
            while True:
                neighbor = random.randint(0, num_vertices - 1)
                if node != neighbor:
                    edges.add((node, neighbor))
                    break

        for _ in range(num_vertices):  # Ekstra rastgele bağlantılar ekle
            u = random.randint(0, num_vertices - 1)
            v = random.randint(0, num_vertices - 1)
            if u != v:
                edges.add((u, v))

        self.G.add_edges_from(edges)
        self.pos = nx.spring_layout(self.G)

    def draw_graph(self, colors=None):
        self.ax.clear()
        nx.draw(self.G, self.pos, with_labels=True, node_color=colors, node_size=500, font_size=10, ax=self.ax)
        self.canvas.draw()

    def apply_greedy_coloring(self):
        colors = self.greedy_coloring()
        self.draw_graph(colors)
        self.info_label.config(text=f"Greedy algoritması ile renklendirildi. Kullanılan renk sayısı: {len(set(colors))}")

    def apply_exhaustive_coloring(self):
        colors = self.exhaustive_coloring()
        if colors:
            self.draw_graph(colors)
            self.info_label.config(text=f"Exhaustive search ile renklendirildi. Kullanılan renk sayısı: {len(set(colors))}")
        else:
            self.info_label.config(text="Exhaustive search ile geçerli bir renklendirme bulunamadı.")

    def greedy_coloring(self):
        colors = {}
        for node in self.G.nodes():

            neighbor_colors = {colors[neighbor] for neighbor in self.G.neighbors(node) if neighbor in colors}

            for color in range(len(self.G)):
                if color not in neighbor_colors:
                    colors[node] = color
                    break
        return [colors[node] for node in self.G.nodes()]

    def exhaustive_coloring(self):
        nodes = list(self.G.nodes())
        min_colors = len(nodes)
        best_coloring = None


        upper_bound = min(len(nodes), 4)
        found_solution = False


        for num_colors in range(1, upper_bound + 1):
            for colors in itertools.product(range(num_colors), repeat=len(nodes)):
                valid = True
                for u, v in self.G.edges():
                    if colors[nodes.index(u)] == colors[nodes.index(v)]:
                        valid = False
                        break
                if valid:
                    best_coloring = colors
                    found_solution = True
                    break
            if found_solution:
                break

        return best_coloring

root = tk.Tk()
app = GraphColoringApp(root)
root.mainloop()
