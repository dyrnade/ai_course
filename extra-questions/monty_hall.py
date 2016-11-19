import random

doors = ["goat", "goat", "car"]

win = 0
lost = 0

for i in range(10000):

    random.shuffle(doors)
    choice = random.randrange(3)
    print("You selected: ", choice)

    for x,_ in enumerate(doors):
        if doors[x] != "car" and x != choice:
            monty = x
    print("Monty selected: ", monty)

    if doors[choice] == "car":
        win += 1
    else:
        lost += 1

print("Win ", win, "Lost : ", lost)
