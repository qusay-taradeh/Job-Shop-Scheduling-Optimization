import pandas  # pandas library that get the values from .xlsx file
import random  # random library to get random choices for GA requirement
import matplotlib.pyplot as plt  # matplot library to plot the Gant Chart of solution
import copy  # copy library to copy results to avoid losing

"""
Name: Qusay Taradeh, ID: 1212508, Section: 4
Name: Ali Khalil, ID: 1210750, Section: 1
"""

"""Note: The required files must be in same file of project or same file where .py file stored!"""


"""Evaluation function to create a schedule for a set of jobs and machines, and to evaluate fitness"""


def create_chromosome_and_evaluate_fitness(jobs):
    machine_avail_times = {machine: 0 for machine in machines}  # set of machine and its available time for choose
    job_avail_times = {j[0]: 0 for j in jobs}  # set of jobs and its available time to correct choose
    schedule_result = []  # schedule as output of the function
    make_span = 0  # make_span of schedule "chromosome"

    while any(j[1] for j in jobs):  # loop to check if there is any available to do
        for j in jobs:
            if not j[1]:  # to check if operations done then skip
                continue

            job_id = j[0]
            current_time = job_avail_times[job_id]  # current time is the last available time set
            next_operation = j[1][0]  # next operation i.e.(M1, 10) in the order to do
            if next_operation[0] == 0 or next_operation[1] <= 0: # to handle unexpected input
                j[1].pop(0)
                continue
            machine = next_operation[0]  # machine of this operation i.e.(M1)
            time_required = next_operation[1]  # time of this operation i.e.(10)

            # start time is chosen to ensure correct order
            start_time = max(current_time, machine_avail_times[machine])
            end_time = start_time + time_required  # end time of each operation is start time plus operation time

            # adding the schedule to the list of schedules
            schedule_result.append((job_id, machine, start_time, end_time))

            # setting the available time of the machine and the job
            machine_avail_times[machine] = end_time
            job_avail_times[job_id] = end_time

            # update make_span (fitness)
            make_span = max(make_span, end_time)

            # delete the completed operation
            j[1].pop(0)
    fitness.append(make_span)  # adding the fitness of current schedule to the list of fitness's
    return schedule_result


"""Generation initial population function gets jobs and size of population intended"""


def generate_initial_population(data, population_size):
    generation = []
    for s in range(population_size):  # loop iterates size number to generate multiple different schedules
        shuffled_jobs = copy.deepcopy(data)  # Deep copy to make sure that data is not lost or changed
        random.shuffle(shuffled_jobs)  # shuffle order of jobs randomly
        order = copy.deepcopy(shuffled_jobs)  # Deep copy to make sure that data is not lost or changed
        orders.append(order)  # save new order in the order list
        schedule = create_chromosome_and_evaluate_fitness(shuffled_jobs)  # calling the creation and evaluation
        generation.append(schedule)  # adding the created schedule in the generation list
    return generation


"""Select parents function"""


def select_parents():
    result = []  # list to store 2 parents
    for k in range(2):
        # tournament: list of 5 schedules indexes in random
        tournament = random.sample(range(len(orders)), 5)
        tournament_fitness = [fitness[t] for t in tournament]
        best_index = tournament[tournament_fitness.index(min(tournament_fitness))]  # best schedule depending on fitness
        result.append(orders[best_index])  # adding parent to the list
    return result


"""Cross-Over function"""


def crossover(parent1, parent2):
    cut_point = 5  # cut point in chromosome
    child1 = parent1[:cut_point]  # from start to cut point initially
    child2 = parent2[:cut_point]  # from start to cut point initially
    for k in range(len(parent1)):  # loop over all jobs count in any parent since they are equal
        if parent2[k] not in child1:  # to ensure all jobs will be scheduled in child 1
            child1.append(parent2[k])

        if parent1[k] not in child2:  # to ensure all jobs will be scheduled in child 2
            child2.append(parent1[k])

    # Deep copy to make sure that data is not lost or changed
    copy_child1 = copy.deepcopy(child1)
    copy_child2 = copy.deepcopy(child2)

    # Mutation for each child
    copy_child1 = mutate(copy_child1)
    copy_child2 = mutate(copy_child2)

    # Creating schedule for each child
    child1_schedule = create_chromosome_and_evaluate_fitness(copy_child1)
    child2_schedule = create_chromosome_and_evaluate_fitness(copy_child2)

    # Update the generation to account for new chromosomes
    # if child fitness less than any first found fitness in the generation, then replace with it and its fitness
    # also delete the extra fitness added to fitness list and not in population list
    update1_flag = 0  # flag to check if population updated or not by child 1
    update2_flag = 0  # flag to check if population updated or not by child 2
    for f in fitness:
        # Check Child 1 fitness
        if fitness[-2] < f:
            if fitness.index(f) > generation_size - 1:  # to check if reached to schedule not in population
                break
            # remove schedule from population then fitness lists
            population.pop(fitness.index(f))
            fitness.pop(fitness.index(f))
            population.append(child1_schedule)  # adding the child to the population
            update1_flag = 1  # set flag to 1 to ensure that population updated
            break

    if update1_flag == 0:  # if population not updated then remove the child from fitness list
        fitness.pop(-2)  # -2 represents the pre-last index in the list that is child 1 index

    for f in fitness:
        # Check Child 2 fitness
        if fitness[-1] < f:
            if fitness.index(f) > generation_size - 1:  # to check if reached to schedule not in population
                break
            # remove schedule from population then fitness lists
            population.pop(fitness.index(f))
            fitness.pop(fitness.index(f))
            population.append(child2_schedule)  # adding the child to the population
            update2_flag = 1  # set flag to 1 to ensure that population updated
            break

    if update2_flag == 0:  # if population not updated then remove the child from fitness list
        fitness.pop(-1)  # -2 represents the last index in the list that is child 2 index


