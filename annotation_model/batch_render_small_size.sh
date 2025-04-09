#!/bin/bash

# Set the initial start_idx and batch size
#31519
id=31519
start_idx=0

num_processes=72
batch_size=720
# Log file for execution time
#time_log_file="./execution_time.log"
time_log_file=./execution_time_${id}.log

# Run the Python script 200 times
for i in {1..100}; do
    # Calculate end_idx
    end_idx=$((start_idx + batch_size))

    # Log start time
    start_time=$(date +%s)
    echo "start"
    echo "Iteration $i: start_idx=$start_idx, end_idx=$end_idx" >> "$time_log_file"
    echo "Start time: $(date)" >> "$time_log_file"

    # Run the Python script with the current start_idx and end_id
    taskset -c 0-71 python3 persistent_batch_render_auto.py --start_idx "$start_idx" --end_idx "$end_idx" --num_processes "$num_processes"

    # Log end time and calculate elapsed time
    end_time=$(date +%s)
    elapsed_time=$((end_time - start_time))

    echo "End time: $(date)" >> "$time_log_file"
    echo "Iteration $i: Execution time: $elapsed_time seconds" >> "$time_log_file"
    echo "----------------------------" >> "$time_log_file"

    # Update start_idx for the next iteration
    start_idx=$end_idx
done
