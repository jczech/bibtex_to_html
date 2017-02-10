#!/usr/bin/env python3

from typing import Dict
import pyparsing as pp
import argparse


class BibTexParser():
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

    articles = []  # type: List[Dict]

    article_start = pp.Literal("@article").setParseAction(
            lambda s, l, t: BibTexParser.articles.append({}))
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

    def strip_one(t) -> None:
        BibTexParser.articles[-1][t[0]] = t[1][:-1]

    def strip_two(t) -> None:
        BibTexParser.articles[-1][t[0]] = t[1][:-2]

    def strip_three(t) -> None:
        BibTexParser.articles[-1][t[0]] = t[1][:-3]

    def save_url(t) -> None:
        BibTexParser.articles[-1][t[0]] = t[1][0].split(" ")[0]

    def save_list_entry(t) -> None:
        BibTexParser.articles[-1][t[0]] = t[1][0]

    def save_string_entry(t) -> None:
        BibTexParser.articles[-1][t[0]] = t[1]

    authors = ("author" + eq + wrapped_messy).setParseAction(strip_two)
    doi = ("doi" + eq + wrapped).setParseAction(save_list_entry)
    journal = ("journal" + eq + wrapped_messy).setParseAction(strip_two)
    mendeley = ("mendeley-tags" + eq + wrapped).setParseAction(save_list_entry)
    issue = ("number" + eq + wrapped_num + comma).setParseAction(
             save_list_entry)
    pages = ("pages" + eq + wrapped).setParseAction(save_list_entry)
    pmid = ("pmid" + eq + wrapped).setParseAction(save_list_entry)
    publisher = ("publisher" + eq + wrapped).setParseAction(save_list_entry)
    title = ("title" + eq + wrapped_title).setParseAction(strip_three)
    url = ("url" + eq + wrapped).setParseAction(save_url)
    volume = ("volume" + eq + wrapped_num + comma).setParseAction(
            save_string_entry)
    year = ("year" + eq + wrapped_num).setParseAction(save_string_entry)
    other = pp.Word(pp.alphas) + eq + pp.restOfLine

    unit = (authors | year | title | journal | volume | issue | pages | doi |
            pmid | mendeley | url | pp.Suppress(other))

    entry = pp.OneOrMore(
        (article_start | inproceedings) + lbr + author_year +
        pp.OneOrMore(unit) + rbr)


def get_authors(authors_entry: str) -> str:
    authors = ""
    caps = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    for idx, author in enumerate(authors_entry.split(" and ")):
        if "," in author:
            surname = author.split(", ")[0]
            initials = "".join([l for l in author.split(", ")[1] if l in caps])
        else:
            surname = author.split(" ")[-1]
            initials = "".join([l[0] for l in author.split(" ")[:-1]])
        authors += "<span class=\"author\">%s %s</span>, " % (
            surname, initials)
    return authors[:-2]


def get_title(article: Dict) -> str:
    if article['title'].endswith("."):
        article['title'] = article['title'][:-1]
    try:
        title = (
            "<span class=\"title\" style=\"color: #2ebbbd;\">"
            "<a href = \"%s\">%s</a></span>" % (
                article['url'], article['title']))
    except KeyError:
        title = (
            "<span class=\"title\" style=\"color: #2ebbbd;\">"
            "%s</span>" % (article['title']))
    return title


def get_vol_issue(article: Dict) -> str:
    vol_issue = ""
    try:
        vol = article['volume']
        try:
            issue = article['issue']
            vol_issue = "<span class=\"volume\">%s(%s):</span>" % (vol, issue)

        except KeyError:
            vol_issue = "<span class=\"volume\">%s:</span>" % (vol)
    except KeyError:
        vol_issue = ""
    return vol_issue


