# simple-hpc
Example of a simple AI project integrated with DTU's hpc using a few MLOPS tools. 

1. Create a Weights and Biases account. Create a project and get the wandb API key.
2. Login to the DTU HPC. Follow the official documentation. 
3. Make sure you are in a linux shell and not a login node - In terminal type: linuxsh
4. Make sure a python module is loaded. In terminal type: module load python3/3.10.7 (Optionally, add it to your .bashrc)
5. Clone this repository
6. Create a python environment - In terminal type: python3 -m venv .venv
7. Activate the environment: source .venv/bin/activate
8. Install the packages in the requirements file: pip install -r requirements.txt
9. Create a file called secret.txt and paste the API key to it. F.ex: echo *my_api_key* >> secret.txt
10. Change the config.yaml file with correct project name and user name
11. Submit jobs to the HPC by typing: python3 create_job.py
    1.  You can change the variables by for example: python3 create_job.py hyper.epochs=10 hyper.batch_size=64
    2.  See the available options in the config.yaml file. Add your own in the create_job.py script.
    3.  Change the BSUB queue options to suite your job needs.
    4.  The LSF hpc logs will be added to the lsf_logs folder. Read them in terminal by f.ex: cat gpu_123456.out