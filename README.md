# pyfes

An implementation of [OGC
FES/ISO1943](http://www.opengeospatial.org/standards/filter)


## Installation

The most straightforward way to install this project  at the moment
is to use pip with the repository's URL. Add the `--editable` flag
to the `pip` command in order to get a dev install and hack on the
code.

    pip install git+[repo_url]#egg=pyfes


### Installation with docker

If you want to run pyfes inside a docker container, since we are not
on dockerhub (yet), just clone this repository and then build the
image with:

    docker build -t pyfes -f Dockerfiles/base.Dockerfile .
    docker run -ti --rm pyfes

If you want to set up a development environment for pyfes, use the
`Dockerfiles/dev.Dockerfile` in addition:

    docker build -t pyfes_dev -f Dockerfiles/dev.Dockerfile .
    docker run -ti --rm pyfes_dev /bin/bash


## Testing


## OGC CQL parser

The CQL parser is generated with grako, taking as input the CQL definition
in ebnf.

In order to regenerate the parser you'll need to:

1. Check out the code from github

2. Install its dev dependencies

    pip install -r requirements/dev.txt

3. Regenerate the parser with the following:

    grako -o serializers/ogccql/cqlparser.py serializers/ogccql/ogc_cql.ebnf
