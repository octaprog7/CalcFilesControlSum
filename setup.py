import setuptools

with open("README.md") as file:
    read_me_description = file.read()

setuptools.setup(
    name="cfcs-package-octaprog7",
    version="0.95",
    author="octaprog7",
    author_email="goctaprog@gmail.com",
    description="calculate files control sum",
    long_description=read_me_description,
    long_description_content_type="text/markdown",
    url="https://github.com/octaprog7/CalcFilesControlSum",
    packages=['cfcs_package'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)