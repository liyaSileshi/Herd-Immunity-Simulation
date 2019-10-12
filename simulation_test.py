import virus
import person
import simulation
import pytest
import os

virus = simulation.Virus('Ebola', 0.25, 0.7)
sim = simulation.Simulation(100,0.5,virus,10)

def test_simulation_instance():
    # Test instantiation without error
    sim = simulation.Simulation(100,0.5,virus,10)
    assert sim
    assert len(sim.population) == 100
    assert sim.pop_size == 100
    assert sim.virus.name == "Ebola"
    assert sim.virus.mortality_rate == 0.7
    assert sim.virus.repro_rate == 0.25
    assert sim.total_dead == 0
    assert sim.total_infected == 10
    assert sim.vaccine_saves == 0

def test_create_population():
    population = sim._create_population(5)
    assert population
    for i in range(len(population)):
        if i < 5:
            person = population[i]
            assert person._id == i
        normal = 0
        vacc = 0
        infected = 0
        for person in sim.population:
            if person.is_vaccinated:
                vacc += 1

            elif person.infection:
                infected += 1
            else:
                normal += 1

    assert normal == 40
    assert infected == 10
    assert vacc == 50

def test_simulation_should_continue():
    assert sim._simulation_should_continue() == True
    for sims in sim.population:
        sims.is_alive = False
    assert sim._simulation_should_continue() == False
    
def test_interaction():
    sim1 = person.Person (1, False, virus)
    sim2 = person.Person(2, False, None)
    interact = sim.interaction(sim1, sim2)
    assert interact
    if interact < virus.repro_rate:
        assert sim.newly_infected[0] == 2
    else:
        assert len(sim.newly_infected) == 0

