#!/usr/bin/env python
import setuptools

with open("README.md") as file:
    read_me_description = file.read()

setuptools.setup(
    name="cfcs-package-octaprog7",
    version="1.0",
    author="Roman Kaban",
    author_email="goctaprog@gmail.com",
    description="calculate files control sum",
    long_description=read_me_description,
    long_description_content_type="text/markdown",
    url="https://github.com/octaprog7/CalcFilesControlSum",
    packages=setuptools.find_packages("src"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
    ],
    package_dir={"": "src"},
    python_requires='>=3.7.2',
)
