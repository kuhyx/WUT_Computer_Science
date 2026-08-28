#!/usr/bin/env python3
"""Implementation of a network analyzing MNIST dataset."""

import logging
import time
from pathlib import Path

import matplotlib.pyplot as plt
import torch
from torch import nn, optim
from torchvision import datasets, transforms

logger = logging.getLogger(__name__)


def set_hyperparameters() -> dict[str, int]:
    """Set hyperparameters used throughout the network."""
    return {
        "num_epochs": 5,
        "init_input_size": 28 * 28,  # MNIST images are 28x28 pixels
        "num_classes": 10,
    }


def load_datasets() -> tuple[object, object]:
    """Load train and test dataset from MNIST."""
    train_dataset = datasets.MNIST(
        root="./data", train=True, transform=transforms.ToTensor(), download=True
    )
    test_dataset = datasets.MNIST(
        root="./data", train=False, transform=transforms.ToTensor(), download=True
    )
    return train_dataset, test_dataset


def create_data_loaders(
    train_dataset: object, test_dataset: object
) -> tuple[object, object]:
    """Create train and test data loaders."""
    train_loader = torch.utils.data.DataLoader(
        dataset=train_dataset, batch_size=BATCH_SIZE, shuffle=True
    )
    test_loader = torch.utils.data.DataLoader(
        dataset=test_dataset, batch_size=BATCH_SIZE, shuffle=False
    )
    return train_loader, test_loader


# Lists to store loss and accuracy values
loss_values = []
train_acc_values = []
val_acc_values = []


def define_model(hyperparameters: dict[str, int]) -> object:
    """Define the multilayer perceptron training_parameters['model']."""
    # Define the multilayer perceptron model
    model = nn.Sequential()
    model.add_module("flatten", nn.Flatten())
    input_size = hyperparameters["init_input_size"]
    for i in range(NUM_HIDDEN_LAYERS):
        model.add_module(f"linear{i}", nn.Linear(input_size, WIDTH))
        model.add_module(f"relu{i}", nn.ReLU())
        input_size = WIDTH
    model.add_module("output", nn.Linear(input_size, hyperparameters["num_classes"]))
    return model


def get_optimizer(model: object) -> object:
    """Return optimizer function."""
    if OPTIMIZER_TYPE == "SGD":
        return optim.SGD(model.parameters(), lr=LEARNING_RATE)
    if OPTIMIZER_TYPE == "SGD_Momentum":
        return optim.SGD(model.parameters(), lr=LEARNING_RATE, momentum=0.9)
    if OPTIMIZER_TYPE == "Adam":
        return optim.Adam(model.parameters(), lr=LEARNING_RATE)
    msg = f"Unsupported optimizer type: {OPTIMIZER_TYPE}"
    raise ValueError(msg)


def initial_configuration() -> tuple[dict[str, int], object, object, object]:
    """Perform all operations needed for training network."""
    # Set random seed for reproducibility
    torch.manual_seed(42)
    hyperparameters = set_hyperparameters()
    # Load MNIST dataset and apply transformations
    train_dataset, test_dataset = load_datasets()
    train_loader, test_loader = create_data_loaders(train_dataset, test_dataset)
    model = define_model(hyperparameters)
    # Loss function
    criterion = nn.CrossEntropyLoss()
    optimizer = get_optimizer(model)
    return hyperparameters, train_loader, test_loader, model, criterion, optimizer


