#!/bin/bash

nohup ./simulation.py -f input1.csv -l 8 -c 1,1 -v 1 > input_1_log 2>&1 &
nohup ./simulation.py -f input2.csv -l 4 -c 1,1 -v 120 > input_2_log 2>&1 & 
nohup ./simulation.py -f input3.csv -l 4 -c 1,1 -v 120 > input_3_log 2>&1 & 
nohup ./simulation.py -f input4.csv -l 4 -c 1,1 -v 50 > input_4_log 2>&1 & 