def get_tags(article: Dict) -> str:
    tags = ""
    try:
        for tag in article['mendeley-tags'].split(","):
            if tag.startswith("MMBIOS1-TRD"):
                tag = tag[8:]
                tag_type = "trd_pub"
                url = BibTexParser.link_dict[tag]
            elif tag.startswith("MMBIOS1-DBP"):
                tag = tag[8:]
                tag_type = "dbp_pub"
                url = BibTexParser.link_dict[tag]
            elif tag.startswith("MMBIOS1-CSP"):
                tag = tag[8:]
                tag_type = "csp_pub"
                url = "research/collaboration-service"
            else:
                continue
            url = "http://mmbios.org/%s" % url
            tags += (
                "<a href=\"%s\" class=%s>%s</a> " % (url, tag_type, tag))
    except KeyError:
        pass
    return tags


def get_pages(article: Dict) -> str:
    try:
        pages = article['pages']
        pages = pages.replace("--", "-")
        pages = "<span class=\"mpgn\">%s</span>" % pages
    except KeyError:
        pages = ""
    return pages


def replace_tex_symbols(lines):
    replace_dict = {
        r"{\'{a}}": "á",
        r"{\'{e}}": "é",
        r"{\'{i}}": "í",
        r"{\"{u}}": "ű",
        r"{\^{i}}": "î",
        r"{\v{c}}": "č",
        r"{\'{o}}": "ó",
        r"{\{o}}": "ø",
        r"{\%}": "%",
        r"{\#}": "#",
        r"{\_}": "_",
        r"{\~{}}": "~",
        r"{\textless}": "",
        r"{\&}": "&",
        r"{\textgreater}": "",
        r"$\mu$": "μ",
    }

    for key in replace_dict:
        lines = lines.replace(key, replace_dict[key])
    return lines


def bibtex_to_html(bibtex_filename: str, output_filename: str) -> None:
    prev_year_int = 0
    html_str = "<meta charset=\"UTF-8\">\n"
    with open(bibtex_filename, "r", encoding="utf8") as bib_file:
        lines = bib_file.read()
        formatted_lines = replace_tex_symbols(lines)
        BibTexParser.entry.parseString(formatted_lines)
        for article in BibTexParser.articles:
            author = get_authors(article['author'])
            year_int = int(article['year'])
            # Add the year header at year boundaries (e.g. when we transition
            # from 2017 to 2016)
            if (year_int != prev_year_int):
                if (prev_year_int != 0):
                    html_str += "\t</ul>\n</div>\n"
                html_str += ("<h1 id=\"%d\"><span style=\"color: #993300;\">%d"
                             "</span>\n</h1>\n" % (year_int, year_int))
                html_str += "<div class=\"biblio\">\n\t<ul>\n"
            year = "<span class=\"pubdate\">(%s) </span>" % article['year']
            title = get_title(article)
            journal = "<span class=\"journal\">%s</span>" % article['journal']
            try:
                doi = "doi: %s." % article['doi']
            except KeyError:
                doi = ""
            try:
                pmid = "<span class=\"pmid\">PMID:%s</span>" % article['pmid']
            except KeyError:
                pmid = ""
            vol_issue = get_vol_issue(article)
            tags = get_tags(article)
            pages = get_pages(article)
            # Put it all together
            formatted_entry = "<p>{}. {} {}. <i>{}</i>. {}{}. {} {} {}".format(
                author, year, title, journal, vol_issue, pages, doi, pmid,
                tags)
            html_str += "\t\t<li>\n"
            html_str += "\t\t\t%s\n" % formatted_entry
            html_str += "\t\t\t</p>\n"
            html_str += "\t\t</li>\n"
            prev_year_int = year_int
    html_str += "\t</ul>\n</div>\n"
    # if user didn't provide an output filename, generate one automatically
    if (not output_filename):
        output_filename = bibtex_filename.split(".")[0] + ".html"
    with open(output_filename, 'w', encoding="UTF8") as out:
        out.write(html_str)


def setup_argparser():
    parser = argparse.ArgumentParser(
        description="Convert BibTeX to marked up HTML:")
    parser.add_argument("bibtex", help="BibTeX file to be converted")
    parser.add_argument(
        "-o", "--output", help="output html file")
    return parser.parse_args()


def main():
    args = setup_argparser()
    bibtex_to_html(args.bibtex, args.output)


if __name__ == "__main__":
    main()
