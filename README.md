# Job-Shop-Scheduling-Optimization
Optimizing Job Shop Scheduling in a Manufacturing Plant using Genetic Algorithm

## Summary
This project aims to develop a genetic algorithm to optimize job shop scheduling in a manufacturing plant. The goal is to determine the optimal sequence and timing for each product to minimize overall production time or maximize throughput while considering machine capacities and job dependencies.

## Specifications
This application should be able to perform the following tasks:
1. Read the input data containing job sequences and machine constraints. The user should provide the number of machines and a list of jobs with their operation sequences.
2. Implement a genetic algorithm to optimize the scheduling of jobs to minimize total production time.
3. Generate a feasible schedule that adheres to job dependencies and machine availability.
4. Display the optimized schedule, including start and end times for each process on each machine.
5. Output the schedule in a graphical format, such as a Gantt Chart, to visualize job execution over time.
6. Allow the user to specify custom job sequences and machine counts for testing different scenarios.
7. Save the final optimized schedule to an output file for further analysis.

## Input Format
- The system takes as input a list of jobs and the number of available machines.
- Each job consists of a sequence of operations, where each operation specifies the machine required and the processing time.
- The sequence of operations for a given job must be performed in the specified order.

### Example Input:
```
Job_1: M1[10] -> M2[5] -> M4[12]
Job_2: M2[7] -> M3[15] -> M1[8]
```

## Output Format
- A schedule indicating the start and end time for each process and the job to which it belongs.
- A Gantt Chart visualization of the schedule.
- An output file containing the final schedule.

## Authors
Qusay Taradeh, Ali Khalil
