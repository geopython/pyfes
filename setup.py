import os
from setuptools import setup, find_packages

from pyfes import __version__

README = open(os.path.join(os.path.dirname(__file__), "README.rst")).read()


setup(
    name="pyfes",
    version=__version__,
    description="",
    long_description=README,
    author="Ricardo Garcia Silva",
    author_email="ricardo.garcia.silva@gmail.com",
    url="",
    classifiers=[""],
    platforms=[""],
    license="Apache license",
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,
    install_requires=[
        "lxml",
        "enum34",
    ]
)
