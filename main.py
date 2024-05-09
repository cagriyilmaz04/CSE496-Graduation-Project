
import tkinter as tk
import math

def mu_coloring(graph, mu):
    colors = {}
    for vertex in sorted(graph, key=lambda x: mu[x]):  # mu değerine göre düğümleri sırala
        available_colors = set(range(mu[vertex] + 1))  # Her düğüm için uygun renk aralığı
        used_colors = {colors[neigh] for neigh in graph[vertex] if neigh in colors}
        for color in sorted(available_colors):  # Kullanılabilir renkler arasında dolaş
            if color not in used_colors:
                colors[vertex] = color
                break
    return colors

def color_palette():
    # Renk paleti
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
        # Düğümleri çiz
        canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill=color, outline='black')
        # Metin etiketlerini düğümlerin hemen üstüne çiz
        canvas.create_text(x, y - radius - text_offset, text=str(i), fill=text_color, font=('Arial', 12, 'bold'))

    # Kenarları çiz
    for v in graph:
        for u in graph[v]:
            if v < u:  # Her kenarı bir kere çizmek için
                canvas.create_line(
                    positions[v][0], positions[v][1],
                    positions[u][0], positions[u][1],
                    fill=edge_color, width=edge_width
                )

def show_coloring():
    graph = {
        0: [1, 2],
        1: [0, 3],
        2: [0, 3],
        3: [1, 2]
    }
    mu = {
        0: 1,  # Düğüm 0 için maksimum renk 1
        1: 1,  # Düğüm 1 için maksimum renk 1
        2: 1,  # Düğüm 2 için maksimum renk 1
        3: 1  # Düğüm 3 için maksimum renk 1
    }
    colors = mu_coloring(graph, mu)
    draw_graph(canvas, graph, colors)

root = tk.Tk()
root.title("Graph Coloring")

# Pencere arka plan rengini belirle
root.configure(bg='gray')

canvas = tk.Canvas(root, width=400, height=400, bg='gray')  # Arka plan rengi burada belirlendi
canvas.pack(expand=True, fill='both')  # Canvas'ı genişlet ve tam boyuta uydur

color_button = tk.Button(root, text="Color Graph", command=show_coloring)
color_button.pack()

root.mainloop()


