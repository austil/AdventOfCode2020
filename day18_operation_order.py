# Day 18 : Operation Order
#
# Input : a math operation
# Part 1 : find the sum of all the operation

import unittest
from typing import List

def compute(operation):
    parts = operation.replace('(', ' ( ').replace(')', ' ) ').split(' ')
    stack = []
    for p in parts:
        if len(stack) and stack[-1] in ['+', '*'] and p.isdigit():
            expr = f'{stack[-2]} {stack[-1]} {p}'
            stack = stack[:-2]
            stack.append(str(eval(expr)))
        elif p == ')':
            r = stack[-1]
            stack = stack[:-2]
            stack.append(r)
            while len(stack) >= 3 and stack[-2] in ['+', '*']:
                expr = f'{stack[-3]} {stack[-2]} {stack[-1]}'
                stack = stack[:-3]
                stack.append(str(eval(expr)))
        elif p != '':
            stack.append(p)
    return int(stack[0])

class SamplesTests(unittest.TestCase):

    def test_part_one(self):
        self.assertEqual(compute('1 + 2 * 3 + 4 * 5 + 6'), 71)
        self.assertEqual(compute('2 * 3 + (4 * 5)'), 26)
        self.assertEqual(compute('1 + (2 * 3) + (4 * (5 + 6))'), 51)
        self.assertEqual(compute('5 + (8 * 3 + 9 + 3 * 4 * 3)'), 437)
        self.assertEqual(compute('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))'), 12240)
        self.assertEqual(compute('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2'), 13632)
    
    # def test_part_two(self):
    #     self.assertEqual(0, 0)

unittest.main(argv=[''], verbosity=2, exit=False)

print("\n------\n")

with open("puzzle_inputs/day18.txt", "r") as f:
    input = f.readlines()
    print('Part 1:', sum([compute(e.strip()) for e in input]))