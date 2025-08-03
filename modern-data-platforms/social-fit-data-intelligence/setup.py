#!/usr/bin/env python3
"""
Setup script for Social FIT Data Intelligence Platform
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

# Read requirements
requirements = []
with open("requirements.txt", "r") as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="social-fit-data-intelligence",
    version="1.0.0",
    author="Social FIT Team",
    author_email="dev@socialfit.com",
    description="Data Intelligence Platform for Gym and Social Media Analytics",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/social_fit",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=1.0.0",
        ],
        "dashboard": [
            "dash>=2.0.0",
            "plotly>=5.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "social-fit=src.main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.sql", "*.txt", "*.md"],
    },
    keywords="etl, analytics, gym, social-media, data-science, business-intelligence",
    project_urls={
        "Bug Reports": "https://github.com/your-username/social_fit/issues",
        "Source": "https://github.com/your-username/social_fit",
        "Documentation": "https://github.com/your-username/social_fit/docs",
    },
) 