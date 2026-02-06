# # CIFAR-10

# ## Ładowanie zbioru danych

# In[ ]:
import sys
import tensorflow as tf


# Check if GPU is available
print(tf.config.list_physical_devices('GPU'))
if tf.config.list_physical_devices('GPU'):
    print("GPU is available")
else:
    print("GPU is not available")
    sys.exit()


from tensorflow import keras
from keras.datasets import cifar10
from keras.utils import to_categorical  
import numpy as np  
import itertools
import matplotlib.pyplot as plt
from keras.models import Sequential 
from sklearn.metrics import confusion_matrix
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from keras.layers import BatchNormalization, Conv2D, MaxPooling2D, ZeroPadding2D, GlobalAveragePooling2D, Flatten, Dense, Dropout, Activation
from tensorflow.keras.optimizers import Adam

def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)


    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.tight_layout()

(X_train, y_train), (X_test, y_test) = cifar10.load_data()

X_train = X_train.astype('float32')         # change integers to 32-bit floating point numbers
X_test = X_test.astype('float32')

X_train /= 255                              # normalize each value for each pixel for the entire vector for each input
X_test /= 255

y_train = y_train.reshape((1,-1))[0]
y_test = y_test.reshape((1,-1))[0]

print("Training matrix shape", X_train.shape, y_train.shape)
print("Testing matrix shape", X_test.shape, y_test.shape)

# one-hot format classes

nb_classes = 10

Y_train = to_categorical(y_train, nb_classes)
Y_test = to_categorical(y_test, nb_classes)

cifar_names = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']


# ## Podgląd zbioru treningowego

# In[ ]:


for i in range(0, 10):
  img_batch = X_train[y_train == i][0:10]
  img_batch = np.reshape(img_batch, (img_batch.shape[0]*img_batch.shape[1], img_batch.shape[2], img_batch.shape[3]))
  if i > 0:
    img = np.concatenate([img, img_batch], axis = 1)
  else:
    img = img_batch
plt.figure(figsize=(10,20))
plt.axis('off')
plt.imshow(img, cmap='gray')


# ## Przygotowanie modelu

# In[ ]:


def generate_model():
  model = Sequential()                                 # Linear stacking of layers

  # Convolution Layer 1
  model.add(Conv2D(16, (3, 3), input_shape=(32,32,3)))
  model.add(Activation('relu') )

  # ...

  model.add(Flatten())                                 # Flatten final output matrix into a vector

  # ...

  # Fully Connected Layer
  model.add(Dense(10))                                 # final 10 FC nodes
  model.add(Activation('softmax'))                     # softmax activation

  model.summary()

  adam = tf.optimizers.Adam(learning_rate=0.001)
  model.compile(loss='categorical_crossentropy', optimizer=adam, metrics=['accuracy'])

  return model

def generate_model_default():
  model = Sequential()                                 # Linear stacking of layers

  # Convolution Layer 1
  model.add(Conv2D(16, (3, 3), input_shape=(32,32,3)))
  model.add(Activation('relu') )

  # ...

  model.add(Flatten())                                 # Flatten final output matrix into a vector

  # ...

  # Fully Connected Layer
  model.add(Dense(10))                                 # final 10 FC nodes
  model.add(Activation('softmax'))                     # softmax activation

  model.summary()

  adam = tf.optimizers.Adam(learning_rate=0.001)
  model.compile(loss='categorical_crossentropy', optimizer=adam, metrics=['accuracy'])

  return model

def generate_model_gemini():
    model = Sequential()

    # Convolutional Layers with Max Pooling
    model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(32, 32, 3)))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(64, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))  # Regularization

    # Flatten and Fully Connected Layers
    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.5))   # Regularization
    model.add(Dense(10, activation='softmax'))

    # Model Compilation
    model.compile(loss='categorical_crossentropy',
                  optimizer='adam',  # Consider trying other optimizers
                  metrics=['accuracy'])

    return model

