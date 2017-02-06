#!/usr/bin/env python

import pyparsing as pp
import re
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

articles = []

article_start = pp.Literal("@article").setParseAction(lambda s, l, t: articles.append({}))
inproceedings = pp.Literal("@inproceedings")
author_year = pp.Suppress(pp.restOfLine)
comma = pp.Suppress(",")
eq = pp.Suppress("=")

lbr = pp.Suppress("{")
rbr = pp.Suppress("}")
atom = pp.CharsNotIn("{}") 
sentence = pp.Group(pp.OneOrMore(atom))
wrapped = lbr + sentence + rbr + pp.Optional(comma)
wrapped_messy = lbr + pp.restOfLine
wrapped_title = lbr + lbr + pp.restOfLine
wrapped_num = lbr + pp.Word(pp.nums) + rbr

def strip_one(s, l, t):
    print(t)
    articles[-1][t[0]] = t[1][:-1] 

def strip_two(s, l, t):
    articles[-1][t[0]] = t[1][:-2] 

def strip_three(s, l, t):
    articles[-1][t[0]] = t[1][:-3] 

def save_url(s, l, t):
    articles[-1][t[0]] = t[1][0].split(" ")[0]

def save_list_entry(s, l, t):
    articles[-1][t[0]] = t[1][0]

def save_string_entry(s, l, t):
    articles[-1][t[0]] = t[1]

authors = ("author" + eq + wrapped_messy).setParseAction(strip_two)
doi = ("doi" + eq + wrapped).setParseAction(save_list_entry)
journal = ("journal" + eq + wrapped_messy).setParseAction(strip_two)
mendeley = ("mendeley-tags" + eq + wrapped).setParseAction(save_list_entry)
number = ("number" + eq + wrapped_num + comma).setParseAction(save_list_entry) # issue
pages = ("pages" + eq + wrapped).setParseAction(save_list_entry)
pmid = ("pmid" + eq + wrapped).setParseAction(save_list_entry)
publisher = ("publisher" + eq + wrapped).setParseAction(save_list_entry)
title = ("title" + eq + wrapped_title).setParseAction(strip_three)
url = ("url" + eq + wrapped).setParseAction(save_url)
volume = ("volume" + eq + wrapped_num + comma).setParseAction(save_string_entry)
year = ("year" + eq + wrapped_num).setParseAction(save_string_entry)
other = pp.Word(pp.alphas) + eq + pp.restOfLine

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
        # print(data)
        for article in articles:
            # pprint(article)
            author = get_authors(article['author'])
            year = "<span class=\"pubdate\">(%s) </span>" % article['year']
            try:
                title = (
                    "<span class=\"title\" style=\"color: #2ebbbd;\">"
                    "<a href = \"%s\">%s</a></span>" % (article['url'], article['title']))
            except KeyError:
                title = (
                    "<span class=\"title\" style=\"color: #2ebbbd;\">"
                    "%s</span>" % (article['title']))
            journal = "<span class=\"journal\">%s</span>" % article['journal']
            print("-"*40)
            print(journal)
            print(author)
            print(title)
            # print(year)
            # if type(d) == str:
            #     print("-"*40)
            # else:
            #     if d[0] == "author":
            #         print(get_authors(d[1]))
            #     elif d[0] == "year":
            #         print("<span class=\"pubdate\">(%s) </span>" % d[1])
            #     else:
            #         print(d)
            #         # print(d[1])


if __name__ == "__main__":
    main()
