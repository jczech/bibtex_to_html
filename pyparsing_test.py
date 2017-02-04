#!/usr/bin/env python

import pyparsing as pp
from string import lowercase
from pprint import pprint

article_start = pp.Suppress("@article")
author_year = pp.Word(pp.alphanums)
comma = pp.Suppress(",")
eq = pp.Suppress("=")

lbr = pp.Suppress("{")
rbr = pp.Suppress("}")
atom = pp.CharsNotIn("{}") 
sentence = pp.Group(pp.OneOrMore(atom))
wrapped = lbr + sentence + rbr + pp.Optional(comma)
wrapped_title = lbr + lbr + sentence + rbr + rbr + pp.Optional(comma)
wrapped_num = lbr + pp.Word(pp.nums) + rbr

abstract = pp.Suppress("abstract" + eq + wrapped)
author = "author" + eq + wrapped
doi = "doi" + eq + wrapped
eprint = "eprint" + eq + wrapped
isbn = "isbn" + eq + wrapped
issn = "issn" + eq + wrapped
journal = "journal" + eq + wrapped
keywords = "keywords" + eq + wrapped
mendeley = "mendeley-tags" + eq + wrapped
month = "month" + eq + wrapped
number = "number" + eq + wrapped_num + comma
pages = "pages" + eq + wrapped
pmid = "pmid" + eq + wrapped
publisher = "publisher" + eq + wrapped
title = "title" + eq + wrapped_title
url = "url" + eq + wrapped
other = pp.Word(pp.alphas) + eq + wrapped
volume = "volume" + eq + wrapped_num + comma
year = "year" + eq + wrapped_num

unit = author | doi | volume | year | pmid | mendeley | title | pp.Suppress(other)

entry = pp.OneOrMore(
    article_start + lbr + author_year + comma + pp.OneOrMore(unit) + rbr)

# entry = pp.OneOrMore(
#     article_start + lbr + author_year + comma + abstract + author + doi +
#     pp.Optional(eprint) + isbn + pp.Optional(issn) + pp.Optional(journal) +
#     pp.Optional(keywords) + pp.Optional(mendeley) + month + pp.Optional(number)
#     + pages + pp.Optional(pmid) + pp.Optional(publisher) + title + url +
#     pp.Optional(volume) + year + rbr)


def main():
    with open("mmbios.bib", "r") as bib_file:
        lines = bib_file.read()
        # print(lines)
        data = entry.parseString(lines)
        for d in data:
            print(d)


if __name__ == "__main__":
    main()
