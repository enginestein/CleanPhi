from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="phi",
    version="1.0.0",
    author="Arya Praneil Pritesh",
    author_email="aryapraneil@gmail.com",
    description="Natural language processing framework to clean sentences and texts.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/enginestein/Phi",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
