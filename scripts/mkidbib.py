#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""DocString

DocString Paragraph

"""

import argparse
import string
from xml.dom import minidom

def parse_id_entry(entry):
    id_entry = { "title": "", "authors": "", "year": "",
            "month": "", "day": "", "file": "" }
   # months = [ 'January', 'February', 'March', 'April', 'May', 'June', 'July',
   #            'August', 'September', 'October', 'November', 'December' ]
    title_final = entry.find('", ')
    id_entry['title'] = entry[1:title_final]
    file_initial = entry.rfind('<')
    file_final = entry.find(',', file_initial)
    if file_final == -1 or file_final < file_initial:
        id_entry['file'] = entry[file_initial+1:-1]
    else:
        id_entry['file'] = entry[file_initial+1:file_final]
    id_entry['year'], id_entry['month'], id_entry['day'] = \
        entry[title_final+2:file_initial].split(",")[-2].strip().split('-')
   # id_entry['month'] = months[int(id_entry['month'])-1]
    id_entry['authors'] = \
        string.join(entry[title_final+2:file_initial].split(",")[:-2], " and").strip()
    return id_entry

def print_id_entry(rfc_entry):
    if args.ieee:
        pass
    elif args.draft:
        print """\
@techreport{{{0},
AUTHOR = "{2}",
TITLE = "{{{1}}}",
HOWPUBLISHED = "{{Working Draft}}",
TYPE = "{{Internet-Draft}}",
NUMBER = "{0}",
YEAR = {3},
MONTH = {4},
DAY = {5},
INSTITUTION = "{{IETF Secretariat}}",
}}""".format(rfc_entry['file'], rfc_entry['title'], rfc_entry['authors'],
             rfc_entry['year'], rfc_entry['month'], rfc_entry['day'])
        return
    print """\
@misc{{{0},
TITLE        = "{{{1}}}",
AUTHOR       = "{2}",
HOWPUBLISHED = "{{I-D {0}}}",
YEAR         = {3},
MONTH        = {4},
DAY          = {5},
}}""".format(rfc_entry['file'], rfc_entry['title'], rfc_entry['authors'],
             rfc_entry['year'], rfc_entry['month'], rfc_entry['day'])

# 1. Parse arguments of the CLI
parser = argparse.ArgumentParser(description="parse the id-index.txt file from"
                                             " IETF web page to a bib file")
parser.add_argument("file", help="id-index.txt file downloaded from "
                                 "IETF web page")
group = parser.add_mutually_exclusive_group()
group.add_argument("--ieee", action="store_true",
       help="similar format to IEEE recomended format for the output bib file "
            "of a RFC document (Default)")
group.add_argument("--draft", action="store_true",
       help="draft-carpenter-rfc-citation-recs-01.txt format for the "
            "output bib file")
args = parser.parse_args()
# 2. Parse the XML file and generate the BIB file
f = open(args.file, 'r')
new_identry = 1
identry = ""
id_entry = {}
for line in f:
    line = line.strip()
    if new_identry:
        if len(line) > 0 and line[0] == '"':
            identry = line
            new_identry = 0
    else:
        if line == '':
            new_identry = 1
            id_entry = parse_id_entry(identry)
            print_id_entry(id_entry)
        else:
            identry = identry + ' ' + line 

# vim: ts=8 sts=4 sw=4 et
