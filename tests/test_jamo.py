"""Unit tests for functional tests on Hangul <-> jamo toolkit.
"""
import unittest
import jamo
import random
import itertools
import io


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
        """is_jamo tests.
        Test if a single character is a jamo character.
        Valid jamo includes all modern and archaic jamo, as well as all HCJ.
        Non-assigned code points are invalid.
        """

        # See http://www.unicode.org/charts/PDF/U1100.pdf
        valid_jamo = (chr(_) for _ in range(0x1100, 0x1200))
        # See http://www.unicode.org/charts/PDF/U3130.pdf
        valid_hcj = (chr(_) for _ in range(0x3131, 0x318f))
        # See http://www.unicode.org/charts/PDF/UA960.pdf
        valid_extA = (chr(_) for _ in range(0xa960, 0xa97d))
        # See http://www.unicode.org/charts/PDF/UD7B0.pdf
        valid_extB = itertools.chain((chr(_) for _ in range(0xd7b0, 0xd7c7)),
                                     (chr(_) for _ in range(0xd7cb, 0xd7fc)))

        invalid_edge_cases = (chr(0x10ff), chr(0x1200),
                              chr(0x3130), chr(0x318f),
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
                 "was not jamo.".format(hex(_)[2:]))
        # Negative tests
        for _ in itertools.chain(invalid_edge_cases,
                                 invalid_hangul,
                                 invalid_other):
            assert not jamo.is_jamo(_),\
                ("Incorrectly decided U+{} "
                 "was jamo.".format(hex(_)[2:]))

    def test_is_jamo_modern(self):
        """is_jamo_modern tests.
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
                 "was not modern jamo.".format(hex(_)[2:]))
        # Negative tests
        for _ in itertools.chain(invalid_edge_cases,
                                 invalid_hangul,
                                 invalid_other):
            assert not jamo.is_jamo_modern(_),\
                ("Incorrectly decided U+{} "
                 "was modern jamo.".format(hex(_)[2:]))

    def test_is_hcj(self):
        """is_hcj tests.
        Test if a single character is a HCJ characterl
        HCJ is defined as the U+313x to U+3138x block, sans two non-assigned
        code points.
        """
        # Note: The chaeum filler U+3164 is not considered HCJ, but a special
        # character as defined in http://www.unicode.org/charts/PDF/U3130.pdf.

        valid_hcj = itertools.chain((chr(_) for _ in range(0x3131, 0x3164)),
                                   (chr(_) for _ in range(0x3134, 0x318f)))

        invalid_edge_cases = (chr(0x3130), chr(0x3164), chr(0x318f))
        invalid_hangul = _get_random_hangul(20)
        invalid_other = "abABzyZY ,.:;~`―—–/!@#$%^&*()[]{}ᄀᄓᅡᅶᆨᇃᇿ"

        # Positive tests
        for _ in valid_hcj:
            assert jamo.is_hcj(_),\
                ("Incorrectly decided U+{} "
                 "was not hcj.".format(hex(_)[2:]))
        # Negative tests
        for _ in itertools.chain(invalid_edge_cases,
                                 invalid_hangul,
                                 invalid_other):
            assert not jamo.is_hcj(_),\
                ("Incorrectly decided U+{} "
                 "was hcj.".format(hex(_)[2:]))

    def test_is_hcj_modern(self):
        """is_hcj_modern tests.
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
                 "was not modern hcj.".format(hex(_)[2:]))
        # Negative tests
        for _ in itertools.chain(invalid_edge_cases,
                                 invalid_hangul,
                                 invalid_other):
            assert not jamo.is_hcj_modern(_),\
                ("Incorrectly decided U+{} "
                 "was modern hcj.".format(hex(_)[2:]))

    def test_is_hangul_char(self):
        """is_hangul_char tests."""

        harcoded_tests = "가나다한글한극어힣"

        invalid_edge_cases = (chr(0xabff), chr(0xd7a4))
        invalid_other = "ㄱㄴㅓabABzyZY ,.:;~`―—–/!@#$%^&*()[]{}ᄀᄓᅡᅶᆨᇃᇿㆎㅥ"

        for _ in itertools.chain(harcoded_tests, _get_random_hangul(1024)):
            assert jamo.is_hangul_char(_),\
                ("Incorrectly decided U+{} "
                 "was not a hangul character.".format(hex(_)[2:]))
        for _ in itertools.chain(invalid_edge_cases, invalid_other):
            assert not jamo.is_hangul_char(_),\
                ("Incorrectly decided U+{} "
                 "was a hangul character.".format(hex(_)[2:]))

    def test_jamo_to_hcj(self):
        """jamo_to_hcj hardcoded tests.
        Arguments may be integers corresponding to U+11xx codepoints, actual
        U+11xx jamo characters, or HCJ characters. These may be in an iterable.

        jamo_to_hcj should convert every U+11xx jamo character into U+31xx HCJ
        in a given string. Non-hangul and HCJ characters are not touched.

        jamo_to_hcj is the generator version of j2hcj, the string version.
        """
        # TODO: Archaic jamo

        # Test U+11xx characters.
        for lead, target in zip(_JAMO_LEADS_MODERN, _HCJ_LEADS_MODERN):
            hcj_lead = jamo.jamo_to_hcj(lead)
            assert hcj_lead.__name__ == "<genexpr>",\
                ("hangul_to_jamo didn't"
                 "return an instance of a"
                 "generator.")
            assert target == ''.join(hcj_lead),\
                ("Matched (chr){lead} "
                 "to {hcj_lead}, "
                 "wanted {target}.").format(lead=hex(ord(lead)),
                                            hcj_lead=''.join(hcj_lead),
                                            target=target)
        for vowel, target in zip(_JAMO_VOWELS_MODERN, _HCJ_VOWELS_MODERN):
            hcj_vowel = jamo.jamo_to_hcj(vowel)
            assert hcj_vowel.__name__ == "<genexpr>",\
                ("hangul_to_jamo didn't"
                 "return an instance of a"
                 "generator.")
            assert target == ''.join(hcj_vowel),\
                ("Matched (chr){vowel} "
                 "to {hcj_vowel}, "
                 "wanted {target}.").format(vowel=hex(ord(vowel)),
                                            hcj_vowel=''.join(hcj_vowel),
                                            target=target)
        for tail, target in zip(_JAMO_TAILS_MODERN, _HCJ_TAILS_MODERN):
            hcj_tail = jamo.jamo_to_hcj(tail)
            assert hcj_tail.__name__ == "<genexpr>",\
                ("hangul_to_jamo didn't"
                 "return an instance of a"
                 "generator.")
            assert target == ''.join(hcj_tail),\
                ("Matched (chr){tail} "
                 "to {hcj_tail}, "
                 "wanted {target}.").format(tail=hex(ord(tail)),
                                            hcj_tail=''.join(hcj_tail),
                                            target=target)

        # Test U+11xx integers.
        for lead, target in zip([ord(_) for _ in _JAMO_LEADS_MODERN],
                                _HCJ_LEADS_MODERN):
            hcj_lead = jamo.jamo_to_hcj(lead)
            assert hcj_lead.__name__ == "<genexpr>",\
                ("hangul_to_jamo didn't"
                 "return an instance of a"
                 "generator.")
            assert target == ''.join(hcj_lead),\
                ("Matched (int){lead} "
                 "to {hcj_lead}, "
                 "wanted {target}.").format(lead=hex(lead),
                                            hcj_lead=''.join(hcj_lead),
                                            target=target)
        for vowel, target in zip([ord(_) for _ in _JAMO_VOWELS_MODERN],
                                 _HCJ_VOWELS_MODERN):
            hcj_vowel = jamo.jamo_to_hcj(vowel)
            assert hcj_vowel.__name__ == "<genexpr>",\
                ("hangul_to_jamo didn't"
                 "return an instance of a"
                 "generator.")
            assert target == ''.join(hcj_vowel),\
                ("Matched (int){vowel} "
                 "to {hcj_vowel}, "
                 "wanted {target}.").format(vowel=hex(ord(vowel)),
                                            hcj_vowel=''.join(hcj_vowel),
                                            target=target)
        for tail, target in zip([ord(_) for _ in _JAMO_TAILS_MODERN],
                                _HCJ_TAILS_MODERN):
            hcj_tail = jamo.jamo_to_hcj(tail)
            assert hcj_tail.__name__ == "<genexpr>",\
                ("hangul_to_jamo didn't"
                 "return an instance of a"
                 "generator.")
            assert target == ''.join(hcj_tail),\
                ("Matched (int){tail} "
                 "to {hcj_tail}, "
                 "wanted {target}.").format(tail=hex(ord(tail)),
                                            hcj_tail=''.join(hcj_tail),
                                            target=target)

        # Test HCJ characters.
        for lead, target in zip(_HCJ_LEADS_MODERN, _HCJ_LEADS_MODERN):
            hcj_lead = jamo.jamo_to_hcj(lead)
            assert hcj_lead.__name__ == "<genexpr>",\
                ("hangul_to_jamo didn't"
                 "return an instance of a"
                 "generator.")
            assert target == ''.join(hcj_lead),\
                ("Matched (hcj){lead} "
                 "to {hcj_lead}, "
                 "wanted {target}.").format(lead=lead,
                                            hcj_lead=''.join(hcj_lead),
                                            target=target)
        for vowel, target in zip(_HCJ_VOWELS_MODERN, _HCJ_VOWELS_MODERN):
            hcj_vowel = jamo.jamo_to_hcj(vowel)
            assert hcj_vowel.__name__ == "<genexpr>",\
                ("hangul_to_jamo didn't"
                 "return an instance of a"
                 "generator.")
            assert target == ''.join(hcj_vowel),\
                ("Matched (hcj){vowel} "
                 "to {hcj_vowel}, "
                 "wanted {target}.").format(vowel=vowel,
                                            hcj_vowel=''.join(hcj_vowel),
                                            target=target)
        for tail, target in zip(_HCJ_TAILS_MODERN, _HCJ_TAILS_MODERN):
            hcj_tail = jamo.jamo_to_hcj(tail)
            assert hcj_tail.__name__ == "<genexpr>",\
                ("hangul_to_jamo didn't"
                 "return an instance of a"
                 "generator.")
            assert target == ''.join(hcj_tail),\
                ("Matched (hcj){tail} "
                 "to {hcj_tail}, "
                 "wanted {target}.").format(tail=tail,
                                            hcj_tail=''.join(hcj_tail),
                                            target=target)

        # TODO: Test strings.

        # TODO: Test iterables of mixed types.
        # Note: 'integers' in strings don't get converted, of course.

        # Negative tests
        for invalid in range(10):
            result = [_ for _ in jamo.jamo_to_hcj(invalid)][0]
            assert invalid == result,\
                ("Did not handle non-jamo integer ({test}) properly, "
                 "got: {result}").format(test=invalid, result=result)

    def test_hcjlify(self):
        """hcjlify hardcoded tests.
        Arguments may be integers corresponding to U+11xx codepoints, actual
        U+11xx jamo characters, or HCJ characters. These may be in an iterable.

        hcjlify should convert every U+11xx jamo character into U+31xx HCJ in
        a given string. Non-hangul and HCJ characters are not touched.

        hcjlify is the string version of jamo_to_hcj, the generator version.
        """

        assert False

    def test_hcj_to_jamo(self):
        assert False

    def test_hcj2j(self):
        assert False

    def test_hangul_to_jamo(self):
        """hangul_to_jamo hardcoded tests.
        Arguments may be iterables of characters.

        hangul_to_jamo should split every Hangul character into U+11xx jamo
        for any given string. Non-hangul characters are not touched.

        hangul_to_jamo is the generator version of h2j, the string version.
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
                        (chr(0x1109), chr(0x1165), chr(0)),
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
                ("Incorrect conversion from "
                 "({hangul}) to "
                 "({lead}, {vowel}, {tail}). "
                 "Got {failure}.").format(hangul=hangul,
                                          lead=hex(ord(target[0])),
                                          vowel=hex(ord(target[1])),
                                          tail=hex(ord(target[2]))
                                          if len(target) == 3 else "",
                                          failure=[hex(ord(_)) for _ in trial])\
                if len(hangul) == 1 else\
                ("Incorrect conversion of ({hangul}). "
                 "Got {failure}.".format(hangul=hangul,
                                         failure=[hex(_) for _ in trial]))

    def test_h2j(self):
        """h2j tests with hardcoded cases.
        Arguments may be iterables of characters.

        h2j should split every Hangul character into U+11xx jamo for any given
        string. Non-hangul characters are not touched.

        h2j is the string version of hangul_to_jamo, the generator version.
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
                      "Do you speak 한국어?"]
        desired_jamo = [(chr(0x110c), chr(0x1161), chr(0)),
                        (chr(0x1106), chr(0x1169), chr(0)),
                        (chr(0x1112), chr(0x1161), chr(0x11ab)),
                        (chr(0x1100), chr(0x1173), chr(0x11af)),
                        (chr(0x1109), chr(0x1165), chr(0)),
                        (chr(0x110b), chr(0x116e), chr(0x11af)),
                        (chr(0x1111), chr(0x1167), chr(0x11bc)),
                        (chr(0x110b), chr(0x1163), chr(0x11bc)),
                        (chr(0x1112), chr(0x1161), chr(0x11ab),
                         chr(0x1100), chr(0x116e), chr(0x11af)),
                        tuple(_ for _ in "Do you speak ") +
                        (chr(0x1112), chr(0x1161), chr(0x11ab),
                         chr(0x1100), chr(0x116e), chr(0x11a8),
                         chr(0x110b), chr(0x1165), chr(0)) + ('?',)]
        desired_strings = [''.join(_) for _ in desired_jamo]  # ez parity
        for hangul, target in zip(test_cases, desired_strings):
            trial = jamo.h2j(hangul)
            assert target == trial,\
                ("Incorrect conversion from "
                 "({hangul} to "
                 "({lead}, {vowel}, {tail}). "
                 "Got {failure}.").format(hangul=hangul,
                                          lead=hex(ord(target[0])),
                                          vowel=hex(ord(target[1])),
                                          tail=hex(ord(target[2])),
                                          failure=[hex(ord(_)) for _ in trial])

    def test_get_jamo_class(self):
        """get_jamo_class hardcoded tests.
        Valid arguments are integers and U+11xx characters. HCJ doesn't make
        sense here.

        get_jamo_class should return the class ["lead" | "vowel" | "tail"] of
        a given character or integer.

        Tests all possible jamo in modern Hangul.
        """
        # TODO: Archaic jamo

        # Test characters
        for lead in _JAMO_LEADS_MODERN+[ord(_) for _ in _JAMO_LEADS_MODERN]:
            jamo_type = jamo.get_jamo_class(lead)
            try:
                _lead_hex = hex(ord(lead))
            except TypeError:
                _lead_hex = hex(lead)
            assert "lead" == jamo_type,\
                ("Thought {lead} "
                 "was a {jamo_type}").format(lead=_lead_hex,
                                             jamo_type=jamo_type)
        for vowel in _JAMO_VOWELS_MODERN+[ord(_) for _ in _JAMO_VOWELS_MODERN]:
            jamo_type = jamo.get_jamo_class(vowel)
            try:
                _vowel_hex = hex(ord(vowel))
            except TypeError:
                _vowel_hex = hex(vowel)
            assert "vowel" == jamo_type,\
                ("Thought {vowel} "
                 "was a {jamo_type}").format(vowel=_vowel_hex,
                                             jamo_type=jamo_type)
        for tail in _JAMO_TAILS_MODERN+[ord(_) for _ in _JAMO_TAILS_MODERN]:
            jamo_type = jamo.get_jamo_class(tail)
            try:
                _tail_hex = hex(ord(tail))
            except TypeError:
                _tail_hex = hex(tail)
            assert "tail" == jamo_type,\
                ("Thought {tail} "
                 "was a {jamo_type}").format(tail=_tail_hex,
                                             jamo_type=jamo_type)

        # Negative tests
        _stderr = jamo.jamo.stderr
        jamo.jamo.stderr = io.StringIO()
        for invalid in range(10):
            try:
                jamo.get_jamo_class(invalid)
                assert False, "Did not catch invalid jamo."
            except jamo.InvalidJamoError:
                pass
        jamo.jamo.stderr = _stderr

    def test_jamo_to_hangul(self):
        """jamo_to_hangul tests with hardcoded cases.
        Arguments may be integers corresponding to the U+11xx codepoints, the
        actual U+11xx jamo characters, or HCJ.

        Outputs a one-character Hangul string.

        This function is identical to j2h.

        Enables use of random Hangul test functions.
        """
        global _JAMO_TO_HANGUL_WORKS

        # Support int -> Hangul conversion.
        int_cases = [(0x110c, 0x1161, 0),
                     (0x1106, 0x1169, 0),
                     (0x1112, 0x1161, 0x11ab),
                     (0x1100, 0x1173, 0x11af),
                     (0x1109, 0x1165, 0),
                     (0x110b, 0x116e, 0x11af),
                     (0x1111, 0x1167, 0x11bc),
                     (0x110b, 0x1163, 0x11bc)]
        # Support chr -> Hangul conversion.
        chr_cases = [tuple(chr(_) for _ in case) for case in int_cases]
        # Support HCJ chr -> Hangul conversion.
        hcj_cases = [('ㅈ', 'ㅏ', ''),
                     ('ㅁ', 'ㅗ', ''),
                     ('ㅎ', 'ㅏ', 'ㄴ'),
                     ('ㄱ', 'ㅡ', 'ㄹ'),
                     ('ㅅ', 'ㅓ', ''),
                     ('ㅇ', 'ㅜ', 'ㄹ'),
                     ('ㅍ', 'ㅕ', 'ㅇ'),
                     ('ㅇ', 'ㅑ', 'ㅇ')]
        desired_hangul = ["자",
                          "모",
                          "한",
                          "글",
                          "서",
                          "울",
                          "평",
                          "양"]

        for hangul, (lead, vowel, tail) in zip(desired_hangul, int_cases):
            trial = jamo.jamo_to_hangul(lead, vowel, tail)
            assert hangul == trial,\
                ("Conversion from int to Hangul failed. "
                 "Incorrect conversion from"
                 "({lead}, {vowel}, {tail}) to "
                 "({hangul}). "
                 "Got {failure}.").format(lead=lead,
                                          vowel=vowel,
                                          tail=tail,
                                          hangul=hangul,
                                          failure=trial)
        for hangul, (lead, vowel, tail) in zip(desired_hangul, chr_cases):
            trial = jamo.jamo_to_hangul(lead, vowel, tail)
            assert hangul == trial,\
                ("Conversion from jamo chr to Hangul failed. "
                 "Incorrect conversion from"
                 "({lead}, {vowel}, {tail}) to "
                 "({hangul}). "
                 "Got {failure}.").format(lead=lead,
                                          vowel=vowel,
                                          tail=tail,
                                          hangul=hangul,
                                          failure=trial)
        for hangul, (lead, vowel, tail) in zip(desired_hangul, hcj_cases):
            trial = jamo.jamo_to_hangul(lead, vowel, tail)
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

        # TODO: Negative tests

        # Test the arity 2 version.
        trial = jamo.jamo_to_hangul('ㅎ', 'ㅏ')
        assert trial == '하',\
            ("jamo_to_hangul/2 failed. "
             "Incorrect conversion from "
             "({lead}, {vowel}) to "
             "({hangul}). "
             "Got {failure}.").format(lead='ㅎ', vowel='ㅏ',
                                      hangul='하', failure=trial)

        # Hardmode: not even supported, but uses jamo, hcj, and int.
        if jamo.jamo_to_hangul('ㅎ', chr(0x1161), 0x11ab) != "한":
            print("No karma on jamo_to_hangul. Mixed type support when.")

        # Enable use of random Hangul functions if all goes well.
        _JAMO_TO_HANGUL_WORKS = True

    def test_hcj_char_to_jamo(self):
        assert False

    def test_j2h(self):
        """j2h hardcoded tests.
        Arguments may be integers corresponding to the U+11xx codepoints, the
        actual U+11xx jamo characters, or HCJ.

        Outputs a one-character Hangul string.

        This function is defined solely for naming conisistency with
        jamo_to_hangul.
        """

        assert jamo.j2h('ㅎ', 'ㅏ', 'ㄴ') == "한",\
            ("j2h doesn't work. "
             "Hint: it's the same as jamo_to_hangul.")

        assert jamo.j2h('ㅎ', 'ㅏ') == "하",\
            ("j2h doesn't work. "
             "Hint: it's the same as jamo_to_hangul.")

    def test_synth_hangul(self):
        # To be implemented in future versions
        pass

if __name__ == "__main__":
    unittest.main()
