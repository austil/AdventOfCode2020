# Day 8 : Handheld Halting
#
# Input : a program
# Part 1 : find the value of the accumulator before the infinite loop

import unittest
from typing import List, Set

def run(program: List[str]):
    accumulator = 0
    instructionPointer = 0
    operationIdxRan = set()
    inInfiniteLoop = False
    terminated = False

    while not inInfiniteLoop and not terminated:
        instruction = program[instructionPointer]
        [operation, argument] = instruction.split(' ')
        operationIdxRan.add(instructionPointer)
        # print(instructionPointer, (operation, argument))

        if operation == 'jmp':
            instructionPointer += int(argument)
        elif operation == 'acc':
            accumulator += int(argument)
            instructionPointer += 1
        elif operation == 'nop':
            instructionPointer += 1
        else:
            raise Exception(f'Unknown operation {instruction}') 

        inInfiniteLoop = instructionPointer in operationIdxRan
        terminated = instructionPointer >= len(program)

    code = 0 if terminated else 1
    return (code, accumulator, operationIdxRan)

def flipOp(program: List[str], operationIdx: int):
    newProgram = list.copy(program)

    targetOp = newProgram[operationIdx]
    if targetOp.startswith('nop'):
        newProgram[operationIdx] = targetOp.replace('nop', 'jmp')
    elif targetOp.startswith('jmp'):
        newProgram[operationIdx] = targetOp.replace('jmp', 'nop')

    return newProgram

def getAlternatives(program: List[str], operationIdxRan: Set[int]):
    return [
        flipOp(program, opIdx)
        for opIdx in operationIdxRan 
        if program[opIdx][:3] in ['jmp', 'nop']
    ]

def findProperTermination(programs: List[List[str]]):
    for p in programs:
        (code, acc, idxRan) = run(p)
        if code == 0: return (code, acc, idxRan)

sampleRules = """
nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6
""".strip().splitlines()

class SamplesTests(unittest.TestCase):

    def test_part_one(self):
        (code, acc, idxRan) = run(sampleRules)
        self.assertEqual(code, 1)
        self.assertEqual(acc, 5)
    
    def test_part_two(self):
        (code, acc, idxRan) = run(sampleRules)
        (code, acc, idxRan) = findProperTermination(getAlternatives(sampleRules, idxRan))
        self.assertEqual(code, 0)
        self.assertEqual(acc, 8)

unittest.main(argv=[''], verbosity=2, exit=False)

print("\n------\n")

with open("puzzle_inputs/day8.txt", "r") as f:
    input = f.readlines()

    (code, acc, idxRan) = run(input)
    print('Part 1:', acc)
    print(f'Ran {len(idxRan)}/{len(input)} operations')

    alternatives = getAlternatives(input, idxRan)
    print(f'Trying {len(alternatives)} alternatives')
    (code, acc, idxRan) = findProperTermination(alternatives)
    print('Part 2:', acc)