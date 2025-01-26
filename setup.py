from setuptools import setup, find_packages

setup(
    name="dfimg",
    version="0.1.0",
    author="Tapanhaz",
    author_email="tapanhaz@gmail.com",
    description="A library to convert polars/ pandas dataframes to image.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Tapanhaz/dfimg",
    packages=find_packages(),
    install_requires=[
        "polars",
        "pandas",
        "pillow",
        "requests",
        "beautifulsoup4",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)
