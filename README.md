# 🌸 Flower Evolution Simulator (Genetic Algorithm GUI)

> **An interactive evolution experiment where digital flowers evolve based on your attention.**  
> Hover longer over the flowers you like — and watch evolution do its magic 🌿  

---

## 🎯 Overview

This project simulates **evolution through natural selection** using a **Genetic Algorithm (GA)** — applied to a population of colorful, dynamic flowers.  

Each flower’s DNA determines:
- 🌼 **Center size**
- 🎨 **Colors** (center, petals, stem)
- 🌸 **Number of petals**

You, the user, act as the **environment**:  
Your **mouse hover time** defines a flower’s *fitness*, deciding which traits survive and evolve into the next generation.

---

## 🧬 Features

✅ **Interactive Fitness Selection** — Hover longer over flowers you like to give them higher fitness.  
✅ **Bit-level Genetic Encoding** — Each flower’s DNA is stored in an 80-bit sequence.  
✅ **Crossover (65%)** — Parent flowers combine their genes to form unique offspring.  
✅ **Mutation (5%)** — Small, random bit flips introduce genetic diversity.  
✅ **Real-time Visualization** — Every generation is drawn dynamically using `tkinter`.  
✅ **Traceable Console Logs** — The full evolution process (selection, crossover, mutation) is logged step-by-step.  

---

## 🧠 How It Works

### 1️⃣ Initialization
A population of 8 random flowers is created:
Population = [Flower1, Flower2, ..., Flower8]

### 2️⃣ Fitness Interaction
Your **hover duration** determines how “fit” a flower is.  
The longer you hover → the higher its fitness score.

### 3️⃣ Selection
Fitter flowers are more likely to reproduce using **elitism selection**.

### 4️⃣ Crossover & Mutation
- **Crossover:** Two parent DNAs are combined bit-by-bit (65% chance).  
- **Mutation:** ~4 bits per DNA sequence are flipped randomly (5% mutation rate).  

### 5️⃣ Evolution
A new generation replaces the old — carrying your preferred traits forward.  

---

## 🖼️ Screenshots (GUI Preview)

| Generation 1 | Generation 3 | Generation 5 |
|---------------|--------------|--------------|
| <img src="https://github.com/user-attachments/assets/960aae1b-f49e-40dc-b44a-dd760844d297" width="250"/> | <img src="https://github.com/user-attachments/assets/ba749be6-2b93-4174-a8f9-c39d1685dd2d" width="250"/> | <img src="https://github.com/user-attachments/assets/1da53663-bdd1-4175-8dc0-766ed574e8d9" width="250"/> |




---

## ⚙️ Technical Details

| Component | Description |
|------------|--------------|
| **Language** | Python 3 |
| **GUI Library** | `tkinter` |
| **Core Concepts** | Genetic Algorithm, Bitwise Operations, Mutation & Crossover |
| **Population Size** | 8 |
| **DNA Length** | 80 bits per flower |
| **Mutation Rate** | 0.05 (≈ 4 bits flipped per flower) |
| **Crossover Probability** | 0.65 |
| **Fitness Metric** | Mouse hover duration |

---

## 💻 Run the Project

### 🪴 Requirements
- Python 3.8+
- No external dependencies — uses only built-in libraries.

### ▶️ How to Run
```bash
python main.py
```

A window will open showing 8 flowers.
Simply hover your mouse over the flowers you like —
then click "Evolve Next Generation" to see evolution in action.

### 📊 Sample Console Output
==================== EVOLUTION STEP ====================

 Current Population:
1: Flower(center_size=16, center_color=(46, 187, 105), ...)
...

 Selected Flowers for Reproduction:
Parent 1: ...
Parent 2: ...

 Crossover and Mutation Results:
 ↳ Child (after crossover): ...
 Before mutation: ...
 After mutation: ...

 Updated Population (Next Generation):
...
========================================================

