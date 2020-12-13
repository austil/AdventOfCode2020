# Day 7 : Handy Haversacks
#
# Input : a list of bag nesting rules
# Part 1 : find how many bag can contains at least one shiny gold bag, directly or not

import unittest
import re
from typing import List, Dict, Tuple, Set

Bag = str
Quantity = int
Capacity = List[Tuple[Quantity, Bag]]

def parseRule(rule: str) -> (Bag, Capacity):
    [bag, containsStr] = re.split(r' bags contain ', rule)
    
    if containsStr.strip() == 'no other bags.':
        return (bag, [])
    
    capacity = []
    for contained in containsStr.split(', '):
        (quantity, containedBag) = re.match(r'(\d+) (.*) bags?', contained).group(1, 2)
        capacity.append((int(quantity), containedBag) )
    return (bag, capacity)

class BagConstraits:
    def __init__(self):
        self.fitsInto = []
        self.canHold = []

def parseBagConstraintsTree(rules: List[str]) -> Dict[str, BagConstraits]:
    bagConstraintsTree = {}
    
    def initBagContraints(bag):
        if not bag in bagConstraintsTree:
            bagConstraintsTree[bag] = BagConstraits()

    for rule in rules:
        (bag, capacity) = parseRule(rule)

        initBagContraints(bag)
        bagConstraintsTree[bag].canHold = capacity

        for (quantity, compatibleBag) in capacity:
            initBagContraints(compatibleBag)
            bagConstraintsTree[compatibleBag].fitsInto.append(bag)

    return bagConstraintsTree

def compatibleHostBags(bagConstraintsTree: Dict[str, BagConstraits], bag: str) -> Set[str]:
    if not bag in bagConstraintsTree: return set()
    host = set(bagConstraintsTree[bag].fitsInto)
    for b in bagConstraintsTree[bag].fitsInto:
        host.update(compatibleHostBags(bagConstraintsTree, b))
    return host

def requiredChildBags(bagConstraintsTree: Dict[str, BagConstraits], bag: str) -> List[str]:
    childBags = []
    for (quantity, bag) in bagConstraintsTree[bag].canHold:
        childBags += ([bag] * quantity)
        childBags += (requiredChildBags(bagConstraintsTree, bag) * quantity)
    return childBags

sampleRules = """
light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.
""".strip().splitlines()

class SamplesTests(unittest.TestCase):

    def test_part_one(self):
        contraintTree = parseBagConstraintsTree(sampleRules)
        self.assertEqual(len(contraintTree), 9)
        self.assertEqual(contraintTree['shiny gold'].fitsInto, ['bright white', 'muted yellow'])

        compatibleHost = compatibleHostBags(contraintTree, 'shiny gold')
        self.assertEqual(len(compatibleHost), 4)
        self.assertSetEqual(set(compatibleHost), set(['bright white', 'muted yellow', 'light red', 'dark orange']))
    
    def test_part_two(self):
        contraintTree = parseBagConstraintsTree(sampleRules)
        self.assertEqual(contraintTree['shiny gold'].canHold, [(1, 'dark olive'), (2, 'vibrant plum')])

        requiredChilds = requiredChildBags(contraintTree, 'shiny gold')
        self.assertEqual(len(requiredChilds), 32)

unittest.main(argv=[''], verbosity=2, exit=False)

print("\n------\n")
with open("puzzle_inputs/day7.txt", "r") as f:
    input = f.readlines()
    contraintTree = parseBagConstraintsTree(input)
    print('Part 1:', len(compatibleHostBags(contraintTree, 'shiny gold')))
    print('Part 2:', len(requiredChildBags(contraintTree, 'shiny gold')))
