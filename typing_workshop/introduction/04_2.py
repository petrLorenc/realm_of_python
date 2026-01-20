# Generic, Python 3.12+

class Animal:
    ...

class Tiger(Animal):
    ...

class Human:
    ...

class Zoo[T: Animal]:
    zoo_animal_list: list[T] = []

    def add_animal(self, animal: T):
        self.zoo_animal_list.append(animal)

class AnotherZoo[T: Animal]:
    def __init__(self, first_animal: T) -> None:
        self.zoo_animal_list = [first_animal]

    def add_animal(self, animal: T):
        self.zoo_animal_list.append(animal)

# zoo = Zoo[int]()
zoo = AnotherZoo(Animal())
zoo.add_animal(Animal())
zoo.add_animal(Tiger())
zoo.add_animal(Human())