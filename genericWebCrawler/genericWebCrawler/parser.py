from urllib.parse import urlparse
import fnmatch


class ParserHelper:
    def __init__(self, keywords):
        self.parsers = list()
        self.keywords = keywords

    def register(self, parser_object):
        if isinstance(parser_object, (list, tuple, set)):
            for obj in parser_object:
                self.parsers.append(obj)
        else:
            self.parsers.append(parser_object)

    def parse(self, response):
        parser_obj = self._match_object(response.url)
        return parser_obj.parser(response, self.keywords)

    def _match_object(self, url):
        domain = self._extract_domain(url)
        for parser_object in self.parsers:
            if fnmatch.fnmatch(domain, parser_object.domain_name):
                return parser_object

    @staticmethod
    def _extract_domain(url):
        url = urlparse(url)
        return url.netloc
