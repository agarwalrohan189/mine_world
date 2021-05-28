import numpy as np
import copy
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

from sympy import *

# 2-d matrices for mapping to numbers
mine = []
percept0 = []
percept1 = []
perceptGreaterThan1 = []

# set the size of the maze as 4*4
n = 4

# heuristic and visited matrices
heuristic = []
visited = []


def variablesToLiterals():
    # assign numeric literals to variables as stated below

    # represent mine presence for all locations as numbers in range 1-16
    # represent percepts=0 for all locations as numbers in range 17-32
    # represent percepts=1 for all locations as numbers in range 33-48
    # represent percepts>1 for all locations as numbers in range 49-64

    # mines
    val = 1
    for i in range(n):
        row = []
        for j in range(n):
            row.append(val)
            val += 1
        mine.append(row)

    # percept=0
    for i in range(n):
        row = []
        for j in range(n):
            row.append(val)
            val += 1
        percept0.append(row)

    # percept=1
    for i in range(n):
        row = []
        for j in range(n):
            row.append(val)
            val += 1
        percept1.append(row)

    # percept>1
    for i in range(n):
        row = []
        for j in range(n):
            row.append(val)
            val += 1
        perceptGreaterThan1.append(row)


def getClauses(cnf):
    # get the cnf form in the way accepted by the pysat solver
    clauses = []
    clause = []
    cnf = cnf.split(' & ')
    for l in cnf:
        l = l.strip('(')
        l = l.strip(')')
        l = l.split(' | ')
        for lit in l:
            if lit[0] == '~':
                clause.append(-int(lit[1:]))
            else:
                clause.append(int(lit))
        clauses.append(clause[:])
        clause.clear()

    clauses.append(clause)
    return clauses


def valid(i, j):
    # check for valid indices for the room
    return i < n and j < n and i >= 0 and j >= 0


def intialise():
    # initialise the knowledge base with background knowledge
    global visited
    clauses = []

    # no mine at {0,0}
    clauses.append([-mine[0][0]])

    d1 = [1, -1, 0, 0]
    d2 = [0, 0, 1, -1]

    # initialise the bijunctions for the percepts for mine
    for i in range(n):
        for j in range(n):
            mines_list = []
            for d in range(4):
                u = i+d1[d]
                v = j+d2[d]
                if valid(u, v) == True:
                    mines_list.append([u, v])

            # for percept=0
            left = symbols(str(percept0[i][j]))
            right = True
            for l in mines_list:
                u, v = l
                right = right & ~symbols(str(mine[u][v]))

            formula = (left >> right) & (right >> left)
            # print(formula)

            for c in getClauses(str(to_cnf(formula))):
                if c != []:
                    clauses.append(c)

            # for percept=1
            left = symbols(str(percept1[i][j]))
            right = False
            for k in range(len(mines_list)):
                cnt = 0
                temp = True
                for l in mines_list:
                    u, v = l
                    if cnt == k:
                        temp = temp & symbols(str(mine[u][v]))
                    else:
                        temp = temp & ~symbols(str(mine[u][v]))
                    cnt += 1

                right = right | temp

            formula = (left >> right) & (right >> left)
            # print(formula)

            for c in getClauses(str(to_cnf(formula))):
                if c != []:
                    clauses.append(c)

            # for percent greater than 1
            left = symbols(str(perceptGreaterThan1[i][j]))
            right = True
            k = len(mines_list)-1

            for x in range(len(mines_list)):
                cnt = 0
                y = x
                temp = False
                while cnt < k:
                    u, v = mines_list[y]
                    temp = temp | symbols(str(mine[u][v]))
                    y = (y+1) % len(mines_list)
                    cnt += 1

                right = right & temp

            formula = (left >> right) & (right >> left)
            # print(formula)

            for c in getClauses(str(to_cnf(formula))):
                if c != []:
                    clauses.append(c)
    # initialise the heuristic values
    for i in range(n):
        row = []
        for j in range(n):
            row.append(n-1-j+n-1-i)
        heuristic.append(row)

    # initialise the visited values
    visited = np.zeros((n, n), dtype='int32')

    return clauses


def find(KB, percept):
    # use entailment to find all the saferooms
    rooms = []
    # check for alll rooms
    for i in range(n):
        for j in range(n):
            if visited[i][j] == 1:
                continue
            # check for entailment of mine not present
            entailment = copy.deepcopy(KB)
            entailment.append([mine[i][j]])
            g = Glucose3()
            g.append_formula(entailment)

            if g.solve() == False:
                rooms.append([i, j])

    return rooms


def check(u, v, safe, vis):
    # Check if the cell is valid, not visited and safe to go
    return u < n and v < n and u >= 0 and v >= 0 and vis[u][v] == 0 and safe[u][v] == 1


