"""Syllable and jamo analysis for Korean. Default exchange form is Hangul
characters, not codepoints. jamo exchange form is U+11xx characters, not
U+3xxx Hangul Compatibility Jamo (HCJ) characters or codepoints.

For more information, see:
http://gernot-katzers-spice-pages.com/var/korean_hangul_unicode.html
"""
from sys import stderr
from itertools import chain

JAMO_OFFSET = 44032
JAMO_LEAD_OFFSET = 0x10ff
JAMO_VOWEL_OFFSET = 0x1160
JAMO_TAIL_OFFSET = 0x11a7
JAMO_TRANSLATIONS = {ord(jamo): hcj for jamo, hcj in\
        zip("ᄀᄁᄂᄃᄄᄅᄆᄇᄈᄉᄊᄋᄌᄍᄎᄏᄐᄑᄒ"
            "ᅡᅢᅣᅤᅥᅦᅧᅨᅩᅪᅫᅬᅭᅮᅯᅰᅱᅲᅳᅴᅵ"
            "ᆨᆩᆪᆫᆬᆭᆮᆯᆰᆱᆲᆳᆴᆵᆶᆷᆸᆹᆺᆻᆼᆽᆾᆿᇀᇁᇂ",
            "ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ"
            "ㅏㅐㅑㅒㅓㅔㅓㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ"
            "ㄱㄲㄳㄴㄵㄶㄷㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅄㅅㅆㅇㅈㅊㅋㅌㅍㅎ")}

class InvalidJamoError(Exception):
    """jamo is a U+11xx codepoint."""
    def __init__(self, message, jamo):
        super(InvalidJamoError, self).__init__(message)
        self.jamo = hex(jamo)
        print("Could not parse jamo: U+{code}".format(code=self.jamo[2:]),
              file=stderr)

def _to_codepoint(character):
    """Accept a Unicode character or integer and return a codepoint."""
    if type(character) == int:
        return character
    else:
        return ord(character)

def _is_hangul(character):
    """Determine if a given unicode character is Hangul.
    Note: does not support old-style Hangul.
    """
    return ord(character) in range(0xAC00, 0xD7A4)

def _hangul_char_to_jamo(syllable):
    """Return a 3-tuple of lead, vowel, and tail jamo characters.
    Note: Non-Hangul characters are echoed back.
    """
    if _is_hangul(syllable):
        rem = ord(syllable) - JAMO_OFFSET
        tail = rem % 28
        vowel = 1 + ((rem - tail) % 588)//28
        lead = 1 + rem//588
        return (chr(lead + JAMO_LEAD_OFFSET),
                chr(vowel + JAMO_VOWEL_OFFSET),
                chr(tail + JAMO_TAIL_OFFSET if tail else 0))
    else:
        return syllable

def _hcj_to_jamo(hcj_char, position="vowel"):
    """Convert HCJ to jamo based on the intended position."""
    # TODO: Implement this.
    if position == "lead":
        return hcj_char
    elif position == "vowel":
        return hcj_char
    elif position == "tail":
        return hcj_char
    raise InvalidJamoError

def _jamo_to_hangul_char(lead, vowel, tail=0):
    """Return the Hangul character for the given jamo characters."""
    # TODO: Allow HCJ input.
    lead = _to_codepoint(lead) - JAMO_LEAD_OFFSET
    vowel = _to_codepoint(vowel) - JAMO_VOWEL_OFFSET
    tail = _to_codepoint(tail) - JAMO_TAIL_OFFSET if tail else 0
    return chr(tail + (vowel-1)*28 + (lead-1)*588 + JAMO_OFFSET)

def jamo_to_hcj(jamo):
    """Change a single jamo codepoint to a HCJ codepoint."""
    # TODO: Allow non-jamo characters to pass without failing.
    jamo = (ord(_) if type(_) == str else _ for _ in jamo)
    return ''.join(JAMO_TRANSLATIONS.get(_) for _ in jamo)

def jamo_to_hangul(lead, vowel, tail=0):
    """Return the Hangul character for the given jamo characters."""
    # TODO: Allow HCJ input.
    # TODO: Implement string input.
    return _jamo_to_hangul_char(lead, vowel, tail)

def hangul_to_jamo(hangul_string):
    """Convert a string of Hangul to jamo."""
    return (_ for _ in\
            chain.from_iterable(_hangul_char_to_jamo(_) for _ in hangul_string))

def get_jamo_class(jamo):
    """Determine if a jamo is a lead, vowel, or tail.
    This function can handle U+11xx (not HCJ) jamo only.
    """
    # Allow single character strings, autoconverting to a codepoint.
    if type(jamo) == str:
        jamo = ord(jamo)
    # Perhaps raise a separate error for U+3xxx jamo.
    if chr(jamo) in "ᄀᄁᄂᄃᄄᄅᄆᄇᄈᄉᄊᄋᄌᄍᄎᄏᄐᄑᄒ":
        return "lead"
    if chr(jamo) in "ᅡᅢᅣᅤᅥᅦᅧᅨᅩᅪᅫᅬᅭᅮᅯᅰᅱᅲᅳᅴᅵ":
        return "vowel"
    if chr(jamo) in "ᆨᆩᆪᆫᆬᆭᆮᆯᆰᆱᆲᆳᆴᆵᆶᆷᆸᆹᆺᆻᆼᆽᆾᆿᇀᇁᇂ":
        return "tail"
    else:
        raise InvalidJamoError("Could not not determine jamo class.", jamo)

def string_to_hcj(string):
    """Convert jamo characters in a string into hcj as much as possible."""
    return ''.join([''.join(''.join(jamo_to_hcj(_)) for _ in string)])
