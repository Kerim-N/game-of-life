import tkinter as tk 
import random 

# Main class for the Game of Life
class GameOfLife:
    def __init__(self, master):
        self.master = master
        self.master.title("Game of Life")

        # Grid and cell settings
        self.grid_size = 20  # Number of rows/columns
        self.cell_size = 20  # Size of each square cell in pixels

        # Create canvas for the grid
        self.canvas = tk.Canvas(master, width=self.grid_size * self.cell_size, height=self.grid_size * self.cell_size, bg="lightgray")
        self.canvas.pack()

        # Initialize the grid (2D list), 0 means dead, 1 means alive
        self.grid = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]

        # Bind left mouse click to toggle cell state
        self.canvas.bind("<Button-1>", self.toggle_cell)

        # Control buttons
        self.start_button = tk.Button(master, text="Start", command=self.start, bg="green", fg="white")
        self.start_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.stop_button = tk.Button(master, text="Stop", command=self.stop, bg="red", fg="white")
        self.stop_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.reset_button = tk.Button(master, text="Reset", command=self.reset, bg="blue", fg="white")
        self.reset_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.random_button = tk.Button(master, text="Random", command=self.fill_random, bg="orange", fg="white")
        self.random_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Label to show number of alive cells
        self.counter_label = tk.Label(master, text="Alive Cells: 0", font=("Arial", 14))
        self.counter_label.pack(side=tk.LEFT, padx=10)

        self.running = False  # Game state flag
        self.update_id = None  # To store the after() callback ID

    # Toggle a cell between alive (1) and dead (0) when clicked
    def toggle_cell(self, event):
        x, y = event.x // self.cell_size, event.y // self.cell_size
        self.grid[y][x] = 1 - self.grid[y][x]  # Flip 1 to 0 or 0 to 1
        self.draw_grid()
        self.update_counter()

    # Draw all cells on the canvas
    def draw_grid(self):
        self.canvas.delete("all")  # Clear canvas
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                color = "black" if self.grid[y][x] == 1 else "white"  # Alive is black, dead is white
                self.canvas.create_rectangle(
                    x * self.cell_size, y * self.cell_size,
                    (x + 1) * self.cell_size, (y + 1) * self.cell_size,
                    fill=color, outline="gray"
                )

    # Start the game loop
    def start(self):
        if not self.running:
            self.running = True
            self.update_grid()

    # Stop the game loop
    def stop(self):
        self.running = False
        if self.update_id:
            self.master.after_cancel(self.update_id)

    # Reset the grid to all dead cells
    def reset(self):
        self.grid = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.draw_grid()
        self.update_counter()

    # Fill the grid with random alive/dead cells
    def fill_random(self):
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                self.grid[y][x] = random.choice([0, 1])
        self.draw_grid()
        self.update_counter()

    # Update the grid based on Game of Life rules
    def update_grid(self):
        new_grid = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]

        for y in range(self.grid_size):
            for x in range(self.grid_size):
                alive_neighbors = self.count_alive_neighbors(x, y)

                # Apply the rules of Conway's Game of Life
                if self.grid[y][x] == 1:
                    # A live cell stays alive if it has 2 or 3 neighbors
                    new_grid[y][x] = 1 if alive_neighbors in (2, 3) else 0
                else:
                    # A dead cell becomes alive if it has exactly 3 neighbors
                    new_grid[y][x] = 1 if alive_neighbors == 3 else 0

        self.grid = new_grid
        self.draw_grid()
        self.update_counter()

        # Schedule the next update if still running
        if self.running:
            self.update_id = self.master.after(100, self.update_grid)

    # Count how many alive neighbors surround the cell at (x, y)
    def count_alive_neighbors(self, x, y):
        count = 0
        for i in range(-1, 2):  # i: -1 to 1
            for j in range(-1, 2):  # j: -1 to 1
                if (i == 0 and j == 0):  # Skip the cell itself
                    continue
                nx, ny = x + i, y + j
                # Skip if out of bounds
                if nx < 0 or ny < 0 or nx >= self.grid_size or ny >= self.grid_size:
                    continue
                count += self.grid[ny][nx]  # Add if neighbor is alive
        return count

    # Count and update the alive cell label
    def update_counter(self):
        alive_count = sum(sum(row) for row in self.grid)
        self.counter_label.config(text=f"Alive Cells: {alive_count}")

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    game = GameOfLife(root)
    root.mainloop()
