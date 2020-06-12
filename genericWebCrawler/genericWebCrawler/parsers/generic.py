from bs4 import BeautifulSoup
from scrapy.linkextractors import LinkExtractor
from spacy.lang.en import English
from genericWebCrawler.genericWebCrawler.items import GenericwebcrawlerItem

nlp = English()
nlp.add_pipe(nlp.create_pipe('sentencizer'))


def generic_parser(url, response):
    # select all texts between <p> tags except script tags: (double // to select all children too)
    bsoup = BeautifulSoup(response.text, 'html.parser')

    item = GenericwebcrawlerItem()
    item['title'] = response.xpath('//title//text()').extract()[0].strip()
    item['url'] = response.meta['url']
    item['sentences'] = []
    item['follow_links'] = list(get_all_links(response))

    # remove <a> tags
    a_tags = bsoup.find_all('a')
    for a in a_tags:
        a.decompose()

    # remove <script> tags
    script_tags = bsoup.find_all('script')
    for s in script_tags:
        s.decompose()

    p_children = bsoup.find_all('p')
    # p_filtered = filter(self.tag_visible, p_children)
    # p_filtered =  u" ".join(t.strip() for t in p_filtered)
    # response = soup.xpath('//*[not(self::script) and not(self::a)]').extract()
    # p_children = response.xpath('//*[not(self::script) and not(self::a)]/p').extract()
    # print("P_CHILDREN: ", p_children)
    # temp = response.xpath('//*[not(self::script) and not(self::a)]/p/text()[re:test(., "\w+")]').extract()

    for child in p_children:
        child = child.get_text()
        string = child.strip()
        doc = nlp(string)
        # remove excess middle whitespaces & minimum 10 chars to be considered as a sentence
        sentences = [" ".join(sent.string.strip().split()) for sent in doc.sents if len(sent.string.strip()) > 10]
        item['sentences'].extend(sentences)

    return item


def get_all_links(response):
    le = LinkExtractor(canonicalize=False,
                       unique=True, process_value=None, deny_extensions=None,
                       strip=True)

    links = le.extract_links(response)
    str_links = set()
    for link in links:
        str_links.add(link.url)

    return str_links
