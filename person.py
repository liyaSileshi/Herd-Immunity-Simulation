import random
random.seed(42)
from virus import Virus
import pytest

class Person(object):
    ''' Person objects will populate the simulation. '''

    def __init__(self, _id, is_vaccinated, infection=None):
        ''' We start out with is_alive = True, because we don't make vampires or zombies.
        All other values will be set by the simulation when it makes each Person object.

        If person is chosen to be infected when the population is created, the simulation
        should instantiate a Virus object and set it as the value
        self.infection. Otherwise, self.infection should be set to None.
        '''
        self._id = _id  
        self.is_alive = True  
        self.is_vaccinated = is_vaccinated  
        self.infection = infection 

    def did_survive_infection(self):
        ''' Generate a random number and compare to virus's mortality_rate.
        If random number is smaller, person dies from the disease.
        If Person survives, they become vaccinated and they have no infection.
        Return a boolean value indicating whether they survived the infection.
        '''
        # Only called if infection attribute is not None.
        # TODO:  Finish this method. Should return a Boolean
        
        if self.infection is not None:
            survival_rate = random.uniform(0.0, 1.0)

            if survival_rate < self.infection.mortality_rate:
                self.is_alive = False

            else:
                self.is_vaccinated = True
                self.infection = None


        return self.is_alive
''' These are simple tests to ensure that you are instantiating your Person class correctly. '''
def test_vacc_person_instantiation():
    # create some people to test if our init method works as expected
    person = Person(1, True)
    assert person._id == 1
    assert person.is_alive is True
    assert person.is_vaccinated is True
    assert person.infection is None


def test_not_vacc_person_instantiation():
    person = Person(2, False)
    assert person._id == 2
    assert person.is_vaccinated is False
    assert person.is_alive is True
    assert person.infection is None
    


def test_sick_person_instantiation():
    # Create a Virus object to give a Person object an infection
    virus = Virus("Dysentery", 0.7, 0.2)
    # Create a Person object and give them the virus infection
    person = Person(3, False, virus)
   
    assert person._id == 3
    assert person.is_vaccinated is False
    assert person.infection.name == virus.name
    assert person.infection.repro_rate == virus.repro_rate
    assert person.infection.mortality_rate == virus.mortality_rate
    assert person.is_alive == True 

    virus2 = Virus("HIV", 0.8, 0.3)
    person2 = Person(4, True,virus2)

    assert person2._id == 4
    assert person2.is_vaccinated is True
    assert person2.infection.name == virus2.name
    assert person2.infection.repro_rate == virus2.repro_rate
    assert person2.infection.mortality_rate == virus2.mortality_rate
    assert person2.is_alive == True 


def test_did_survive_infection():
    # Create a Virus object to give a Person object an infection
    virus = Virus("Dysentery", 0.7, 0.2)
    # Create a Person object and give them the virus infection
    person = Person(4, False, virus)

    # Resolve whether the Person survives the infection or not
    survived = person.did_survive_infection()
    # Check if the Person survived or not
    if survived:
        assert person.is_alive is True
        # TODO: Write your own assert statements that test
        # the values of each attribute for a Person who survived
        # assert ...
        assert person.is_vaccinated == True
        assert person.infection == None

    else:
        assert person.is_alive is False
        # TODO: Write your own assert statements that test
        # the values of each attribute for a Person who did not survive
        # assert ...
        assert person.is_vaccinated == False
        assert person.infection.name == virus.name
        assert person.infection.repro_rate == virus.repro_rate
        assert person.infection.mortality_rate == virus.mortality_rate