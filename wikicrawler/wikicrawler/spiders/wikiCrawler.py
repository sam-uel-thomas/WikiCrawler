import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re

class WikipediaLinksSpider(CrawlSpider):
    name = 'wikipedia_links'
    allowed_domains = ['en.wikipedia.org']
    start_urls = ['https://en.wikipedia.org/wiki/Spider']
    visited_urls = set()

    rules = (
        Rule(LinkExtractor(allow=('/wiki/',), restrict_css=('div#bodyContent',)),
             callback='parse_link', follow=False),
        Rule(LinkExtractor(allow=(r'/wiki/(?!File:).+',), restrict_css=('div#bodyContent',)),
         callback='parse_link', follow=False),
    )


    def parse_link(self, response):
        for relative_url in response.css('div#bodyContent a::attr(href)').getall():
            # Extract the link text
            link_text = response.css(f'a[href="{relative_url}"]::text').get()

            # Check if the link text is part of a phrase inside brackets
            if not re.search(r'\(.*' + re.escape(link_text) + '.*\)', response.text):
                link = 'https://en.wikipedia.org' + relative_url
                if link not in self.visited_urls:
                    self.visited_urls.add(link)
                    yield {'link': link}
# Run the spider
