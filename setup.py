from setuptools import setup, find_packages
import sys

if sys.version_info <= (3, 0):
    error = "ERROR: jamo requires Python 3.0 or later"
    print(error, file=sys.stderr)
    sys.exit(1)

with open('README.rst') as f:
    long_description = f.read()

setup(
    name="jamo",
    version=__version__,
    description="A Hangul syllable and jamo analyzer.",
    long_description=long_description,
    author="Joshua Dong",
    author_email="jdong42@gmail.com",
    url="http://github.com/jdong820/python-jamo",
    install_requires=[
        "botocore >= 0.25.0",
    ],
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    license="Apache2",
)

