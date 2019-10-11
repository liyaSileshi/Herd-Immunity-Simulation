import random, sys
random.seed(42)
from person import Person
from logger import Logger
from virus import Virus


class Simulation(object):
    ''' Main class that will run the herd immunity simulation program.
    Expects initialization parameters passed as command line arguments when file is run.

    Simulates the spread of a virus through a given population. The percentage of the
    population that are vaccinated, the size of the population, and the amount of initially
    infected people in a population are all variables that can be set when the program is run.
    '''
    def __init__(self, pop_size, vacc_percentage, virus, initial_infected=1):
        ''' Logger object logger records all events during the simulation.
        Population represents all Persons in the population.
        The next_person_id is the next available id for all created Persons,
        and should have a unique _id value.
        The vaccination percentage represents the total percentage of population
        vaccinated at the start of the simulation.
        You will need to keep track of the number of people currently infected with the disease.
        The total infected people is the running total that have been infected since the
        simulation began, including the currently infected people who died.
        You will also need to keep track of the number of people that have die as a result
        of the infection.

        All arguments will be passed as command-line arguments when the file is run.
        HINT: Look in the if __name__ == "__main__" function at the bottom.
        '''
       
        
        self.next_person_id = 0 # Int
        self.virus = virus # Virus object
        self.initial_infected = initial_infected # Int
        self.total_infected = 0 # Int
        self.current_infected = 0 # Int
        self.vacc_percentage = vacc_percentage # float between 0 and 1
        self.total_dead = 0 # Int
        self.file_name = "{}_simulation_pop_{}_vp_{}_infected_{}.txt".format(
            self.virus.name, pop_size, vacc_percentage, initial_infected)

        self.logger = Logger(self.file_name)
        self.pop_size = pop_size # Int
        self.infected_list = []
        self.new_vaccinated = 0
        self.vaccine_saves = 0
        self.population = self._create_population(self.initial_infected)

        self.newly_infected = []
        

    def _create_population(self, initial_infected):
        '''This method will create the initial population.
            Args:
                initial_infected (int): The number of infected people that the simulation
                will begin with.

            Returns:
                list: A list of Person objects.

        '''
        
        population = []
        self.next_person_id = 0

        
        people_vacc = round(self.vacc_percentage * self.pop_size)
       
        for i in range(self.pop_size):

            if initial_infected > 0:
                person = Person(self.next_person_id, False, self.virus)
                population.append(person)
                self.infected_list.append(person)
                initial_infected -= 1
                self.total_infected += 1

            elif people_vacc > 0:
                population.append(Person(self.next_person_id, True))
                people_vacc -= 1
                self.new_vaccinated += 1

            else:
                population.append(Person(self.next_person_id, False))
            self.next_person_id += 1

        return population


    def _simulation_should_continue(self):
        ''' The simulation should only end if the entire population is dead
        or everyone is vaccinated.
            Returns:
                bool: True for simulation should continue, False if it should end.
        '''
        
        for person in self.population:
            if person.is_alive and person.infection is not None :

                return True
        
        return False



    def run(self):
        ''' This method should run the simulation until all requirements for ending
        the simulation are met.
        '''
        self.logger.write_metadata(self.pop_size, self.vacc_percentage, self.virus.name, self.virus.mortality_rate, self.virus.repro_rate)

        # HINT: You may want to call the logger's log_time_step() method at the end of each time step.
        # TODO: Set this variable using a helper
        time_step_counter = 0
        #should_continue = self._simulation_should_continue()
        while self._simulation_should_continue():
        # TODO: for every iteration of this loop, call self.time_step() to compute another
        # round of this simulation.
            self.time_step()
            time_step_counter += 1
            self.logger.log_time_step(time_step_counter, self.total_infected, self.total_dead, self.vaccine_saves)
        print(f'The simulation has ended after {time_step_counter} turns.')
           
        
    def get_rand_person(self):
        rand_person = random.choice(self.population)
        if rand_person.is_alive :
            return rand_person
        else:
            return self.get_rand_person()
    
    def time_step(self):
        ''' This method should contain all the logic for computing one time step
        in the simulation.

        This includes:
            1. 100 total interactions with a randon person for each infected person
                in the population
            2. If the person is dead, grab another random person from the population.
                Since we don't interact with dead people, this does not count as an interaction.
            3. Otherwise call simulation.interaction(person, random_person) and
                increment interaction counter by 1.
            '''
        interaction_counter = 0
        for infected in self.infected_list:
            interaction_counter = 0
            while interaction_counter <= 100 and infected.is_alive:

                rand_person = self.get_rand_person()
                self.interaction(infected, rand_person)
                interaction_counter += 1

        for infected_person in self.infected_list:

            if infected_person.did_survive_infection():
                self.logger.log_infection_survival(infected_person, True)
                self.new_vaccinated += 1

            else:

                self.logger.log_infection_survival(infected_person, False)
                self.total_dead += 1


        self.infected_list = []
        self._infect_newly_infected()
        
        print(self.total_dead+self.new_vaccinated)
               

    def interaction(self, person, random_person):
        '''This method should be called any time two living people are selected for an
        interaction. It assumes that only living people are passed in as parameters.

        Args:
            person1 (person): The initial infected person
            random_person (person): The person that person1 interacts with.
        '''
        # Assert statements are included to make sure that only living people are passed
        # in as params
        #print(person.is_alive)
        assert person.is_alive == True
        assert random_person.is_alive == True

        # TODO: Finish this method.
        #  The possible cases you'll need to cover are listed below:
            # random_person is vaccinated:
            #     nothing happens to random person.
            # random_person is already infected:
            #     nothing happens to random person.
            # random_person is healthy, but unvaccinated:
            #     generate a random number between 0 and 1.  If that number is smaller
            #     than repro_rate, random_person's ID should be appended to
            #     Simulation object's newly_infected array, so that their .infected
            #     attribute can be changed to True at the end of the time step.
        # TODO: Call slogger method during this method.
        if random_person.is_vaccinated :

            self.logger.log_interaction(person, random_person, random_person_vacc= True)
            self.vaccine_saves += 1

        elif random_person.is_vaccinated == False and random_person.infection == None:
            num = random.uniform(0.0, 1.0)
            if num < self.virus.repro_rate :
                self.newly_infected.append(random_person._id)
                print('got infected')
                self.logger.log_interaction(person, random_person, did_infect = True)
            

        # if random_person.is_vaccinated == True or random_person.infection is not None:
        
        
        elif random_person.infection:

            self.logger.log_interaction(person, random_person, random_person_sick = True)

    def _infect_newly_infected(self):
        ''' This method should iterate through the list of ._id stored in self.newly_infected
        and update each Person object with the disease. '''
        # TODO: Call this method at the end of every time step and infect each Person.
        # TODO: Once you have iterated through the entire list of self.newly_infected, remember
        # to reset self.newly_infected back to an empty list.
        # senew_vaccinated = []
        #infected_people = []
        for id in self.newly_infected:
            for person in self.population:
                if id == person._id:
                    person.infection = self.virus
                    self.infected_list.append(person)
                    self.total_infected += 1
                    
                   
        self.newly_infected = []            
                    
        



if __name__ == "__main__":
    # params = sys.argv[1:]
    # virus_name = str(params[0])
    # repro_num = float(params[1])
    # mortality_rate = float(params[2])

    # pop_size = int(params[3])
    # vacc_percentage = float(params[4])

    # if len(params) == 6:
    #     initial_infected = int(params[5])
    # else:
    #     initial_infected = 1
    # virus = Virus(name, repro_rate, mortality_rate)
    # sim = Simulation(pop_size, vacc_percentage, initial_infected, virus)

    # sim.run()
    # virus = Virus("Ebola",0.25 , 0.7)
    virus = Virus("Smallpox", 0.06 , 0.15)
    #sim = Simulation(100000,90,virus,10)
    sim = Simulation(1000, 0.8, virus, 50)
    #sim._create_population(10)
    #print(sim.population)
    # print(len(sim._create_population(15)))
    # print(len(sim.infected_list))
    # sim.interaction(Person(1, False, virus), Person(2, False))
    # print(sim.newly_infected[0])
    #for sim in sim.newly_infected:
    # sim._infect_newly_infected()
    sim.run()
    # print(sim.total_dead+sim.new_vaccinated)
    # print(sim.total_dead+sim.new_vaccinated+sim.initial_infected)
