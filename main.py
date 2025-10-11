import tkinter as tk
import random
import math
import time


class Flower:
    def __init__(self, center_size, center_color, petal_color, stem_color, num_petals, fitness=0.0):
        self.center_size = center_size
        self.center_color = center_color
        self.petal_color = petal_color
        self.stem_color = stem_color
        self.num_petals = num_petals
        self.fitness = fitness

    def __repr__(self):
        return (
            f"Flower(center_size={self.center_size}, "
            f"center_color={self.center_color}, "
            f"petal_color={self.petal_color}, "
            f"stem_color={self.stem_color}, "
            f"num_petals={self.num_petals}, "
            f"fitness={self.fitness:.2f})"
        )


def create_population(size=8):
    return [
        Flower(
            center_size=random.randint(8, 20),
            center_color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
            petal_color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
            stem_color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
            num_petals=random.randint(0, 7)
        )
        for _ in range(size)
    ]


class FlowerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Flower Evolution GUI")

        self.canvas = tk.Canvas(root, width=800, height=600, bg="white")
        self.canvas.pack()

        self.button = tk.Button(root, text="Evolve Next Generation", command=self.evolve)
        self.button.pack(pady=10)

        # Hover tracking
        self.hover_start = None
        self.hover_flower = None

        # Initial population
        self.population = create_population()
        self.flower_positions = []  # Track each flower’s clickable area
        self.draw_population()
        for flower in self.population:
            print (flower)

    def draw_population(self):
        """Draw all flowers and attach hover listeners."""
        self.canvas.delete("all")
        self.flower_positions.clear()

        cols = 4
        spacing_x = 200
        spacing_y = 250
        for i, flower in enumerate(self.population):
            x = (i % cols) * spacing_x + 100
            y = (i // cols) * spacing_y + 120
            self.draw_flower(x, y, flower, i)

    def draw_flower(self, cx, cy, flower, index):
        size = flower.center_size

        # Stem
        self.canvas.create_rectangle(cx - 6, cy, cx + 6, cy + size * 7,
                                     fill=self.rgb_to_hex(flower.stem_color), outline="")

        # Petals
        for i in range(flower.num_petals):
            angle = 2 * math.pi * i / max(1, flower.num_petals)
            x = cx + math.cos(angle) * size * 1.2
            y = cy + math.sin(angle) * size * 1.2
            self.canvas.create_oval(x - size * 1.2, y - size * 1.2,
                                    x + size * 1.2, y + size * 1.2,
                                    fill=self.rgb_to_hex(flower.petal_color), outline="")

        # Center
        flower_id = self.canvas.create_oval(cx - size * 1.5, cy - size * 1.5,
                                            cx + size * 1.5, cy + size * 1.5,
                                            fill=self.rgb_to_hex(flower.center_color),
                                            outline="")

        # Bind hover tracking
        self.canvas.tag_bind(flower_id, "<Enter>", lambda e, i=index: self.on_hover_start(i))
        self.canvas.tag_bind(flower_id, "<Leave>", lambda e, i=index: self.on_hover_end(i))

        # Save clickable region
        self.flower_positions.append((cx, cy, flower))

        # Show fitness text
        self.canvas.create_text(cx, cy + 60, text=f"Fitness: {flower.fitness:.2f}", font=("Arial", 10))

    def on_hover_start(self, index):
        """Record when hover starts."""
        self.hover_start = time.time()
        self.hover_flower = index

    def on_hover_end(self, index):
        """Increase fitness based on hover duration."""
        if self.hover_start is not None and self.hover_flower == index:
            duration = time.time() - self.hover_start
            self.population[index].fitness += duration
            self.hover_start = None
            self.hover_flower = None
            print(f"Flower {index + 1} fitness updated: {self.population[index].fitness:.2f}")
            self.draw_population()  

    def evolve(self):
        """Perform selection, crossover, and mutation, with detailed logging."""
        print("\n==================== EVOLUTION STEP ====================")

        # --- 1. Show Current Population ---
        print("\n Current Population:")
        for i, f in enumerate(self.population, start=1):
            print(f"{i}: {f}")

        # --- 2. Sort and Display by Fitness ---
        sorted_pop = sorted(self.population, key=lambda f: f.fitness, reverse=True)
        print("\n Population after Sorting by Fitness:")
        for i, f in enumerate(sorted_pop, start=1):
            print(f"{i}: {f}")

        # --- 3. Selection (Roulette Wheel) ---
        total_fitness = sum(f.fitness for f in self.population)
        if total_fitness == 0:
            parents = random.choices(self.population, k=len(self.population))
        else:
            probs = [f.fitness / total_fitness for f in self.population]
            parents = random.choices(self.population, weights=probs, k=len(self.population))

        print("\n Selected Flowers for Reproduction:")
        for i, p in enumerate(parents, start=1):
            print(f"Parent {i}: {p}")

        # --- 4. Crossover and Mutation ---
        new_population = []
        print("\n Crossover and Mutation Results:")
        for i in range(len(self.population)):
            p1, p2 = random.sample(parents, 2)
            print(f"\n➡️  Reproduction {i + 1}:")
            print(f"Parent 1: {p1}")
            print(f"Parent 2: {p2}")

            # Crossover
            child = self.crossover(p1, p2)

            print(f"  ↳ Child (after crossover): {child}")

            # Mutation
            print(" Before mutation:", child)
            self.mutate(child)
            print(" After mutation :", child)

            new_population.append(child)

        # --- 5. Update Population ---
        self.population = new_population

        print("\n Updated Population (Next Generation):")
        for i, f in enumerate(self.population, start=1):
            print(f"{i}: {f}")

        print("========================================================\n")

        # Redraw flowers on the canvas
        self.draw_population()


    def crossover(self, parent1, parent2, prob=0.65):
        """Mix genes from two parents."""
        if random.random() > prob:
            return random.choice([parent1, parent2])  # No crossover → clone one

        return Flower(
            center_size=random.choice([parent1.center_size, parent2.center_size]),
            center_color=tuple(random.choice([c1, c2]) for c1, c2 in zip(parent1.center_color, parent2.center_color)),
            petal_color=tuple(random.choice([c1, c2]) for c1, c2 in zip(parent1.petal_color, parent2.petal_color)),
            stem_color=tuple(random.choice([c1, c2]) for c1, c2 in zip(parent1.stem_color, parent2.stem_color)),
            num_petals=random.choice([parent1.num_petals, parent2.num_petals])
        )

    def mutate(self, flower, rate=0.05):
        """Randomly tweak some attributes."""
        if random.random() < rate:
            flower.center_size = max(5, flower.center_size + random.randint(-2, 2))
        if random.random() < rate:
            flower.num_petals = max(0, flower.num_petals + random.randint(-1, 1))
        if random.random() < rate:
            flower.center_color = tuple(min(255, max(0, c + random.randint(-30, 30))) for c in flower.center_color)
        if random.random() < rate:
            flower.petal_color = tuple(min(255, max(0, c + random.randint(-30, 30))) for c in flower.petal_color)
        if random.random() < rate:
            flower.stem_color = tuple(min(255, max(0, c + random.randint(-30, 30))) for c in flower.stem_color)

    @staticmethod
    def rgb_to_hex(rgb):
        return '#%02x%02x%02x' % rgb


root = tk.Tk()
gui = FlowerGUI(root)
root.mainloop()
