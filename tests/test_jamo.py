"""Unit tests for functional tests on Hangul <-> jamo toolkit.
"""
import random
import unittest
from jamo import jamo
import sys
import io

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
    """Test Hangul syllable decomposition into jamo and
    transformations into Hangul Compatibility jamo.
    """
    def test_jamo_to_hangul(self):
        """Functional test for jamo_to_hangul using hardcoded test cases."""
        test_cases = [(0x110c, 0x1161, 0),
                      (0x1106, 0x1169, 0),
                      (0x1112, 0x1161, 0x11ab),
                      (0x1100, 0x1173, 0x11af),
                      (0x1109, 0x1165, 0),
                      (0x110b, 0x116e, 0x11af),
                      (0x1111, 0x1167, 0x11bc),
                      (0x110b, 0x1163, 0x11bc)]
        desired_hangul = ["자",
                          "모",
                          "한",
                          "글",
                          "서",
                          "울",
                          "평",
                          "양"]
        for hangul, (lead, vowel, tail) in zip(desired_hangul, test_cases):
            trial = jamo.jamo_to_hangul(lead, vowel, tail)
            assert hangul == trial,\
                ("Incorrect conversion from"
                 "({lead}, {vowel}, {tail}) to "
                 "{hangul}). "
                 "Got {failure}.").format(lead=lead,
                                          vowel=vowel,
                                          tail=tail,
                                          hangul=hangul,
                                          failure=trial)

    def test_hangul_to_jamo(self):
        """Functional test for hangul_to_jamo using hardcoded test cases."""
        test_cases = ["자",
                      "모",
                      "한",
                      "글",
                      "서",
                      "울",
                      "평",
                      "양"]
        desired_jamo = [(chr(0x110c), chr(0x1161), chr(0)),
                        (chr(0x1106), chr(0x1169), chr(0)),
                        (chr(0x1112), chr(0x1161), chr(0x11ab)),
                        (chr(0x1100), chr(0x1173), chr(0x11af)),
                        (chr(0x1109), chr(0x1165), chr(0)),
                        (chr(0x110b), chr(0x116e), chr(0x11af)),
                        (chr(0x1111), chr(0x1167), chr(0x11bc)),
                        (chr(0x110b), chr(0x1163), chr(0x11bc))]
        for hangul, target in zip(test_cases, desired_jamo):
            assert target == jamo.hangul_to_jamo(hangul),\
                ("Incorrect conversion from "
                 "{hangul} to "
                 "({lead}, {vowel}, {tail}). "
                 "Got {failure}.").format(hangul=hangul,
                                          lead=hex(target[0]),
                                          vowel=hex(target[1]),
                                          tail=hex(target[2]),
                                          failure=jamo.hangul_to_jamo(hangul))

    def test_get_jamo_class(self):
        """Functional test for determining the class of jamo. Tests all
        possible jamo in modern Hangul.
        """
        # All valid leads in modern Hangul.
        test_leads = "ᄀᄁᄂᄃᄄᄅᄆᄇᄈᄉᄊᄋᄌᄍᄎᄏᄐᄑᄒ"
        # All valid vowels in modern Hangul.
        test_vowels = "ᅡᅢᅣᅤᅥᅦᅧᅨᅩᅪᅫᅬᅭᅮᅯᅰᅱᅲᅳᅴᅵ"
        # All valid tails in modern Hangul.
        test_tails = "ᆨᆩᆪᆫᆬᆭᆮᆯᆰᆱᆲᆳᆴᆵᆶᆷᆸᆹᆺᆻᆼᆽᆾᆿᇀᇁᇂ"
        for lead in test_leads:
            jamo_type = jamo.get_jamo_class(lead)
            assert "lead" == jamo_type,\
                ("Thought {lead} "
                 "was a {jamo_type}").format(lead=hex(ord(lead)),
                                             jamo_type=jamo_type)
        for vowel in test_vowels:
            jamo_type = jamo.get_jamo_class(vowel)
            assert "vowel" == jamo_type,\
                ("Thought {vowel} "
                 "was a {jamo_type}").format(vowel=hex(ord(vowel)),
                                             jamo_type=jamo_type)
        for tail in test_tails:
            jamo_type = jamo.get_jamo_class(tail)
            assert "tail" == jamo_type,\
                ("Thought {tail} "
                 "was a {jamo_type}").format(tail=hex(ord(tail)),
                                             jamo_type=jamo_type)
        _stderr = jamo.stderr
        jamo.stderr = io.StringIO()
        for invalid in range(10):
            try:
                jamo.get_jamo_class(invalid)
                assert False, "Did not catch invalid jamo."
            except jamo.InvalidJamoError:
                pass
        jamo.stderr = _stderr

    def test_jamo_to_hcj(self):
        """Functional test verifying correctness of jamo to HCJ translation."""
        # All valid leads in modern Hangul.
        test_leads = "ᄀᄁᄂᄃᄄᄅᄆᄇᄈᄉᄊᄋᄌᄍᄎᄏᄐᄑᄒ"
        hcj_leads = "ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ"
        # All valid vowels in modern Hangul.
        test_vowels = "ᅡᅢᅣᅤᅥᅦᅧᅨᅩᅪᅫᅬᅭᅮᅯᅰᅱᅲᅳᅴᅵ"
        hcj_vowels = "ㅏㅐㅑㅒㅓㅔㅓㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ"
        # All valid tails in modern Hangul.
        test_tails = "ᆨᆩᆪᆫᆬᆭᆮᆯᆰᆱᆲᆳᆴᆵᆶᆷᆸᆹᆺᆻᆼᆽᆾᆿᇀᇁᇂ"
        hcj_tails = "ㄱㄲㄳㄴㄵㄶㄷㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅄㅅㅆㅇㅈㅊㅋㅌㅍㅎ"
        for lead, target in zip(test_leads, hcj_leads):
            hcj_lead = jamo.jamo_to_hcj(lead)
            assert target == hcj_lead,\
                ("Matched {lead} "
                 "to {hcj_lead}, "
                 "wanted {target}").format(lead=hex(ord(lead)),
                                           hcj_lead=hcj_lead,
                                           target=target)
        for vowel, target in zip(test_vowels, hcj_vowels):
            hcj_vowel = jamo.jamo_to_hcj(vowel)
            assert target == hcj_vowel,\
                ("Matched {vowel} "
                 "to {hcj_vowel}").format(vowel=hex(ord(vowel)),
                                          hcj_vowel=hcj_vowel)
        for tail, target in zip(test_tails, hcj_tails):
            hcj_tail = jamo.jamo_to_hcj(tail)
            assert target == hcj_tail,\
                ("Matched {tail} "
                 "to {hcj_tail}").format(tail=hex(ord(tail)),
                                         hcj_tail=hcj_tail)
        _stderr = jamo.stderr
        jamo.stderr = io.StringIO()
        for invalid in range(10):
            try:
                jamo.get_jamo_class(invalid)
                assert False, "Did not catch invalid jamo."
            except jamo.InvalidJamoError:
                pass
        jamo.stderr = _stderr

if __name__ == "__main__":
    unittest.main()
