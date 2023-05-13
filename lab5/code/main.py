# numpy for loading dataset
import numpy as np
# pytorch for deep learning models
import torch
import torch.nn as nn
import torch.optim as optim

# Pima indians describes pateitn medical data and whether they had diabetes for last 5 years
# It is binary classification (they could either have diabetes 1 or not 0)
# load the file as a matrix of numbers,
dataset = np.loadtxt('pima-indians-diabetes.csv', delimiter=',')
# split into input (X) -> in this case everything beside info whether patient had diabetes or not is input
# We are spliting data into two subsets by using NumPy slie operator : and choose first 8 columns using 0:8 slice
X = dataset[:,0:8]
# and output (y) variables -> in this case we are only interested whether patient had diabetes or not as an output
# you can simplify that y = f(X)
# We are spliting the data by using slice operator : and choosing last column
y = dataset[:,8]

# we need to convert this data to pytorch tensors 
# Pyutoarch usually operates on 32-bit floating point and NumPy by default uses 64 bit floating point
X = torch.tensor(X, dtype=torch.float32)
# We can also correct the shape to fit what PyTorch would expect (here we are converting n vectors to n x 1 matrix)
# This simplifies handling matrix multiplication operations (which are the basis of deep learning models)
# reshape is converting the output variable y from a 1-dimensional NumPy array to a 2-dimensional PyTorch tensor with a shape of (n, 1), where n is the number of samples in the dataset.
y = torch.tensor(y, dtype=torch.float32).reshape(-1, 1)

# define the model
class PimaClassifier(nn.Module):
    def __init__(self):
        super().__init__()
        self.hidden1 = nn.Linear(8, 12)
        self.act1 = nn.ReLU()
        self.hidden2 = nn.Linear(12, 8)
        self.act2 = nn.ReLU()
        self.output = nn.Linear(8, 1)
        self.act_output = nn.Sigmoid()

    def forward(self, x):
        x = self.act1(self.hidden1(x))
        x = self.act2(self.hidden2(x))
        x = self.act_output(self.output(x))
        return x

model = PimaClassifier()
print(model)

# train the model
loss_fn   = nn.BCELoss()  # binary cross entropy
optimizer = optim.Adam(model.parameters(), lr=0.001)

n_epochs = 100
batch_size = 10

for epoch in range(n_epochs):
    for i in range(0, len(X), batch_size):
        Xbatch = X[i:i+batch_size]
        y_pred = model(Xbatch)
        ybatch = y[i:i+batch_size]
        loss = loss_fn(y_pred, ybatch)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

# compute accuracy
y_pred = model(X)
accuracy = (y_pred.round() == y).float().mean()
print(f"Accuracy {accuracy}")

# make class predictions with the model
predictions = (model(X) > 0.5).int()
for i in range(5):
    print('%s => %d (expected %d)' % (X[i].tolist(), predictions[i], y[i]))