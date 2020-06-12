class CrawlResult:
    def __init__(self, SearchQuery, FilterKeywords, Results):
        super().__init__()

        self.SearchQuery = str(SearchQuery)
        self.FilterKeywords = [keyword.strip() for keyword in FilterKeywords.split(',')]
        self.Results = list(Results)
