#!/bin/bash

# Define the number of instances to run
NUM_INSTANCES=30
TOTAL_KEYWORDS=77755

CHUNK_SIZE=$((TOTAL_KEYWORDS / NUM_INSTANCES))
echo "Chunk size for each instance: $CHUNK_SIZE"#

for ((i=0; i<$NUM_INSTANCES; i++)); do
    # Calculate the start index for this instance
    START_INDEX=$((i * CHUNK_SIZE))

    # Calculate the end index for this instance
    if [ $i -eq $((NUM_INSTANCES - 1)) ]; then
        # If this is the last iteration, include the remaining keywords
        END_INDEX=$TOTAL_KEYWORDS
    else
        END_INDEX=$((START_INDEX + CHUNK_SIZE))
    fi

    echo "$START_INDEX - $END_INDEX"
	python main.py --start $START_INDEX --end $END_INDEX &
done
