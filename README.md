# SAT-solver
This project was created during the course Logic in Computer Science at 
University of Ljubljana, Faculty of Mathematics and Physics by the group 
named #IOLo.

## Dependencies
Python 3 and Numpy are needed to execute this SAT-solver. Note that 
availability of several cores improves its performance.

## Running
The SAT-solver can be run under Python 3 using the following command
```
python solver.py input_file.txt output_file.txt
```
 
## Testing
The program was tested on 4-core CPU. Using parallelisation, nearly 10-fold 
speed-up was achieved on the provided input file.