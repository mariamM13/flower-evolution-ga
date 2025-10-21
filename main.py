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

    def to_array(self):
        return [
            self.center_size,
            *self.center_color,
            *self.petal_color,
            *self.stem_color,
            self.num_petals
        ]

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

        self.generation = 1
        self.generation_label = tk.Label(root, text=f"Generation: {self.generation}", font=("Arial", 14, "bold"))
        self.generation_label.pack(pady=5)

        # Hover tracking
        self.hover_start = None
        self.hover_flower = None

        # Initial population
        self.population = create_population()
        self.flower_positions = []  # Track each flower’s clickable area
        self.draw_population()
        print("Initial Population:")
        for flower in self.population:
            print(flower.to_array())

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
            text_y = 50  
        else:
            text_y = 560  

        self.canvas.create_text(cx, text_y, text=f"Fitness: {flower.fitness:.2f}", font=("Arial", 10))

    def on_hover_start(self, index):
        self.hover_start = time.time()
        self.hover_flower = index

    def on_hover_end(self, index):
        if self.hover_start is not None and self.hover_flower == index:
            duration = time.time() - self.hover_start
            self.population[index].fitness += duration
            self.hover_start = None
            self.hover_flower = None
            print(f"Flower {index + 1} fitness updated: {self.population[index].fitness:.2f}")
            self.draw_population()  

    def evolve(self):
        print("\n EVOLUTION STEP")

        self.generation += 1
        self.generation_label.config(text=f"Generation: {self.generation}")

        print("\n Current Population:")
        for flower in self.population:
            print(flower.to_array())


        sorted_pop = sorted(self.population, key=lambda f: f.fitness, reverse=True)
        print("\n Population after Sorting:")
        for flower in sorted_pop:
            print(flower.to_array())

        # Elitism Selection
        elites = sorted_pop[:4]
        new_population = elites + [copy.deepcopy(f) for f in elites]

        print("\n Selected Population:")
        for flower in new_population:
            print(flower.to_array())

        random.shuffle(new_population)

        print("\nCrossover and Mutation Results:")
        children = []

        for i in range(0, len(new_population), 2):
            p1, p2 = new_population[i], new_population[i + 1]

            print(f"\nPair {i // 2 + 1}:")
            print("Parent 1:", p1.to_array())
            print("Parent 2:", p2.to_array())

            child1, child2 = self.crossover(p1, p2)

            # ---- MUTATION ----
            print("Before mutation (child1):", child1.to_array())
            self.mutate(child1)
            print("After mutation  (child1):", child1.to_array())

            print("Before mutation (child2):", child2.to_array())
            self.mutate(child2)
            print("After mutation  (child2):", child2.to_array())

            children.extend([child1, child2])

        # Update population
        self.population = children[:len(self.population)]

        # Reset fitness
        for f in self.population:
            f.fitness = 0.0

        print("\nUpdated Population:")
        for f in self.population:
            print(f.to_array())


        self.draw_population()


    def crossover(self, parent1, parent2, prob=0.65):

        genes1 = parent1.to_array()
        genes2 = parent2.to_array()


        if random.random() > prob:
            print("No crossover (children are clones)")
            child1_genes, child2_genes = genes1[:], genes2[:]
        else:
            point = random.randint(1, len(genes1) - 1)
            print(f"Crossover happened at point {point}")
            child1_genes = genes1[:point] + genes2[point:]
            child2_genes = genes2[:point] + genes1[point:]

        def create_flower(genes):
            return Flower(
                center_size=genes[0],
                center_color=tuple(genes[1:4]),
                petal_color=tuple(genes[4:7]),
                stem_color=tuple(genes[7:10]),
                num_petals=genes[10],
                fitness=0.0
            )

        child1 = create_flower(child1_genes)
        child2 = create_flower(child2_genes)

        print("Parent 1:", genes1)
        print("Parent 2:", genes2)
        print("Child 1 :", child1_genes)
        print("Child 2 :", child2_genes)

        return child1, child2

        
        ## parent 1 : [11,255,10,|103,70,5]
        ## parent 2 : [15,100,200,|50,150,3]

        ## randam.randam()<0.65
        ## generate randam cut point 
        ## child 1: [11,255,10,50,150,3]
        ## child 2: [15,100,200, 103,70,5]

        ## child1: parent 1
        ## child2: parent 2
        
        ## mutation : prob check for each gene for each indiv < 0.05 --> flip

        ## population1: [11,255,10,50,150,3] 
        ## rande 8 -20 , 11 --> randam.rand()<0.05  then randam.randint(0,20)


        # Otherwise create child via binary crossover on each gene


    def mutate(self, flower, rate=0.05):

        def to_bin(value, bits):
            return format(value, f'0{bits}b')

        def to_int(binary):
            return int(binary, 2)

        dna = (
            to_bin(flower.center_size, 5) +
            ''.join(to_bin(c, 8) for c in flower.center_color) +
            ''.join(to_bin(c, 8) for c in flower.petal_color) +
            ''.join(to_bin(c, 8) for c in flower.stem_color) +
            to_bin(flower.num_petals, 3)
        )

        dna_list = list(dna)
        dna_length = len(dna_list)

        for i in range(dna_length):
            if random.random() < rate:
                dna_list[i] = '1' if dna_list[i] == '0' else '0'

        mutated_dna = ''.join(dna_list)

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
        flower.center_size = min(max(flower.center_size, 8), 20)

        flower.center_color = tuple(min(max(c, 0), 255) for c in flower.center_color)
        flower.petal_color = tuple(min(max(c, 0), 255) for c in flower.petal_color)
        flower.stem_color = tuple(min(max(c, 0), 255) for c in flower.stem_color)

        flower.num_petals = min(max(flower.num_petals, 0), 7)

        return flower



    @staticmethod
    def rgb_to_hex(rgb):
        return '#%02x%02x%02x' % rgb


root = tk.Tk()
gui = FlowerGUI(root)
root.mainloop()
