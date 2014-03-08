import logging
from xml.etree import ElementTree

logger = logging.getLogger(__name__)
DOCTYPE = (
    '<!DOCTYPE data PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" ' +
    '"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">')


def parse(inp):
    parser = ElementTree.XMLParser()
    parser.entity['mdash'] = chr(8212)
    parser.entity['ldquo'] = chr(8220)
    parser.entity['rdquo'] = chr(8221)
    inp = inp.split('\n')
    inp[1:1] = [DOCTYPE]
    inp = '\n'.join(inp)
    try:
        tree = ElementTree.XML(inp, parser=parser)
    except ElementTree.ParseError as e:
        logger.warning('Encountered parse error %r', e)
        logger.warning(inp)
        import sys; sys.exit(1)
        return None
    else:
        return tree
