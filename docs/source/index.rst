.. _Jamo:

============================
A Guide to using Python-Jamo
============================

*Note: Documentation may not match actual module usage due to the beta status
of the python-jamo package.*

`Hangul <https://en.wikipedia.org/wiki/Hangul>`_ is a modern writing system
that originated in 1443 to represent the Korean language. It uses an alphabet
of 24 consonants and vowels, each of which are called **jamo** (자모, 字母).

Let's analyze Korean phonemes by decomposing some Hangul. Using the individual 
jamo characters, we can construct some Hangul afterwards.


Hangul Decomposition
--------------------

The python jamo library aims to provide a straightforward interface to Hangul
decomposition::

    >>> from jamo import h2j
    >>> h2j("한굴")
    '한굴'

Oops! What is that? Notice that the characters may not have rendered correctly.
This is because there are actually two sets of jamo in Unicode. We printed the
U+11xx set. The set that computers actually use for *rendering* individual
jamo characters is called **Hangul Compatibility Jamo**, here on referenced as
*HCJ*. To render HCJ instead of U+11xx jamo::

    >>> from jamo import h2j, hcjlify
    >>> hcjlify(h2j("한굴"))
    'ㅎㅏㄴㄱㅜㄹ'
    >>> hcjlify(h2j("자모=字母"))
    'ㅈㅏㅁㅗ=字母'

Here we convert the Hangul characters to U+11xx jamo characters, then convert
them to HCJ for proper display.

This documentation has a short writeup on `Hangul Compatibility Jamo` (soon).
Also related, Gernot Katzers has an excellent writeup on
`Hangul representation in unicode`_ that is well worth a read.


Hangul Synthesis
----------------

Hangul synthesis combines a lead, vowel, and optional tail to form a single
jamo character::
    
    >>> from jamo import j2h
    >>> j2h('ㅇ', 'ㅕ', 'ㅇ')
    영
    >>> j2h('ㅇ', 'ㅓ')
    어

A little hack you can use is the splat operator ``*`` if your arguments are
in string form::

    >>> j2h(*'ㅇㅕㅇ')
    영
    >>> j2h(*'ㅇㅓ')
    어

Note that the jamo to hangul function is quite tolerant of input type. HCJ,
U+11xx jamo, and even integers corresponding to HCJ or U+11xx codepoints are
all valid::

    >>> j2h(0x1100, 0x1161)
    '가'


Large Texts
------------

When working with large files, we will end up with lots of output. To handle
large files, it is recommended to use the generator functions::

    >>> from jamo import hangul_to_jamo
    >>> long_story = open("구운몽.txt", 'r').read()
    >>> hangul_to_jamo(long_story)
    <generator object <genexpr> at 0xdeadbeef9001>

and for HCJ::

    >>> from jamo import hangul_to_jamo, hangul_to_hcj
    >>> long_story = open("구운몽.txt", 'r').read()
    >>> hangul_to_hcj(hangul_to_jamo(long_story))
    <generator object <genexpr> at 0x12cafebabe34>


Naming Conventions
------------------

The python-jamo module is designed to be simple and lightweight. There are no
classes to wrap Hangul strings or jamo characters. Many functions have string
or generator equivalents. All string-generator pairs are shown below:

+---------------------+-----------------+--------------------------------------------------------------+
| Generator Function  | String Function | Short Description                                            |
+=====================+=================+==============================================================+
| hcj_transform       | hcjlify         | Transform values(s) into HCJ.                                |
+---------------------+-----------------+--------------------------------------------------------------+
| hangul_to_jamo      | h2j             | Convert a Hangul characters in a string to jamo.             |
+---------------------+-----------------+--------------------------------------------------------------+
| hangul_transform    | hangulify       | Transform jamo or HCJ characters into Hangul where possible. |
+---------------------+-----------------+--------------------------------------------------------------+

Module output favors U+11xx jamo characters whenever possible, as these are
the most specific. For example, any reference to 'jamo' refers to U+11xx jamo,
and not HCJ.


Examples (soon)
---------------

Some example uses of jamo are shown below:

* `Highlight tricky vocabulary terms` (soon)
* `Frequency analysis of heads, vowels, and tails in Hangul` (soon)
* `Jamo-level trigram analysis for Hangul` (soon)
* `Jamo-level autocompletion` (soon)


.. _Hangul representation in unicode: http://gernot-katzers-spice-pages.com/var/korean_hangul_unicode.html
