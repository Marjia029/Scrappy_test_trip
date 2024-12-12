import scrapy


class ScraperSpider(scrapy.Spider):
    name = "scraper"
    allowed_domains = ["uk.trip.com"]
    start_urls = ["https://uk.trip.com/hotels/?locale=en-GB&curr=GBP"]

    def parse(self, response):
        # Extract all h3 tags
        h3_tags = response.css("h3::text").getall()
        for h3 in h3_tags:
            yield {"h3_text": h3}

        # Extract all URLs (from <a> tags)
        links = response.css("a::attr(href)").getall()
        for link in links:
            # Join relative URLs with the domain if necessary
            full_url = response.urljoin(link)
            yield {"url": full_url}
