import pytorch_lightning as pl
import torch
from torchvision.models import resnet18
from torch import nn
from torch.utils.data import DataLoader
from torchvision.datasets import MNIST
from torchvision.transforms import ToTensor

train_ds= MNIST("mnist", train=True, download=True, transform=ToTensor())
test_ds= MNIST("mnist", train=False, download=True, transform=ToTensor())
train_dl= DataLoader(train_ds, batch_size=64, shuffle=True)
test_dl= DataLoader(test_ds, batch_size=64)

class ResNetMNIST(pl.LightningModule):
    def __init__(self):
        super().__init__()
        self.model= resnet18(num_classes=10)
        self.model.conv1 = nn.Conv2d(1, 64, kernel_size=(7, 7), stride=(2, 2), padding=(3, 3), bias=False)
        self.loss= nn.CrossEntropyLoss()

    def forward(self, x):
        return self.model(x)
    
    def training_step(self, batch, batch_no):
        x, y = batch
        logits = self(x)
        loss = self.loss(logits, y)
        return loss
    def configure_optimizers(self):
        return torch.optim.RMSprop(self.parameters(), lr=0.005)

model = ResNetMNIST()
trainer = pl.Trainer(max_epochs=1000)
trainer.fit(model, train_dl)
trainer.save_checkpoint("resnet18_mnist.pt")

def get_prediction(x, model: pl.LightningModule):
    model.freeze() # prepares model for predicting
    probabilities = torch.softmax(model(x), dim=1)
    predicted_class= torch.argmax(probabilities, dim=1)
    return predicted_class, probabilities

from tqdm.autonotebook import tqdm

inference_model= ResNetMNIST.load_from_checkpoint("resnet18_mnist.pt", map_location="cuda")
true_y, pred_y= [], []
for batch in tqdm(iter(test_dl), total=len(test_dl)):
    x, y = batch
    true_y.extend(y)
    preds, probs = get_prediction(x, inference_model)
    pred_y.extend(preds.cpu())

from sklearn.metrics import classification_report

print(classification_report(true_y, pred_y, digits=3))