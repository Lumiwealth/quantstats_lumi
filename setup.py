#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""QuantStats: Portfolio analytics for quants
https://github.com/ranaroussi/quantstats
QuantStats performs portfolio profiling, to allow quants and
portfolio managers to understand their performance better,
by providing them with in-depth analytics and risk metrics.
"""

# from codecs import open
import io
from os import path

from setuptools import find_packages, setup

# --- get version ---
version = "unknown"
with open("quantstats_lumi/version.py") as f:
    line = f.read().strip()
    version = line.replace("version = ", "").replace('"', "")
# --- /get version ---

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with io.open(path.join(here, "README.md"), encoding="utf-8") as f:  # Changed from README.rst
    long_description = f.read()

with io.open(path.join(here, "requirements.txt"), encoding="utf-8") as f:
    requirements = [line.rstrip() for line in f]

setup(
    name="quantstats-lumi",
    version=version,
    description="Portfolio analytics for quants",
    long_description=long_description,
    long_description_content_type="text/markdown",  # Changed from text/x-rst
    url="https://github.com/Lumiwealth/quantstats_lumi",
    author="Robert Grzesik (Lumiwealth)",
    author_email="rob@lumiwealth.com",
    license="Apache Software License",
    python_requires='>=3.6',
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        # 'Development Status :: 1 - Planning',
        # 'Development Status :: 2 - Pre-Alpha',
        # 'Development Status :: 3 - Alpha',
        # 'Development Status :: 4 - Beta',
        "Development Status :: 5 - Production/Stable",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "Intended Audience :: Science/Research",
        "Topic :: Office/Business :: Financial",
        "Topic :: Office/Business :: Financial :: Investment",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Scientific/Engineering :: Mathematics",
        # 'Programming Language :: Python :: 3.5',
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    platforms=["any"],
    keywords="""quant algotrading algorithmic-trading quantitative-trading
                quantitative-analysis algo-trading visualization plotting""",
    packages=find_packages(exclude=["contrib", "docs", "tests", "examples"]),
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "sample=sample:main",
        ],
    },
    include_package_data=True,
    package_data={
        "quantstats_lumi": ["report.html"],
    },
)
