#!/usr/bin/python
"""
Solves a boggle board using perfect play
Modified solution from:
http://stackoverflow.com/questions/746082/how-to-find-list-of-possible-words-from-a-letter-matrix-boggle-solver
"""

import re

dictionary = set(word.strip('\n') for word in open('words.txt'))
savedwords = {}
saveorder = []


def solve(grid):
    alphabet = ''.join(sum(grid, []))
    aset = tuple(sorted(list(set(alphabet))))
    if aset in savedwords:
        words = savedwords[aset]
    else:
        bogglable = re.compile('^[' + alphabet + ']{3,}$', re.I).match
        words = set(word for word in dictionary if bogglable(word))
        savedwords[aset] = words
        saveorder.append(aset)
        if len(saveorder) > 100:
            del savedwords[saveorder[0]]
            del saveorder[0]
    prefixes = set(word[:i] for word in words
                   for i in range(2, len(word)+1))
    for y, row in enumerate(grid):
        for x, letter in enumerate(row):
            for result in extending(letter, ((x, y),), words, grid, prefixes):
                yield result


def extending(prefix, path, words, grid, prefixes):
    if prefix in words:
        yield (prefix, path)
    for (nx, ny) in neighbors(path[-1], len(grid), len(grid[0])):
        if (nx, ny) not in path:
            prefix1 = prefix + grid[ny][nx]
            if prefix1 in prefixes:
                for result in extending(prefix1, path + ((nx, ny),), 
                                        words, grid, prefixes):
                    yield result


def neighbors((x, y), ncols, nrows):
    for nx in range(max(0, x-1), min(x+2, ncols)):
        for ny in range(max(0, y-1), min(y+2, nrows)):
            yield (nx, ny)


def wordscore(word):
    if 3 <= len(word) <= 4:
        return 1
    if len(word) == 5:
        return 2
    if len(word) == 6:
        return 3
    if len(word) == 7:
        return 5
    if len(word) >= 8:
        return 11
    return 0


def score(grid):
    solutions = set([ar[0] for ar in solve(grid)])
    return sum(wordscore(i) for i in solutions)


if __name__ == '__main__':
    #simple test
    s = 'okam asxm neni gtfl'
    grid = [[i for i in ar] for ar in s.split()]
    print grid
    print score(grid)
    for i, j in solve(grid):
        print i
