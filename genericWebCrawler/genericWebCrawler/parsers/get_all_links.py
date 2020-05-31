import re
from scrapy.linkextractors import LinkExtractor

def get_all_links(response, keywords): # 'keywords' is an array of keyword strings
    le = LinkExtractor(canonicalize=False,
                       unique=True, process_value=None, deny_extensions=None,
                       strip=True)
    links = le.extract_links(response)
    str_links = set()
    keywords = keywords.split(',')
    print("keywords", keywords)
    for link in links:
        found = False
        for keyword in keywords:
            if re.search(r"\b%s\b" % re.escape(keyword), link.url):
                print("url '%s' contains keyword '%s'" % (link.url, keyword))
                found = True
                break
        if found:
            str_links.add(link.url)

    return str_links