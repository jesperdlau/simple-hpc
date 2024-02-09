import subprocess
from omegaconf import OmegaConf
import hydra
import os

# Set environment variable
<<<<<<< Updated upstream
os.environ['WANDB_API_KEY'] = "your_api_key"
print(os.environ['WANDB_API_KEY'])
=======
os.environ['WANDB_API_KEY'] = "8d8198f8b41c68eed39ef9021f8bea9633eb2f6e" 
print(os.environ['MY_VARIABLE'])
>>>>>>> Stashed changes

# 
@hydra.main(config_name="config.yaml", config_path="./", version_base="1.3")
def main(config):
    print(f"configuration: \n {OmegaConf.to_yaml(config)}")
    
    command = f"""bsub -q {config.bsub.queue} 
                -J {config.bsub.name} 
                -gpu {config.bsub.gpu_num}
                -n {config.bsub.cpu_num}
                -R "rusage[mem={config.bsub.cpu_mem}GB]"
                -R "span[hosts=1]"
                -W 24:00
                -B 
                -N 
                -o lsf_logs/gpu_%J.out
                -e lsf_logs/gpu_%J.err
                -env "all" 
                python3 my_program.py 
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
