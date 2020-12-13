# Day 6 : Custom Customs
#
# Input : a list of group answer to questions for which people answered yes
# Goal : count the sum of number of question for whom anyone answered yes

import unittest
import re
from typing import List
from collections import Counter

def countQuestionAnswered(answers: str) -> int:
    usedLetters = set(answers)
    if '\n' in usedLetters: usedLetters.remove('\n')
    return len(usedLetters)

def sumQuestionAnsweredInGroups(groupAnswers: str) -> int:
    splittedGroups = re.split(r'\n\n', groupAnswers)
    return sum([countQuestionAnswered(a) for a in splittedGroups])



def countQuestionEveryoneAnswered(answers: str) -> int:
    groupSize = len(answers.strip().split('\n'))
    lettersCount = Counter(answers)
    del lettersCount['\n']
    return len([ l for l in lettersCount if lettersCount[l] == groupSize])

def sumQuestionEveryoneAnsweredInGroups(groupAnswers: str) -> int:
    splittedGroups = re.split(r'\n\n', groupAnswers)
    return sum([countQuestionEveryoneAnswered(a) for a in splittedGroups])

sampleAnswers = """
abcx
abcy
abcz
"""

sampleGroupAnswers = """
abc

ab
"""

class SamplesTests(unittest.TestCase):

    def test_part_one(self):
      self.assertEqual(countQuestionAnswered(sampleAnswers), 6)
      self.assertEqual(countQuestionAnswered(sampleGroupAnswers), 3)

      self.assertEqual(sumQuestionAnsweredInGroups(sampleGroupAnswers), 5)

    def test_part_two(self):
        self.assertEqual(countQuestionEveryoneAnswered(sampleAnswers), 3)

        self.assertEqual(sumQuestionEveryoneAnsweredInGroups(sampleGroupAnswers), 5)

unittest.main(argv=[''], verbosity=2, exit=False)

print("\n------\n")

with open("puzzle_inputs/day6.txt", "r") as f:
    input = f.read()
    print('Part 1:', sumQuestionAnsweredInGroups(input))
    print('Part 2:', sumQuestionEveryoneAnsweredInGroups(input))
