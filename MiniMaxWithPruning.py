# import math as math
import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox


class Node:
    def __init__(self, label, is_max=True):
        self.label = label
        self.value = None
        self.is_max = is_max
        self.children = []
        self.coords = (0, 0)

class MinimaxTreeVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Minimax Tree Visualizer")
        self.canvas_width = 800
        self.canvas_height = 600
        self.total_nodes = 0
        self.nodes = []

        self.depth_label = tk.Label(root, text="Depth of Minimax Tree:")
        self.depth_label.pack()
        self.depth_entry = tk.Entry(root)
        self.depth_entry.pack()

        self.create_tree_button = tk.Button(root, text="Create Minimax Tree", command=self.create_tree)
        self.create_tree_button.pack()

        self.assign_values_button = tk.Button(root, text="Assign Terminal Node Values", command=self.prompt_terminal_node_values)
        self.assign_values_button.pack()

        self.calculate_minimax_button = tk.Button(root, text="Calculate Minimax Values", command=self.calculate_minimax_values)
        self.calculate_minimax_button.pack()

        self.canvas_frame = tk.Frame(root)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.canvas_frame, width=self.canvas_width, height=self.canvas_height, bg="white")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.x_scrollbar = tk.Scrollbar(self.canvas_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.y_scrollbar = tk.Scrollbar(self.canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.config(xscrollcommand=self.x_scrollbar.set, yscrollcommand=self.y_scrollbar.set)

        # Draw initial symbols
        self.draw_initial_symbols()

    def draw_initial_symbols(self):
        self.canvas.create_oval(20, 20, 60, 60, fill="lightblue")
        self.canvas.create_text(120, 40, text="Max Node Player", fill="black")
        self.canvas.create_rectangle(20, 80, 60, 120, fill="lightgreen")
        self.canvas.create_text(120, 100, text="Min Node Player", fill="black")

    def create_tree(self):
        self.canvas.delete("all")
        self.draw_initial_symbols()
        self.total_nodes = 0
        self.nodes = []
        depth = int(self.depth_entry.get())
        if depth > 5:
            self.canvas_width = 200 * depth
            self.canvas_height = 150 * depth
            self.canvas.config(width=self.canvas_width, height=self.canvas_height)
        self.draw_tree(depth, self.canvas_width / 2, 50, self.canvas_width / 4)

    def draw_tree(self, depth, x, y, delta_x, is_max=True):
        if depth == 0:
            return
        self.total_nodes += 1
        node_label = self.get_unique_label()
        node = Node(node_label, is_max)
        node.coords = (x, y)
        self.nodes.append(node)
        if is_max:
            node_shape = self.canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill="lightblue")
        else:
            node_shape = self.canvas.create_rectangle(x - 20, y - 20, x + 20, y + 20, fill="lightgreen")
        self.canvas.create_text(x, y, text=str(node_label), fill="black")
        offset_y = 100
        child_delta_x = delta_x / 2
        if depth > 1:
            child1 = self.draw_tree(depth - 1, x - delta_x, y + offset_y, child_delta_x, not is_max)
            child2 = self.draw_tree(depth - 1, x + delta_x, y + offset_y, child_delta_x, not is_max)
            node.children.extend([child1, child2])
            self.canvas.create_line(x, y + 20, x - delta_x, y + offset_y - 20)
            self.canvas.create_line(x, y + 20, x + delta_x, y + offset_y - 20)
        return node

    # def prompt_terminal_node_values(self):
    #     terminal_nodes = [node for node in self.nodes if not node.children]
    #     for node in terminal_nodes:
    #         value = simpledialog.askstring("Terminal Node Value", f"Enter value for node {node.label}:")
    #         node.value = int(value)
    #     _, pruned_nodes = self.compute_minimax_values_recursively(self.nodes[0])
    #     self.redraw_tree_with_minimax(pruned_nodes)

    def prompt_terminal_node_values(self):
        terminal_nodes = [node for node in self.nodes if not node.children]
        for node in terminal_nodes:
            value = None
            while value is None:
                try:
                    value = int(simpledialog.askstring("Terminal Node Value", f"Enter value for node {node.label}:"))
                except ValueError:
                    messagebox.showerror("Invalid Input", "Please enter a valid number.")
                    print("Invalid input. Please enter a valid number.")
            node.value = value
        _, pruned_nodes = self.compute_minimax_values_recursively(self.nodes[0])
        self.redraw_tree_with_minimax(pruned_nodes)



    def calculate_minimax_values(self):
        _, pruned_nodes = self.compute_minimax_values_recursively(self.nodes[0])
        self.redraw_tree_with_minimax(pruned_nodes)

    def compute_minimax_values_recursively(self, node, alpha=float('-inf'), beta=float('inf')):
        pruned_nodes = []
        if not node.children:
            return node.value, pruned_nodes
        if node.is_max:
            max_value = float('-inf')
            for child in node.children:
                value, pruned = self.compute_minimax_values_recursively(child, alpha, beta)
                pruned_nodes.extend(pruned)
                max_value = max(max_value, value)
                alpha = max(alpha, value)
                if beta <= alpha:
                    pruned = node.children[node.children.index(child)+1:]
                    pruned_nodes.extend(pruned)  # Add unexplored nodes to pruned_nodes
                    print(f"Pruned branches: {[node.label for node in pruned]}")
                    break  # beta cut-off
            node.value = max_value
        else:
            min_value = float('inf')
            for child in node.children:
                value, pruned = self.compute_minimax_values_recursively(child, alpha, beta)
                pruned_nodes.extend(pruned)
                min_value = min(min_value, value)
                beta = min(beta, value)
                if beta <= alpha:
                    pruned = node.children[node.children.index(child)+1:]
                    pruned_nodes.extend(pruned)  # Add unexplored nodes to pruned_nodes
                    print(f"Pruned branches: {[node.label for node in pruned]}")
                    break  # alpha cut-off
            node.value = min_value
        return node.value, pruned_nodes

    def redraw_tree_with_minimax(self, pruned_nodes):
        self.canvas.delete("all")
        self.draw_initial_symbols()
        for node in self.nodes:
            x, y = node.coords
            if node.is_max:
                color = "lightblue"
                self.canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill=color)
            else:
                color = "lightgreen"
                self.canvas.create_rectangle(x - 20, y - 20, x + 20, y + 20, fill=color)  # Change this line
            if node in pruned_nodes:
                color = "red"
                self.canvas.create_line(x-10, y-10, x+10, y+10, fill=color, width=4)
                self.canvas.create_line(x-10, y+10, x+10, y-10, fill=color, width=4)

            self.canvas.create_text(x, y, text=str(node.label), fill="black")
            if node.value is not None:
                self.canvas.create_text(x, y + 30, text=str(node.value), fill="black")
            for child in node.children:
                if child in pruned_nodes:
                    color = "red"
                    # self.canvas.create_line(x-15, y, x+15, y, fill=color, width=4)
                    # self.canvas.create_line(x, y-15, x, y+15, fill=color, width=4)    
                    # width = 4
                else:
                    color = "black"
                    # width = 1
                cx, cy = child.coords
                self.canvas.create_line(x, y + 20, cx, cy - 20, fill=color, width=2)
                if child in pruned_nodes:
                    mid_x = (x + cx) / 2
                    mid_y = (y + cy) / 2
                    self.canvas.create_line(mid_x - 10, mid_y + 10, mid_x + 10, mid_y - 10, width=2, fill="red")
                    self.canvas.create_line(mid_x - 8, mid_y + 16, mid_x + 12, mid_y - 4, width=2, fill="red")

                
    def get_unique_label(self):
        label = ""
        count = len(self.nodes) + 1
        while count:
            count, remainder = divmod(count - 1, 26)
            label = chr(65 + remainder) + label
        return label + str((len(self.nodes) // 26) + 1)

def main():
    root = tk.Tk()
    app = MinimaxTreeVisualizer(root)
    root.mainloop()

if __name__ == "__main__":
    main()