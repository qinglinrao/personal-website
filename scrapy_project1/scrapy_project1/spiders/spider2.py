import scrapy


class QuotesSpider(scrapy.Spider):
    name = "spider1"
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
        'http://quotes.toscrape.com/page/2/',
    ]

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'spider-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)

