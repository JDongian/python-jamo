# -*- coding: utf-8 -*-
"""Unit tests for functional tests on Hangul <-> jamo toolkit.
"""
import unittest
# ModuleNotFound Error
# import jamo
import random
import itertools
import io

# +++ TEMPORARY WORKAROUND TO IMPORT JAMO +++
import os
import sys
# set current working directory to location of test_jamo.py to make
# relative directory ("..") consistent regardless of where the file is
# launched from
original_cwd = os.getcwd()
os.chdir(sys.path[0])
sys.path.append(os.path.abspath(os.path.join("..")))
os.chdir(original_cwd)
import jamo
# +++ END WORKAROUND TO IMPORT JAMO +++

# See http://www.unicode.org/charts/PDF/U1100.pdf
_JAMO_LEADS_MODERN = [chr(_) for _ in range(0x1100, 0x1113)]
_JAMO_VOWELS_MODERN = [chr(_) for _ in range(0x1161, 0x1176)]
_JAMO_TAILS_MODERN = [chr(_) for _ in range(0x11a8, 0x11c3)]

# Corresponding HCJ for all valid leads in modern Hangul.
_HCJ_LEADS_MODERN = [_ for _ in "ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ"]
# Corresponding HCJ for all valid vowels in modern Hangul.
# "ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ"
# See http://www.unicode.org/charts/PDF/U3130.pdf
_HCJ_VOWELS_MODERN = [chr(_) for _ in range(0x314f, 0x3164)]
# Corresponding HCJ for all valid tails in modern Hangul.
_HCJ_TAILS_MODERN = "ㄱㄲㄳㄴㄵㄶㄷㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅄㅅㅆㅇㅈㅊㅋㅌㅍㅎ"


def _get_random_hangul(count=(0xd7a4 - 0xac00)):
    """Generate a sequence of random, unique, valid Hangul characters.
    Returns all possible modern Hangul characters by default.
    """
    valid_hangul = [chr(_) for _ in range(0xac00, 0xd7a4)]
    return random.sample(valid_hangul, count)


