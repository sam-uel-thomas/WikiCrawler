import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re
from scrapy.exceptions import CloseSpider

class WikipediaLinksSpider(CrawlSpider):
    name = 'wikipedia_links'
    allowed_domains = ['en.wikipedia.org']
    start_urls = ['https://en.wikipedia.org/wiki/Clown']
    visited_urls = set()

    def parse_start_url(self, response):
        return self.parse_link(response)

    def parse_link(self, response):
        if response.url == 'https://en.wikipedia.org/wiki/Philosophy':
            raise CloseSpider('Reached Philosophy page')

        # Select the first link in the main text
        paragraphs = response.css('div#bodyContent div#mw-content-text div.mw-parser-output p').getall()
        for paragraph in paragraphs:
            relative_urls = re.findall(r'href="(/wiki/[^"]*)"', paragraph)
            for relative_url in relative_urls:
                preceding_text = paragraph.split(relative_url)[0]
                if "(" not in preceding_text or ")" in preceding_text.split("(")[-1]:
                    link_title = response.css(f'a[href="{relative_url}"]::attr(title)').get()
                    if link_title and not "Help:" in link_title:
                        link = 'https://en.wikipedia.org' + relative_url
                        if link not in self.visited_urls:
                            self.visited_urls.add(link)
                            yield {'link': link}
                            yield scrapy.Request(url=link, callback=self.parse_link)
                            return