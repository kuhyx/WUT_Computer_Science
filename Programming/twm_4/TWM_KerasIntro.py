#!/usr/bin/env python3
"""CIFAR-10 half of the lab notebook, exported so the code can be diffed.

Four CNN variants are built and only `model_chat` is trained, then evaluated
with a confusion matrix and sample grids of its right and wrong answers.

Needs a GPU: the script exits early without one, exactly as the notebook does.
`print` is `sys.stdout.write` here so the output is identical to the notebook's
without a logging handler having to be configured first.
"""

from __future__ import annotations

import itertools
import sys
from dataclasses import dataclass
from typing import TYPE_CHECKING

import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from keras.datasets import cifar10
from keras.layers import (
    Activation,
    BatchNormalization,
    Conv2D,
    Dense,
    Dropout,
    Flatten,
    MaxPooling2D,
)
from keras.models import Sequential
from keras.utils import to_categorical
from sklearn.metrics import confusion_matrix
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator

if TYPE_CHECKING:
    from collections.abc import Sequence

    from matplotlib.colors import Colormap

# CIFAR-10 has ten classes, and the training split has 40000 images once the
# generator has held back its 20% for validation.
NUM_CLASSES = 10
BATCH_SIZE = 128
TRAIN_IMAGES = 40000
VALID_IMAGES = 10000
EPOCHS = 20

# ## Ładowanie zbioru danych

# Check if GPU is available
sys.stdout.write(f"{tf.config.list_physical_devices('GPU')}\n")
if tf.config.list_physical_devices("GPU"):
    sys.stdout.write("GPU is available\n")
else:
    sys.stdout.write("GPU is not available\n")
    sys.exit()


@dataclass(frozen=True)
class Predictions:
    """A model's output, with the images and true labels it was produced from."""

    scores: np.ndarray
    images: np.ndarray
    labels: np.ndarray
    names: Sequence[str] | None = None


def plot_confusion_matrix(
    cm: np.ndarray,
    classes: Sequence[str],
    *,
    normalize: bool = False,
    title: str = "Confusion matrix",
    cmap: Colormap = plt.cm.Blues,
) -> None:
    """Print and plot the confusion matrix.

    Normalization can be applied by setting `normalize=True`.
    """
    if normalize:
        cm = cm.astype("float") / cm.sum(axis=1)[:, np.newaxis]
        sys.stdout.write("Normalized confusion matrix\n")
    else:
        sys.stdout.write("Confusion matrix, without normalization\n")

    sys.stdout.write(f"{cm}\n")

    plt.imshow(cm, interpolation="nearest", cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = ".2f" if normalize else "d"
    thresh = cm.max() / 2.0
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(
            j,
            i,
            format(cm[i, j], fmt),
            horizontalalignment="center",
            color="white" if cm[i, j] > thresh else "black",
        )

    plt.ylabel("True label")
    plt.xlabel("Predicted label")
    plt.tight_layout()


(X_train, y_train), (X_test, y_test) = cifar10.load_data()

X_train = X_train.astype("float32")  # change integers to 32-bit floating point numbers
X_test = X_test.astype("float32")

X_train /= (
    255  # normalize each value for each pixel for the entire vector for each input
)
X_test /= 255

y_train = y_train.reshape((1, -1))[0]
y_test = y_test.reshape((1, -1))[0]

sys.stdout.write(f"Training matrix shape {X_train.shape} {y_train.shape}\n")
sys.stdout.write(f"Testing matrix shape {X_test.shape} {y_test.shape}\n")

# one-hot format classes

Y_train = to_categorical(y_train, NUM_CLASSES)
Y_test = to_categorical(y_test, NUM_CLASSES)

cifar_names = [
    "airplane",
    "automobile",
    "bird",
    "cat",
    "deer",
    "dog",
    "frog",
    "horse",
    "ship",
    "truck",
]


# ## Podgląd zbioru treningowego

# Ten samples of each class, stacked into one wide strip. Built as a list and
# concatenated once: growing `img` in place only bound it in the loop's `else`
# branch, which reads as a use-before-assignment and is what ruff flagged.
strips = []
for class_id in range(NUM_CLASSES):
    img_batch = X_train[y_train == class_id][0:10]
    strips.append(
        np.reshape(
            img_batch,
            (
                img_batch.shape[0] * img_batch.shape[1],
                img_batch.shape[2],
                img_batch.shape[3],
            ),
        )
    )
img = np.concatenate(strips, axis=1)
plt.figure(figsize=(10, 20))
plt.axis("off")
plt.imshow(img, cmap="gray")


# ## Przygotowanie modelu


def generate_model() -> Sequential:
    """Build the minimal variant: one conv layer straight into the classifier."""
    model = Sequential()  # Linear stacking of layers

    # Convolution Layer 1
    model.add(Conv2D(16, (3, 3), input_shape=(32, 32, 3)))
    model.add(Activation("relu"))

    # ...

    model.add(Flatten())  # Flatten final output matrix into a vector

    # ...

    # Fully Connected Layer
    model.add(Dense(NUM_CLASSES))  # final 10 FC nodes
    model.add(Activation("softmax"))  # softmax activation

    model.summary()

    adam = tf.optimizers.Adam(learning_rate=0.001)
    model.compile(loss="categorical_crossentropy", optimizer=adam, metrics=["accuracy"])

    return model


def generate_model_default() -> Sequential:
    """Build the same architecture again, kept as the baseline to compare against."""
    model = Sequential()  # Linear stacking of layers

    # Convolution Layer 1
    model.add(Conv2D(16, (3, 3), input_shape=(32, 32, 3)))
    model.add(Activation("relu"))

    # ...

    model.add(Flatten())  # Flatten final output matrix into a vector

    # ...

    # Fully Connected Layer
    model.add(Dense(NUM_CLASSES))  # final 10 FC nodes
    model.add(Activation("softmax"))  # softmax activation

    model.summary()

    adam = tf.optimizers.Adam(learning_rate=0.001)
    model.compile(loss="categorical_crossentropy", optimizer=adam, metrics=["accuracy"])

    return model


def generate_model_gemini() -> Sequential:
    """Build the variant Gemini proposed: two conv blocks and heavy dropout."""
    model = Sequential()

    # Convolutional Layers with Max Pooling
    model.add(Conv2D(32, (3, 3), activation="relu", input_shape=(32, 32, 3)))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(64, (3, 3), activation="relu"))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))  # Regularization

    # Flatten and Fully Connected Layers
    model.add(Flatten())
    model.add(Dense(128, activation="relu"))
    model.add(Dropout(0.5))  # Regularization
    model.add(Dense(NUM_CLASSES, activation="softmax"))

    # Model Compilation
    model.compile(
        loss="categorical_crossentropy",
        optimizer="adam",  # Consider trying other optimizers
        metrics=["accuracy"],
    )

    return model