def generate_model_chat():
    model = Sequential()                                 # Linear stacking of layers

    # Convolution Layer 1
    model.add(Conv2D(32, (3, 3), padding='same', input_shape=(32, 32, 3)))
    model.add(Activation('relu'))
    model.add(BatchNormalization())

    # Convolution Layer 2
    model.add(Conv2D(32, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.3))

    # Convolution Layer 3
    model.add(Conv2D(64, (3, 3), padding='same'))
    model.add(Activation('relu'))
    model.add(BatchNormalization())

    # Convolution Layer 4
    model.add(Conv2D(64, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.3))

    # Flattening the convolutions
    model.add(Flatten())

    # Fully Connected Layer
    model.add(Dense(512))                                 # Large fully connected layer
    model.add(Activation('relu'))
    model.add(BatchNormalization())
    model.add(Dropout(0.6))

    # Output Layer
    model.add(Dense(10))                                  # final 10 FC nodes
    model.add(Activation('softmax'))                      # softmax activation

    model.summary()

    # Compile the model
    adam = Adam(learning_rate=0.001)
    model.compile(loss='categorical_crossentropy', optimizer=adam, metrics=['accuracy'])

    return model


# In[ ]:


model = generate_model()
model_default = generate_model_default()
model_gemini = generate_model_gemini()
model_chat = generate_model_chat()
models = [model_chat]


# ## Trening

# In[ ]:


gen = ImageDataGenerator(rotation_range=8, width_shift_range=0.08, shear_range=0.3,
                         height_shift_range=0.08, zoom_range=0.08, validation_split=0.2)

train_generator = gen.flow(X_train, Y_train, batch_size=128, subset='training')
valid_generator = gen.flow(X_train, Y_train, batch_size=128, subset='validation')


# In[ ]:


# Max 20 epoch
for model in models:
  model.fit(train_generator, steps_per_epoch=40000//128, epochs=20, verbose=1, validation_data=valid_generator, validation_steps = 10000 // 128)


# ## Test

# In[ ]:

for model in models:
  score = model.evaluate(X_test, Y_test)
  print('Test score:', score[0])
  print('Test accuracy:', score[1])

  # The predict_classes function outputs the highest probability class
  # according to the trained classifier for each input example.
  predicted = model.predict(X_test)
  predicted_classes = np.argmax(predicted, axis=1)

  # Check which items we got right / wrong
  correct_indices = np.nonzero(predicted_classes == y_test)[0]

  incorrect_indices = np.nonzero(predicted_classes != y_test)[0]


  cnf_matrix = confusion_matrix(y_test, predicted_classes)

  class_names = [str(i) for i in range(10)]

  # Plot non-normalized confusion matrix
  plt.figure()
  plot_confusion_matrix(cnf_matrix, classes=class_names,
                        title='Confusion matrix, without normalization')

  plt.show()


# In[ ]:


def show_samples_rgb(indices, preds, images, labels, count=3, names = []):
    plt.figure()
    for i, sample in enumerate(indices[:count**2]):
        pred_id = int(np.argmax(preds[sample]))
        real_id = int(labels[sample])
        pred_score = preds[sample][pred_id]
        real_score = preds[sample][real_id]
        plt.subplot(count,count,i+1)
        plt.imshow(images[sample], interpolation='none')
        plt.axis('off')
        if len(names) > 0:
          plt.title("P: {} ({:.2f})\nE: {} ({:.2f})".format(names[pred_id], pred_score, names[real_id], real_score))
        else:
          plt.title("P: {} ({:.2f})\nE: {} ({:.2f})".format(pred_id, pred_score, real_id, real_score))

    plt.tight_layout()


# ## Poprawne klasyfikacje

# In[ ]:


show_samples_rgb(correct_indices, predicted, X_test, y_test, 5, cifar_names)


# ## Błędne klasyfikacje

# In[ ]:


show_samples_rgb(incorrect_indices, predicted, X_test, y_test, 5, cifar_names)

