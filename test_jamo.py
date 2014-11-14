"""Unit tests for Hangul -> Jamo toolkit.
"""
import random
import unittest
import jamo

def get_random_hangul(count=20*22*27):
    """Generate a sequence of random, unique, valid Hangul characters.
    Returns all syllables by default.
    NOTE: Relies on jamo.jamo_to_hangul; ensure the function is tested before
    this is called."""
    syllables = [jamo.jamo_to_hangul(lead, vowel, tail)\
                 for lead in range(1, 20)\
                 for vowel in range(1, 22)\
                 for tail in range(1, 27)]
    return random.sample(syllables, count)

class TestJamo(unittest.TestCase):
    """Test Hangul syllable decomposition into Jamo and
    transformations into Hangul Compatibility Jamo.
    """
    def test_jamo_to_hangul(self):
        """Functional test for jamo_to_hangul using hardcoded test cases."""
        test_cases = [(13, 1, 0),
                      (7, 9, 0),
                      (19, 1, 4),
                      (1, 19, 8),
                      (10, 5, 0),
                      (12, 14, 8),
                      (18, 7, 21),
                      (12, 3, 21)]
        desired_hangul = ["자",
                          "모",
                          "한",
                          "글",
                          "서",
                          "울",
                          "평",
                          "양"]
        for hangul, (lead, vowel, tail) in zip(desired_hangul, test_cases):
            assert hangul == jamo.jamo_to_hangul(lead, vowel, tail),\
                ("Incorrect conversion from"
                 "({lead}, {vowel}, {tail}) to"
                 "{hangul})").format(lead=lead,
                                     vowel=vowel,
                                     tail=tail,
                                     hangul=hangul)

if __name__ == "__main__":
    unittest.main()
