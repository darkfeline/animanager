import logging
from xml.etree import ElementTree
import sys

logger = logging.getLogger(__name__)
DOCTYPE = (
    '<!DOCTYPE data PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" ' +
    '"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">')


def parse(text):
    parser = ElementTree.XMLParser()
    parser.entity['acute'] = chr(180)
    parser.entity['micro'] = chr(181)
    parser.entity['auml'] = chr(228)
    parser.entity['eacute'] = chr(233)
    parser.entity['ocirc'] = chr(244)
    parser.entity['ouml'] = chr(246)
    parser.entity['mu'] = chr(956)
    parser.entity['ndash'] = chr(8211)
    parser.entity['mdash'] = chr(8212)
    parser.entity['lsquo'] = chr(8216)
    parser.entity['rsquo'] = chr(8217)
    parser.entity['ldquo'] = chr(8220)
    parser.entity['rdquo'] = chr(8221)
    parser.entity['bull'] = chr(8226)
    parser.entity['rsquo'] = chr(8227)
    parser.entity['hellip'] = chr(8230)
    text = text.split('\n')
    text[1:1] = [DOCTYPE]
    text = '\n'.join(text)
    try:
        tree = ElementTree.XML(text, parser=parser)
    except ElementTree.ParseError as e:
        logger.error('Encountered parse error %r', e)
        line, col = e.position
        logger.error('Error at line %s, column %s', line, col)
        response_lines = response.split('\n')
        logger.error(response_lines[line])
        logger.error(' ' * (col-1) + '^')
        sys.exit(1)
    else:
        return tree
