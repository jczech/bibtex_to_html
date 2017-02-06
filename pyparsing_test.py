#!/usr/bin/env python

import pyparsing as pp
from string import lowercase
from pprint import pprint

link_dict = {
    "DBP1": "research/driving-biomedical-projects/glutamate-transport",
    "DBP2": "research/driving-biomedical-projects/synaptic-signaling",
    "DBP3": "research/driving-biomedical-projects/dat-function",
    "DBP4": "research/driving-biomedical-projects/t-cell-signaling",
    "DBP5": "research/driving-biomedical-projects/neural-circuits",
    "TRD1": "research/technology-research-and-development/molecular-modeling",
    "TRD2": "research/technology-research-and-development/cell-modeling",
    "TRD3": "research/technology-research-and-development/image-processing",
    "CSP":  "research/collaboration-service",
}

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

def get_authors(authors_entry):
    authors = ""
    caps = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    for idx, author in enumerate(authors_entry.split(" and ")):
        try:
            if "," in author:
                surname = author.split(", ")[0]
                initials = "".join([l for l in author.split(", ")[1] if l in caps])
            else:
                surname = author.split(" ")[-1]
                initials = "".join([l[0] for l in author.split(" ")[:-1]])
            authors += "<span class=\"author\">%s %s</span>, " % (
                surname, initials)
        # There's an entry but no surname, so it's prolly an institution
        except KeyError:
            assert("Warning!")
            # authors += "<span class=\"author\">%s</span>, " % (author['literal'])
    return authors


def main():
    with open("mmbios.bib", "r") as bib_file:
        lines = bib_file.read()
        data = entry.parseString(lines)
        for d in data:
            if type(d) == str:
                print("-"*40)
            else:
                if d[0] == "author":
                    print(get_authors(d[1]))
                else:
                    print(d[1])


if __name__ == "__main__":
    main()
