from urllib.parse import urlparse
import fnmatch
import collections

class Parser:
    def __init__(self, keywords):
        self.parsers = list()
        self.keywords = keywords

    def register(self, domain, function):
        if isinstance(domain, (list, tuple, set)):
            for d in domain:
                self.parsers.append((d, function))
        else:
            self.parsers.append((domain, function))

    def parse(self, url, response):
        function = self._match_function(url)
        return function(url, response, self.keywords)

    def _extract_domain(self, url):
        url = urlparse(url)
        return url.netloc

    def _match_function(self, url):
        domain = self._extract_domain(url)
        for parser in self.parsers:
            (pattern, function) = parser
            if fnmatch.fnmatch(domain, pattern):
                return function

