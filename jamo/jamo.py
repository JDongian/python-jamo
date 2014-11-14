"""Syllable and jamo analysis for Korean. Default exchange form is Hangul
characters, not codepoints. jamo exchange form is U+11xx codepoints, not
Hangul Compatibility Jamo (HCJ) codepoints U+3xxx or characters.

For more information, see:
http://gernot-katzers-spice-pages.com/var/korean_hangul_unicode.html
"""
from sys import stderr

JAMO_OFFSET = 44032
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

def jamo_to_hangul(lead, vowel, tail=0):
    """Return the Hangul character for the given jamo parts."""
    # TODO: allow non-index input i.e. HCJ and 0x11XX jamo.
    return chr(tail + (vowel-1)*28 + (lead-1)*588 + JAMO_OFFSET)

def hangul_to_jamo(syllable):
    """Return a 3-tuple of lead, vowel, and tail jamo."""
    rem = ord(syllable) - JAMO_OFFSET
    tail = rem % 28
    vowel = 1 + ((rem - tail) % 588)//28
    lead = 1 + rem//588
    return lead + 0x10ff, vowel + 0x1160, tail + 0x11a7 if tail else 0

def get_jamo_class(jamo):
    """Determine if a jamo is a lead, vowel, or tail.
    This function can handle U+11xx (not HCJ) jamo only.
    """
    # Allow single character strings, autoconverting to a codepoint.
    if type(jamo) == str:
        jamo = ord(jamo)
    # TODO: Stricter jamo constraint checking (not all in range are valid).
    if 0x1100 <= jamo <= 0x1112:
        return "lead"
    if 0x1161 <= jamo <= 0x1175:
        return "vowel"
    if 0x11a8 <= jamo <= 0x11c2:
        return "tail"
    else:
        raise InvalidJamoError("Could not not determine jamo class.", jamo)

def jamo_to_hcj(jamo):
    """Change a jamo codepoint to a HCJ codepoint (better for display)."""
    # Allow single character strings, autoconverting to a codepoint.
    if type(jamo) == str:
        jamo = ord(jamo)
    return JAMO_TRANSLATIONS.get(jamo)
