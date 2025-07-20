import tkinter as tk
import random

class GameOfLife:
    def __init__(self, master):
        self.master = master
        self.master.title("Game of Life")
        
        self.grid_size = 20
        self.cell_size = 20
        self.canvas = tk.Canvas(master, width=self.grid_size * self.cell_size, height=self.grid_size * self.cell_size, bg="lightgray")
        self.canvas.pack()
        
        self.grid = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        
        self.canvas.bind("<Button-1>", self.toggle_cell)
        
        self.start_button = tk.Button(master, text="Start", command=self.start, bg="green", fg="white")
        self.start_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.stop_button = tk.Button(master, text="Stop", command=self.stop, bg="red", fg="white")
        self.stop_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.reset_button = tk.Button(master, text="Reset", command=self.reset, bg="blue", fg="white")
        self.reset_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.random_button = tk.Button(master, text="Random", command=self.fill_random, bg="orange", fg="white")
        self.random_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.counter_label = tk.Label(master, text="Alive Cells: 0", font=("Arial", 14))
        self.counter_label.pack(side=tk.LEFT, padx=10)
        
        self.running = False
        self.update_id = None

    def toggle_cell(self, event):
        x, y = event.x // self.cell_size, event.y // self.cell_size
        self.grid[y][x] = 1 - self.grid[y][x]  # Toggle cell state
        self.draw_grid()
        self.update_counter()

    def draw_grid(self):
        self.canvas.delete("all")
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                color = "black" if self.grid[y][x] == 1 else "white"
                self.canvas.create_rectangle(x * self.cell_size, y * self.cell_size,
                                              (x + 1) * self.cell_size, (y + 1) * self.cell_size,
                                              fill=color, outline="gray")

    def start(self):
        if not self.running:
            self.running = True
            self.update_grid()

    def stop(self):
        self.running = False
        if self.update_id:
            self.master.after_cancel(self.update_id)

    def reset(self):
        self.grid = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.draw_grid()
        self.update_counter()

    def fill_random(self):
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                self.grid[y][x] = random.choice([0, 1])  # Randomly set cell to alive or dead
        self.draw_grid()
        self.update_counter()

    def update_grid(self):
        new_grid = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                alive_neighbors = self.count_alive_neighbors(x, y)
                if self.grid[y][x] == 1:
                    new_grid[y][x] = 1 if alive_neighbors in (2, 3) else 0
                else:
                    new_grid[y][x] = 1 if alive_neighbors == 3 else 0
        self.grid = new_grid
        self.draw_grid()
        self.update_counter()
        if self.running:
            self.update_id = self.master.after(100, self.update_grid)

    def count_alive_neighbors(self, x, y):
        count = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if (i == 0 and j == 0) or (x + i < 0) or (x + i >= self.grid_size) or (y + j < 0) or (y + j >= self.grid_size):
                    continue
                count += self.grid[y + j][x + i]
        return count

    def update_counter(self):
        alive_count = sum(sum(row) for row in self.grid)
        self.counter_label.config(text=f"Alive Cells: {alive_count}")

if __name__ == "__main__":
    root = tk.Tk()
    game = GameOfLife(root)
    root.mainloop()
