# Day 2 : password philosophy
# 
# Input : a list of password and their policy
# Part 1 : find how many password are valid

import unittest
import re
from collections import Counter, namedtuple
from typing import List, Callable

Password = namedtuple("Password", "policy_min, policy_max, policy_letter, value")

def parsePassword(line: str) -> Password:
    pattern = '(\d+)-(\d+) (\w): (\w+)'
    matches = re.match(pattern, line)
    (policy_min, policy_max, policy_letter, value) = matches.group(1, 2, 3, 4)
    return Password(int(policy_min), int(policy_max), policy_letter, value)

def passwordIsValid_deprecated(p: Password) -> bool:
    lettersCount = Counter(p.value)
    return p.policy_min <= lettersCount[p.policy_letter] <= p.policy_max

def passwordIsValid(p: Password) -> bool:
    firstPositionOk = p.value[p.policy_min - 1] == p.policy_letter
    secondPositionOk = p.value[p.policy_max - 1] == p.policy_letter
    return bool(firstPositionOk) != bool(secondPositionOk)

def countValidPasswords(passwords: List[str], validator: Callable[[str], bool]) -> int:
    return sum(validator(parsePassword(p)) for p in passwords)

samplePasswords = [
    "1-3 a: abcde",
    "1-3 b: cdefg",
    "2-9 c: ccccccccc",
]

class SamplesTests(unittest.TestCase):

    def test_part_one(self):
        self.assertEqual(countValidPasswords(samplePasswords, passwordIsValid_deprecated), 2)
    
    def test_part_two(self):
        self.assertEqual(countValidPasswords(samplePasswords, passwordIsValid), 1)

unittest.main(argv=[''], verbosity=2, exit=False)

print("\n------\n")

with open("puzzle_inputs/day2.txt", "r") as f:
    input = f.readlines()
    print("Part 1 :", countValidPasswords(input, passwordIsValid_deprecated))
    print("Part 2 :", countValidPasswords(input, passwordIsValid))
