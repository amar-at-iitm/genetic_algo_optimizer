# src/operators.py
import random

def create_individual(data):
    """
    Creates a random individual (schedule).
    An individual is a list of (job_id, machine_id) tuples.
    The order of the list is a permutation of jobs.
    """
    jobs = list(data['jobs'].keys())
    random.shuffle(jobs) # Random job sequence
    
    individual = []
    for job_id in jobs:
        # Assign a random machine
        machine_id = random.choice(data['machines'])
        individual.append((job_id, machine_id))
        
    return individual

def repair_individual(individual, data):
    """
    Repairs an individual to satisfy precedence constraints.
    Ensures that for any (A, B) precedence, A appears before B in the list.
    
    This is a simple but potentially inefficient repair function.
    More advanced repair mechanisms could be used for larger problems.
    """
    job_order = [job_id for job_id, _ in individual]
    job_indices = {job: i for i, job in enumerate(job_order)}
    
    for prec in data.get('precedence', []):
        job_a, job_b = prec[0], prec[1]
        idx_a = job_indices.get(job_a, -1)
        idx_b = job_indices.get(job_b, -1)
        
        # If B comes before A, swap them
        if idx_a > idx_b:
            # Swap positions in the original individual list
            individual[idx_a], individual[idx_b] = individual[idx_b], individual[idx_a]
            # Update indices to reflect the swap for the rest of the loop
            job_indices[job_a], job_indices[job_b] = idx_b, idx_a
            
    return individual