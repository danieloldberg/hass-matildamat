"""Setup for Matilda Platform Integration."""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="matilda-platform-ha",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Home Assistant integration for Matilda Platform menus",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/matilda-platform-ha",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Home Automation",
    ],
    python_requires=">=3.11",
    install_requires=[
        "aiohttp>=3.8.0",
    ],
)