def generate_model_chat() -> Sequential:
    """Build the variant ChatGPT proposed: four conv layers with batch norm.

    This is the only one that actually gets trained below.
    """
    model = Sequential()  # Linear stacking of layers

    # Convolution Layer 1
    model.add(Conv2D(32, (3, 3), padding="same", input_shape=(32, 32, 3)))
    model.add(Activation("relu"))
    model.add(BatchNormalization())

    # Convolution Layer 2
    model.add(Conv2D(32, (3, 3)))
    model.add(Activation("relu"))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.3))

    # Convolution Layer 3
    model.add(Conv2D(64, (3, 3), padding="same"))
    model.add(Activation("relu"))
    model.add(BatchNormalization())

    # Convolution Layer 4
    model.add(Conv2D(64, (3, 3)))
    model.add(Activation("relu"))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.3))

    # Flattening the convolutions
    model.add(Flatten())

    # Fully Connected Layer
    model.add(Dense(512))  # Large fully connected layer
    model.add(Activation("relu"))
    model.add(BatchNormalization())
    model.add(Dropout(0.6))

    # Output Layer
    model.add(Dense(NUM_CLASSES))  # final 10 FC nodes
    model.add(Activation("softmax"))  # softmax activation

    model.summary()

    # Compile the model
    adam = Adam(learning_rate=0.001)
    model.compile(loss="categorical_crossentropy", optimizer=adam, metrics=["accuracy"])

    return model


model = generate_model()
model_default = generate_model_default()
model_gemini = generate_model_gemini()
model_chat = generate_model_chat()
models = [model_chat]


# ## Trening

gen = ImageDataGenerator(
    rotation_range=8,
    width_shift_range=0.08,
    shear_range=0.3,
    height_shift_range=0.08,
    zoom_range=0.08,
    validation_split=0.2,
)

train_generator = gen.flow(X_train, Y_train, batch_size=BATCH_SIZE, subset="training")
valid_generator = gen.flow(X_train, Y_train, batch_size=BATCH_SIZE, subset="validation")

# Max 20 epoch
for trained in models:
    trained.fit(
        train_generator,
        steps_per_epoch=TRAIN_IMAGES // BATCH_SIZE,
        epochs=EPOCHS,
        verbose=1,
        validation_data=valid_generator,
        validation_steps=VALID_IMAGES // BATCH_SIZE,
    )


# ## Test

for evaluated in models:
    score = evaluated.evaluate(X_test, Y_test)
    sys.stdout.write(f"Test score: {score[0]}\n")
    sys.stdout.write(f"Test accuracy: {score[1]}\n")

    # The predict_classes function outputs the highest probability class
    # according to the trained classifier for each input example.
    predicted = evaluated.predict(X_test)
    predicted_classes = np.argmax(predicted, axis=1)
    results = Predictions(
        scores=predicted, images=X_test, labels=y_test, names=cifar_names
    )

    # Check which items we got right / wrong
    correct_indices = np.nonzero(predicted_classes == y_test)[0]

    incorrect_indices = np.nonzero(predicted_classes != y_test)[0]

    cnf_matrix = confusion_matrix(y_test, predicted_classes)

    class_names = [str(i) for i in range(NUM_CLASSES)]

    # Plot non-normalized confusion matrix
    plt.figure()
    plot_confusion_matrix(
        cnf_matrix, classes=class_names, title="Confusion matrix, without normalization"
    )

    plt.show()


def show_samples_rgb(
    indices: np.ndarray, results: Predictions, *, count: int = 3
) -> None:
    """Plot a `count` x `count` grid of samples, titled predicted vs expected."""
    plt.figure()
    for i, sample in enumerate(indices[: count**2]):
        pred_id = int(np.argmax(results.scores[sample]))
        real_id = int(results.labels[sample])
        pred_score = results.scores[sample][pred_id]
        real_score = results.scores[sample][real_id]
        plt.subplot(count, count, i + 1)
        plt.imshow(results.images[sample], interpolation="none")
        plt.axis("off")
        if results.names:
            predicted_label: str | int = results.names[pred_id]
            real_label: str | int = results.names[real_id]
        else:
            predicted_label = pred_id
            real_label = real_id
        plt.title(
            f"P: {predicted_label} ({pred_score:.2f})\n"
            f"E: {real_label} ({real_score:.2f})"
        )

    plt.tight_layout()


# ## Poprawne klasyfikacje

show_samples_rgb(correct_indices, results, count=5)


# ## Błędne klasyfikacje

show_samples_rgb(incorrect_indices, results, count=5)
