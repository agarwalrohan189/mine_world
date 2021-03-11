from pysat.solvers import Glucose3
from Agent import *  # See the Agent.py file
# CS F407: Artificial Intelligence
# Programming Assignment 2
# Sujith Thomas
# •
# Mar 9

# Agent.py
# Text

# Problem2.pdf
# PDF

# ROLLXYZ_FIRSTNAME.py
# Text

# SatSolverExample.py
# Text
# Class comments


#!/usr/bin/env python3

# All your code can go here.

# You can change the main function as you wish. Run this program to see the output. Also see Agent.py code.


def main():
    ag = Agent()
    print('curLoc', ag.FindCurrentLocation())
    print('Percept ', ag.PerceiveCurrentLocation())
    ag.TakeAction('Right')
    print('Percept ', ag.PerceiveCurrentLocation())
    ag.TakeAction('Right')
    print('Percept ', ag.PerceiveCurrentLocation())


if __name__ == '__main__':
    main()
# ROLLXYZ_FIRSTNAME.py
# Displaying Agent.py.
