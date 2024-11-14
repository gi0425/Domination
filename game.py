import tkinter as tk
from PIL import Image, ImageTk
import random
import threading
import time
import concurrent.futures

root = tk.Tk()
root.title("The Last One Standing")
root.geometry("1000x700")

image_path = "mapa_empires.png"
background_image = Image.open(image_path)
scaled_image = background_image.resize((950, 650))
background_photo = ImageTk.PhotoImage(scaled_image)

canvas = tk.Canvas(root, width=1000, height=700)
canvas.pack()
canvas.create_image(500, 350, anchor="center", image=background_photo)

country_centers = {
    "Vikings": (70, 250), 
    "Mongolia": (280, 280),
    "Rome": (400, 105), 
    "Russia": (740, 150), 
    "Atacama": (100, 520), 
    "Greece": (270, 440), 
    "China": (550, 550), 
    "France": (550, 300), 
    "Egypt": (750, 550),
    "Britain": (780, 380)
}

markers = {}

for country, (x, y) in country_centers.items():
    oval = canvas.create_oval(x - 15, y - 15, x + 15, y + 15, fill="green")
    canvas.create_text(x, y + 25, text=country, fill="black", font=("Arial", 12))
    markers[country] = oval  

class Empire:
    def __init__(self, name):
        self.name = name
        self.weapons = random.randint(5000, 10000)
        self.warriors = random.randint(5000, 10000)
        self.budget = random.randint(5000, 10000)
        self.lands = random.randint(5000, 10000)
        self.wealth = random.randint(5000, 10000)
        self.lock = threading.Lock()

    def calculate_points(self):
        return (self.weapons * 2 + self.warriors * 1 + self.budget * 3 
                + self.lands * 2 + self.wealth * 3)

    def lose_random_percentage(self):
        reduction_percentage = random.randint(15, 100) / 100
        with self.lock:
            self.weapons = int(self.weapons * (1 - reduction_percentage))
            self.warriors = int(self.warriors * (1 - reduction_percentage))
            self.budget = int(self.budget * (1 - reduction_percentage))
            self.lands = int(self.lands * (1 - reduction_percentage))
            self.wealth = int(self.wealth * (1 - reduction_percentage))
        return reduction_percentage

    def absorb_resources(self, other_empire):
        with self.lock:
            self.weapons += other_empire.weapons
            self.warriors += other_empire.warriors
            self.budget += other_empire.budget
            self.lands += other_empire.lands
            self.wealth += other_empire.wealth

    def __str__(self):
        return (f"{self.name}: Weapons={self.weapons}, Warriors={self.warriors}, "
                f"Budget={self.budget}, Lands={self.lands} sq km, Wealth={self.wealth} gold, "
                f"Points: {self.calculate_points()}")

def update_marker_color(empire_name, color):
    oval = markers.get(empire_name)
    if oval:
        canvas.itemconfig(oval, fill=color)
    root.update_idletasks()  

def battle(empire1, empire2, empires, empire_lock=threading.Lock()):
    with empire_lock:
        print(f"\nBattle Start: {empire1.name} vs {empire2.name}")
        update_marker_color(empire1.name, "red")
        update_marker_color(empire2.name, "red")

    time.sleep(1) 

    points1 = empire1.calculate_points()
    points2 = empire2.calculate_points()

    if points1 > points2:
        winner, loser = empire1, empire2
    else:
        winner, loser = empire2, empire1

    winner.lose_random_percentage()
    loser.lose_random_percentage()
    winner.absorb_resources(loser)

    with empire_lock:
        print(f"\nWinner: {winner.name} absorbed {loser.name} after battle.")
        print(f"{winner}")
        update_marker_color(empire1.name, "green")
        update_marker_color(empire2.name, "green")

        if loser in empires:
            empires.remove(loser)
            canvas.itemconfig(markers[loser.name], state="hidden")

def main_game_loop():
    empires = [
        Empire("Vikings"),
        Empire("Mongolia"),
        Empire("Rome"),
        Empire("Russia"),
        Empire("Atacama"),
        Empire("Greece"),
        Empire("China"),
        Empire("France"),
        Empire("Egypt"),
        Empire("Britain")
    ]

    print("Initial Empires:")
    for empire in empires:
        print(empire)

    while len(empires) > 1:
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = []
            for _ in range(len(empires) // 2):
                if len(empires) < 2:
                    break
                empire1, empire2 = random.sample(empires, 2)
                futures.append(executor.submit(battle, empire1, empire2, empires))
            concurrent.futures.wait(futures)

    winner = empires[0]
    print("\nAll empires conquered!")
    print(f"{winner.name} owns the world")
    print(f"Final Stats: {winner}")

def start_game():
    game_thread = threading.Thread(target=main_game_loop)
    game_thread.start()

root.after(100, start_game)
root.mainloop()


