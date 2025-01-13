cd code 

pyenv init

COPY AND PASTE PYENV CONFIGURATION TO YOUR SHELL CONFIG

source ~/.zshrc (or your shell)

pyenv install 3.11

pyenv global 3.11

Ensure that python DID change its version

python --version

python -m venv ./venv 

source ./venv/bin/activate

pip install -r requirements.txt

python main.py
