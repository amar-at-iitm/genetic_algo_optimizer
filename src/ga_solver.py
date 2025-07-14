# src/ga_solver.py
import random
import argparse
import json

from deap import base, creator, tools, algorithms
import numpy

from utils import load_problem_data
from evaluator import evaluate_schedule
from operators import create_individual, repair_individual

# --- DEAP Setup ---
# Define the fitness objectives. We want to MINIMIZE all of them.
# (lateness, makespan, -profit, violations)
creator.create("FitnessMulti", base.Fitness, weights=(-1.0, -1.0, -1.0, -1.0))
creator.create("Individual", list, fitness=creator.FitnessMulti)

def main(config_path, output_path, use_nsga2=False):
    """Main function to run the GA solver."""
    
    # Load problem data
    data = load_problem_data(config_path)
    if data is None:
        return

    toolbox = base.Toolbox()

    # Attribute generator: creates one gene (job, machine)
    toolbox.register("individual", tools.initIterate, creator.Individual, lambda: create_individual(data))
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    # Operator registration
    toolbox.register("evaluate", evaluate_schedule, data=data)
    toolbox.register("mate", tools.cxOrdered) # Order crossover for the sequence
    toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.1) # Shuffle jobs
    toolbox.register("select", tools.selNSGA2 if use_nsga2 else tools.selTournament, tournsize=3)
    
    # --- GA Parameters ---
    POP_SIZE = 100
    CXPB = 0.8  # Crossover probability
    MUTPB = 0.3 # Mutation probability
    NGEN = 150  # Number of generations

    # --- Statistics and Logging ---
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean, axis=0)
    stats.register("std", numpy.std, axis=0)
    stats.register("min", numpy.min, axis=0)
    stats.register("max", numpy.max, axis=0)

    logbook = tools.Logbook()
    logbook.header = "gen", "evals", "min", "avg", "max"

    pop = toolbox.population(n=POP_SIZE)

    # --- Run GA ---
    print(" Starting GA evolution...")
    
    # This is the standard DEAP evolutionary algorithm
    algorithms.eaMuPlusLambda(
        population=pop,
        toolbox=toolbox,
        mu=POP_SIZE,
        lambda_=POP_SIZE,
        cxpb=CXPB,
        mutpb=MUTPB,
        ngen=NGEN,
        stats=stats,
        halloffame=tools.HallOfFame(1),
        verbose=True
    )
    
    # --- Results ---
    best_ind = tools.selBest(pop, 1)[0]
    best_fitness = best_ind.fitness.values

    print("\nEvolution Finished!")
    print(f" Best Individual Found: \n{best_ind}")
    print(f"Fitness: Lateness={best_fitness[0]:.2f}, Makespan={best_fitness[1]:.2f}, Profit={-best_fitness[2]:.2f}, Violations={best_fitness[3]}")
    
    # Save results to output file
    if output_path:
        results = {
            "best_schedule": best_ind,
            "fitness": {
                "lateness": best_fitness[0],
                "makespan": best_fitness[1],
                "profit": -best_fitness[2],
                "violations": best_fitness[3]
            }
        }
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2)
        print(f" Results saved to {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GA Job Shop Scheduler")
    parser.add_argument("--input", type=str, required=True, help="Path to the problem data JSON file.")
    parser.add_argument("--output", type=str, default="schedule_results.json", help="Path to save the output schedule.")
    parser.add_argument("--nsga2", action='store_true', help="Use NSGA-II for multi-objective selection.")
    
    args = parser.parse_args()
    main(args.input, args.output, args.nsga2)