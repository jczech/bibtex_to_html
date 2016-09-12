#!/usr/bin/env python3

import json
import re
import argparse


def get_year(item):
    return int(item['issued']['date-parts'][0][0])


def bibjson_to_html(bibjson_filename):
    with open(bibjson_filename) as json_file:
        try:
            bib_data = json.load(json_file)
        except ValueError as e:
            print("Cannot load JSON file: %s" % e)
            return

    caps = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    prev_year_int = 0
    html_str = "<meta charset=\"UTF-8\">\n"
    # Bibliography in reverse chronological order (newest first)
    bib_data = sorted(bib_data, key=get_year, reverse=True)

    for bib_entry in bib_data:
        year_int = int(bib_entry['issued']['date-parts'][0][0])
        if (year_int != prev_year_int):
            if (prev_year_int != 0):
                html_str += "\t</ul>\n</div>\n"
            html_str += "<h1 id=\"%d\"><span style=\"color: #993300;\">%d\
                         </span>\n</h1>\n" % (year_int, year_int)
            html_str += "<div class=\"biblio\">\n\t<ul>\n"
        year = "<span class=\"pubdate\">(%d)</span>" % year_int
        authors = ""
        # Convert authors name to "Surname First-Middle initials"
        # (e.g. "Czech JA")
        for idx, author in enumerate(bib_entry['author']):
            if (idx > 5):
                authors += "et al  " 
                break
            try:
                surname = author['family']
                initials = "".join([l for l in author['given'] if l in caps])
                authors += "<span class=\"author\">%s %s</span>, " % (
                    surname, initials)
            # There's an entry but no surname, so it's prolly an institution
            except KeyError:
                authors += "<span class=\"author\">%s</span>, " % (
                    author['literal'])
        authors = authors[:-2]
        journal = bib_entry['container-title']
        journal = "<span class=\"journal\">%s</span>" % journal
        url = bib_entry['URL'].split(" ")[0]
        title = bib_entry['title']
        # XXX: regex is unsafe against malicious code. unlikely issue here.
        title = re.sub('<[^<]+?>', '', title)
        title = title[:-1]
        title = "<span class=\"title\" style=\"color: #2ebbbd;\">\
                 <a href = \"%s\">%s</a></span>" % (url, title)
        vol = bib_entry['volume']
        try:
            issue = bib_entry['issue']
            vol_issue = "<span class=\"volume\">%s(%s):</span>" % (vol, issue)

        except KeyError:
            vol_issue = "<span class=\"volume\">%s:</span>" % (vol)
        pages = bib_entry['page']
        pages = "<span class=\"mpgn\">%s</span>" % pages
        pmid = bib_entry['PMID']
        pmid = "<span class=\"pmid\">PMID:%s</span>" % pmid
        doi = bib_entry['DOI']
        entry = "<p>%s. %s %s. <i>%s</i>. %s%s. doi: %s. %s" % (
            authors, year, title, journal, vol_issue, pages, doi, pmid)
        html_str += "\t\t<li>\n"
        html_str += "\t\t\t%s\n" % entry
        html_str += "\t\t\t</p>\n"
        html_str += "\t\t</li>\n"
        prev_year_int = year_int
    html_str += "\t</ul>\n</div>\n"

    with open("output.html", 'w') as out:
        out.write(html_str)


def setup_argparser():
    parser = argparse.ArgumentParser(
        description="Convert BibJSON to marked up HTML:")
    parser.add_argument("bibjson", help="BibJSON file to be converted")
    return parser.parse_args()


def main():
    args = setup_argparser()
    bibjson_to_html(args.bibjson)


if __name__ == "__main__":
    main()
