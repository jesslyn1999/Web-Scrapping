from bs4 import BeautifulSoup
from scrapy.linkextractors import LinkExtractor
from spacy.lang.en import English # updated

nlp = English()
nlp.add_pipe(nlp.create_pipe('sentencizer'))

def generic_parser(url, response):
    # see request result
    # print("THE URL: ", response.url)
    # print("RESPONSE: ")
    # print(response)
    # response("<em> <td> Halo, </td> aku text outlier </em>")
    title = response.xpath('//title//text()').extract()[0].strip()

    # select all texts between <p> tags except script tags: (double // to select all children too)
    bsoup = BeautifulSoup(response.text, 'html.parser')
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

    listOfSentences = []
    for child in p_children:
        child = child.get_text()
        string = child.strip()
        doc = nlp(string)
        # remove excess middle whitespaces & minimum 10 chars to be considered as a sentence
        sentences = [" ".join(sent.string.strip().split()) for sent in doc.sents if len(sent.string.strip()) > 10]
        listOfSentences.extend(sentences)

    all_urls = get_all_links(response)

    return (title, response.meta['url'], listOfSentences, all_urls)


def get_all_links(response):
    le = LinkExtractor(canonicalize=False,
                       unique=True, process_value=None, deny_extensions=None,
                       strip=True)

    links = le.extract_links(response)
    str_links = set()
    for link in links:
        str_links.add(link.url)

    return str_links
