#!/usr/bin/env python
import setuptools

with open("README.md") as file:
    read_me_description = file.read()

setuptools.setup(
    name="calc_files_control_sum",
    version="1.0",
    author="Roman Shevchik",
    author_email="goctaprog@gmail.com",
    description="calculate files control sum",
    long_description=read_me_description,
    long_description_content_type="text/markdown",
    url="https://github.com/octaprog7/CalcFilesControlSum",
    py_modules=["cfcs", "my_utils", "my_strings", "config"],
    packages=setuptools.find_packages(),
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
    python_requires='>=3.7.2',
    entry_points={
        'console_scripts': [
            'cfcs = cfcs:main',
        ],
    }
)
