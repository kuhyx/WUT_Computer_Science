import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
import matplotlib.pyplot as plt

# Set random seed for reproducibility
torch.manual_seed(42)

# Define hyperparameters
learning_rate = 0.001
batch_size = 64
num_epochs = 10
input_size = 28 * 28  # MNIST images are 28x28 pixels
hidden_size = 128
num_classes = 10

# Load MNIST dataset and apply transformations
train_dataset = datasets.MNIST(
    root='./data', train=True, transform=transforms.ToTensor(), download=True
)
test_dataset = datasets.MNIST(
    root='./data', train=False, transform=transforms.ToTensor(), download=True
)

# Create data loaders
train_loader = torch.utils.data.DataLoader(
    dataset=train_dataset, batch_size=batch_size, shuffle=True
)
test_loader = torch.utils.data.DataLoader(
    dataset=test_dataset, batch_size=batch_size, shuffle=False
)

# Define the multilayer perceptron model
model = nn.Sequential(
    nn.Linear(input_size, hidden_size),
    nn.ReLU(),
    nn.Linear(hidden_size, num_classes)
)

# Loss function
criterion = nn.CrossEntropyLoss()

# Optimizer
optimizer = optim.Adam(model.parameters(), lr=learning_rate)

# Lists to store loss and accuracy values
loss_values = []
train_acc_values = []
val_acc_values = []

# Training loop
for epoch in range(num_epochs):
    for batch_idx, (data, targets) in enumerate(train_loader):
        # Reshape the input data
        data = data.view(data.size(0), -1)

        # Forward pass
        outputs = model(data)
        loss = criterion(outputs, targets)

        # Backward pass and optimization
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        # Append loss value for every learning step
        loss_values.append(loss.item())

    # Calculate accuracy on train set after each epoch
    correct = 0
    total = 0
    for data, targets in train_loader:
        data = data.view(data.size(0), -1)
        outputs = model(data)
        _, predicted = torch.max(outputs.data, 1)
        total += targets.size(0)
        correct += (predicted == targets).sum().item()

    train_accuracy = 100 * correct / total
    train_acc_values.append(train_accuracy)

    # Calculate accuracy on validation set after each epoch
    correct = 0
    total = 0
    for data, targets in test_loader:
        data = data.view(data.size(0), -1)
        outputs = model(data)
        _, predicted = torch.max(outputs.data, 1)
        total += targets.size(0)
        correct += (predicted == targets).sum().item()

    validation_accuracy = 100 * correct / total
    val_acc_values.append(validation_accuracy)

    # Print loss value for every learning step
    print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss_values[-1]:.4f}, Train Accuracy: {train_accuracy:.2f}%, Validation Accuracy: {validation_accuracy:.2f}%')

# Plot the loss value for every learning step
plt.plot(loss_values)
plt.xlabel('Learning Step')
plt.ylabel('Loss')
plt.title('Loss Value')
plt.savefig('loss_value.png')
plt.show()

# Plot the accuracy on train set after each epoch
plt.plot(train_acc_values)
plt.xlabel('Epoch')
plt.ylabel('Train Accuracy')
plt.title('Accuracy on Train Set')
plt.savefig('train_accuracy.png')
plt.show()

# Plot the accuracy on validation set after each epoch
plt.plot(val_acc_values)
plt.xlabel('Epoch')
plt.ylabel('Validation Accuracy')
plt.title('Accuracy on Validation Set')
plt.savefig('validation_accuracy.png')
plt.show()
