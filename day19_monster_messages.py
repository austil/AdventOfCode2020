# Day 19 : Monster Messages
#
# Input : rules and messages
# Part 1 : find how many messages match the first rule

import unittest
import re

def handleSelfReferringRules(n, parts, index):
    guardIndex = parts.index('|')
    [left, right] = [parts[:guardIndex], parts[guardIndex + 1:]]

    sideWithSelfRef = left if n in left else right
    otherSide = left if n not in left else right
    selfRefIsNested = 0 < sideWithSelfRef.index(n) < len(sideWithSelfRef) - 1

    if ''.join(left).replace(n, '') != ''.join(right).replace(n, '') or len(sideWithSelfRef) > 3:
        raise Exception(f'I cannot handle {n}: {parts}')

    def get1(p = otherSide):
        expanded = ''.join([index[r]() for r in p])
        return '(' + expanded + ')+'

    def get2(p = otherSide):
        # Hardcode some possibilities and hope it's enough (hack found of AoC subreddit)
        a = index[p[0]]()
        b = index[p[1]]()
        expanded = '|'.join(f'{a}{{{n}}}{b}{{{n}}}' for n in range(1, 10))
        return '(' + expanded + ')'

    return get2 if selfRefIsNested else get1

def parseRules(rules):
    index = {}
    for rule in rules:
        [n, body] = rule.split(': ')
        characterMatch = re.match(r'"\w"', body)

        if characterMatch:
            character = characterMatch.group().replace('"', '')
            def get(c = character):
                return c
        else:
            parts = body.split(' ')
            if n in parts:
                get = handleSelfReferringRules(n, parts, index)
            else:
                def get(p = parts):
                    expanded = ''.join([index[r]() if r.isdigit() else r for r in p])
                    return '(' + expanded + ')'

        index[n] = get

    return index

def rulesToRegex(rules):
    rulesIndex = parseRules(rules)
    return '^' + rulesIndex['0']() + '$'

def countValid(rule, messages):
    return sum([ 1 if re.match(rule, m) else 0 for m in messages])

sampleInput = """
0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb
""".strip()

[sampleRules, sampleMessages] = [ s.splitlines() for s in re.split(r'\n\n', sampleInput) ]

class SamplesTests(unittest.TestCase):

    def test_part_one(self):
        self.assertEqual(len(parseRules(sampleRules)), 6)
        self.assertEqual(rulesToRegex(sampleRules), '^(a((aa|bb)(ab|ba)|(ab|ba)(aa|bb))b)$')
        self.assertEqual(countValid(rulesToRegex(sampleRules), sampleMessages), 2)
    
    def test_part_two(self):
        sampleRulesWithLoop = [
            '0: 8',
            '8: 42 | 42 8',
            '11: 42 31 | 42 11 31', # Can Python regex match this type of patterns => Nope
            '42: "a"',
            '31: "b"',
        ]

        # print(rulesToRegex(sampleRulesWithLoop))

        with open("puzzle_inputs/day19_part2_test.txt", "r") as f:
            input = f.read().strip()
            [rules, messages] = [ s.splitlines() for s in re.split(r'\n\n', input) ]
            # print(rulesToRegex(rules))
            self.assertEqual(countValid(rulesToRegex(rules), messages), 12)

unittest.main(argv=[''], verbosity=2, exit=False)

print("\n------\n")

with open("puzzle_inputs/day19.txt", "r") as f:
    input = f.read().strip()
    [rules, messages] = [ s.splitlines() for s in re.split(r'\n\n', input) ]
    p1 = countValid(rulesToRegex(rules), messages)
    print('Part 1:', p1, '/', len(messages))
    assert p1 == 149

with open("puzzle_inputs/day19_part2.txt", "r") as f:
    input = f.read().strip()
    [rules, messages] = [ s.splitlines() for s in re.split(r'\n\n', input) ]
    p2 = countValid(rulesToRegex(rules), messages)
    print('Part 2:', p2, '/', len(messages))
