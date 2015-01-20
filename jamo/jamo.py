"""Syllable and jamo analysis for Korean. Default internal exchange form is
Hangul characters, not codepoints. Jamo exchange form is U+11xx characters,
not U+3xxx Hangul Compatibility Jamo (HCJ) characters or codepoints.

For more information, see:
http://python-jamo.readthedocs.org/ko/latest/
"""

from sys import stderr
from itertools import chain

JAMO_OFFSET = 44032
JAMO_LEAD_OFFSET = 0x10ff
JAMO_VOWEL_OFFSET = 0x1160
JAMO_TAIL_OFFSET = 0x11a7
JAMO_TO_HCJ_TRANSLATIONS = {jamo: hcj for jamo, hcj in
                            zip("ᄀᄁᄂᄃᄄᄅᄆᄇᄈᄉᄊᄋᄌᄍᄎᄏᄐᄑᄒ"
                                "ᅡᅢᅣᅤᅥᅦᅧᅨᅩᅪᅫᅬᅭᅮᅯᅰᅱᅲᅳᅴᅵ"
                                "ᆨᆩᆪᆫᆬᆭᆮᆯᆰᆱᆲᆳᆴᆵᆶᆷᆸᆹᆺᆻᆼᆽᆾᆿᇀᇁᇂ",
                                "ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ"
                                "ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ"
                                "ㄱㄲㄳㄴㄵㄶㄷㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅄㅅㅆㅇㅈㅊㅋㅌㅍㅎ")}
VALID_JAMO = JAMO_TO_HCJ_TRANSLATIONS.keys()
VALID_HCJ = JAMO_TO_HCJ_TRANSLATIONS.values()

JAMO_LEADS = [chr(_) for _ in range(0x1100, 0x115F)]
JAMO_LEADS_MODERN = [chr(_) for _ in range(0x1100, 0x1113)]
JAMO_VOWELS = [chr(_) for _ in range(0x1161, 0x11A8)]
JAMO_VOWELS_MODERN = [chr(_) for _ in range(0x1161, 0x1176)]
JAMO_TAILS = [chr(_) for _ in range(0x11A8, 0x1200)]
JAMO_TAILS_MODERN = [chr(_) for _ in range(0x11A8, 0x11C3)]


class InvalidJamoError(Exception):
    """jamo is a U+11xx codepoint."""
    def __init__(self, message, jamo):
        super(InvalidJamoError, self).__init__(message)
        self.jamo = hex(ord(jamo))
        print("Could not parse jamo: U+{code}".format(code=self.jamo[2:]),
              file=stderr)


def _to_codepoint(character):
    """Accept a Unicode character or integer and return a codepoint."""
    if not character:
        raise TypeError
    if type(character) == int:
        return character
    else:
        return ord(character)


def _value_to_jamo(value, jamo_class=None):
    try:
        _value = chr(value)
    except TypeError:
        _value = value
    # If given a jamo char or jamo integer
    if _value in VALID_JAMO:
        return value
    # If given a hcj char or hcj integer
    if _value in VALID_HCJ:
        translations = {get_jamo_class(jamo): jamo for jamo, hcj in
                        JAMO_TO_HCJ_TRANSLATIONS.items() if hcj == _value}
        # TODO: Add a custom exception for KeyError.
        return translations[jamo_class]
    # If given something else
    return value


def _hangul_char_to_jamo(syllable):
    """Return a 3-tuple of lead, vowel, and tail jamo characters.
    Note: Non-Hangul characters are echoed back.
    """
    if is_hangul_char(syllable):
        rem = ord(syllable) - JAMO_OFFSET
        tail = rem % 28
        vowel = 1 + ((rem - tail) % 588) // 28
        lead = 1 + rem // 588
        return (chr(lead + JAMO_LEAD_OFFSET),
                chr(vowel + JAMO_VOWEL_OFFSET),
                chr(tail + JAMO_TAIL_OFFSET if tail else 0))
    else:
        return syllable


def _jamo_to_hangul_char(lead, vowel, tail=0):
    """Return the Hangul character for the given jamo characters.
    Equivalent to jamo_to_hangul, but exported function has a shorter name.
    """
    lead = _to_codepoint(_value_to_jamo(lead, "lead"))
    vowel = _to_codepoint(_value_to_jamo(vowel, "vowel"))
    tail = _to_codepoint(_value_to_jamo(tail, "tail")) if tail else 0

    lead -= JAMO_LEAD_OFFSET
    vowel -= JAMO_VOWEL_OFFSET
    tail = tail - JAMO_TAIL_OFFSET if tail else 0
    return chr(tail + (vowel - 1) * 28 + (lead - 1) * 588 + JAMO_OFFSET)


def is_jamo(character):
    """Test if a single character is a jamo character.
    Valid jamo includes all modern and archaic jamo, as well as all HCJ.
    Non-assigned code points are invalid.
    """
    code = ord(character)
    return 0x1100 <= code <= 0x11FF or\
        0xA960 <= code <= 0xA97C or\
        0xD7B0 <= code <= 0xD7C6 or 0xD7CB <= code <= 0xD7FB or\
        is_hcj(character)


