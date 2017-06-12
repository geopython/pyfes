# pyfes

[![Build
Status](https://travis-ci.org/geopython/pyfes.svg?branch=master)](https://travis-ci.org/geopython/pyfes)
[![codecov](https://codecov.io/gh/geopython/pyfes/branch/master/graph/badge.svg)](https://codecov.io/gh/geopython/pyfes)


An implementation of [OGC FES/ISO1943](http://www.opengeospatial.org/standards/filter)


## Installation

The most straightforward way to install this project  at the moment
is to clone this repository and use pip to install both the requirements and 
the project itself. pyfes will eventually be available on pypi, once the 
development stabilizes a bit

    mkvirtualenv pyfes  # if using virtualenvwrapper
    git clone https://github.com/geopython/pyfes.git
    cd pyfes
    pip install --requirement requirements/dev.txt
    pip install --editable .


## Testing

pyfes uses [py.test](http://docs.pytest.org/en/latest/) for testing.
Run tests with:

    py.test -m unit --cov pyfes


## OGC CQL parser - work-in-progress

The CQL parser is generated with grako, taking as input the CQL definition
in ebnf.

In order to regenerate the parser you'll need to:

1. Check out the code from github

2. Install its dev dependencies

    pip install -r requirements/dev.txt

3. Regenerate the parser with the following:

    grako -o serializers/ogccql/cqlparser.py serializers/ogccql/ogc_cql.ebnf