def single_train_iteration(
    data: object,
    training_parameters: dict[str, object],
    targets: object,
    batch_idx: int,
    epoch: int,
) -> tuple[object, object]:
    """Train network for single batch."""
    # Reshape the input data
    _ = data.view(data.size(0), -1)
    # Forward pass
    outputs = training_parameters["model"](data)
    loss = training_parameters["criterion"](outputs, targets)
    # Backward pass and optimization
    training_parameters["optimizer"].zero_grad()
    loss.backward()
    training_parameters["optimizer"].step()
    # Print loss value for every learning step
    if (batch_idx + 1) % 100 == 0:
        logger.info(
            "\n            Epoch [%s/%s],\n            Step [%s/%s],\n           "
            " Loss: %s\n            ",
            epoch + 1,
            training_parameters["hyperparameters"]["num_epochs"],
            batch_idx + 1,
            len(training_parameters["loaders"]["train_loader"]),
            loss.item(),
        )
    # Append loss value for every learning step
    loss_values.append(loss.item())
    return data, training_parameters["optimizer"]


def set_loaders(train_loader: object, test_loader: object) -> dict[str, object]:
    """Put train and test loaders into one object."""
    return {"train_loader": train_loader, "test_loader": test_loader}


def set_training_parameters(
    hyperparameters: dict[str, int],
    loaders: dict[str, object],
    model: object,
    criterion: object,
    optimizer: object,
) -> dict[str, object]:
    """Put all training parameters into one object."""
    return {
        "hyperparameters": hyperparameters,
        "loaders": {
            "train_loader": loaders["train_loader"],
            "test_loader": loaders["test_loader"],
        },
        "model": model,
        "criterion": criterion,
        "optimizer": optimizer,
    }


def training_loop(
    training_parameters: dict[str, object], *, print_info: bool = True
) -> tuple[int, object]:
    """Train network for all epochs."""
    epochs_num = training_parameters["hyperparameters"]["num_epochs"]
    # Training loop
    for epoch in range(epochs_num):
        for batch_idx, (data, targets) in enumerate(
            training_parameters["loaders"]["train_loader"]
        ):
            _, training_parameters["optimizer"] = single_train_iteration(
                data, training_parameters, targets, batch_idx, epoch
            )
        calculate_accuracy_epoch(training_parameters, epoch, print_info)
        calculate_validation_set_accuracy(training_parameters, epoch, print_info)
    return epoch, training_parameters["loaders"]["train_loader"]


def calculate_accuracy_epoch(
    training_parameters: dict[str, object], epoch: int, *, print_info: bool = True
) -> None:
    """Calculate accuracy on train set after each epoch."""
    correct = 0
    total = 0
    for data, targets in training_parameters["loaders"]["train_loader"]:
        _ = data.view(data.size(0), -1)
        outputs = training_parameters["model"](data)
        _, predicted = torch.max(outputs.data, 1)
        total += targets.size(0)
        correct += (predicted == targets).sum().item()
    train_accuracy = 100 * correct / total
    if print_info:
        logger.info(
            "Accuracy on Train Set after Epoch %s: %s%%", epoch + 1, train_accuracy
        )
    train_acc_values.append(train_accuracy)


def calculate_validation_set_accuracy(
    training_parameters: dict[str, object], epoch: int, *, print_info: bool = True
) -> None:
    """Calculate accuracy on validation set after each epoch."""
    correct = 0
    total = 0
    for data, targets in training_parameters["loaders"]["test_loader"]:
        _ = data.view(data.size(0), -1)
        outputs = training_parameters["model"](data)
        _, predicted = torch.max(outputs.data, 1)
        total += targets.size(0)
        correct += (predicted == targets).sum().item()

    validation_accuracy = 100 * correct / total
    if print_info:
        logger.info(
            "Accuracy on Validation Set after Epoch %s: %s%%",
            epoch + 1,
            validation_accuracy,
        )
        logger.info("---")
    val_acc_values.append(validation_accuracy)


