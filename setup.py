import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="SciFlow-ChalkLab", # Replace with your own username
    version="0.0.1",
    author="Chalk",
    author_email="schalk@unf.edu",
    description="An interface for management and storage of SciData JSON-LD files in a Graph database",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)