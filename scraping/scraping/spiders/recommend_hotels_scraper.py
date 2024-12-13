import scrapy
import json
import re


class ScraperSpider(scrapy.Spider):
    name = "recommend_hotels_scraper"
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
                    
                    # Extract `recommendHotels` for each city
                    recommend_hotels = []
                    for city in inbound_cities:
                        city_name = city.get("name", "Unknown")
                        hotels = city.get("recommendHotels", [])
                        for hotel in hotels:
                            recommend_hotels.append({
                                "city_name": city_name,
                                "hotel": hotel
                            })
                    
                    # Save the `recommendHotels` data into a JSON file
                    with open("recommend_hotels.json", "w", encoding="utf-8") as f:
                        json.dump(recommend_hotels, f, ensure_ascii=False, indent=4)
                    self.logger.info("Saved recommendHotels data to recommend_hotels.json")
                except json.JSONDecodeError as e:
                    self.logger.error(f"Failed to parse JSON: {e}")
