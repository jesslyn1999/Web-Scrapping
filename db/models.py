class CrawlRequest:
    def __init__(self, SearchQuery, FilterKeywords, Site, TimeStart, TimeFinish, State):
        super().__init__()

        self.SearchQuery = str(SearchQuery)
        self.FilterKeywords = [keyword.strip() for keyword in FilterKeywords.split(',')]
        self.Site = list(Site)
        self.TimeStart = TimeStart
        self.TimeFinish = TimeFinish
        self.State = str(State)  # inProgress | finish


class CrawlResult:
    def __init__(self, Request, Results):
        super().__init__()

        self.Request = str(Request)  # Request Id
        self.Results = list(Results)

