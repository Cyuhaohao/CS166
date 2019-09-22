
import datetime


# create the class for person
class Person:
    def __init__(self):
        name=input("What's your name:")  # get information
        self.name=name
        age = int(input("How old are you:"))
        self.birthyear = datetime.datetime.now().year-age
        birthplace = input("What's your birthplace:")
        self.birthplace = birthplace
        ID_Num = input("What's your ID_Num:")
        self.ID_Num = ID_Num

    def introduce_yourself(self):  # define method
        print("Hello, my name is %s" % self.name)

    def age_now(self):  # define a complicated method
        return datetime.datetime.now().year-self.birthyear


# check results
Eric = Person()
Eric.introduce_yourself()
print("The current age of %s is: %i" % (Eric.name, Eric.age_now()))
print("The birth year of %s is %i" % (Eric.name, Eric.birthyear))


