# Day 14 : Docking Data
#
# Input : a program aka a list of mask and memory assignements
# Part 1 : find the sum of value in memory after everything ran

import unittest
import re
from collections import Counter
from itertools import product
from typing import List

memorySize = 36  # bits


def applyMask(mask: str, n: int) -> int:
    assert len(
        mask) == memorySize, f'mask should have a length of {len(memorySize)}'
    result = list(format(n, 'b').zfill(len(mask)))
    for i, maskBit in enumerate(mask):
        if maskBit != 'X':
            result[i] = maskBit
    return int("".join(result), 2)


def applyMaskV2(mask: str, n: int) -> List[int]:
    assert len(
        mask) == memorySize, f'mask should have a length of {len(memorySize)}'

    floatingBits = Counter(mask)['X']
    floatingBitsCombination = product([0, 1], repeat=floatingBits)

    baseResult = list(format(n, 'b').zfill(len(mask)))
    results = []

    for fb in floatingBitsCombination:
        current = baseResult.copy()
        fbi = 0
        for i, maskBit in enumerate(mask):
            if maskBit == 'X':
                current[i] = str(fb[fbi])
                fbi += 1
            elif maskBit == '1':
                current[i] = '1'
        assert fbi == floatingBits
        results.append(current)

    return [int("".join(r), 2) for r in results]


def run(program: List[str]) -> int:
    memory = {}
    currentMask = ""

    for instruction in program:
        [operation, argument] = instruction.split(' = ')
        if operation == 'mask':
            currentMask = argument.strip()
        elif operation[:3] == 'mem':
            address = int(re.search(r'\d+', operation).group())
            value = int(argument)
            memory[address] = applyMask(currentMask, value)
        else:
            raise Exception(f'Unknown operation {instruction}')

    return sum([memory[k] for k in memory])


def runV2(program: List[str]) -> int:
    memory = {}
    currentMask = ""

    i = 0
    for instruction in program:
        i += 1
        [operation, argument] = instruction.split(' = ')
        if operation == 'mask':
            currentMask = argument.strip()
        elif operation[:3] == 'mem':
            value = int(argument)
            address = int(re.search(r'\d+', operation).group())
            addresses = applyMaskV2(currentMask, address)
            for addr in addresses:
                memory[addr] = value
        else:
            raise Exception(f'Unknown operation {instruction}')

    return sum([memory[k] for k in memory])


sampleProgram = """
mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0
""".strip().splitlines()

sampleProgram2 = """
mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1
""".strip().splitlines()


class SamplesTests(unittest.TestCase):

    def test_part_one(self):
        self.assertEqual(
            applyMask('XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X', 11), 73)
        self.assertEqual(
            applyMask('XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X', 101), 101)
        self.assertEqual(
            applyMask('XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X', 0), 64)

        self.assertEqual(run(sampleProgram), 165)

    def test_part_two(self):
        results = applyMaskV2('000000000000000000000000000000X1001X', 24)
        self.assertEqual(results, [26, 27, 58, 59])

        self.assertEqual(runV2(sampleProgram2), 208)


unittest.main(argv=[''], verbosity=2, exit=False)

print("\n------\n")

with open("puzzle_inputs/day14.txt", "r") as f:
    input = f.readlines()
    print('Part 1:', run(input))
    print('Part 1:', runV2(input))
