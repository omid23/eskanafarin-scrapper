import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="eskanafarin-scrapper-omid",  # Replace with your own username
    version="0.9",
    author="Omid Mohamad Beigi",
    author_email="omidbeigi23@gmail.com",
    description="scraps data from abs24.ir",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/omid23/eskanafarin-scrapper",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)