def go(d, u, v, safe, vis, path, goal, KB, ag):
    # Take a step in the given direction
    if d == 'u':
        if check(u, v+1, safe, vis):
            ag.TakeAction('Up')
            if move(ag, safe, vis, goal, KB, path):
                return True
            ag.TakeAction('Down')
    elif d == 'r':
        if check(u+1, v, safe, vis):
            ag.TakeAction('Right')
            if move(ag, safe, vis, goal, KB, path):
                return True
            ag.TakeAction('Left')
    elif d == 'l':
        if check(u-1, v, safe, vis):
            ag.TakeAction('Left')
            if move(ag, safe, vis, goal, KB, path):
                return True
            ag.TakeAction('Right')
    else:
        if check(u, v-1, safe, vis):
            ag.TakeAction('Down')
            if move(ag, safe, vis, goal, KB, path):
                return True
            ag.TakeAction('Up')


def move(ag, safe, vis, goal, KB, path, flag=1):
    # add to path if not already added
    if flag:
        path.append(ag.FindCurrentLocation())
    #
    u, v = ag.FindCurrentLocation()
    u -= 1
    v -= 1

    # print(u, v)
    if [u, v] == goal:
        return True
    vis[u][v] = 1

    if visited[u][v] == 0:
        addPercept(KB, ag.PerceiveCurrentLocation(), ag.FindCurrentLocation())

    # choose direction to go in order to optimise the path to the currently set goal
    dir = []

    if u > goal[0] and v > goal[1]:
        dir = ['l', 'd', 'r', 'u']
    elif u > goal[0] and v == goal[1]:
        dir = ['l', 'r', 'u', 'd']
    elif u > goal[0] and v < goal[1]:
        dir = ['l', 'u', 'r', 'd']
    elif u == goal[0] and v < goal[1]:
        dir = ['u', 'r', 'l', 'd']
    elif u < goal[0] and v < goal[1]:
        dir = ['r', 'u', 'l', 'd']
    elif u < goal[0] and v == goal[1]:
        dir = ['r', 'u', 'l', 'd']
    elif u < goal[0] and v > goal[1]:
        dir = ['r', 'd', 'l', 'u']
    else:
        dir = ['d', 'r', 'l', 'u']

    for d in range(4):
        if go(dir[d], u, v, safe, vis, path, goal, KB, ag):
            return True

    return False


def addPercept(KB, per, loc):
    # add percept to the knowledge base
    i, j = loc
    i -= 1
    j -= 1

    if per[1] == '0':
        KB.append([percept0[i][j]])
    elif per[0] == '=':
        KB.append([percept1[i][j]])
    else:
        KB.append([perceptGreaterThan1[i][j]])

    return KB


def main():
    # initializations
    variablesToLiterals()
    ag = Agent()
    KB = intialise()
    safe = [[0 for j in range(n)] for i in range(n)]
    safe[0][0] = 1

    path = []
    path.append(ag.FindCurrentLocation())
    safeRooms = []

    # simulation
    while(ag.FindCurrentLocation() != [n, n]):
        loc = ag.FindCurrentLocation()
        visited[loc[0]-1][loc[1]-1] = 1
        print('curLoc = ', loc)
        per = ag.PerceiveCurrentLocation()
        print('Percept ', per)
        KB = addPercept(KB, per, loc)
        for room in find(KB, per):
            safeRooms.append(room)
        print("safe rooms = ", end=' ')
        for room in safeRooms:
            print(f'[{room[0]+1}, {room[1]+1}]', end=' ')

        # choose a safe unvisited Goal
        goal = []
        closest = 50
        minSteps = 50
        for u, v in safeRooms:
            if visited[u][v] == 1:
                continue
            if heuristic[u][v] < closest:
                closest = heuristic[u][v]
                minSteps = abs((loc[0]-1)-u)+abs((loc[1]-1)-v)
                goal = [u, v]
            elif heuristic[u][v] == closest:
                if abs((loc[0]-1)-u)+abs((loc[1]-1)-v) < minSteps:
                    closest = heuristic[u][v]
                    minSteps = abs((loc[0]-1)-u)+abs((loc[1]-1)-v)
                    goal = [u, v]
            safe[u][v] = 1
        if goal == []:
            print("\nA path without any risk does not exist")
            return
        else:
            print(f'\nGoal = [{ goal[0]+1}, {goal[1]+1}]')

        # move agent to the Goal
        vis = [[0 for j in range(n)] for i in range(n)]
        move(ag, safe, vis, goal, KB, path, 0)

    print("Final Path =", end=' ')
    for i, room in enumerate(path):
        if(i != len(path)-1):
            print(room, end=' -> ')
        else:
            print(room)


if __name__ == '__main__':
    main()
# ROLLXYZ_FIRSTNAME.py
# Displaying Agent.py.
