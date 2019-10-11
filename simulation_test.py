import virus
import person
import simulation
import pytest

virus = simulation.Virus('Ebola', 0.25, 0.7)
sim = simulation.Simulation(100,0.5,virus,10)

def test_simulation_instance():
    # Test instantiation without error
    sim = simulation.Simulation(100,0.5,virus,10)
    assert sim


def test_create_population():
    population = sim._create_population(5)
    assert population
    for i in range(len(population)):
        if i < 5:
            person = population[i]
            assert person._id == i

