#!/usr/bin/env python3
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="easyparse",
    version="1.0.3",
    author="Sh3llcod3",
    author_email="no-reply@gmail.co.uk",
    description="A user-friendly, lightweight command-line argument parser.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sh3llcod3/Easyparse",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: POSIX :: Linux",
    ),
)
