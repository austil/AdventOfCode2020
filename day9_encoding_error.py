# Day 9 : Encoding Error
#
# Input : XMAS encrypted data
# Part 1 : find the first invalid code

from itertools import product
import unittest
from typing import List

def isValidNumber(preamble: List[int], number: int) -> bool:
    combinations = [ a + b for (a, b) in product(preamble, repeat=2) if a != b]
    return number in combinations

def checkData(data: List[int], preambleSize: int):
    for i in range(preambleSize, len(data)):
        preamble = data[i-preambleSize:i]
        isValid = isValidNumber(preamble, data[i])
        if not isValid: return data[i]
    return None

def findContiguousSum(data: List[int], target: int):
    subsetStartIdx = 0
    subsetSize = 2
    while subsetStartIdx < len(data):
        subset = data[subsetStartIdx : subsetStartIdx + subsetSize]
        subsetSum = sum(subset)
        if subsetSum == target: return subset
        elif subsetSum > target:
            subsetStartIdx += 1
            subsetSize = 2
        else:
            subsetSize += 1
    return []

samplePreamble = [20] + list(range(1, 20)) + list(range(21, 26))

sampleData = [ 35, 20, 15, 25, 47, 40, 62, 55, 65, 95, 102, 117, 150, 182, 127, 219, 299, 277, 309, 576 ]

class SamplesTests(unittest.TestCase):

    def test_part_one(self):
        self.assertEqual(isValidNumber(samplePreamble, 26), True)
        self.assertEqual(isValidNumber(samplePreamble, 49), True)
        self.assertEqual(isValidNumber(samplePreamble, 100), False)
        self.assertEqual(isValidNumber(samplePreamble, 50), False)

        self.assertEqual(checkData(sampleData, 5), 127)
    
    def test_part_two(self):
        self.assertEqual(findContiguousSum(sampleData, 127), [15, 25, 47, 40])

unittest.main(argv=[''], verbosity=2, exit=False)

print("\n------\n")

with open("puzzle_inputs/day9.txt", "r") as f:
    input = [int(i) for i in f.readlines()]
    invalidCode = checkData(input, 25)
    print('Part 1:', invalidCode)
    encryptionWeakness = findContiguousSum(input, invalidCode)
    print('Part 2:', min(encryptionWeakness) + max(encryptionWeakness))