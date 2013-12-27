ietf2bib
========

Some scripts to parse RFC and I-D lists to a bib database.

## About

Two scripts are provided:

- `scripts/mkrfcbib.py`, which parses a RFC index file and generates a bib file
  of RFCs.
- `scripts/mkidbib.py`, which parses a I-D index file and generates a bib file of
  currently active Internet-Drafts.

Two output formats are available:

- By default or with option `--ieee`, the generated bib file will have the
  recommended format for IEEE magazines.
- with option `--draft`, the generated bib file will have the recomended format
  detailed in the I-D *draft-carpenter-rfc-citation-recs-01.txt*.

## Usage

For parsing RFCs, download the latest RFC index file in XML format and parse it
with `mkrfcbib.py`.

	wget http://www.rfc-editor.org/in-notes/rfc-index.xml
	scripts/mkrfcbib.py rfc-index.xml > rfc.bib

For parsing I-Ds, download the latest I-D index file in html format and parse
it with `mkidbib.py`.

	wget https://www.ietf.org/download/id-index.txt
	scripts/mkidbib.py id-index.txt > i-d.bib

Please for all the list of options, read the help `-h`.

	scripts/mkrfcbib.py -h
	scripts/mkidbib.py -h
