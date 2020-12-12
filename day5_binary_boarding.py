# Day 5 : Binary Boarding
#
# Input : A list of boarding pass with binary space Seat ID
# Part 1 : Find the highest Seat ID in the list

import unittest
from collections import namedtuple
from typing import Literal, List

Range = namedtuple("Range", "min, max")

planeSeatsRowRange = Range(0, 127)
planeSeatsColumnRange = Range(0, 7)

def getHalfRange(half: Literal['lower', 'upper'], range: Range) -> Range:
    (min, max) = range
    median = min + (max - min) // 2
    return Range(min, median) if(half == 'lower') else Range(median + 1, max)

def decodeBoardingPass(boardingPass: str) -> (int, int):
    seatRowRange = planeSeatsRowRange
    seatColumnRange = planeSeatsColumnRange

    for letter in boardingPass:
        if(letter in ['F', 'B']):
            half = 'lower' if letter == 'F' else 'B'
            seatRowRange = getHalfRange(half, seatRowRange)
        elif(letter in ['L', 'R']):
            half = 'lower' if letter == 'L' else 'R'
            seatColumnRange = getHalfRange(half, seatColumnRange)

    assert seatRowRange.min == seatRowRange.max
    assert seatColumnRange.min == seatColumnRange.max

    return (seatRowRange.min, seatColumnRange.max)

def getSeatID(seatPosition: (int, int)) -> int:
    (row, column) = seatPosition
    return row * 8 + column

def getMaxSeatId(boardingPasses: List[str]) -> int:
    return max([getSeatID(decodeBoardingPass(p)) for p in boardingPasses])

def findEmptySeats(boardingPasses: List[str], ignoredRownsAtFront = 0, ignoredRownsAtBack = 0):
    (minR, maxR) = (planeSeatsRowRange.min + ignoredRownsAtFront, planeSeatsRowRange.max - ignoredRownsAtBack)
    (minC, maxC) = planeSeatsColumnRange
    allSeatIds = [getSeatID((r, c)) for r in range(minR, maxR + 1) for c in range(minC, maxC + 1)]
    occupiedSeatIds = [getSeatID(decodeBoardingPass(p)) for p in boardingPasses]
    emptySeats = [id for id in allSeatIds if id not in occupiedSeatIds]
    return emptySeats

class SamplesTests(unittest.TestCase):

    def test_part_one(self):
        self.assertEqual(getHalfRange('lower', (0, 127)), (0, 63))
        self.assertEqual(getHalfRange('upper', (0, 127)), (64, 127))
        self.assertEqual(getHalfRange('upper', (64, 127)), (96, 127))
        
        self.assertEqual(getHalfRange('lower', (64, 65)), (64, 64))
        self.assertEqual(getHalfRange('upper', (64, 65)), (65, 65))

        self.assertEqual(decodeBoardingPass('FBFBBFFRLR'), (44, 5))
        self.assertEqual(getSeatID(decodeBoardingPass('FBFBBFFRLR')), 357)

unittest.main(argv=[''], verbosity=2, exit=False)

print("\n------\n")

with open("puzzle_inputs/day5.txt", "r") as f:
    input = f.readlines()
    print('Part 1:', getMaxSeatId(input))
    print('Part 2:', findEmptySeats(input, ignoredRownsAtFront = 1, ignoredRownsAtBack = 6))