class TestJamo(unittest.TestCase):
    def test_is_jamo(self):
        """is_jamo tests
        Test if a single character is a jamo character.
        Valid jamo includes all modern and archaic jamo, as well as all HCJ.
        Non-assigned code points are invalid.
        """

        # See http://www.unicode.org/charts/PDF/U1100.pdf
        valid_jamo = (chr(_) for _ in range(0x1100, 0x1200))
        # See http://www.unicode.org/charts/PDF/U3130.pdf
        valid_hcj = itertools.chain((chr(_) for _ in range(0x3131, 0x3164)),
                                    (chr(_) for _ in range(0x3165, 0x318f)))
        # See http://www.unicode.org/charts/PDF/UA960.pdf
        valid_extA = (chr(_) for _ in range(0xa960, 0xa97d))
        # See http://www.unicode.org/charts/PDF/UD7B0.pdf
        valid_extB = itertools.chain((chr(_) for _ in range(0xd7b0, 0xd7c7)),
                                     (chr(_) for _ in range(0xd7cb, 0xd7fc)))

        invalid_edge_cases = (chr(0x10ff), chr(0x1200),
                              chr(0x3130), chr(0x3164), chr(0x318f),
                              chr(0xa95f), chr(0xa07d),
                              chr(0xd7af), chr(0xd7c7),
                              chr(0xd7ca), chr(0xd7fc))
        invalid_hangul = _get_random_hangul(20)
        invalid_other = "abABzyZY ,.:;~`―—–/!@#$%^&*()[]{}"

        # Positive tests
        for _ in itertools.chain(valid_jamo, valid_hcj,
                                 valid_extA, valid_extB):
            assert jamo.is_jamo(_),\
                ("Incorrectly decided U+{} "
                 "was not jamo.").format(hex(ord(_))[2:])
        # Negative tests
        for _ in itertools.chain(invalid_edge_cases,
                                 invalid_hangul,
                                 invalid_other):
            assert not jamo.is_jamo(_),\
                ("Incorrectly decided U+{} "
                 "was jamo.").format(hex(ord(_))[2:])

    def test_is_jamo_modern(self):
        """is_jamo_modern tests
        Test if a single character is a modern jamo character.
        Modern jamo includes all U+11xx jamo in addition to HCJ in usage.
        """

        modern_jamo = itertools.chain(_JAMO_LEADS_MODERN,
                                      _JAMO_VOWELS_MODERN,
                                      _JAMO_TAILS_MODERN)
        modern_hcj = itertools.chain(_HCJ_LEADS_MODERN,
                                     _HCJ_VOWELS_MODERN,
                                     _HCJ_TAILS_MODERN)

        invalid_edge_cases = (chr(0x10ff), chr(0x1113),
                              chr(0x1160), chr(0x1176),
                              chr(0x11a7), chr(0x11c3))
        invalid_hangul = _get_random_hangul(20)
        invalid_other = "abABzyZY ,.:;~`―—–/!@#$%^&*()[]{}ᄓ"

        # Positive tests
        for _ in itertools.chain(modern_jamo, modern_hcj):
            assert jamo.is_jamo_modern(_),\
                ("Incorrectly decided U+{} "
                 "was not modern jamo.").format(hex(ord(_))[2:])
        # Negative tests
        for _ in itertools.chain(invalid_edge_cases,
                                 invalid_hangul,
                                 invalid_other):
            assert not jamo.is_jamo_modern(_),\
                ("Incorrectly decided U+{} "
                 "was modern jamo.").format(hex(ord(_))[2:])

    def test_is_hcj(self):
        """is_hcj tests
        Test if a single character is a HCJ character.
        HCJ is defined as the U+313x to U+318x block, sans two non-assigned
        code points.
        """

        # Note: The chaeum filler U+3164 is not considered HCJ, but a special
        # character as defined in http://www.unicode.org/charts/PDF/U3130.pdf.
        valid_hcj = itertools.chain((chr(_) for _ in range(0x3131, 0x3164)),
                                    (chr(_) for _ in range(0x3165, 0x318f)))

        invalid_edge_cases = (chr(0x3130), chr(0x3164), chr(0x318f))
        invalid_hangul = _get_random_hangul(20)
        invalid_other = "abABzyZY ,.:;~`―—–/!@#$%^&*()[]{}ᄀᄓᅡᅶᆨᇃᇿ"

        # Positive tests
        for _ in valid_hcj:
            assert jamo.is_hcj(_),\
                ("Incorrectly decided U+{} "
                 "was not hcj.").format(hex(ord(_))[2:])
        # Negative tests
        for _ in itertools.chain(invalid_edge_cases,
                                 invalid_hangul,
                                 invalid_other):
            assert not jamo.is_hcj(_),\
                ("Incorrectly decided U+{} "
                 "was hcj.").format(hex(ord(_))[2:])

    def test_is_hcj_modern(self):
        """is_hcj_modern tests
        Test if a single character is a modern HCJ character.
        Modern HCJ is defined as HCJ that corresponds to a U+11xx jamo
        character in modern usage.
        """

        # Note: The chaeum filler U+3164 is not considered HCJ, but a special
        # character as defined in http://www.unicode.org/charts/PDF/U3130.pdf.
        valid_hcj_modern = (chr(_) for _ in range(0x3131, 0x3164))

        invalid_edge_cases = (chr(0x3130), chr(0x3164))
        invalid_hangul = _get_random_hangul(20)
        invalid_other = "abABzyZY ,.:;~`―—–/!@#$%^&*()[]{}ᄀᄓᅡᅶᆨᇃᇿㆎㅥ"

        # Positive tests
        for _ in valid_hcj_modern:
            assert jamo.is_hcj_modern(_),\
                ("Incorrectly decided U+{} "
                 "was not modern hcj.").format(hex(ord(_))[2:])
        # Negative tests
        for _ in itertools.chain(invalid_edge_cases,
                                 invalid_hangul,
                                 invalid_other):
            assert not jamo.is_hcj_modern(_),\
                ("Incorrectly decided U+{} "
                 "was modern hcj.").format(hex(ord(_))[2:])

    def test_is_hangul_char(self):
        """is_hangul_char tests
        Test if a single character is in the U+AC00 to U+D7A3 code block,
        excluding unassigned codes.
        """

        harcoded_tests = "가나다한글한극어힣"

        invalid_edge_cases = (chr(0xabff), chr(0xd7a4))
        invalid_other = "ㄱㄴㅓabABzyZY ,.:;~`―—–/!@#$%^&*()[]{}ᄀᄓᅡᅶᆨᇃᇿㆎㅥ"

        for _ in itertools.chain(harcoded_tests, _get_random_hangul(1024)):
            assert jamo.is_hangul_char(_),\
                ("Incorrectly decided U+{} "
                 "was not a hangul character.").format(hex(ord(_))[2:])
        for _ in itertools.chain(invalid_edge_cases, invalid_other):
            assert not jamo.is_hangul_char(_),\
                ("Incorrectly decided U+{} "
                 "was a hangul character.").format(hex(ord(_))[2:])

    def test_get_jamo_class(self):
        """get_jamo_class tests
        Valid arguments are U+11xx characters (not HCJ). An InvalidJamoError
        exception is thrown if invalid input is used.

        get_jamo_class should return the class ["lead" | "vowel" | "tail"] of
        a given character.

        Note: strict adherence to Unicode 7.0
        """

        # Note: Fillers are considered initial consonants according to
        # www.unicode.org/charts/PDF/U1100.pdf
        leads = (chr(_) for _ in range(0x1100, 0x1160))
        lead_targets = ("lead" for _ in range(0x1100, 0x1161))
        vowels = (chr(_) for _ in range(0x1160, 0x11a8))
        vowel_targets = ("vowel" for _ in range(0x1160, 0x11a8))
        tails = (chr(_) for _ in range(0x11a8, 0x1200))
        tail_targets = ("tail" for _ in range(0x11a8, 0x1200))

        invalid_cases = [chr(0x10ff), chr(0x1200), 'a', '~']
        invalid_other_cases = ['', "ᄂᄃ"]

        all_tests = itertools.chain(zip(leads, lead_targets),
                                    zip(vowels, vowel_targets),
                                    zip(tails, tail_targets))

        # Test characters
        for test, target in all_tests:
            try:
                trial = jamo.get_jamo_class(test)
            except jamo.InvalidJamoError:
                assert False,\
                    ("Thought U+{code} "
                     "was invalid input.").format(code=hex(ord(test))[2:])
            assert trial == target,\
                ("Incorrectly decided {test} "
                 "was a {trial}. "
                 "(it's a {target})").format(test=hex(ord(test)),
                                             trial=trial,
                                             target=target)

        # Negative tests
        _stderr = jamo.jamo.stderr
        jamo.jamo.stderr = io.StringIO()
        for _ in invalid_cases:
            try:
                jamo.get_jamo_class(_)
                assert False, "Did not catch invalid jamo."
            except jamo.InvalidJamoError:
                pass
        for _ in invalid_other_cases:
            try:
                jamo.get_jamo_class(_)
                assert False, "Accepted bad input without throwing exception."
            except (AssertionError, TypeError):
                pass
        jamo.jamo.stderr = _stderr

    def test_jamo_to_hcj(self):
        """jamo_to_hcj tests
        Arguments may be iterables or single characters.

        jamo_to_hcj should convert every U+11xx jamo character into U+31xx HCJ
        in a given input. Anything else is unchanged.
        """

        test_chars = itertools.chain(_JAMO_LEADS_MODERN,
                                     _JAMO_VOWELS_MODERN,
                                     _JAMO_TAILS_MODERN)
        target_chars = itertools.chain(_HCJ_LEADS_MODERN,
                                       _HCJ_VOWELS_MODERN,
                                       _HCJ_TAILS_MODERN)
        # TODO: Complete archaic jamo coverage
        test_archaic = ["ᄀᄁᄂᄃᇹᇫ"]
        target_archaic = ["ㄱㄲㄴㄷㆆㅿ"]
        test_strings_idempotent = ["", "aAzZ ,.:;~`―—–/!@#$%^&*()[]{}",
                                   "汉语 / 漢語; Hànyǔ or 中文; Zhōngwén",
                                   "ㄱㆎ"]
        target_strings_idempotent = test_strings_idempotent
        # TODO: Add more tests for unmapped jamo characters.
        test_strings_unmapped = ["ᅶᅷᅸᅹᅺᅻᅼᅽᅾᅿᆆ",
                                 ""]
        target_strings_unmapped = test_strings_unmapped

        all_tests = itertools.chain(zip(test_chars, target_chars),
                                    zip(test_archaic, target_archaic),
                                    zip(test_strings_idempotent,
                                        target_strings_idempotent),
                                    zip(test_strings_unmapped,
                                        target_strings_unmapped))

        for test, target in all_tests:
            trial = jamo.jamo_to_hcj(test)
            assert trial.__name__ == "<genexpr>",\
                "jamo_to_hcj didn't return an instance of a generator."
            trial, target = ''.join(trial), ''.join(target)
            assert trial == target,\
                ("Matched {test} to {trial}, but "
                 "expected {target}.").format(test=''.join(test),
                                              trial=trial,
                                              target=target)

    def test_j2hcj(self):
        """j2hcj tests
        Arguments may be iterables or single characters.

        j2hcj should convert every U+11xx jamo character into U+31xx HCJ in a
        given input. Anything else is unchanged.
        """

        test_strings = ["", "test123", "ᄀᄁᄂᄃᇹᇫ"]
        target_strings = ["", "test123", "ㄱㄲㄴㄷㆆㅿ"]

        all_tests = itertools.chain(zip(test_strings, target_strings))

        for test, target in all_tests:
            trial = jamo.j2hcj(test)
            assert trial == target,\
                ("Matched {test} to {trial}, but "
                 "expected {target}.").format(test=''.join(test),
                                              trial=trial,
                                              target=target)

    def test_hcj_to_jamo(self):
        """hcj_to_jamo tests
        Arguments may be single characters along with the desired jamo class
        (lead, vowel, tail).
        """
        test_args = [("ㄱ", "lead"), ("ㄱ", "tail"),
                     ("ㅎ", "lead"), ("ㅎ", "tail"),
                     ("ㅹ", "lead"), ("ㅥ", "tail"),
                     ("ㅏ", "vowel"), ("ㅣ", "vowel")]
        targets = [chr(0x1100), chr(0x11a8),
                   chr(0x1112), chr(0x11c2),
                   chr(0x112c), chr(0x11ff),
                   chr(0x1161), chr(0x1175)]

        all_tests = itertools.chain(zip(test_args, targets))

        for (jamo_class, jamo_char), target in all_tests:
            trial = jamo.hcj_to_jamo(jamo_class, jamo_char)
            assert trial == target,\
                ("Converted {jamo_char} as {jamo_class} to {trial}, but "
                 "expected {target}.").format(jamo_char=hex(ord(jamo_char)),
                                              jamo_class=jamo_class,
                                              trial=hex(ord(trial)),
                                              target=hex(ord(target)))

    def test_hcj2j(self):
        """hcj2j tests
        Arguments may be single characters along with the desired jamo class
        (lead, vowel, tail).
        """
        test_args = [("ㄱ", "lead"), ("ㄱ", "tail"),
                     ("ㅎ", "lead"), ("ㅎ", "tail"),
                     ("ㅹ", "lead"), ("ㅥ", "tail"),
                     ("ㅏ", "vowel"), ("ㅣ", "vowel")]
        targets = [chr(0x1100), chr(0x11a8),
                   chr(0x1112), chr(0x11c2),
                   chr(0x112c), chr(0x11ff),
                   chr(0x1161), chr(0x1175)]

        all_tests = itertools.chain(zip(test_args, targets))

        for args, target in all_tests:
            jamo_class, jamo_char = args
            trial = jamo.hcj2j(jamo_class, jamo_char)
            assert trial == target,\
                ("Converted {jamo_char} as {jamo_class} to {trial}, but "
                 "expected {target}.").format(jamo_char=hex(ord(jamo_char)),
                                              jamo_class=jamo_class,
                                              trial=hex(ord(trial)),
                                              target=hex(ord(target)))

    def test_hangul_to_jamo(self):
        """hangul_to_jamo tests
        Arguments may be iterables or characters.

        hangul_to_jamo should split every Hangul character into U+11xx jamo
        for any given string. Anything else is unchanged.
        """

        test_cases = ["자",
                      "모",
                      "한",
                      "글",
                      "서",
                      "울",
                      "평",
                      "양",
                      "한굴",
                      "Do you speak 한국어?",
                      "자모=字母"]
        desired_jamo = [(chr(0x110c), chr(0x1161)),
                        (chr(0x1106), chr(0x1169)),
                        (chr(0x1112), chr(0x1161), chr(0x11ab)),
                        (chr(0x1100), chr(0x1173), chr(0x11af)),
                        (chr(0x1109), chr(0x1165)),
                        (chr(0x110b), chr(0x116e), chr(0x11af)),
                        (chr(0x1111), chr(0x1167), chr(0x11bc)),
                        (chr(0x110b), chr(0x1163), chr(0x11bc)),
                        (chr(0x1112), chr(0x1161), chr(0x11ab),
                         chr(0x1100), chr(0x116e), chr(0x11af)),
                        tuple(_ for _ in "Do you speak ") +
                        (chr(0x1112), chr(0x1161), chr(0x11ab),
                         chr(0x1100), chr(0x116e), chr(0x11a8),
                         chr(0x110b), chr(0x1165)) + ('?',),
                        (chr(0x110c), chr(0x1161), chr(0x1106), chr(0x1169),
                         "=", "字", "母")]

        for hangul, target in zip(test_cases, desired_jamo):
            trial = jamo.hangul_to_jamo(hangul)
            assert trial.__name__ == "<genexpr>",\
                ("hangul_to_jamo didn't return"
                 "an instance of a generator.")
            trial = tuple(trial)
            assert target == trial,\
                ("Converted {hangul} to {failure}, but expected "
                 "({lead}, {vowel}, "
                 "{tail}).").format(hangul=hangul,
                                    lead=hex(ord(target[0])),
                                    vowel=hex(ord(target[1])),
                                    tail=hex(ord(target[2]))
                                    if len(target) == 3 else "",
                                    failure=tuple([hex(ord(_)) for _ in
                                                  trial]))\
                if len(hangul) == 1 else\
                ("Incorrectly converted {hangul} to "
                 "{failure}.".format(hangul=hangul,
                                     failure=[hex(ord(_)) for _ in trial]))

    def test_h2j(self):
        """h2j tests
        Arguments may be iterables or characters.

        h2j should split every Hangul character into U+11xx jamo for any given
        string. Anything else is unchanged.
        """
        tests = ["한굴", "자모=字母"]
        targets = ["한굴", "자모=字母"]
        tests_idempotent = ["", "test123~", "ㄱㄲㄴㄷㆆㅿ"]
        targets_idempotent = tests_idempotent

        all_tests = itertools.chain(zip(tests, targets),
                                    zip(tests_idempotent, targets_idempotent))

        for test, target in all_tests:
            trial = jamo.h2j(test)
            assert trial == target,\
                ("Converted {test} to {trial}, but "
                 "expected {target}.").format(test=test,
                                              trial=trial,
                                              target=target)

    def test_jamo_to_hangul(self):
        """jamo_to_hangul tests
        Arguments may be jamo characters including HCJ. Throws an
        InvalidJamoError if there is no corresponding Hangul character to the
        inputs.

        Outputs a single Hangul character.
        """

        # Support jamo -> Hangul conversion.
        chr_cases = ((chr(0x110c), chr(0x1161), chr(0)),
                     (chr(0x1106), chr(0x1169), chr(0)),
                     (chr(0x1112), chr(0x1161), chr(0x11ab)),
                     (chr(0x1100), chr(0x1173), chr(0x11af)),
                     (chr(0x1109), chr(0x1165), chr(0)),
                     (chr(0x110b), chr(0x116e), chr(0x11af)),
                     (chr(0x1111), chr(0x1167), chr(0x11bc)),
                     (chr(0x110b), chr(0x1163), chr(0x11bc)))
        # Support HCJ -> Hangul conversion.
        hcj_cases = (('ㅈ', 'ㅏ', ''),
                     ('ㅁ', 'ㅗ', ''),
                     ('ㅎ', 'ㅏ', 'ㄴ'),
                     ('ㄱ', 'ㅡ', 'ㄹ'),
                     ('ㅅ', 'ㅓ', ''),
                     ('ㅇ', 'ㅜ', 'ㄹ'),
                     ('ㅍ', 'ㅕ', 'ㅇ'),
                     ('ㅇ', 'ㅑ', 'ㅇ'))
        desired_hangul1 = ("자",
                           "모",
                           "한",
                           "글",
                           "서",
                           "울",
                           "평",
                           "양")
        # Test the arity 2 version.
        arity2_cases = (('ㅎ', 'ㅏ'),)
        desired_hangul2 = ("하",)
        # Support mixed jamo and hcj conversion.
        mixed_cases = (('ᄒ', 'ㅏ', 'ㄴ'),)
        desired_hangul3 = ("한",)

        invalid_cases = [('a', 'b', 'c'), ('a', 'b'),
                         ('ㄴ', 'ㄴ', 'ㄴ'), ('ㅏ', 'ㄴ')]

        all_tests = itertools.chain(zip(chr_cases, desired_hangul1),
                                    zip(hcj_cases, desired_hangul1),
                                    zip(arity2_cases, desired_hangul2),
                                    zip(mixed_cases, desired_hangul3))

        for args, hangul in all_tests:
            trial = jamo.jamo_to_hangul(*args)
            assert hangul == trial,\
                ("Conversion from hcj to Hangul failed. "
                 "Incorrect conversion from"
                 "({lead}, {vowel}, {tail}) to "
                 "({hangul}). "
                 "Got {failure}.").format(lead=lead,
                                          vowel=vowel,
                                          tail=tail,
                                          hangul=hangul,
                                          failure=trial)

        # Negative tests
        _stderr = jamo.jamo.stderr
        jamo.jamo.stderr = io.StringIO()
        for _ in invalid_cases:
            try:
                # print(_)
                jamo.jamo_to_hangul(*_)
                assert False, "Accepted bad input without throwing exception."
            except jamo.InvalidJamoError:
                pass
        jamo.jamo.stderr = _stderr

    def test_j2h(self):
        """j2h hardcoded tests.
        Arguments may be integers corresponding to the U+11xx codepoints, the
        actual U+11xx jamo characters, or HCJ.

        Outputs a one-character Hangul string.

        This function is defined solely for naming conisistency with
        jamo_to_hangul.
        """

        assert jamo.j2h('ㅎ', 'ㅏ', 'ㄴ') == "한",\
            "j2h doesn't work. Hint: it's the same as jamo_to_hangul."

        assert jamo.j2h('ㅎ', 'ㅏ') == "하",\
            "j2h doesn't work. Hint: it's the same as jamo_to_hangul."

    def test_decompose_jamo(self):
        """decompose_jamo tests
        Arguments should be compound jamo - double consonants, consonant
        clusters, or dipthongs.

        Should output a tuple of non-compound jamo for every compound
        jamo.
        """
        invalid_hangul = _get_random_hangul(20)
        invalid_other = "abABzyZY ,.:;~`―—–/!@#$%^&*()[]{}"

        # TODO: Expand tests to be more comprehensive, maybe use unicode names.
        test_chars = ["ㄸ", "ㅢ"]
        target_chars = [("ㄷ", "ㄷ"), ("ㅡ", "ㅣ")]

        test_chars_idempotent = list(itertools.chain(invalid_hangul,
                                     invalid_other))
        target_chars_idempotent = test_chars_idempotent

        # Invalid
        invalid_strings = ["ab", "ㄸㄲ"]

        # Not implemented
        not_implemented_archaics = ["ᇑ", "ᇲ", "ퟡ"]

        all_tests = itertools.chain(zip(test_chars, target_chars),
                                    zip(test_chars_idempotent,
                                        target_chars_idempotent))

        for test, target in all_tests:
            trial = jamo.decompose_jamo(test)
            assert not jamo.is_jamo_compound(trial),\
                "decompose_jamo returned a compound"
            # Test for strict version of decompose_jamo():
            # assert 2 <= len(trial) <= 3,\
            #     "decompose_jamo failed to return a tuple of 2-3 jamo " +\
            #     "and instead returned " + str(trial) + " for " + str(test)
            if trial != test:  # for lenient version ONLY
                for trial_char in trial:
                    assert jamo.is_jamo(trial_char),\
                        "decompose_jamo returned non-jamo character"
            trial, target = ''.join(trial), ''.join(target)
            assert trial == target,\
                ("Matched {test} to {trial}, but "
                 "expected {target}.").format(test=''.join(test),
                                              trial=trial,
                                              target=target)

        # Negative tests
        _stderr = jamo.jamo.stderr
        jamo.jamo.stderr = io.StringIO()
        for test_string in invalid_strings:
            try:
                jamo.decompose_jamo(test_string)
                assert False, "Accepted bad input without throwing exception."
            except (AssertionError, TypeError):
                pass
        for not_implemented_archaic in not_implemented_archaics:
            try:
                jamo.decompose_jamo(not_implemented_archaic)
                assert False, "Accepted archaic jamo without throwing " +\
                    "exception."
            except (AssertionError, NotImplementedError):
                pass
        jamo.jamo.stderr = _stderr

    def test_compose_jamo(self):
        """compose_jamo tests
        Arguments should be non-compound jamo that combine to form valid
        double consonants, consonant clusters, or dipthongs.

        Should output a compound jamo for every valid combination of
        components and raise InvalidJamoError in all other cases.
        """

        # TODO: Expand tests to be more comprehensive, maybe use unicode names
        test_chars = [("ㄷ", "ㄷ"), ("ᄃ", "ㄷ"), ("ᄃ", "ᄃ"), ("ㅡ", "ㅣ")]
        target_chars = ["ㄸ", "ㄸ", "ㄸ", "ㅢ"]

        # Invalid
        invalid_cases = [("ㄷ", "ㄷ", "ㄷ"), ("ㅡ", "ㄷ")]

        # Not implemented
        not_implemented_archaics = [("ㄹ", "ㅁ", "ㄱ"), ("ㄹ", "ㄹ")]

        all_tests = zip(test_chars, target_chars)
        for test, target in all_tests:
            trial = jamo.compose_jamo(*test)
            assert jamo.is_jamo(trial),\
                "compose_jamo returned non-jamo character"
            assert jamo.is_jamo_compound(trial),\
                "compose_jamo returned non-compound"
            trial, target = ''.join(trial), ''.join(target)
            assert trial == target,\
                ("Matched {test} to {trial}, but "
                 "expected {target}.").format(test=''.join(test),
                                              trial=trial,
                                              target=target)

        # Negative tests
        _stderr = jamo.jamo.stderr
        jamo.jamo.stderr = io.StringIO()
        for invalid_case in invalid_cases:
            try:
                jamo.compose_jamo(*invalid_case)
                assert False, "Accepted bad input without throwing exception."
            except (AssertionError, TypeError, jamo.InvalidJamoError):
                pass
        for not_implemented_archaic in not_implemented_archaics:
            try:
                jamo.compose_jamo(*not_implemented_archaic)
                assert False, "Accepted unimplemented archaic input without" +\
                              " throwing exception."
            except (AssertionError, TypeError, jamo.InvalidJamoError):
                pass
        jamo.jamo.stderr = _stderr

    def test_is_jamo_compound(self):
        """Returns True for modern or archaic jamo compounds and False
        for others, raising a TypeError if receiving more than one
        character as input.
        """
        valid_compounds = "ᄁᄄᄈᄊᄍᄓᄔᄕᄖᄗᄘᄙᄚᄛᄜᄝᄞᄟᄠᄡᄢᄣᄤᄥᄦᄧᄨ" +\
            "ᄩᄪᄫᄬᄭᄮᄯᄰᄱᄲᄳᄴᄵᄶᄷᄸᄹᄺᄻᄽᄿᅁᅂᅃᅄᅅᅆᅇᅈᅉᅊᅋᅍᅏᅑ" +\
            "ᅒᅓᅖᅗᅘᅙᅚᅛᅜᅝᅞᅪᅫᅬᅯᅰᅱᅴᅶᅷᅸᅹᅺᅻᅼᅽᅾᅿᆀᆁᆂᆃᆄᆅᆆ" +\
            "ᆇᆈᆉᆊᆋᆌᆍᆎᆏᆐᆑᆒᆓᆔᆕᆖᆗᆘᆙᆚᆛᆜᆝᆟᆠᆡᆢᆣᆤᆥᆦᆧᆩᆪᆬ" +\
            "ᆭᆰᆱᆲᆳᆴᆵᆶᆹᆻᇃᇄᇅᇆᇇᇈᇉᇊᇋᇌᇍᇎᇏᇐᇑᇒᇓᇔᇕᇖᇗᇘᇙᇚᇛ" +\
            "ᇜᇝᇞᇟᇠᇡᇢᇣᇤᇥᇦᇧᇨᇩᇪᇬᇭᇮᇯᇱᇲᇳᇴᇵᇶᇷᇸᇹᇺᇻᇼᇽᇾ" +\
            "ᇿㄲㄳㄵㄶㄸㄺㄻㄼㄽㄾㄿㅀㅃㅄㅆㅉㅘㅙㅚㅝㅞㅟㅢㅥㅦㅧㅨㅩㅪㅫㅬㅭㅮㅯ" +\
            "ㅰㅱㅲㅳㅴㅵㅶㅷㅸㅹㅺㅻㅼㅽㅾㆀㆂㆃㆄㆅㆆㆇㆈㆉㆊㆋㆌㆎꥠꥡꥢꥣ" +\
            "ꥤꥥꥦꥧꥨꥩꥪꥫꥬꥭꥮꥯꥰꥱꥲꥳꥴꥵꥶꥷꥸꥹꥺ" +\
            "ꥻꥼힰힱힲힳힴힵힶힷힸힹힺힻힼힽힾힿퟀퟁퟂퟃퟄ" +\
            "ퟅퟆퟋퟌퟍퟎퟏퟐퟑퟒퟓퟔퟕퟖퟗퟘퟙퟚퟛퟜퟝퟞퟟ" +\
            "ퟠퟡퟢퟣퟤퟥퟦퟧퟨퟩퟪퟫퟬퟭퟮퟯퟰퟱퟲퟳퟴퟵퟶ" +\
            "ퟷퟸퟹퟺퟻ"

        non_compound_jamo = "ᄀᄂᄃᄅᄆᄇᄉᄋᄌᄎᄏᄐᄑᄒᄼᄾᅀᅌᅎᅐᅔᅕ" +\
                            "ᅟᅠᅡᅢᅣᅤᅥᅦᅧᅨᅩᅭᅮᅲᅳᅵᆞᆨᆫᆮᆯᆷᆸ" +\
                            "ᆺᆼᆽᆾᆿᇀᇁᇂᇫᇰㄱㄴㄷㄹㅁ ㅂㅅㅇㅈㅊㅋㅌ" +\
                            "ㅍㅎㅏㅐㅑㅒㅓㅔㅕㅖㅗㅛㅜㅠㅡㅣㅿㆁㆍ"
        invalid_hangul = _get_random_hangul(20)
        invalid_other = "abABzyZY ,.:;~`―—–/!@#$%^&*()[]{}"

        # Positive tests
        for valid_compound in itertools.chain(valid_compounds):
            assert jamo.is_jamo_compound(valid_compound),\
                ("Incorrectly decided U+{} was not a " +
                 "jamo compound.").format(hex(ord(valid_compound))[2:])
        # Negative tests
        for invalid_case in itertools.chain(non_compound_jamo,
                                            invalid_hangul,
                                            invalid_other):
            assert not jamo.is_jamo_compound(invalid_case),\
                ("Incorrectly decided U+{} "
                 "was jamo.").format(hex(ord(invalid_case))[2:])

    def test_synth_hangul(self):
        # To be implemented in a future version
        pass


if __name__ == "__main__":
    unittest.main()  # verbosity = 2)
