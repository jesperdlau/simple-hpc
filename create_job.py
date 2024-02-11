import subprocess
from omegaconf import OmegaConf
import hydra
import os

# Set environment variable by reading from secret file
# This is a good practice to avoid exposing your API key
# You can also set this in your bashrc or zshrc file
with open("secret.txt", "r") as f:
    os.environ['WANDB_API_KEY'] = f.read().strip()

# 
@hydra.main(config_name="config.yaml", config_path="./", version_base="1.3")
def main(config):
    print(f"configuration: \n {OmegaConf.to_yaml(config)}")
    
    command = f"""bsub -q {config.bsub.queue} 
                -J {config.bsub.name} 
                -gpu "num={config.bsub.gpu_num}"
                -n {config.bsub.cpu_num}
                -R "rusage[mem={config.bsub.cpu_mem}GB]"
                -R "span[hosts=1]"
                -W 24:00
                -B 
                -N 
                -o lsf_logs/gpu_%J.out
                -e lsf_logs/gpu_%J.err
                -env "all" 
                python3 train.py
                hyper.lr={config.hyper.lr} 
                hyper.epochs={config.hyper.epochs}
                hyper.batch_size={config.hyper.batch_size}
                hyper.hidden_dim={config.hyper.hidden_dim}
                """
    command = command.replace("\n", " ")
    command = " ".join(command.split())
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    output, error = process.communicate()
    
    if error:
        print(f"Error: {error}")
    else:
        print(f"Output: {output.decode('utf-8')}")
        
if __name__ == "__main__":
    main()
