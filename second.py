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

# helper arrays for getting adjacent rooms
d1 = [1, -1, 0, 0]
d2 = [0, 0, 1, -1]


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


def valid(i, j):
    # check for valid indices for the room
    return i < n and j < n and i >= 0 and j >= 0


def intialise():
    # initialise the knowledge base with background knowledge
    global visited
    clauses = []

    # no mine at {0,0} and at {n-1,n-1}
    clauses.append([-mine[0][0]])
    clauses.append([-mine[n-1][n-1]])

    # initialise the bijunctions for the percepts with mines
    for i in range(n):
        for j in range(n):
            mines_list = []
            for d in range(4):
                u = i+d1[d]
                v = j+d2[d]
                if valid(u, v) == True:
                    mines_list.append([u, v])

            # for percept=0

            formula = []
            clause = [percept0[i][j]]
            for l in mines_list:
                u, v = l
                clause.append(mine[u][v])
                formula.append([-mine[u][v], -percept0[i][j]])

            formula.append(clause)
            # print(formula)

            for c in formula:
                clauses.append(c)

            # for percept=1

            formula = []
            for x in range(len(mines_list)):
                for y in range(x+1, len(mines_list)):
                    clause = [-percept1[i][j]]
                    u, v = mines_list[x]
                    clause.append(-mine[u][v])
                    u, v = mines_list[y]
                    clause.append(-mine[u][v])
                    formula.append(clause)

            for x in range(-1, len(mines_list)):
                clause = []
                if x == -1:
                    clause.append(-percept1[i][j])
                else:
                    clause.append(percept1[i][j])
                for y in range(len(mines_list)):
                    u, v = mines_list[y]
                    if y == x:
                        clause.append(-mine[u][v])
                    else:
                        clause.append(mine[u][v])

                formula.append(clause)

            # print(formula)
            for c in formula:
                clauses.append(c)

            # for percent greater than 1

            formula = []
            for x in range(len(mines_list)):
                clause = [-perceptGreaterThan1[i][j]]
                for y in range(len(mines_list)):
                    u, v = mines_list[y]
                    if x == y:
                        continue
                    clause.append(mine[u][v])
                formula.append(clause)

            for x in range(len(mines_list)):
                for y in range(x+1, len(mines_list)):
                    clause = [perceptGreaterThan1[i][j]]
                    u, v = mines_list[x]
                    clause.append(-mine[u][v])
                    u, v = mines_list[y]
                    clause.append(-mine[u][v])
                    formula.append(clause)

            for c in formula:
                clauses.append(c)
            # print(formula)

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
            g = Glucose3()
            g.append_formula(KB)
            g.add_clause([mine[i][j]])

            if g.solve() == False:
                rooms.append([i, j])

    return rooms


def check(u, v, safe):
    # Check if the cell is valid, not visited and safe to go
    return u < n and v < n and u >= 0 and v >= 0 and safe[u][v] == 1


def go(d, safe, ag, path):
    # take a move in the defined direction and add to path
    path.append(ag.FindCurrentLocation())
    u, v = ag.FindCurrentLocation()
    u -= 1
    v -= 1
    # Take a step in the given direction
    if d == 'u':
        if check(u, v+1, safe):
            ag.TakeAction('Up')
    elif d == 'r':
        if check(u+1, v, safe):
            ag.TakeAction('Right')
    elif d == 'l':
        if check(u-1, v, safe):
            ag.TakeAction('Left')
    else:
        if check(u, v-1, safe):
            ag.TakeAction('Down')


def planRoute(ag, safe, goal):
    # get the shortest safe path to the current goal using BFS as each step costs 1
    vis = np.zeros((n, n), dtype='int32')
    u, v = ag.FindCurrentLocation()
    u -= 1
    v -= 1

    # queue to add rooms with the path
    queue = []
    queue.append([[u, v], ''])

    while queue:
        node = queue.pop(0)
        u, v = node[0]
        path = node[1]
        if u == goal[0] and v == goal[1]:
            return path

        if vis[u][v] == 1:
            continue

        vis[u][v] = 1

        # up
        if valid(u, v+1) and safe[u][v+1]:
            queue.append([[u, v+1], path+'u'])
        # right
        if valid(u+1, v) and safe[u+1][v]:
            queue.append([[u+1, v], path+'r'])
        # down
        if valid(u, v-1) and safe[u][v-1]:
            queue.append([[u, v-1], path+'d'])
        # left
        if valid(u-1, v) and safe[u-1][v]:
            queue.append([[u-1, v], path+'l'])

    # if a safe path is not possible
    return 'not possible'


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

    # memory to remember the safe rooms already entailed
    safe = np.zeros((n, n), dtype='int32')
    safe[0][0] = 1
    safe[n-1][n-1] = 1

    # final safe path taken
    path = []
    # list of the entailed safe rooms
    safeRooms = []

    # simulation
    while(ag.FindCurrentLocation() != [n, n]):

        # get current location and make it visited
        loc = ag.FindCurrentLocation()
        visited[loc[0]-1][loc[1]-1] = 1
        print('\ncurLoc = ', loc)

        # explore the current cell and add the percept to knowledge base
        per = ag.PerceiveCurrentLocation()
        print('Percept ', per)
        KB = addPercept(KB, per, loc)

        # find the safe rooms which can be entailed from the knowledge base
        for room in find(KB, per):
            if room not in safeRooms:
                safeRooms.append(room)
        print("safe rooms = ", end=' ')
        for room in safeRooms:
            print(f'[{room[0]+1}, {room[1]+1}]', end=' ')

        # choose a safe unvisited Goal nearest to [n,n]
        goal = []
        checked = []
        while goal == []:
            closest = 50
            minSteps = 50

            for u, v in safeRooms:
                # continue if room is visited or already checked for goal
                if visited[u][v] == 1 or [u, v] in checked:
                    continue
                # find the closest safe room based on manhattan distance heuristic
                if heuristic[u][v] < closest:
                    closest = heuristic[u][v]
                    minSteps = abs((loc[0]-1)-u)+abs((loc[1]-1)-v)
                    goal = [u, v]
                # if same distance then choose the one nearest to current room
                elif heuristic[u][v] == closest:
                    if abs((loc[0]-1)-u)+abs((loc[1]-1)-v) < minSteps:
                        closest = heuristic[u][v]
                        minSteps = abs((loc[0]-1)-u)+abs((loc[1]-1)-v)
                        goal = [u, v]
                # mark the room safe
                safe[u][v] = 1
            # if no goal then no safe path exists
            if goal == []:
                print("\nA path without any risk does not exist")
                return

            # get the shortest safe path
            safePath = planRoute(ag, safe, goal)

            # move to another goal if a safe path to current goal is not possible
            if safePath[0] == 'n':
                checked.append(goal)
                goal = []

        print(f'\nCurrent Goal = [{ goal[0]+1}, {goal[1]+1}]')

        # use the safe path to move to the current goal
        for c in safePath:
            go(c, safe, ag, path)

    # print the final path
    print("\nFinal Path =", end=' ')
    path.append([n, n])
    for i, room in enumerate(path):
        if(i != len(path)-1):
            print(room, end=' -> ')
        else:
            print(room)


if __name__ == '__main__':
    main()
# ROLLXYZ_FIRSTNAME.py
# Displaying Agent.py.
