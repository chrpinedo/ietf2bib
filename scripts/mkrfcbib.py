#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""DocString

DocString Paragraph

"""

import argparse
from xml.dom import minidom

def parse_rfc_entry(node):
    rfc_entry = { "num": "", "title": "", "authors": "", "year": "",
                  "month": "", "pages": "" }
    for subnode in node.childNodes:
        if subnode.nodeType == subnode.ELEMENT_NODE and \
           subnode.tagName == "doc-id":
            rfc_entry['num'] = str(int(subnode.firstChild.nodeValue[3:]))
        elif subnode.nodeType == subnode.ELEMENT_NODE and \
             subnode.tagName == "title":
            rfc_entry['title'] = subnode.firstChild.nodeValue
        elif subnode.nodeType == subnode.ELEMENT_NODE and \
             subnode.tagName == "author":
            for subsubnode in subnode.childNodes:
                if subsubnode.nodeType == subnode.ELEMENT_NODE and \
                   subsubnode.tagName == "name":
                    if len(rfc_entry['authors']) > 0:
                        rfc_entry['authors'] += " and "
                    rfc_entry['authors'] += subsubnode.firstChild.nodeValue
        elif subnode.nodeType == subnode.ELEMENT_NODE and \
             subnode.tagName == "date":
            for subsubnode in subnode.childNodes:
                if subsubnode.nodeType == subnode.ELEMENT_NODE and \
                   subsubnode.tagName == "year":
                    rfc_entry['year'] = subsubnode.firstChild.nodeValue
                elif subsubnode.nodeType == subnode.ELEMENT_NODE and \
                     subsubnode.tagName == "month":
                    rfc_entry['month'] = subsubnode.firstChild.nodeValue
        elif subnode.nodeType == subnode.ELEMENT_NODE and \
             subnode.tagName == "format":
            for subsubnode in subnode.childNodes:
                if subsubnode.nodeType == subnode.ELEMENT_NODE and \
                   subsubnode.tagName == "page-count":
                    rfc_entry['pages'] = subsubnode.firstChild.nodeValue
        elif subnode.nodeType == subnode.ELEMENT_NODE and \
             subnode.tagName == "doi":
            rfc_entry['doi'] = subnode.firstChild.nodeValue
    return rfc_entry

def print_rfc_entry(rfc_entry):
    if args.ieee:
        pass
    elif args.draft:
        print """\
@techreport{{rfc{0},
AUTHOR          = {{{2}}},
TITLE           = {{{{{1}}}}},
HOWPUBLISHED    = {{Internet Requests for Comments}},
TYPE            = {{{{RFC}}}},
NUMBER          = {0},
PAGES           = {{1-{5}}},
YEAR            = {3},
MONTH           = {{{4}}},
PUBLISHER       = {{{{RFC Editor}}}},
INSTITUTION     = {{{{RFC Editor}}}},
URL             = {{http://www.rfc-editor.org/rfc/rfc{0}.txt}},
DOI             = {{{6}}},
}}""".format(rfc_entry['num'], rfc_entry['title'], rfc_entry['authors'],
             rfc_entry['year'], rfc_entry['month'], rfc_entry['pages'],
             rfc_entry['doi'])
        return
    print """\
@misc{{rfc{0},
TITLE           = {{{{{1}}}}},
AUTHOR          = {{{2}}},
HOWPUBLISHED    = {{{{RFC}} {0}}},
YEAR            = {3},
MONTH           = {{{4}}},
DOI             = {{{5}}},
URL             = {{http://www.rfc-editor.org/info/rfc{0}}},
}}""".format(rfc_entry['num'], rfc_entry['title'], rfc_entry['authors'],
             rfc_entry['year'], rfc_entry['month'], rfc_entry['doi'])

# 1. Parse arguments of the CLI
parser = argparse.ArgumentParser(description="parse the RFC xml file "
                                             "downloaded from RFC "
                                             "Editor web page to a bib file")
parser.add_argument("file", help="rfc-index.xml file downloaded from RFC "
                                 "Editor web page")
group = parser.add_mutually_exclusive_group()
group.add_argument("--ieee", action="store_true",
       help="IEEE recomended format for the output bib file (Default)")
group.add_argument("--draft", action="store_true",
       help="draft-carpenter-rfc-citation-recs-01.txt format for the "
            "output bib file")
args = parser.parse_args()
# 2. Parse the XML file and generate the BIB file
xmldoc = minidom.parse(args.file)
root_node = xmldoc.documentElement
for node in root_node.childNodes:
    if node.nodeType == node.ELEMENT_NODE and node.tagName == "rfc-entry":
        rfc_entry = parse_rfc_entry(node)
        print_rfc_entry(rfc_entry)

# vim: ts=8 sts=4 sw=4 et
