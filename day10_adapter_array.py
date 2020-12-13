# Day 10 : Adapter Array
#
# Input : a list of jolts adapter
# Part 1 : find the adapter chain to reach a specific joltage

import unittest
from typing import List, Dict
from collections import Counter
from itertools import groupby
from math import prod

deviceAdapterDelta = 3

def getAdapterChainDeltas(adapters: List[int]) -> List[int]:
    deviceAdapter = max(adapters) + deviceAdapterDelta
    adaptersChain = [0] + sorted(adapters) + [deviceAdapter]
    deltas = [ adaptersChain[i] - adaptersChain[i-1] for i in range(1, len(adaptersChain)) ]
    return deltas

def getAdapterDeltas(adapters: List[int]) -> Dict[int, int]:
    deltas = getAdapterChainDeltas(adapters)
    return Counter(deltas)

onesChainsToArrangementCount = {
    2: 2,
    3: 4,
    4: 7
}

def countArrangements(adapters: List[int]) -> int:
    deltas = getAdapterChainDeltas(adapters)
    deltasChains = [list(g) for k, g in groupby(deltas)]
    onesChains = [c for c in deltasChains if c[0] == 1 and len(c) > 1]
    return prod([onesChainsToArrangementCount[len(c)] for c in onesChains])

sampleAdapters = [ 16, 10, 15, 5, 1, 11, 7, 19, 6, 12, 4 ]
sampleAdapters2 = [ 28, 33, 18, 42, 31, 14, 46, 20, 48, 47, 24, 23, 49, 45, 19, 38, 39, 11, 1, 32, 25, 35, 8, 17, 7, 9, 4, 2, 34, 10, 3 ]

class SamplesTests(unittest.TestCase):

    def test_part_one(self):
        self.assertEqual(getAdapterDeltas(sampleAdapters), { 1: 7, 3: 5 })
    
    def test_part_two(self):
        self.assertEqual(countArrangements(sampleAdapters), 8)
        self.assertEqual(countArrangements(sampleAdapters2), 19208)

unittest.main(argv=[''], verbosity=2, exit=False)

print("\n------\n")

with open("puzzle_inputs/day10.txt", "r") as f:
    input = [int(i) for i in f.readlines()]
    adapterDeltas = getAdapterDeltas(input)
    print('Part 1:', adapterDeltas, '=>', adapterDeltas[1] * adapterDeltas[3])
    print('Part 2:', countArrangements(input))
