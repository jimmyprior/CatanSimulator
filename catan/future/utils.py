import random

def roll_dice(num_dice = 2):
    total = 0
    for _ in range(num_dice):
        total += random.randint(1, 6)
    return total 


def simulate_dice_rolls(num_rolls, num_dice): 
    store = {}
    for _ in range(num_rolls):
        roll = roll_dice(num_dice)
        if store.get(roll):
            store[roll] += 1
        else:
            store[roll] = 1
            
    rolls_sorted = sorted(list(store.keys()))
    for roll in rolls_sorted:
        print(f"{roll} : {store[roll] / num_rolls * 100}%")
    