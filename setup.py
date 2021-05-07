"""setup.py file for packaging"""
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sciflow",
    version="0.2",
    author="Dylan Johnson, Caleb Weber, Stuart Chalk",
    author_email="n01448636@unf.edu, cweb1182@gmail.com, schalk@unf.edu",
    description="An interface for management and storage of SciData "
                "JSON-LD files in a graph database",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ChalkLab/sciflow",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
