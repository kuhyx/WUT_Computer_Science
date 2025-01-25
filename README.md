# USD

## Task:
Zapoznaj się z [MetaDrive](https://github.com/metadriverse/metadrive/). Wytrenuj co najmniej dwóch różnych agentów 
wykorzystując algorytmy **wieloagentowe** (MA), na co
najmniej trzech różnych mapach. Omów otrzymane wyniki oraz zwizualizuj działanie
wytrenowanych agentów.


## Setup
```
conda create -n copo python=3.7
conda activate copo

# Install MetaDrive version 0.2.5
pip install git+https://github.com/metadriverse/metadrive.git@releases/0.2.5

pip install torch

git clone https://github.com/decisionforce/CoPO
cd CoPO/copo_code
pip install -e .

pip install -U ray==1.2.0 "ray[rllib]==1.2.0"
pip install -U "numpy<1.24.0"
pip uninstall opencv-python
pip uninstall opencv-python-headless
pip install opencv-python==4.5.5.64
pip install pydantic==1.9.0
```

## How to train a RL agents

```
cd CoPo/copo_code/copo/
python train_all_cl.py --exp-name my_cl
```
Training process 4.7h
```
python train_all_ippo.py --exp-name my_ippo
```
Training process 7.3h
