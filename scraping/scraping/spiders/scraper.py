import scrapy
import json
import re


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

        # Extract and parse `window.IBU_HOTEL` data
        script_data = response.xpath("//script[contains(text(), 'window.IBU_HOTEL')]/text()").get()
        if script_data:
            # Use regex to extract JSON-like data
            match = re.search(r"window\.IBU_HOTEL\s*=\s*(\{.*?\});", script_data, re.DOTALL)
            if match:
                json_data = match.group(1)
                try:
                    # Parse the JSON data
                    ibu_hotel_data = json.loads(json_data)
                    # Save the data into a JSON file
                    with open("ibu_hotel_data.json", "w", encoding="utf-8") as f:
                        json.dump(ibu_hotel_data, f, ensure_ascii=False, indent=4)
                    self.logger.info("Saved window.IBU_HOTEL data to ibu_hotel_data.json")
                except json.JSONDecodeError as e:
                    self.logger.error(f"Failed to parse JSON: {e}")
