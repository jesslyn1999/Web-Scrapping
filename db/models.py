class CrawlResult:
    def __init__(self, title, url, sentences=None, id=None, links=None):
        super().__init__()

        self.title = title
        self.url = url
        self.sentences = sentences
        self.id = id
        self.links = links

