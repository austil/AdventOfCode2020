# Day 4: Passport Processing
#
# Input : passport data batch
# Part 1: count valid passport (according to our own rules :p)

import unittest
import re
from typing import List

def validateHeight(v):
    m = re.match(r'(\d+)(in|cm)', v)
    if m is None: return False

    (size, unit) = m.group(1, 2)
    if unit == 'in' and (59 <= int(size) <= 76): return True
    elif unit == 'cm' and (150 <= int(size) <= 193): return True
    else: return False

requiredFields = {
    'byr': lambda v: 1920 <= int(v) <= 2002, # (Birth Year)
    'iyr': lambda v: 2010 <= int(v) <= 2020, # (Issue Year)
    'eyr': lambda v: 2020 <= int(v) <= 2030, # (Expiration Year)
    'hcl': lambda v: re.match(r'^#\w{6}$', v), # (Hair Color)
    'ecl': lambda v: v in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'], # (Eye Color)
    'pid': lambda v: re.match(r'^\d{9}$', v), # (Passport ID)
    'hgt': validateHeight,
}

def parsePassports(passportsStr):
    splittedEntries = re.split(r'\n\n', passportsStr)

    parseFieldTuples = lambda e : [
        tuple(f.split(':')) 
        for f in re.split(r'(\w+:\S+)', e) 
        if f not in ['', ' ', '\n']
    ]

    return [dict(parseFieldTuples(e)) for e in splittedEntries]

def passportIsValid(passport, checkValues):
    return all([
        rf in passport and (not checkValues or requiredFields[rf](passport[rf])) 
        for rf in requiredFields
    ])

def countValidPassports(passports, checkValues = False):
    return sum([passportIsValid(p, checkValues) for p in passports])

samplePassportsStr = """
ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in
"""

class SamplesTests(unittest.TestCase):

    def test_part_one(self):
        samplePassports = parsePassports(samplePassportsStr)

        self.assertEqual(len(samplePassports), 4)
        self.assertEqual(samplePassports[0]['cid'], '147')
        self.assertFalse('cid' in samplePassports[2])

        self.assertEqual(countValidPassports(samplePassports), 2)
    
    def test_part_two(self):
        with open("puzzle_inputs/day4_part2_test.txt", "r") as f:
            samplePassports = parsePassports(f.read())
            self.assertEqual(countValidPassports(samplePassports, checkValues=True), 4)

unittest.main(argv=[''], verbosity=2, exit=False)

print("\n------\n")

with open("puzzle_inputs/day4.txt", "r") as f:
    input = parsePassports(f.read())
    print("Part 1 :", countValidPassports(input))
    print("Part 2 :", countValidPassports(input, checkValues=True))
