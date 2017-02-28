from lxml import etree

class FesFilterParser(object):
    VERSION = "2.0.0"
    PARSER_TYPE = "FILTER_PARSER"

    def __init__(self, etree_parser=None):
        self.etree_parser = etree_parser or etree.XMLParser()

    def parser(self, data):
        raise NotImplementedError