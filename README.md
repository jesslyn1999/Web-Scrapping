# GenericWebCrawlerPrototype

Run these commands in GenericWebCrawlerPrototype directory: (change "py" into whatever name you associate python with in your terminal):
1. install spaCy NLP model:
    - py -m spacy download en_core_web_sm
2. Crawl a website with depth = 0:
    - py -m scrapy crawl url-extractor -a root=<WEBSITE ROOT URL> -a allow_domains=<DOMAIN NAME> -a depth=0 -a allow=<ALLOWED ROUTE> 
    NOTE: ("Allowed route is an optional param")
        - Example: py -m scrapy crawl url-extractor -a root=https://www.kompas.com/ -a allow_domains="kompas.com" -a depth=0
            
This is still a prototype.