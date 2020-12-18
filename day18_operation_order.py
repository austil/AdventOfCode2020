# Day 18 : Operation Order
#
# Input : a math operation
# Part 1 : find the sum of all the operation

import unittest
from typing import List

def apply(stack, operators):
    while ( len(stack) >= 3
        and stack[-3].isdigit()
        and stack[-2] in operators
        and stack[-1].isdigit()):
        expr = f'{stack[-3]} {stack[-2]} {stack[-1]}'
        stack = stack[:-3]
        stack.append(str(eval(expr)))
    return stack

def compute(operation):
    parts = operation.replace('(', ' ( ').replace(')', ' ) ').split(' ')
    stack = []
    for p in parts:
        if p == ')':
            # get rid of parenthesis
            assert stack[-2] == '(' and stack[-1].isdigit()
            stack = stack[:-2] + [stack[-1]]
        elif p != '':
            stack.append(p)

        # apply ALL operators as we go
        stack = apply(stack, ['+', '*'])

    assert len(stack) == 1
    return int(stack[0])

def compute2(operation):
    parts = operation.replace('(', ' ( ').replace(')', ' ) ').split(' ')
    stack = []
    for p in parts:
        if p == ')':
            stack = apply(stack, ['*'])
            # get rid of parenthesis
            assert stack[-2] == '(' and stack[-1].isdigit()
            stack = stack[:-2] + [stack[-1]]
        elif p != '':
            # stack
            stack.append(p)
        
        # apply only + as we go
        stack = apply(stack, ['+'])
        
    stack = apply(stack, ['*'])

    assert len(stack) == 1
    return int(stack[0])

class SamplesTests(unittest.TestCase):

    def test_part_one(self):
        self.assertEqual(compute('1 + 2 * 3 + 4 * 5 + 6'), 71)
        self.assertEqual(compute('1 + (2 * 3) + (4 * (5 + 6))'), 51)
        self.assertEqual(compute('2 * 3 + (4 * 5)'), 26)
        self.assertEqual(compute('5 + (8 * 3 + 9 + 3 * 4 * 3)'), 437)
        self.assertEqual(compute('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))'), 12240)
        self.assertEqual(compute('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2'), 13632)
    
    def test_part_two(self):
        self.assertEqual(compute2('1 + 2 * 3 + 4 * 5 + 6'), 231)
        self.assertEqual(compute2('1 + (2 * 3) + (4 * (5 + 6))'), 51)
        self.assertEqual(compute2('2 * 3 + (4 * 5)'), 46)
        self.assertEqual(compute2('5 + (8 * 3 + 9 + 3 * 4 * 3)'), 1445)
        self.assertEqual(compute2('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))'), 669060)
        self.assertEqual(compute2('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2'), 23340)

unittest.main(argv=[''], verbosity=2, exit=False)

print("\n------\n")

with open("puzzle_inputs/day18.txt", "r") as f:
    input = f.readlines()
    print('Part 1:', sum([compute(e.strip()) for e in input]))
    assert sum([compute(e.strip()) for e in input]) == 9535936849815
    print('Part 2:', sum([compute2(e.strip()) for e in input]))
    assert sum([compute2(e.strip()) for e in input]) == 472171581333710
