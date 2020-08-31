class CrawlerBase:
    def __init__(self, crawl_url, crawl_type):
        self.url = crawl_url
        self.crawl_type = crawl_type
        self.raw_crawled_data = None


