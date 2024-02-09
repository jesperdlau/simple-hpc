#!/bin/sh
### General options
### –- specify queue --
#BSUB -q hpc
### -- set the job Name --
#BSUB -J test

### GPU
### -- Select the resources: 1 gpu in exclusive process mode --
#BSUB -gpu "num=1"
### BSUB -R "select[gpu40gb]"

### CPU
### -- ask for number of CPU cores (default: 4) (at least 4x amount of gpus) --
#BSUB -n 4
#BSUB -R "rusage[mem=4GB]"
#BSUB -R "span[hosts=1]"

### -- set walltime limit: hh:mm --  maximum 24 hours for GPU-queues right now
#BSUB -W 24:00
### -- set the email address --
# please uncomment the following line and put in your e-mail address,
# if you want to receive e-mail notifications on a non-default address
##BSUB -u your_email_address
### -- send notification at start --
#BSUB -B
### -- send notification at completion--
#BSUB -N
### -- Specify the output and error file. %J is the job-id --
### -- -o and -e mean append, -oo and -eo mean overwrite --
#BSUB -o gpu_%J.out
#BSUB -e gpu_%J.err
# -- end of LSF options --

# Load the python module and activate the virtual environment
module load python3/3.10.7
source /zhome/2e/b/169155/projects/simple-hpc/.venv/bin/activate

echo "Environment variables within job:"
echo "Epochs: $arg1"
echo "Batch_size: $arg2"
echo "wandb_api_key: $WANDB_API_KEY"

# Run the python script
python3 /zhome/2e/b/169155/projects/simple-hpc/train.py hyper.epochs=$arg1 hyper.batch_size=$arg2