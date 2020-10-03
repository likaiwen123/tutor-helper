#!/usr/bin/env python

from setuptools import setup, find_packages
import gpa

# read version number
version = gpa.__version__()

# read long description from README.md
with open("README.md", encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name="tutorhelper",
    version=version,
    author="Kaiwen Li",
    author_email="likw18@mails.tsinghua.edu.cn",
    description="Tools to automate tutor's work",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    url='https://github.com/likaiwen123/tutor-helper', install_requires=['pandas', 'openpyxl']
)