def is_jamo_modern(character):
    """Test if a single character is a modern jamo character.
    Modern jamo includes all U+11xx jamo in addition to HCJ in modern usage,
    as defined in Unicode 7.0.
    WARNING: U+1160 is NOT considered a modern jamo character, but it is listed
    under 'Medial Vowels' in the Unicode 7.0 spec.
    """
    code = ord(character)
    return 0x1100 <= code <= 0x1112 or\
        0x1161 <= code <= 0x1175 or\
        0x11A8 <= code <= 0x11C2 or\
        is_hcj_modern(character)


def is_hcj(character):
    """Test if a single character is a HCJ character.
    HCJ is defined as the U+313x to U+318x block, sans two non-assigned code
    points.
    """
    return 0x3131 <= ord(character) <= 0x318E and ord(character) != 0x3164


def is_hcj_modern(character):
    """Test if a single character is a modern HCJ character.
    Modern HCJ is defined as HCJ that corresponds to a U+11xx jamo character
    in modern usage.
    """
    code = ord(character)
    return 0x3131 <= code <= 0x314E or\
        0x314F <= code <= 0x3163


def is_hangul_char(character):
    """Test if a single character is in the U+AC00 to U+D7A3 code block,
    excluding unassigned codes.
    """
    return 0xAC00 <= ord(character) <= 0xD7A3


def get_jamo_class(jamo):
    """Determine if a jamo character is a lead, vowel, or tail.
    Integers and U+11xx characters are valid arguments. HCJ consonants are not
    valid here.

    get_jamo_class should return the class ["lead" | "vowel" | "tail"] of a
    given character or integer.

    Note: jamo class directly corresponds to the Unicode 7.0 specification,
    thus includes filler characters as having a class.
    """
    # TODO: Perhaps raise a separate error for U+3xxx jamo.
    if jamo in JAMO_LEADS or jamo == chr(0x115F):
        return "lead"
    if jamo in JAMO_VOWELS or jamo == chr(0x1160) or\
            0x314F <= ord(jamo) <= 0x3163:
        return "vowel"
    if jamo in JAMO_TAILS:
        return "tail"
    else:
        raise InvalidJamoError("Invalid or classless jamo argument.", jamo)


def jamo_to_hcj(data):
    """Convert jamo to HCJ.
    Arguments may be iterables or single characters.

    jamo_to_hcj should convert every jamo character into HCJ in a given input,
    if possible. Anything else is unchanged.

    jamo_to_hcj is the generator version of j2hcj, the string version. Passing
    a character to jamo_to_hcj will still return a generator.
    """
    if len(data) == 1:
        return (_ for _ in JAMO_TO_HCJ_TRANSLATIONS.get(data, data))
    return (JAMO_TO_HCJ_TRANSLATIONS.get(_, _) for _ in data)


def j2hcj(jamo):
    """Convert jamo into HCJ.
    Arguments may be iterables or single characters.

    j2hcj should convert every jamo character into HCJ in a given input, if
    possible. Anything else is unchanged.

    j2hcj is the string version of jamo_to_hcj, the generator version.
    """
    return ''.join(jamo_to_hcj(jamo))


def hcj_to_jamo(hcj_char, position="vowel"):
    """Convert a HCJ character to a jamo character.
    Arguments may be single characters along with the desired jamo class
    (lead, vowel, tail). Non-mappable input will raise an InvalidJamoError.
    """
    if position == "lead":
        return None
    elif position == "vowel":
        return None
    elif position == "tail":
        return None
    raise InvalidJamoError("No mapping from input to jamo.", hcj_char)


def hcj2j(hcj_char, position="vowel"):
    """Convert a HCJ character to a jamo character.
    Identical to hcj_to_jamo.
    """
    return hcj_to_jamo(hcj_char, position)


def hangul_to_jamo(hangul_string):
    """Convert a string of Hangul to jamo.
    Arguments may be iterables of characters.

    hangul_to_jamo should split every Hangul character into U+11xx jamo
    characters for any given string. Non-hangul characters are not changed.

    hangul_to_jamo is the generator version of h2j, the string version.
    """

    return (_ for _ in
            chain.from_iterable(_hangul_char_to_jamo(_) for _ in
                                hangul_string))


def h2j(hangul_string):
    """Convert a string of Hangul to jamo.
    Arguments may be iterables of characters.

    h2j should split every Hangul character into U+11xx jamo for any given
    string. Non-hangul characters are not touched.

    h2j is the string version of hangul_to_jamo, the generator version.
    """

    return ''.join(hangul_to_jamo(hangul_string))


def jamo_to_hangul(lead, vowel, tail=0):
    """Return the Hangul character for the given jamo input.
    Integers corresponding to U+11xx jamo codepoints, U+11xx jamo characters,
    or HCJ are valid inputs.

    Outputs a one-character Hangul string.

    This function is identical to j2h.
    """

    # TODO: Allow HCJ input.
    # TODO: Implement string input.

    # Internally, we convert everything to a jamo char,
    # then pass it to _jamo_to_hangul_char
    return _jamo_to_hangul_char(lead, vowel, tail)


def j2h(lead, vowel, tail=0):
    """Arguments may be integers corresponding to the U+11xx codepoints, the
    actual U+11xx jamo characters, or HCJ.

    Outputs a one-character Hangul string.

    This function is defined solely for naming conisistency with
    jamo_to_hangul.
    """

    return jamo_to_hangul(lead, vowel, tail)


def synth_hangul(string):
    """Convert jamo characters in a string into hcj as much as possible."""
    raise NotImplementedError
    return ''.join([''.join(''.join(jamo_to_hcj(_)) for _ in string)])
