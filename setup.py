#!/usr/bin/env python

import io
from glob import glob
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import splitext

from setuptools import setup, find_packages


def read(*names, **kwargs):
    return io.open(
        join(dirname(__file__), *names),
        encoding=kwargs.get("encoding", "utf-8")
    ).read()


setup(
    name="pyfes",
    version=read("VERSION"),
    description="A python implementation of OGC FES/ISO 19143",
    long_description=read("README.md"),
    author="Ricardo Garcia Silva",
    author_email="ricardo.garcia.silva@gmail.com",
    url="https://github.com/geopython/pyfes",
    classifiers=[""],
    platforms=[""],
    license="Apache license",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    py_modules=[splitext(basename(path))[0] for path in glob("src/*.py")],
    include_package_data=True,
    install_requires=[
        "lxml",
        "enum34",
    ]
)
