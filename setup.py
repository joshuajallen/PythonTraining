# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 21:23:17 2020

@author: 331574
"""

from setuptools import setup, find_packages

setup(
      name="EEA",
      version="0.1.0",
      author="Sean Bray",
      packages=find_packages(exclude=['*tests']),
      install_requires=['numpy', 'pandas', 'matplotlib']
)