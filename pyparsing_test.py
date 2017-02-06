#!/usr/bin/env python

import pyparsing as pp
from string import lowercase
from pprint import pprint

article_start = pp.Word("@article")
author_year = pp.Suppress(pp.Word(pp.alphanums))
comma = pp.Suppress(",")
eq = pp.Suppress("=")

lbr = pp.Suppress("{")
rbr = pp.Suppress("}")
atom = pp.CharsNotIn("{}") 
sentence = pp.Group(pp.OneOrMore(atom))
wrapped = lbr + sentence + rbr + pp.Optional(comma)
wrapped_title = lbr + lbr + sentence + rbr + rbr + pp.Optional(comma)
wrapped_num = lbr + pp.Word(pp.nums) + rbr

authors = "author" + eq + wrapped
doi = "doi" + eq + wrapped
journal = "journal" + eq + wrapped
keywords = "keywords" + eq + wrapped
mendeley = "mendeley-tags" + eq + wrapped
number = "number" + eq + wrapped_num + comma # issue
pages = "pages" + eq + wrapped
pmid = "pmid" + eq + wrapped
publisher = "publisher" + eq + wrapped
title = "title" + eq + wrapped_title
url = "url" + eq + wrapped
volume = "volume" + eq + wrapped_num + comma
year = "year" + eq + wrapped_num
other = pp.Word(pp.alphas) + eq + wrapped

unit = (authors | year | title | journal | volume | number | pages | doi |
        pmid | mendeley | url | pp.Suppress(other))

entry = pp.OneOrMore(
    article_start + lbr + author_year + comma + pp.OneOrMore(unit) + rbr)

def main():
    with open("mmbios.bib", "r") as bib_file:
        lines = bib_file.read()
        # print(lines)
        data = entry.parseString(lines)
        for d in data:
            if type(d) == str:
                if d == "@article":
                    print("-"*40)
                else:
                    print(d)
            else:
                print(d[0])


if __name__ == "__main__":
    main()
