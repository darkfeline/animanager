import logging
from xml.etree import ElementTree

logger = logging.getLogger(__name__)
DOCTYPE = (
    '<!DOCTYPE data PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" ' +
    '"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">')


def parse(inp):
    parser = ElementTree.XMLParser()
    parser.entity['acute'] = chr(180)
    parser.entity['auml'] = chr(228)
    parser.entity['ocirc'] = chr(244)
    parser.entity['ouml'] = chr(246)
    parser.entity['ndash'] = chr(8211)
    parser.entity['mdash'] = chr(8212)
    parser.entity['ldquo'] = chr(8220)
    parser.entity['rdquo'] = chr(8221)
    parser.entity['lsquo'] = chr(8226)
    parser.entity['rsquo'] = chr(8227)
    parser.entity['hellip'] = chr(8230)
    inp = inp.split('\n')
    inp[1:1] = [DOCTYPE]
    inp = '\n'.join(inp)
    try:
        tree = ElementTree.XML(inp, parser=parser)
    except ElementTree.ParseError as e:
        logger.warning('Encountered parse error %r', e)
        logger.warning(inp)
        print("Caught ParseError: {}".format(e))
        return None
    else:
        return tree
