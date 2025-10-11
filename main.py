import tkinter as tk
import random
import math
import time
import copy


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
        cols = 4
        row = index // cols  # 0 = top row, 1 = bottom row

        if row == 0:
            text_y = 50   # fixed height near top
        else:
            text_y = 560  # fixed height near bottom

        self.canvas.create_text(cx, text_y, text=f"Fitness: {flower.fitness:.2f}", font=("Arial", 10))

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
            print(f"\n***  Reproduction {i + 1}:")
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
        """Binary crossover with safe cloning and fitness reset."""

        def binary_crossover(v1, v2, bits=8):
            b1, b2 = format(v1, f'0{bits}b'), format(v2, f'0{bits}b')
            # choose a random crossover point (1..bits-1)
            point = random.randint(1, bits - 1)
            child_bin = b1[:point] + b2[point:]
            return int(child_bin, 2)

        # If no crossover, clone parent's genes into a NEW Flower (do NOT return the same object)
        if random.random() > prob:
            src = random.choice([parent1, parent2])
            child = Flower(
                center_size = src.center_size,
                center_color = tuple(src.center_color),
                petal_color = tuple(src.petal_color),
                stem_color = tuple(src.stem_color),
                num_petals = src.num_petals,
                fitness = 0.0   # IMPORTANT: reset fitness for offspring
            )
            return child

        # Otherwise create child via binary crossover on each gene
        child = Flower(
            center_size = binary_crossover(parent1.center_size, parent2.center_size, bits=5),
            center_color = tuple(binary_crossover(c1, c2, bits=8) for c1, c2 in zip(parent1.center_color, parent2.center_color)),
            petal_color  = tuple(binary_crossover(c1, c2, bits=8) for c1, c2 in zip(parent1.petal_color, parent2.petal_color)),
            stem_color   = tuple(binary_crossover(c1, c2, bits=8) for c1, c2 in zip(parent1.stem_color, parent2.stem_color)),
            num_petals   = binary_crossover(parent1.num_petals, parent2.num_petals, bits=3),
            fitness = 0.0
        )

        return child


    def mutate(self, flower, rate=0.05):
        """Perform bit-level mutation (flip ~4 bits per flower DNA)."""

        # Helper: convert a value to binary string with fixed bits
        def to_bin(value, bits):
            return format(value, f'0{bits}b')

        # Helper: convert binary string back to int
        def to_int(binary):
            return int(binary, 2)

        # --- Encode full DNA into one binary string (80 bits total) ---
        dna = (
            to_bin(flower.center_size, 5) +
            ''.join(to_bin(c, 8) for c in flower.center_color) +
            ''.join(to_bin(c, 8) for c in flower.petal_color) +
            ''.join(to_bin(c, 8) for c in flower.stem_color) +
            to_bin(flower.num_petals, 3)
        )

        dna_list = list(dna)
        dna_length = len(dna_list)

        # --- Flip bits with probability = rate ---
        for i in range(dna_length):
            if random.random() < rate:
                dna_list[i] = '1' if dna_list[i] == '0' else '0'

        mutated_dna = ''.join(dna_list)

        # --- Decode DNA back into flower attributes ---
        idx = 0
        flower.center_size = to_int(mutated_dna[idx:idx+5]); idx += 5

        flower.center_color = tuple(
            to_int(mutated_dna[idx + i*8: idx + (i+1)*8]) for i in range(3)
        )
        idx += 24

        flower.petal_color = tuple(
            to_int(mutated_dna[idx + i*8: idx + (i+1)*8]) for i in range(3)
        )
        idx += 24

        flower.stem_color = tuple(
            to_int(mutated_dna[idx + i*8: idx + (i+1)*8]) for i in range(3)
        )
        idx += 24

        flower.num_petals = to_int(mutated_dna[idx:idx+3])
        self.repair_flower(flower)


    def repair_flower(self, flower):
        """Ensure all mutated attributes stay within valid and aesthetic ranges."""

        # Keep center size between 8 and 20 (so flower stays visible)
        flower.center_size = min(max(flower.center_size, 8), 20)

        # Keep colors in valid RGB range (0–255)
        flower.center_color = tuple(min(max(c, 0), 255) for c in flower.center_color)
        flower.petal_color = tuple(min(max(c, 0), 255) for c in flower.petal_color)
        flower.stem_color = tuple(min(max(c, 0), 255) for c in flower.stem_color)

        # Keep petals between 0–7
        flower.num_petals = min(max(flower.num_petals, 0), 7)

        return flower



    @staticmethod
    def rgb_to_hex(rgb):
        return '#%02x%02x%02x' % rgb


root = tk.Tk()
gui = FlowerGUI(root)
root.mainloop()
