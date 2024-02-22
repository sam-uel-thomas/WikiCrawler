import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re
from scrapy.exceptions import CloseSpider

class WikipediaLinksSpider(CrawlSpider):
    name = 'wikipedia_links'
    allowed_domains = ['en.wikipedia.org']
    visited_urls = set()
    link_list = []

    def __init__(self, start_url='https://en.wikipedia.org/wiki/Web_scraping', *args, **kwargs):
        super(WikipediaLinksSpider, self).__init__(*args, **kwargs)
        self.start_urls = [start_url]

    def parse_start_url(self, response):
        return self.parse_link(response)

    def parse_link(self, response):
        if response.url == 'https://en.wikipedia.org/wiki/Philosophy':
            print(f"Reached Philosophy page in {self.steps} steps. Links followed: {self.link_list}")
            raise CloseSpider('Reached Philosophy page')

        paragraphs = response.css('div#bodyContent div#mw-content-text div.mw-parser-output > p').getall()
        for paragraph in paragraphs:
            relative_urls = re.findall(r'href="(/wiki/[^"]*)"', paragraph)
            for relative_url in relative_urls:
                preceding_text = paragraph.split(relative_url)[0]
                if preceding_text.count("(") == preceding_text.count(")"):
                    link_title = response.css(f'a[href="{relative_url}"]::attr(title)').get()
                    if link_title and not "Help:" in link_title:
                        link = 'https://en.wikipedia.org' + relative_url
                        if link not in self.visited_urls:
                            self.visited_urls.add(link)
                            self.link_list.append(link)
                            return scrapy.Request(link, self.parse_link)