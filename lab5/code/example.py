# numpy for loading dataset
import numpy as np
# pytorch for deep learning models
import torch
# nn like neural network
import torch.nn as nn
import torch.optim as optim

# Pima indians describes patient medical data and whether they had diabetes for last 5 years
# It is binary classification (they could either have diabetes 1 or not 0)
# load the file as a matrix of numbers,
dataset = np.loadtxt('pima-indians-diabetes.csv', delimiter=',')
input_columns = 8
# split into input (X) -> in this case everything beside info whether patient had diabetes or not is input
# We are splitting data into two subsets by using NumPy slice operator : and choose first 8 columns using 0:8 slice
X = dataset[:,0:input_columns]
# and output (y) variables -> in this case we are only interested whether patient had diabetes or not as an output
# you can simplify that y = f(X)
# We are splitting the data by using slice operator : and choosing last column
y = dataset[:,input_columns]

# we need to convert this data to pytorch tensors 
# Pytorch usually operates on 32-bit floating point and NumPy by default uses 64 bit floating point
X = torch.tensor(X, dtype=torch.float32)
# We can also correct the shape to fit what PyTorch would expect (here we are converting n vectors to n x 1 matrix)
# This simplifies handling matrix multiplication operations (which are the basis of deep learning models)
# reshape is converting the output variable y from a 1-dimensional NumPy array to a 2-dimensional PyTorch tensor with a shape of (n, 1), where n is the number of samples in the dataset.
y = torch.tensor(y, dtype=torch.float32).reshape(-1, 1)

# define the model
# this class is a subclass of nn.Module -> base class provided by PyTorch for building neural network models.
class PimaClassifier(nn.Module):
    def __init__(self):
        super().__init__()
        # There are 3 (fully connected) layers in class, each with their activation function
        # creates Linear layer, it maps input to a hidden layer of 12 neurons
        # input features have a size of 8 (same number as number of features in pima indians diabetes dataset)
        first_output_neurons = 12
        self.hidden1 = nn.Linear(input_columns, first_output_neurons)
        # This creates ReLU (rectified linear unit) activation function applied after first hidden layer
        self.act1 = nn.ReLU() 

        # This maps the output of first layer (which was 12 neurons) to new hidden layer of 8 neurons
        second_output_neurons = 8
        self.hidden2 = nn.Linear(first_output_neurons, second_output_neurons)
        # ReLU activation function applied after second hidden layer
        self.act2 = nn.ReLU()

        # We map output of second layer to a single output neuron -> which will represent the predicted 
        # probability of a sample having diabetes
        self.output = nn.Linear(second_output_neurons, 1)
        # sigmoid function forces output to be either 0 or 1
        self.act_output = nn.Sigmoid()

    # forward pass is computation of output based on input 'x' 
    def forward(self, x):
        # Applies first hidden layer (and then ReLU activation) to input x
        x = self.act1(self.hidden1(x))
        # Applies second hidden layer (and then ReLU activation) to input x
        x = self.act2(self.hidden2(x))
        # Applies output layer (and then Sigmoid activation) to input x
        x = self.act_output(self.output(x))
        # returns final output (0 or 1)
        return x

# Create object from model class
model = PimaClassifier()
print(model)

# train the model
# first we need to specify what is the goal of training 
# we have input X and output y and we want the model to be as close to y as possible
# Since this is binary classification problem we will use "binary cross entropy" to measure the distance between 
# our prediction and y
loss_fn   = nn.BCELoss()  # binary cross entropy
# Optimizer adjust model weights to produce better output 
# Its described as being able to tune itself to a lot of problems
# inputs are:
# parameters which it will optimize (from the model)
# and lr (learning rate) which is step size of each iteration 
optimizer = optim.Adam(model.parameters(), lr=0.001)


# epoch is the entire training dataset passed to a model once
n_epochs = 100
# batch is one or more sample passed to model
# number of epochs and the size of a batch can be chosen experimentally by trial and error.
# a lot of epochs and big size of batch means more time and more memory consumption but more accurate results
batch_size = 10

# We split dataset into batches and pass batches one by one into a model to training loop
# after using all batches we finish one epoch and can start over again to refine the model
# we use two nested for loops for training, one is for epochs
for epoch in range(n_epochs):
    # and one for batches
    for i in range(0, len(X), batch_size):
        # Split X data into a batch with the size from batch_size
        Xbatch = X[i:i+batch_size]
        # run the model on the batch and return "batched" output
        y_pred = model(Xbatch)
        # Split y data into a batch with the size from batch_size
        ybatch = y[i:i+batch_size]
        # Compare loss
        loss = loss_fn(y_pred, ybatch)
        # optimize model
        optimizer.zero_grad()
        # calculate the inaccuracy
        loss.backward()
        # optimizer takes next step
        optimizer.step()

# compute final accuracy
y_pred = model(X)
accuracy = (y_pred.round() == y).float().mean()
print(f"Accuracy {accuracy}")

# make class predictions with the model
predictions = (model(X) > 0.5).int()
for i in range(5):
    print('%s => %d (expected %d)' % (X[i].tolist(), predictions[i], y[i]))