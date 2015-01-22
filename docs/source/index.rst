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

Notice that the characters may have display issues because they are from the
U+11xx jamo code block. This is because there are actually two sets of jamo in
Unicode. Computers use jamo from the U+31xx code block, known as  **Hangul
Compatibility Jamo**, here on referenced as *HCJ*. To render HCJ instead of
U+11xx jamo::

    >>> from jamo import h2j, j2hcj
    >>> j2hcj(h2j("한굴"))
    'ㅎㅏㄴㄱㅜㄹ'
    >>> j2hcj(h2j("자모=字母=jamo"))
    'ㅈㅏㅁㅗ=字母=jamo'

Here we convert the Hangul characters to U+11xx jamo characters, then convert
them to HCJ for more uniform display.

If you are curious, learn more about the differences between U+11xx and U+31xx
jamo at :ref:`unicode_tutorial`. Related, Gernot Katzers has an excellent
writeup on `Hangul representation in unicode`_ that is well worth a read.


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


Large Texts
------------

When working with large files, we will end up with lots of output. To handle
large files, it is recommended to use the provided generator functions::

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

+---------------------+-----------------+
| Generator Function  | String Function |
+=====================+=================+
| jamo_to_hcj         | j2hcj           |
+---------------------+-----------------+
| hangul_to_jamo      | h2j             |
+---------------------+-----------------+
| hangul_transform    | hangulify       |
+---------------------+-----------------+

Module output favors characters whenever possible.


Examples
--------

Basic examples: :ref:`sample_usage`.
.. 
.. Some example uses of jamo are shown below:
.. 
.. * `Highlight tricky vocabulary terms` (soon)
.. * `Frequency analysis of heads, vowels, and tails in Hangul` (soon)
.. * `Jamo-level trigram analysis for Hangul` (soon)
.. * `Jamo-level autocompletion` (soon)


.. _Hangul representation in unicode: http://gernot-katzers-spice-pages.com/var/korean_hangul_unicode.html
