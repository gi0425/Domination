import threading
import time
import concurrent.futures
import random
import traceback

class Empire:
    # Parameters: weapons, warriors, budget, land, wealth, lock
    def __init__(self, name):
        self.name = name
        self.weapons = random.randint(5000, 10000)
        self.warriors = random.randint(5000, 10000)
        self.budget = random.randint(5000, 10000)
        self.lands = random.randint(2000, 5000)
        self.wealth = random.randint(1000, 5000)
        self.lock = threading.Lock() # each Empire has its own lock

    def calculate_points(self):
        return (self.weapons * 2 + self.warriors * 1 + self.budget * 3 
                + self.lands * 2 + self.wealth * 3)

    def lose_resources(self):
        # all resources decrease by 1/2 for the Empires that lose
        with self.lock:
            self.weapons = int(self.weapons * 0.5)
            self.warriors = int(self.warriors * 0.5)
            self.budget = int(self.budget * 0.5)
            self.lands = int(self.lands * 0.5)
            self.wealth = int(self.wealth * 0.5)

    def gain_resources(self, other_empire):
        # all resources increase by 1/2 for the Empires that won
        with self.lock:
            self.weapons += int(other_empire.weapons * 0.5)
            self.warriors += int(other_empire.warriors * 0.5)
            self.budget += int(other_empire.budget * 0.5)
            self.lands += int(other_empire.lands * 0.5)
            self.wealth += int(other_empire.wealth * 0.5)

    def __str__(self):
        return (f'''{self.name}: Weapons={self.weapons}, Warriors={self.warriors}, Budget={self.budget}, Lands={self.lands} sq km, Wealth={self.wealth} gold,
                Points: {self.calculate_points()}''')

def battle(empire1, empire2):
    # calculate current points per empire before the battle
    print(f"\nBattle Start: {empire1.name} vs {empire2.name}")
    points1 = empire1.calculate_points()
    points2 = empire2.calculate_points()

    # A battle is won depending on who has more points
    if points1 > points2:
        winner, loser = empire1, empire2
    else:
        winner, loser = empire2, empire1

    loser.lose_resources()
    winner.gain_resources(loser)

    print(f"Winner: {winner.name}")
    print(f"After Battle - {empire1.name}: {empire1}")
    print(f"After Battle - {empire2.name}: {empire2}")
    time.sleep(5)

def sign_peace_treaty(empires):
    # peace treaty = end of the game -> shows results
    print("\nPeace Treaty Signed! Ranking Empires...\n")
    scores = {empire.name: empire.calculate_points() for empire in empires}
    ranked_empires = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    print("Final Rankings:")
    for rank, (empire_name, score) in enumerate(ranked_empires, 1):
        print(f"{rank}. {empire_name} - Score: {score}")

def main():
    empires = [
        Empire("Rome"),
        Empire("Greece"),
        Empire("Vikings"),
        Empire("Egypt"),
        Empire("Mongolia")]

    print("Initial Empires:")
    for empire in empires:
        print(empire)
        time.sleep(1)

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        for i in range(len(empires) - 1):
            executor.submit(battle, empires[i], empires[i + 1])
            time.sleep(1)

    sign_peace_treaty(empires)

if __name__ == "__main__":
    main()


