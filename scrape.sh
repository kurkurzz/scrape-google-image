#!/bin/bash

# Define the number of instances to run
NUM_INSTANCES=2

echo "Total instance: $NUM_INSTANCES"#

for ((i=0; i<$NUM_INSTANCES; i++)); do
	python main_extended.py &
done

# Wait for all instances to finish
wait

echo "All instances have finished."
