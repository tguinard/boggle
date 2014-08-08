#!/usr/bin/python
"""
Generate random letters/boards where each letter is chosen with probability proportional to how often it occurs in the
dictionary
"""

import boggle
import string
import random

occurances = dict([(s, 0) for s in string.lowercase])

for line in open('words.txt'):
    for letter in line.strip():
        occurances[letter] += 1

choicestr = ''  # construct a string where the frequency of each letter is approx. equal to that of the dictionary
divide_by = 1000  # so the choice string is not too large
for s in string.lowercase:
    choicestr += s * (occurances[s]/divide_by)


def randletter():
    return random.choice(choicestr)


def randboard():
    return [[randletter() for _ in range(4)] for _ in range(4)]


def randscore():
    return boggle.score(randboard())


if __name__ == '__main__':
    for i in range(100):
        print randscore()
