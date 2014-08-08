#!/usr/bin/python
"""
Simulated annealing
"""
import boggle
import ratio
import math
import uniform
import random
import sys


def mutate(board, ratioLetter=True):
    """replace one letter with a random letter"""
    newboard = [ar[:] for ar in board]
    i = random.choice(range(4))
    j = random.choice(range(4))
    if ratioLetter:
        newboard[i][j] = ratio.randletter()
    else:
        newboard[i][j] = uniform.randletter()
    return newboard


def crossover(board):
    """swap two adjancent squares"""
    if random.random() < .5:
        i1, j1 = random.choice(range(3)), random.choice(range(4))
        i2, j2 = i1+1, j1
    else:
        i1, j1 = random.choice(range(4)), random.choice(range(3))
        i2, j2 = i1, j1+1
    newboard = [ar[:] for ar in board]
    newboard[i1][j1], newboard[i2][j2] = board[i2][j2], board[i1][j1]
    return newboard


def rcrossover(board):
    """swap two random (possibly nonadjacent) squares"""
    choices = [(i,j) for i in range(4) for j in range(4)]
    i1, j1 = random.choice(choices)
    i2 = i1
    j2 = j1
    while i2 == i1 and j1 == j2:
        i2, j2 = random.choice(choices)
    newboard = [ar[:] for ar in board]
    newboard[i1][j1], newboard[i2][j2] = board[i2][j2], board[i1][j1]
    return newboard


def p(score, newscore, temp):
    """probability of changing board"""
    return min(math.exp((newscore - score)/temp), 1)


def temperature(frac, maxtemp):
    """Temperature function, decreases as the iterations increase"""
    return (1 - frac)*maxtemp


def anneal(kmax, maxtemp, ratioBoard=True, ratioLetter=True):
    """
    Main annealing function:
    kmax: max iterations
    maxtemp: maximum temperature
    ratioBoard: whether to start with a board with dictionary probability distribution
    ratioLetter: whether to select letters with dictionary probability distribution
    """
    if ratioBoard:
        board = ratio.randboard()
    else:
        board = uniform.randboard()
    score = boggle.score(board)
    maxboard = board
    maxscore = score
    for k in range(kmax):
        temp = temperature(k / float(kmax), maxtemp)
        newboard = crossover(board)
        newscore = boggle.score(newboard)
        if p(score, newscore, temp) > random.random():
            board = newboard
            score = newscore
            print 'crossover'
        if newscore > maxscore:
            maxscore = newscore
            maxboard = newboard
        newboard = mutate(board, ratioLetter=ratioLetter)
        newscore = boggle.score(newboard)
        if p(score, newscore, temp) > random.random():
            board = newboard
            score = newscore
            print 'mutate'
        if newscore > maxscore:
            maxscore = newscore
            maxboard = newboard
        newboard = rcrossover(board)
        newscore = boggle.score(newboard)
        if p(score, newscore, temp) > random.random():
            board = newboard
            score = newscore
            print 'rcrossover'
        if newscore > maxscore:
            maxscore = newscore
            maxboard = newboard
        print k, score
    return maxscore, maxboard


if __name__ == '__main__':
    #usage: ./anneal.py temp f|t f|t
    # print sys.argv
    maxtemp = int(sys.argv[1])
    ratioBoard=True
    ratioLetter=True
    if sys.argv[2] == 'f':
        ratioBoard=False
        # print >> sys.stderr, 'ratioboard false'
    if sys.argv[3] == 'f':
        ratioLetter=False
        # print >> sys.stderr, 'ratioletter false'
    print anneal(1000, maxtemp, ratioBoard=ratioBoard, ratioLetter=ratioLetter)
