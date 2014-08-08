#!/usr/bin/python
"""
Genetic algorithms implementation
"""


import random
import string
import sys
import boggle
import ratio
import uniform


def combine(board1, board2):
    """two boards combine, with no mutations"""
    newboard = [[random.choice(board1[i][j] + board2[i][j])
                 for i in range(4)] for j in range(4)]
    return newboard


def uniq(boards):
    """get rid of duplicate boards in population"""
    tuples = set([tuple(tuple(j for j in i) for i in ar) for ar in boards])
    lists = [list(list(j for j in i) for i in ar) for ar in boards]
    return lists


def mutate(board, chance, ratioletter=True):
    """replace one letter with a random letter"""
    while random.random() < chance:
        i = random.choice(range(4))
        j = random.choice(range(4))
        if ratioletter:
            board[i][j] = ratio.randletter()
        else:
            board[i][j] = uniform.randletter()
    return board


def crossover(board, chance):
    """swap two adjacent squares"""
    while random.random() < chance:
        if random.random() < .5:
            i1, j1 = random.choice(range(3)), random.choice(range(4))
            i2, j2 = i1+1, j1
        else:
            i1, j1 = random.choice(range(4)), random.choice(range(3))
            i2, j2 = i1, j1+1
        board[i1][j1], board[i2][j2] = board[i2][j2], board[i1][j1]
    return board


def printboard(board):
    """use for debugging"""
    for i in board:
        print i



def genetic(popcap, elite, reproduce, mutchance, crosschance, ratiostart=True, ratioletter=True):
    if ratiostart:
        population = [ratio.randboard() for _ in range(popcap)]
    else:
        population = [uniform.randboard() for _ in range(popcap)]
        
    boring = 0
    highscore = 0
    #while boring < 20:
    for g in range(1000):
        print >> sys.stderr, g
        #population = uniq(population)
        scores = [(p, boggle.score(p)) for p in population]
        scores.sort(key=lambda pair: -pair[1])
        parents = [a[0] for a in scores[:reproduce]]
        print scores[0][1]
        if highscore < scores[0][1]:
            highscore = scores[0][1]
            boring = 0
        else:
            boring += 1
        nextgen = parents[:elite]
        random.shuffle(parents)
        numkids = (popcap - len(nextgen))/len(parents)
        extrakids = popcap - len(nextgen) - len(parents)*numkids
        for p1,p2 in zip(parents[::2], parents[1::2]):
            for _ in range(numkids):
                nextgen.append(mutate(crossover(combine(p1, p2), crosschance), mutchance, ratioletter=ratioletter))
            if extrakids > 0:
                extrakids -= 1
                nextgen.append(mutate(crossover(combine(p1, p2), mutchance), mutchance))
                
        population = nextgen
    print scores[0][1]
    printboard(scores[0][0])

if __name__ == '__main__':
    #usage ./genetic.py t|f t|f
    ratiostart=True
    ratioletter=True
    if sys.argv[1] == 'f':
        ratiostart=False
        # print >> sys.stderr, 'ratiostart false'
    if sys.argv[2] == 'f':
        ratioletter=False
        # print >> sys.stderr, 'ratioletter false'
    
    genetic(100, 10, 30, .2, .2, ratiostart=ratiostart, ratioletter=ratioletter)
