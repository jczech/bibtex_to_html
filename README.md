# Convert BibJSON and BibTeX to HTML

## Overview

This was originally designed around the workflow of exporting a BibTeX file
from Mendeley, converting that into a BibJSON file via pandoc-citeproc, and
using this script to convert the BibJSON and BibTeX file into marked up HTML.
Currently, this is very tailored to a specific solution on a specific website,
but it could in principle be made much more general.

The new method only requires a bibtex file and a version of python with
pyparsing.

## Dependencies

Technically you only need Python3 to use this script, but if you're starting
with a bibtex file, you also need pandoc-citeproc to create the json file.

### Old Method

On Ubuntu, you can just do the following:

    sudo apt-get install pandoc-citeproc  

### New Method

On Ubuntu, you can just do the following:

    sudo pip3 install pyparsing  


## How to use (starting with .bib file)

### Old Method

- ``pandoc-citeproc --bib2json mmbios.bib > mmbios.json``
- ``./bibjson_to_html.py mmbios.json mmbios.bib``

### New Method
- ``./bibtex_to_html.py mmbios.bib``

This will create an mmbios.html file.
