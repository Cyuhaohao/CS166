import random

class Building():
    def __init__(self, num_floors):
        self.num_floors = num_floors


# Create a passenger with unique location and destination
class Passenger():
    def __init__(self, location, destination, at_destination):
        self.location = location
        self.destination = destination


# Create an elevator
class Elevator():

    def __init__(self, location, capacity):
        self.location = location
        self.capacity = capacity
        self.occupants = []

    # Move the elevator up one floor
    def move_up(self):
        self.location += 1

    # Move the elevator down one floor
    def move_down(self):
        self.location -= 1

    # Move the elevator to a given floor
    def to_floor(self, go_to):
        self.location = go_to

    # For each peron on the elevator, remove people whose destinations are the same
    # floor as the elevator
    def unload(self):
        for person in self.occupants:
            if person.destination == self.location:
                person.location = 'arrived'
                self.occupants.remove(person)
                print("A passenger is unloaded.")

    # Add as many people as will fit on the elevator
    def load(self, people):
        if len(self.occupants) < self.capacity:
            queued = [person for person in people if person.location == self.location]
            for person in queued[:(self.capacity - len(self.occupants))]:
                person.location = 'on elevator'
                self.occupants.append(person)
                print("A passenger is loaded.")
            return
        elif len(self.occupants) == self.capacity:
            return
        else:
            print('overfull')


def finish_check(people):
    for passenger in people:
        if passenger.location!='arrived':
            return False
    return True


def strategy3_yuhao():
    elevator3 = Elevator(capacity=10, location=1)
    building3 = Building(6)
    tot_people=100
    num_of_stops = 0
    num_floors = 0
    people3=[]
    names = locals()
    for i in range(tot_people):
        init_floor = random.randint(1, building3.num_floors)
        f = [x for x in range(1, building3.num_floors+1) if x != init_floor]
        destination = random.choice(f)
        person = Passenger(location=init_floor, destination=destination, at_destination=0)
        people3.append(person)

    while finish_check(people3) is False:
        print("The elevator moves to Floor %s and opens the door." % elevator3.location)

        elevator3.unload()

        elevator3.load(people3)

        num_in_destinations=[]
        num_of_waitings=[]

        if len(elevator3.occupants)!=0:
            for floor in range(1,building3.num_floors+1):
                num_in_floor=0
                for person in elevator3.occupants:
                    if person.destination==floor:
                        num_in_floor+=1
                num_in_destinations.append(num_in_floor)
            max_val=max(num_in_destinations)
            next_floor=num_in_destinations.index(max(num_in_destinations))+1

        else:
            for floor in range(1,building3.num_floors+1):
                num_in_floor=0
                for person in people3:
                    if person.location==floor:
                        num_in_floor+=1
                num_of_waitings.append(num_in_floor)
            next_floor=num_of_waitings.index(max(num_of_waitings))+1

        num_floors+= abs(next_floor-elevator3.location)

        elevator3.to_floor(next_floor)
        print("The elevator closes the door.")
        num_of_stops += 1

    print("\nAll people get their destination.\n")
    print("The total number of stops is:", num_of_stops)
    print("The total number of floors is:", num_floors)
    return people3


people3=strategy3_yuhao()
print(finish_check(people3))