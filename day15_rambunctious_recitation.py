# Day 15 : Rambunctious Recitation
#
# Input : a list of starting numbers for a spoken memory game
# Part 1 : find the the 2020th number spoken

import unittest
from typing import List

def spokenNumbersGame(startingNumbers):
    previouslySpokenIndex = dict([(n, i) for (i, n) in enumerate(startingNumbers)])
    lastSpoken = 0
    n = len(startingNumbers)
    yield lastSpoken
    while True:
        if not lastSpoken in previouslySpokenIndex:
            nextSpoken = 0
        else:
            nextSpoken = n - previouslySpokenIndex[lastSpoken]
        previouslySpokenIndex[lastSpoken] = n
        yield nextSpoken
        lastSpoken = nextSpoken
        n += 1
        if(n % 1000000 == 0): print('iterated :', n, 'times')

def idx(generator, init, n):
    return next(x for i,x in enumerate(generator(init)) if i == n - len(init) - 1)

sampleGame = spokenNumbersGame([0,3,6])

class SamplesTests(unittest.TestCase):

    def test_part_one(self):
        self.assertEqual([ next(sampleGame) for _ in range(7) ], [0,3,3,1,0,4,0])
        self.assertEqual(idx(spokenNumbersGame, [0,3,6], 2020), 436)
        self.assertEqual(idx(spokenNumbersGame, [1,3,2], 2020), 1)
        self.assertEqual(idx(spokenNumbersGame, [2,1,3], 2020), 10)
    
    # def test_part_two(self):
    #     self.assertEqual(idx(spokenNumbersGame, [0,3,6], 30_000_000), 175594)

unittest.main(argv=[''], verbosity=2, exit=False)

print("\n------\n")

input = [8,0,17,4,1,12]
print('Part 1:', idx(spokenNumbersGame, input, 2020))
# print('Part 2:', idx(spokenNumbersGame, input, 30_000_000))
