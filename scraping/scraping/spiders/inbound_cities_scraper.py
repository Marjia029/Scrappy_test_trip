import scrapy
import json
import re


class ScraperSpider(scrapy.Spider):
    name = "inbound_cities_scraper"
    allowed_domains = ["uk.trip.com"]
    start_urls = ["https://uk.trip.com/hotels/?locale=en-GB&curr=GBP"]

    def parse(self, response):
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
                    
                    # Extract `inboundCities` from `initData.htlsData`
                    inbound_cities = ibu_hotel_data.get("initData", {}).get("htlsData", {}).get("inboundCities", [])
                    
                    # Save the `inboundCities` data into a JSON file
                    with open("inbound_cities.json", "w", encoding="utf-8") as f:
                        json.dump(inbound_cities, f, ensure_ascii=False, indent=4)
                    self.logger.info("Saved window.IBU_HOTEL.initData.htlsData.inboundCities to inbound_cities.json")
                except json.JSONDecodeError as e:
                    self.logger.error(f"Failed to parse JSON: {e}")
