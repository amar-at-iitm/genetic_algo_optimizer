# src/evaluator.py
import sys

def evaluate_schedule(individual, data):
    """
    Calculates the fitness of a given schedule (individual).
    
    The fitness vector is:
    [total_lateness, makespan, -total_profit, constraint_violations]
    We aim to MINIMIZE all these values.
    """
    machine_finish_times = {m: 0 for m in data['machines']}
    job_completion_times = {}
    
    total_profit = 0
    total_lateness = 0
    constraint_violations = 0
    
    # Create a map for quick job data access
    job_data = data['jobs']
    
    # 1. Check for precedence constraint violations
    job_order = [job_id for job_id, machine_id in individual]
    job_indices = {job: i for i, job in enumerate(job_order)}
    
    for prec in data.get('precedence', []):
        job_a, job_b = prec[0], prec[1]
        if job_indices.get(job_a, -1) > job_indices.get(job_b, -1):
            constraint_violations += 1
            
    # 2. Calculate schedule timings and metrics
    for job_id, machine_id in individual:
        proc_time = job_data[job_id]['processing_times'][machine_id]
        
        # Start time is the latest of machine available time or predecessor finish time
        machine_ready_time = machine_finish_times[machine_id]
        
        predecessor_finish_time = 0
        for prec in data.get('precedence', []):
            if prec[1] == job_id: # if job_id is the successor
                pred_job_id = prec[0]
                if pred_job_id in job_completion_times:
                    predecessor_finish_time = max(predecessor_finish_time, job_completion_times[pred_job_id])
        
        start_time = max(machine_ready_time, predecessor_finish_time)
        finish_time = start_time + proc_time
        
        # Update machine and job completion times
        machine_finish_times[machine_id] = finish_time
        job_completion_times[job_id] = finish_time
        
        # Calculate profit and lateness
        total_profit += job_data[job_id]['profit']
        lateness = max(0, finish_time - job_data[job_id]['deadline'])
        total_lateness += lateness * data['penalties']['lateness_per_unit']

    # 3. Calculate makespan (total time)
    makespan = max(machine_finish_times.values()) if machine_finish_times else 0
    
    # The penalty for violations should be very high to discourage them
    violation_penalty = constraint_violations * data['penalties']['violation']
    
    # Return the fitness tuple for minimization
    # Note: We return -total_profit because DEAP minimizes, so minimizing a negative is maximizing.
    return (total_lateness, makespan, -total_profit, violation_penalty)