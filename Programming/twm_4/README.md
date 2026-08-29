# TWM — lab 4: introduction to Keras

Coursework for TWM (Techniki Wizyjne / machine vision), lab 4.

| Path | What it is |
|---|---|
| `TWM_KerasIntro.ipynb` | The submitted notebook — the deliverable. |
| `TWM_KerasIntro.py` | An `nbconvert` export of the notebook's **CIFAR-10 section only**. |
| `twm.py` | Prints the TensorFlow version the notebook will run against. |

The notebook is the source of truth. The `.py` is kept because it makes that
section's code reviewable and diffable, but it is not a full export: it covers
28 of the notebook's 81 code cells, all of them from the CIFAR-10 half, and it
has been edited since. Treat the two as separate artifacts rather than
regenerating one from the other.

Both need a GPU. The notebook's first cell calls `sys.exit()` when TensorFlow
reports no physical GPU device, and running it end to end downloads MNIST,
CIFAR-10 and a slice of the Quick, Draw! bitmaps into `data/`.
