# simple-hpc
Example of a simple AI project integrated with DTU's hpc using a few MLOPS tools. 

1. Login to the DTU HPC. Follow the official documentation. 
2. Make sure you are in a linux shell and not a login node - In terminal type: linuxsh
3. Make sure a python module is loaded. In terminal type: module load python3/3.10.7
4. Clone this repository
5. Create a python environment - In terminal type: python3 -m venv .venv
6. Activate the environment: source .venv/bin/activate
7. Install the packages in the requirements file: pip install -r requirements.txt
8. Create a Weights and Biases account. Create a project and paste the API key to the create_job.sh script. 
9. Make sure the create_job.sh and submit.sh scripts are executable - In terminal type (for both): chmod +x create_job.sh
10. Submit jobs to the HPC by typing: ./create_job.sh
11. You can change the variables by for example: ./create_job.sh -a 10 -b 64