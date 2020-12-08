# Day 3: Toboggan Trajectory
# 
# Input : a matrix map of the sourding area with open squares '.' and trees '#'
# Part 1 : find how many we encounter crossing the map with the slope (right 3, down 1)

import unittest
from collections import namedtuple
from typing import List
from math import prod


Coordinate = namedtuple("Coordinate", "x, y")
Slope = Coordinate
Terrain = List[str]

Tree = '#'
OpenSquare = '.'

def isValidLocation(val):
    return val == Tree or val == OpenSquare

def lookupLocation(terrain: Terrain, coordinate: Coordinate):
    knownTerrainWidth = len(terrain[0])
    location = terrain[coordinate.y][coordinate.x % knownTerrainWidth]
    assert isValidLocation(location), f"'{location}' at coord ({coordinate.x}, {coordinate.y}) is not a valid location"
    return location

def nextVisitedCoordinate(maxY: int, slope: Slope) -> Coordinate:
    current = Coordinate(0, 0)
    while current.y < maxY:
        yield current
        current = Coordinate(current.x + slope.x, current.y + slope.y)

def countEncounteredTree(terrain: Terrain, slope: Slope):
    encountered = [lookupLocation(terrain, c) for c in nextVisitedCoordinate(len(terrain), slope)]
    return sum([location == Tree for location in encountered ])
    
def getSlopesChecksum(terrain: Terrain, slopes: List[Slope]):
    return prod([countEncounteredTree(terrain, s) for s in slopes])

sampleMapStr = """
..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#
"""

sampleMap = sampleMapStr.strip().split('\n')

testedSlopes = [
    Slope(1, 1),
    Slope(3, 1),
    Slope(5, 1),
    Slope(7, 1),
    Slope(1, 2),
]

class SamplesTests(unittest.TestCase):

    def test_part_one(self):
        self.assertEqual(countEncounteredTree(sampleMap, Slope(3, 1)), 7)
    
    def test_part_two(self):
        self.assertEqual(getSlopesChecksum(sampleMap, testedSlopes), 336)

unittest.main(argv=[''], verbosity=2, exit=False)

print("\n------\n")

with open("puzzle_inputs/day3.txt", "r") as f:
    input = [l.strip() for l in f.readlines()]
    print("Part 1 :", countEncounteredTree(input, Slope(3, 1)))
    print("Part 2 :", getSlopesChecksum(input, testedSlopes))
