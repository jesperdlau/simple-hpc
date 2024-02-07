import numpy as np
import torch 
import torch.nn as nn
from torch import optim
from torch.nn import functional as F
import wandb


class MLP(nn.Module):
    def __init__(self, config):
        super(MLP, self).__init__()
        self.config = config
        self.relu = nn.ReLU()
        self.conv1 = nn.Conv2d(1, 32, 3, 1)
        self.conv2 = nn.Conv2d(32, 64, 3, 1)
        self.dropout1 = nn.Dropout(0.25)
        self.dropout2 = nn.Dropout(0.5)
        self.fc1 = nn.Linear(9216, 128)
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):
        x = self.conv1(x)
        x = self.relu(x)
        x = self.conv2(x)
        x = self.relu(x)
        x = F.max_pool2d(x, 2)
        x = self.dropout1(x)
        x = torch.flatten(x, 1)
        x = self.fc1(x)
        x = self.relu(x)
        x = self.dropout2(x)
        x = self.fc2(x)
        output = F.log_softmax(x, dim=1)
        return output

class Trainer():
    def __init__(self, config, model):
        self.config = config
        self.model = model
        self.optimizer = optim.Adam(model.parameters(), lr=config.hyper.lr)
        self.criterion = nn.CrossEntropyLoss()
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model.to(self.device)
        self.model.train()
        
    def train(self, train_loader, valid_loader):
        
        for epoch in range(self.config.hyper.epochs):
            self.model.train()
            training_loss = 0.0
            for batch_idx, (data, target) in enumerate(train_loader):
                data, target = data.to(self.device), target.to(self.device)
                self.optimizer.zero_grad()
                output = self.model(data)
                loss = self.criterion(output, target)
                loss.backward()
                self.optimizer.step()
                training_loss += loss.item()
            
            self.model.eval()
            valid_loss = 0.0
            for batch_idx, (data, target) in enumerate(valid_loader):
                data, target = data.to(self.device), target.to(self.device)
                output = self.model(data)
                loss = self.criterion(output, target)
                valid_loss += loss.item()
                
            wandb.log({"training_loss": training_loss / len(train_loader)})
            wandb.log({"val_loss": valid_loss / len(valid_loader)})
            print(f"Epoch: {epoch} / {self.config.hyper.epochs}")
            print(f"training_loss: {training_loss / len(train_loader)}")
            print(f"val_loss: {valid_loss / len(valid_loader)}")
            
            
        print('Finished Training')

    # def test(self, test_loader):
    #     self.model.eval()
    #     test_loss = 0
    #     correct = 0
    #     with torch.no_grad():
    #         for data, target in test_loader:
    #             data, target = data.to(self.device), target.to(self.device)
    #             output = self.model(data)
    #             test_loss += self.criterion(output, target).item()
    #             pred = output.argmax(dim=1, keepdim=True)
    #             correct += pred.eq(target.view_as(pred)).sum().item()

    #     test_loss /= len(test_loader.dataset)
    #     accuracy = 100. * correct / len(test_loader.dataset)
    #     #wandb.log({"val_loss": test_loss, "val_accuracy": accuracy})
    #     print(f"\nTest set accuracy: {test_loss:.4f}, Accuracy: {correct}/{len(test_loader.dataset)} ({accuracy:.0f}%)\n")
    