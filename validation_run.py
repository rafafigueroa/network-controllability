#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'rafa'


import networkx as nx
import pygraphviz as pgv
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import copy
from NetworkControllability import *

from IPython.display import Image

validation_A = []
validation_B = []

# S1, b
A = [[0, 0, 0],
    ['a21', 0, 0],
    ['a31', 0, 0]]

B = [['b1'], [0], [0]]

validation_A.append(A)
validation_B.append(B)

# S1, c
A = [[0, 0, 0],
    ['a21', 0, 0],
    ['a31', 0, 'a33']]

B = [['b1'], [0], [0]]

validation_A.append(A)
validation_B.append(B)

# S1, d
A = [[0, 0, 0],
    ['a21', 0, 'a23'],
    ['a31', 'a32', 0]]

B = [['b1'],
     [0],
     [0]]

validation_A.append(A)
validation_B.append(B)

# Main

A = [[0 for i in range(20)] for j in range(20)]
A[0][18] = 'a19_1'
A[0][1] = 'a2_1'
A[2][8] = 'a9_3'
A[2][1] = 'a2_3'
A[4][3] = 'a4_5'
A[5][10] = 'a11_6'
A[5][1] = 'a2_6'
A[6][5] = 'a6_7'
A[6][2] = 'a3_7'
A[7][6] = 'a7_8'
A[8][7] = 'a8_9'
A[9][5] = 'a6_10'
A[10][9] = 'a10_11'
A[11][5] = 'a6_12'
A[11][1] = 'a2_12'
A[12][11] = 'a12_13'
A[13][12] = 'a13_14'
A[14][11] = 'a12_15'
A[14][15] = 'a16_15'
A[15][14] = 'a15_16'
A[16][11] = 'a12_17'
A[16][0] = 'a1_17'
A[17][16] = 'a17_18'
A[18][17] = 'a18_19'
A[19][3] = 'a4_20'


B = [[0 for i in range(3)] for j in range(20)]
B[0] = ['b1', 0, 0]
B[1] = ['b1', 0, 0]
B[2] = ['b1', 0, 0]
B[3] = [0, 'b2', 0]
B[4] = [0, 0, 'b3']

validation_A.append(A)
validation_B.append(B)

# test with dilation
A2 = copy.deepcopy(A)
A2[14][15] = 0  # 'a16_15'

validation_A.append(A2)
validation_B.append(B)

# DINT

A = [[0, 1],
     [0, 0]]
B = [[0],
     [1]]

validation_A.append(A)
validation_B.append(B)

# Ball rolling

A = [[0, 1, 0, 0],
     [0, 0, 'm1', 0],
     [0, 0, 0, 'm2'],
     [0, 0, 'm3', 0]]
B = [[0],
     ['f1'],
     [0],
     ['f2']]

validation_A.append(A)
validation_B.append(B)

# Controllable form

A = [[0, 1, 0, 0],
     [0, 0, 1, 0],
     [0, 0, 0, 1],
     ['a0', 'a1', 'a2', 'a3']]
B = [[0],
     [0],
     [0],
     [1]]

validation_A.append(A)
validation_B.append(B)

for valindex in range(5, len(validation_A)):
    A = validation_A[valindex]
    B = validation_B[valindex]
    print A
    s = LtiNetwork(A, B, 'test_' + str(valindex) )

    s.analysis_ab()
    #s.matching_a()

