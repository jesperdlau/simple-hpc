import wandb
import hydra
from models.model import MLP, Trainer
from omegaconf import OmegaConf
import torch
from torchvision import datasets, transforms
from torch.utils.data import DataLoader, Subset
import numpy as np

@hydra.main(config_name="config.yaml", config_path="./", version_base="1.3")
def main(config):
    print(f"configuration: \n {OmegaConf.to_yaml(config)}")
    # Reformulate the config to be used in wandb
    config_dict = OmegaConf.to_container(config)
    
    # project is the name of the project in wandb, entity is the username
    # You can also add tags, group etc. 
    wandb.init(project=config.wandb.project, 
               config=config_dict, 
               entity=config.wandb.entity)

    # Usual PyTorch training code using a Trainer class
    model = MLP(config)
    trainer = Trainer(config, model)
    torch.manual_seed(config.hyper.seed)
    
    transform=transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))
        ])
    train_dataset = datasets.MNIST(config.data_path, train=True, download=True, transform=transform)
    valid_dataset = datasets.MNIST(config.data_path, train=False, transform=transform)
    train_dataset = Subset(train_dataset, np.arange(10000))
    valid_dataset = Subset(valid_dataset, np.arange(10000))
    train_loader = DataLoader(train_dataset, batch_size=config.hyper.batch_size, shuffle=True)
    valid_loader = DataLoader(valid_dataset, batch_size=config.hyper.batch_size, shuffle=False)
    
    trainer.train(train_loader=train_loader, valid_loader=valid_loader)
    
    
if __name__ == "__main__":
    main()