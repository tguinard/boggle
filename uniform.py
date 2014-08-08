#!/usr/bin/python
"""
Generate random letters/boards where each letter is chosen with equal probability
"""
import random
import string
import boggle


def randletter():
    return random.choice(string.lowercase)


def randboard():
    return [[randletter() for _ in range(4)] for _ in range(4)]


def randscore():
    return boggle.score(randboard())


if __name__ == '__main__':
    for i in range(100):
        print randscore()