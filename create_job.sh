#!/bin/bash

# Take arguments from CLI with flags
while getopts ":a:b:" opt; do
  case $opt in
    a) arg1="$OPTARG"
    ;;
    b) arg2="$OPTARG"
    ;;
    \?) echo "Invalid option -$OPTARG" >&2
    ;;
  esac
done

# Set the W&B API key environmental variable
export WANDB_API_KEY="your_api_key_here"
export arg1=$arg1
export arg2=$arg2

echo "Environment variables outside job:"
echo "Epochs: $arg1"
echo "Batch_size: $arg2"
echo "wandb_api_key: $WANDB_API_KEY"

# Launch an LSF job by parsing a submit.sh script to bsub with the arguments
bsub -env "all" < submit.sh
