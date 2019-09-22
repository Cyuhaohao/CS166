import random


class Passenger():
    def __init__(self, location, destination):
        self.location = location  # e.g: start_floor, on elevator, destination, etc
        self.destination = destination

    def relocate(self,new_location):
        self.location=new_location


# Building class

# I would suggest we use a distribution for the residents by floor so once we have the number of floors,
# Use maybe a dirichlet distribution to populate each floor. We can then use a random generator between 0 and residents size
# To get a random resident and then pick their floor as per the defined distribution. This would be a stop we pick

class Building():
    def __init__(self, floors, residents):
        self.floors = floors
        self.residents = residents

# Elevator class

class Elevator():
    def __init__(self, capacity, speed, current_floor, occupancy, stopping_time, tot_time=0):
        self.capacity = capacity
        self.current_floor = current_floor
        self.speed = speed
        self.occupancy = occupancy
        self.stopping_time = stopping_time
        self.tot_time = tot_time
        self.current_passenger=[]

    # Define the method of move so that elevator can recalculate the value of current floor    
    def move(self, steps):
        self.current_floor += steps

    def drop_off_method(self,passenger):
        self.occupancy -= 1
        self.current_passenger.remove(passenger)

    def accept_method(self,passenger):
        self.occupancy += 1
        self.current_passenger.append(passenger)



def finish_check(people):
    for passenger in people:
        if passenger.destination!=passenger.location:
            return False
    return True


def simulation1_yuhao():
    elevator1=Elevator(capacity=10, speed=5, current_floor=1, occupancy=0, stopping_time=2)
    building1=Building(6,1000)
    people1=[]
    locations1=[]
    destinations1=[]
    num_of_stops=0
    names = locals()
    for i in range(building1.residents):
        names['passenger%s' % i]=Passenger(random.randint(1,building1.floors),random.randint(1,building1.floors))
        locations1.append(names['passenger%s' % i].location)
        destinations1.append(names['passenger%s' % i].destination)
        people1.append(names['passenger%s' % i])

    direction=-1

    while finish_check(people1) is False:
        print("The elevator arrives at Floor %s and opens the door." % elevator1.current_floor)
        for passenger in elevator1.current_passenger:
            if passenger.destination==elevator1.current_floor:
                passenger.relocate(elevator1.current_floor)
                elevator1.drop_off_method(passenger)
                print("A passenger arrives at his destination and gets out.")

        for passenger in people1:
            if passenger.location==elevator1.current_floor and passenger.location!=passenger.destination and elevator1.occupancy<elevator1.capacity:
                elevator1.accept_method(passenger)
                print("A passenger gets in.")

        c=len(elevator1.current_passenger)

        if elevator1.current_floor==1 or elevator1.current_floor==building1.floors:
            direction=-direction
        elevator1.move(direction)
        if direction>0:
            print("The elevator closes the door and moves up.")
        else:
            print("The elevator closes the door and moves down.")

        num_of_stops+=1

    print("\nAll people get their destination.\n")
    print("The total number of stops is:",num_of_stops)


simulation1_yuhao()