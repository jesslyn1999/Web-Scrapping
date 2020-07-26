class CrawlRequest:
    def __init__(self, SearchQuery, FilterKeywords, Site, TimeStart, TimeFinish, State):
        super().__init__()

        self.SearchQuery = SearchQuery
        self.FilterKeywords = [keyword.strip() for keyword in FilterKeywords.split(',')]
        self.Site = Site
        self.TimeStart = TimeStart
        self.TimeFinish = TimeFinish
        self.State = State  # inProgress | finish
