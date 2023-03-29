To run the program install python, go to project repository and just run python main.py:
python main.py 

you can specify the name of the file which stores maze by typing:
python main.py mazeFile.txt

python main.py -h --help print help prompt

python main.py -t --test non interactive (does not print steps) for testing 
different heuristics, goes through entire generatedMazes folder and
compares heuristic speed and path length, saves solved mazes to solvedMazes folder

python main.py -t --test [FOLDER] non interactive (does not print steps) for testing 
different heuristics, goes through entire [FOLDER] folder and
compares heuristic speed and path length, saves solved mazes to solvedMazes folder

python main.py -g --generate [NUMBER] - generates as many mazes as entered in
Number parameter and puts it in the generatedMazes folder


