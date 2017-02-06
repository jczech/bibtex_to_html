#!/usr/bin/env python

import pyparsing as pp
from string import lowercase
from pprint import pprint

article_start = pp.Literal("@article")
inproceedings = pp.Literal("@inproceedings")
author_year = pp.Suppress(pp.restOfLine())
comma = pp.Suppress(",")
eq = pp.Suppress("=")

lbr = pp.Suppress("{")
rbr = pp.Suppress("}")
atom = pp.CharsNotIn("{}") 
sentence = pp.Group(pp.OneOrMore(atom))
wrapped = lbr + sentence + rbr + pp.Optional(comma)
wrapped_title = lbr + lbr + sentence + rbr + rbr + pp.Optional(comma)
wrapped_num = lbr + pp.Word(pp.nums) + rbr

authors = ("author" + eq + wrapped).setParseAction(lambda s, l, t: (t[0], t[1][0]))
doi = ("doi" + eq + wrapped).setParseAction(lambda s, l, t: (t[0], t[1][0]))
journal = ("journal" + eq + wrapped).setParseAction(lambda s, l, t: (t[0], t[1][0]))
keywords = ("keywords" + eq + wrapped).setParseAction(lambda s, l, t: (t[0], t[1][0]))
mendeley = ("mendeley-tags" + eq + wrapped).setParseAction(lambda s, l, t: (t[0], t[1][0]))
number = ("number" + eq + wrapped_num + comma).setParseAction(lambda s, l, t: (t[0], t[1][0])) # issue
pages = ("pages" + eq + wrapped).setParseAction(lambda s, l, t: (t[0], t[1][0]))
pmid = ("pmid" + eq + wrapped).setParseAction(lambda s, l, t: (t[0], t[1][0]))
publisher = ("publisher" + eq + wrapped).setParseAction(lambda s, l, t: (t[0], t[1][0]))
title = ("title" + eq + wrapped_title).setParseAction(lambda s, l, t: (t[0], t[1][0]))
url = ("url" + eq + wrapped).setParseAction(lambda s, l, t: (t[0], t[1][0]))
volume = ("volume" + eq + wrapped_num + comma).setParseAction(lambda s, l, t: (t[0], t[1]))
year = ("year" + eq + wrapped_num).setParseAction(lambda s, l, t: (t[0], t[1]))
other = pp.Word(pp.alphas) + eq + pp.restOfLine()

unit = (authors | year | title | journal | volume | number | pages | doi |
        pmid | mendeley | url | pp.Suppress(other))

entry = pp.OneOrMore(
    (article_start | inproceedings) + lbr + author_year + pp.OneOrMore(unit) +
    rbr)

def main():
    with open("mmbios.bib", "r") as bib_file:
        lines = bib_file.read()
        data = entry.parseString(lines)
        for d in data:
            print(d)
            # if type(d) == str:
            #     if d.startswith("@"):
            #         print("-"*40)
            #     else:
            #         print(d)
            # else:
            #     print(d[0])


if __name__ == "__main__":
    main()
