import random
import numpy as np
required_experiments = 10000

# The contestant picks a door and we check whether she gets the car.

experiments = 0
successes = 0
while experiments < required_experiments:

    # The car is hidden behind a random door.
    car_door = random.randint(1, 3)

    # The contestant selects a random door.
    contestant_door = random.randint(1, 3)

    # Did the contestant get the car? Count that as a success.
    if contestant_door == car_door:
        successes += 1
    experiments += 1

print(successes / experiments)

set([1,2,3])^set([2])

# The Monty Hall scenario.
# FOR YOU TO IMPLEMENT.

experiments = 0
successes = 0
while experiments < required_experiments:

    # The car is hidden behind a random door.
    car_door = random.randint(1, 3)

    # The contestant selects a random door.
    contestant_door = random.randint(1, 3)

    # The host opens a different door that has a goat behind it.
    if car_door == contestant_door:
        doors = np.array([1, 2, 3])
        doors = np.delete(doors, car_door - 1)
        host_door = np.random.choice(doors)
    else:
        host_door = np.delete(doors, [car_door - 1, contestant_door - 1])

    # The contestant switches to the other door (not the one she chose originally and not the goat).
    contestant_door = np.delete([1, 2, 3], [contestant_door - 1, host_door - 1])

    # Did the contestant get the car? Count that as a success.
    if contestant_door == car_door:
        successes += 1
    experiments += 1
#
# # The earthquake scenario.
# # FOR YOU TO IMPLEMENT.
#
# experiments = 0
# successes = 0
# while experiments < required_experiments:
#
#     # The car is hidden behind a random door.
#     car_door = random.randint(1, 3)
#
#     # The contestant selects a random door.
#     contestant_door = random.randint(1, 3)
#
#     # The earthquake opens a random door.
#     earthquake_door = random.randint(1, 3)
#
#     # What if the earthquake opened the contestant's door?
#     if (car_door == contestant_door) and (earthquake_door == car_door):
#         successes += 1
#     else:
# # What if the earthquake opened the door with a car behind it?
#
# # The contestant switches to the other door (not the one she chose originally and not the goat).
#
# # Did the contestant get the car? Count that as a success.
#
