from flask import Flask, jsonify, request
from scrapy.crawler import CrawlerProcess
from multiprocessing import Process, Manager
from wikicrawler.spiders.wikiCrawler import WikipediaLinksSpider

app = Flask(__name__)

def run_spider(link_list, start_url):
    class CustomSpider(WikipediaLinksSpider):
        start_urls = [start_url]

        def closed(self, reason):
            link_list.extend(self.link_list)

    process = CrawlerProcess()
    process.crawl(CustomSpider, start_url=start_url)
    process.start()

@app.route('/run_spider', methods=['GET'])
def start_spider():
    start_url = request.args.get('start_url', type = str)
    with Manager() as manager:
        link_list = manager.list()
        p = Process(target=run_spider, args=(link_list, start_url))
        p.start()
        p.join()
        return jsonify({"message": f"Reached philosophy in {len(link_list)} steps.", "visited_links": list(link_list)}), 200
    
if __name__ == '__main__':
    app.run(port=5000)