# Generic, Python 3.11<

from typing import TypeVar, Generic

TAnimal = TypeVar("TAnimal", bound="Animal")

class Animal:
    ...

class Tiger(Animal):
    ...

class Human:
    ...

class Zoo(Generic[TAnimal]):
    zoo_animal_list: list[TAnimal] = []

    def add_animal(self, animal: TAnimal):
        self.zoo_animal_list.append(animal)

class AnotherZoo(Generic[TAnimal]):
    def __init__(self, first_animal: TAnimal) -> None:
        self.zoo_animal_list = [first_animal]

    def add_animal(self, animal: TAnimal):
        self.zoo_animal_list.append(animal)

# zoo = Zoo[int]()
zoo = AnotherZoo(Animal())
zoo.add_animal(Animal())
zoo.add_animal(Tiger())
zoo.add_animal(Human())