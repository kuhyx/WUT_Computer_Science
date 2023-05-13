""" Implementation of a network analyzing MNIST dataset """
import torch
from torch import nn
from torch import optim
from torchvision import datasets, transforms


def set_hyperparameters():
    """ sets hyperparameters used throughout the network """
    return {
        "learning_rate": 0.001,
        "batch_size": 64,
        "num_epochs": 2,
        "input_size": 28 * 28,  # MNIST images are 28x28 pixels
        "hidden_size": 128,
        "num_classes": 10,
    }


def load_datasets():
    """ Loads train and test dataset from MNIST """
    train_dataset = datasets.MNIST(
        root="./data", train=True, transform=transforms.ToTensor(), download=True
    )
    test_dataset = datasets.MNIST(
        root="./data", train=False, transform=transforms.ToTensor(), download=True
    )
    return train_dataset, test_dataset


def create_data_loaders(train_dataset, test_dataset, hyperparameters):
    """ Create train and test data loaders """
    train_loader = torch.utils.data.DataLoader(
        dataset=train_dataset, batch_size=hyperparameters["batch_size"], shuffle=True
    )
    test_loader = torch.utils.data.DataLoader(
        dataset=test_dataset, batch_size=hyperparameters["batch_size"], shuffle=False
    )
    return train_loader, test_loader


def define_model(hyperparameters):
    """ Define the multilayer perceptron training_parameters['model'] """
    model = nn.Sequential(
        nn.Linear(hyperparameters["input_size"],
                  hyperparameters["hidden_size"]),
        nn.ReLU(),
        nn.Linear(hyperparameters["hidden_size"],
                  hyperparameters["num_classes"]),
    )
    return model


def initial_configuration():
    """
    Perform all operations needed for training network
    """
    # Set random seed for reproducibility
    torch.manual_seed(42)
    hyperparameters = set_hyperparameters()
    # Load MNIST dataset and apply transformations
    train_dataset, test_dataset = load_datasets()
    train_loader, test_loader = create_data_loaders(
        train_dataset, test_dataset, hyperparameters
    )
    model = define_model(hyperparameters)
    # Loss function
    criterion = nn.CrossEntropyLoss()
    # training_parameters['optimizer']
    optimizer = optim.Adam(
        model.parameters(), lr=hyperparameters["learning_rate"])
    return hyperparameters, train_loader, test_loader, model, criterion, optimizer


def single_train_iteration(
    data, training_parameters, targets, batch_idx, epoch
):
    """
    Train network for single batch
    """
    # Reshape the input data
    data = data.view(data.size(0), -1)
    # Forward pass
    outputs = training_parameters['model'](data)
    loss = training_parameters['criterion'](outputs, targets)
    # Backward pass and optimization
    training_parameters['optimizer'].zero_grad()
    loss.backward()
    training_parameters['optimizer'].step()
    # Print loss value for every learning step
    if (batch_idx + 1) % 100 == 0:
        print(
            f'''
            Epoch [{epoch+1}/{training_parameters['hyperparameters']["num_epochs"]}],
            Step [{batch_idx+1}/ \
                {len(training_parameters['loaders']['train_loader'])}],
            Loss: {loss.item():.4f}
            '''
        )
    return data, training_parameters['optimizer']


def set_loaders(train_loader, test_loader):
    """
    Put train and test loaders into one object
    """
    return {
        'train_loader': train_loader,
        'test_loader': test_loader
    }


def set_training_parameters(hyperparameters, loaders, model, criterion, optimizer):
    """
    Put all training parameters into one object
    """
    return {
        'hyperparameters': hyperparameters,
        'loaders': {
            'train_loader': loaders['train_loader'],
            'test_loader': loaders['test_loader']
        },
        'model': model,
        'criterion': criterion,
        'optimizer': optimizer,
    }


def training_loop(training_parameters):
    """
    Train network for all epochs
    """
    epochs_num = training_parameters["hyperparameters"]["num_epochs"]
    # Training loop
    for epoch in range(epochs_num):
        for batch_idx, (data, targets) in enumerate(training_parameters['loaders']['train_loader']):
            data, training_parameters['optimizer'] = single_train_iteration(
                data, training_parameters, targets, batch_idx, epoch
            )
        calculate_accuracy_epoch(
            training_parameters, epoch)
        calculate_validation_set_accuracy(
            training_parameters, epoch)
    return epoch, training_parameters['loaders']['train_loader']


def calculate_accuracy_epoch(training_parameters, epoch):
    """ Calculate accuracy on train set after each epoch """
    correct = 0
    total = 0
    for data, targets in training_parameters['loaders']['train_loader']:
        data = data.view(data.size(0), -1)
        outputs = training_parameters['model'](data)
        _, predicted = torch.max(outputs.data, 1)
        total += targets.size(0)
        correct += (predicted == targets).sum().item()
    train_accuracy = 100 * correct / total
    print(
        f"Accuracy on Train Set after Epoch {epoch+1}: {train_accuracy:.2f}%")


def calculate_validation_set_accuracy(training_parameters, epoch):
    """ Calculate accuracy on validation set after each epoch """
    correct = 0
    total = 0
    for data, targets in training_parameters['loaders']['test_loader']:
        data = data.view(data.size(0), -1)
        outputs = training_parameters['model'](data)
        _, predicted = torch.max(outputs.data, 1)
        total += targets.size(0)
        correct += (predicted == targets).sum().item()

    validation_accuracy = 100 * correct / total
    print(
        f"Accuracy on Validation Set after Epoch {epoch+1}: {validation_accuracy:.2f}%"
    )
    print("---")


if __name__ == "__main__":
    (
        HYPERPARAMETERS,
        TRAIN_LOADER,
        TEST_LOADER,
        MODEL,
        CRITERION,
        OPTIMIZER,
    ) = initial_configuration()
    LOADERS = set_loaders(
        TRAIN_LOADER, TEST_LOADER)
    TRAINING_PARAMETERS = set_training_parameters(
        HYPERPARAMETERS, LOADERS, MODEL, CRITERION, OPTIMIZER)
    training_loop(TRAINING_PARAMETERS)
