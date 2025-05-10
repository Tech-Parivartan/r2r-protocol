
from setuptools import setup, find_packages

setup(
    name="r2r",
    version="0.1.0",
    description="Robot-to-Robot (R2R) Communication Protocol SDK in Python",
    long_description=open("../README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Tech-Parivartan/r2r-protocol ",
    author="Tech-Parivartan",
    author_email="techparivartan022@gmail.com",
    license="MIT",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Robotics :: Communication",
    ],
    python_requires='>=3.7',
)
