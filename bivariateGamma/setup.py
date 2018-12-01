import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bivariateGamma",
    version="0.0.1",
    author="Blaise Murraylee",
    author_email="thatdataguyau@gmail.com",
    description="A package to generate samples of correlated gamma variables",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/blaiseem/bivariateGamma",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)