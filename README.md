# pyfes

An implementation of [OGC
FES/ISO1943](http://www.opengeospatial.org/standards/filter)


## Installation

The most straightforward way to install this project  at the moment
is to use pip with the repository's URL. Add the `--editable` flag
to the `pip` command in order to get a dev install and hack on the
code.

    pip install git+[repo_url]#egg=pyfes


## Testing

pyfes uses [py.test](http://docs.pytest.org/en/latest/) for testing.
Run tests with:

    py.test -m unit --cov pyfes


## OGC CQL parser (work-in-progress)

The CQL parser is generated with grako, taking as input the CQL definition
in ebnf.

In order to regenerate the parser you'll need to:

1. Check out the code from github

2. Install its dev dependencies

    pip install -r requirements/dev.txt

3. Regenerate the parser with the following:

    grako -o serializers/ogccql/cqlparser.py serializers/ogccql/ogc_cql.ebnf
