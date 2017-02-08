# Convert BibTeX to HTML

## Overview

Convert a BibTeX file (e.g. from Mendeley) into marked up HTML. Currently, this
is very tailored to a specific solution on a specific website, but it could in
principle be made much more general.

## Dependencies

A relatively recent version of Python3 and pyparsing

On Ubuntu, you can just do the following:

    sudo pip3 install pyparsing  

On Windows, you might want to use
[anaconda](https://www.continuum.io/downloads).

## How to use

Simply type this at the command line: 

    ./bibtex_to_html.py mmbios.bib

If using anaconda, you could use IPython:

    %run ./bibtex_to_html.py mmbios.bib

In either case, this will create an mmbios.html file.