"""Mutation function"""


def mutate(schedule):
    mutation_rate = 0.1
    mutated = copy.deepcopy(schedule)  # Deep copy to make sure that data is not lost or changed
    mutation_index1 = random.randint(0, len(mutated) - 1)  # randomly chosen index 1
    mutation_index2 = random.randint(0, len(mutated) - 1)  # randomly chosen index 2

    if random.random() < mutation_rate:  # get random value and check if less than the rate to apply mutation
        temp = mutated[mutation_index1]  # temp list to store the value of 1st index
        # swap 1st and 2nd indices
        mutated[mutation_index1] = mutated[mutation_index2]
        mutated[mutation_index2] = temp
    return mutated


"""Function to print the schedule in simple and descriptive form"""


def print_schedule(schedule, k):
    for job_id, machine, start_time, end_time in schedule:
        print(f"Job: {job_id}, Machine: {machine}, Start: {start_time}, End: {end_time}")
    print(f"Fitness of Schedule: {fitness[k]}")


"""Function to plot the schedule as a Gantt chart"""


def plot_gantt_chart(schedule):
    fig, ax = plt.subplots()  # get figure name and axis from subplot to write on them

    # Set up y-axis ticks and labels for machines
    machines_list = sorted(set(operation[1] for operation in schedule))  # sorted list of machines to display
    ax.set_yticks(range(len(machines_list)))
    ax.set_yticklabels(machines_list)

    job_colors = {}

    # Plot bars for each operation
    for k, (job_id, machine, start_time, end_time) in enumerate(schedule):
        if job_id not in job_colors:
            job_colors[job_id] = f'C{k % 10}'  # Assign a unique color for each job
        machine_index = machines_list.index(machine)
        ax.barh(machine_index, end_time - start_time, left=start_time, height=0.7, color=job_colors[job_id],
                edgecolor='black')

    # Set labels and title
    ax.set_xlabel('Time')
    ax.set_ylabel('Machine')
    ax.set_title('Job Shop Scheduling')

    # Create a legend (list of jobs colors) and place it outside the plot
    handles = [plt.Rectangle((0, 0), 1, 1, color=job_colors[job_id]) for job_id in job_colors]
    labels = [f'Job {job_id}' for job_id in job_colors]
    ax.legend(handles, labels, bbox_to_anchor=(1.05, 1), loc='upper left')

    # Invert y-axis to have 1st machine at the top
    ax.invert_yaxis()

    plt.tight_layout(rect=[0, 0, 0.85, 1])  # Adjust layout to make space for legend
    plt.show()  # display the result gantt chart


"""===============================================Main==============================================="""
# Reading data from Excel and parsing it into a list of tuples
input_file = pandas.read_excel('input.xlsx', sheet_name='Sheet1', skiprows=0)
job_list = input_file.values.tolist()
job_order = []  # list of job in order like original order

# machines: list of generated machines based on number of them entered by user
machines = []

# loop to store each job and its operations in tuple ('job_ID', list of operations[])
# and each operation is tuple of machine and required time for it i.e.('M1', 10)
for job in job_list:
    job_order.append(
        (job[0], [(job[1], job[2]), (job[3], job[4]), (job[5], job[6]), (job[7], job[8]), (job[9], job[10])]))

    for i in range(1,10,2):
        if job[i] not in machines:
            if job[i] == 0:
                continue
            machines.append(job[i])

# Define generation size and fitness list to store final time of each chromosome as the fitness of it
# orders: list of order to store the order of jobs that scheduled later
generation_size = 20
fitness = []
orders = []

generation_limit = 30  # sufficient generations
# generate a population calling generation function and passing size and order of jobs
population = generate_initial_population(job_order, generation_size)
i = 0
while i < generation_limit:  # loop to generate until the limit set
    # Implementing genetic algorithm
    parents = select_parents()
    crossover(parents[0], parents[1])
    i += 1

best_fitness = min(fitness)  # choose the best fitness which is the minimum time required
best_fitness_index = fitness.index(best_fitness)  # determine the index of it
best_schedule = population[best_fitness_index]  # get the schedule of best fitness schedule
print("The Optimal Schedule is: ")
print_schedule(schedule=best_schedule, k=best_fitness_index)  # printing the schedule and its details on output
plot_gantt_chart(best_schedule)  # plotting the Gantt Chart in Figure interface shows clearly the schedule
print("====================================Thanks====================================")