def main_part(*, show_plot: bool = True) -> None:
    """Train the model, evaluate it, and optionally plot the losses."""
    (
        hyperparameters,
        train_loader,
        test_loader,
        model,
        criterion,
        optimizer,
    ) = initial_configuration()
    start_time = time.time()
    loaders = set_loaders(train_loader, test_loader)
    training_parameters = set_training_parameters(
        hyperparameters, loaders, model, criterion, optimizer
    )
    training_loop(training_parameters, show_plot)
    with Path("results.txt").open("a") as file:
        rule = "-" * 85 + "\n"
        file.write(rule)
        file.write(
            f"loss-lr{LEARNING_RATE}-bs{BATCH_SIZE}-hl{NUM_HIDDEN_LAYERS}"
            f"-w{WIDTH}-{OPTIMIZER_TYPE}\n"
        )
        file.write(f"Execution time: {time.time() - start_time}\n")
        file.write(rule)

    # Plot the loss value for every learning step
    learning_step_title = (
        f"loss-lr{LEARNING_RATE}-bs{BATCH_SIZE}-hl{NUM_HIDDEN_LAYERS}"
        f"-w{WIDTH}-{OPTIMIZER_TYPE}.png"
    )
    plt.plot(loss_values)
    plt.xlabel("Learning Step")
    plt.ylabel("Loss")
    plt.title(learning_step_title)
    plt.savefig(learning_step_title)
    if show_plot:
        plt.show()
    plt.close()

    # Plot the accuracy on train set after each epoch
    train_accuracy_title = (
        f"trainAccuracy-lr{LEARNING_RATE}-bs{BATCH_SIZE}-hl"
        f"{NUM_HIDDEN_LAYERS}-w{WIDTH}-{OPTIMIZER_TYPE}.png"
    )
    plt.plot(train_acc_values)
    plt.xlabel("Epoch")
    plt.ylabel("Train Accuracy")
    plt.title(train_accuracy_title)
    plt.savefig(train_accuracy_title)
    if show_plot:
        plt.show()
    plt.close()

    # Plot the accuracy on validation set after each epoch
    validation_accuracy_title = (
        f"validationAccuracy-lr{LEARNING_RATE}-bs{BATCH_SIZE}"
        f"-hl{NUM_HIDDEN_LAYERS}-w{WIDTH}-{OPTIMIZER_TYPE}.png"
    )
    plt.plot(val_acc_values)
    plt.xlabel("Epoch")
    plt.ylabel("Validation Accuracy")
    plt.title(validation_accuracy_title)
    plt.savefig(validation_accuracy_title)
    if show_plot:
        plt.show()
    plt.close()


if __name__ == "__main__":
    logging.basicConfig(format="%(message)s", level=logging.INFO)
    LEARNING_RATE = 0.001
    BATCH_SIZE = 64
    NUM_HIDDEN_LAYERS = 2
    WIDTH = 128
    OPTIMIZER_TYPE = "Adam"
    main_part(show_plot=True)
    """
    learning_rate_values = [0.1, 0.01, 0.001]
    i = 0
    MAX_TESTS = 17
    for lr in learning_rate_values:
        LEARNING_RATE = lr
        main_part(False)
        i += 1
        print(f"Test {i}/{MAX_TESTS} ran")
    LEARNING_RATE = 0.001

    batch_size_values = [64, 128, 256]
    for bs in batch_size_values:
        BATCH_SIZE = bs
        main_part(False)
        i += 1
        print(f"Test {i}/{MAX_TESTS} ran")
    BATCH_SIZE = 64

    hidden_layers_values = [1, 2, 3]
    for hl in hidden_layers_values:
        NUM_HIDDEN_LAYERS = hl
        main_part(False)
        i += 1
        print(f"Test {i}/{MAX_TESTS} ran")
    NUM_HIDDEN_LAYERS = 2

    width_values = [64, 128, 256, 512, 1024]
    for width in width_values:
        WIDTH = width
        main_part(False)
        i += 1
        print(f"Test {i}/{MAX_TESTS} ran")
    WIDTH = 128

    for optimizer in ['SGD', 'SGD_Momentum', 'Adam']:
        OPTIMIZER_TYPE = optimizer
        main_part(False)
        i += 1
        print(f"Test {i}/{MAX_TESTS} ran")
    """
