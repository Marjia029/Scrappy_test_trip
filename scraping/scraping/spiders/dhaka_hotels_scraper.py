import scrapy
import json
import re

class DhakaHotelsSpider(scrapy.Spider):
    name = "dhaka_hotels_scraper"
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
                    
                    # Find Dhaka city and extract its recommendHotels
                    dhaka_hotels = []
                    for city in inbound_cities:
                        if city.get("name", "").lower() == "dhaka":
                            dhaka_hotels = city.get("recommendHotels", [])
                            break
                    
                    # Process and yield each Dhaka hotel
                    dhaka_hotels_list = []
                    for hotel in dhaka_hotels:
                        hotel_info = {
                            "hotel_name": hotel.get("hotelName", ""),
                            "hotel_id": hotel.get("hotelId", ""),
                            "price": hotel.get("prices", {}).get("priceInfos", [{}])[0].get("price", ""),
                            "star_rating": hotel.get("star", ""),
                            "district": hotel.get("districtName", ""),
                            "address": hotel.get("fullAddress", "")
                        }
                        dhaka_hotels_list.append(hotel_info)
                        yield hotel_info
                    
                    # Save to a JSON file
                    if dhaka_hotels_list:
                        with open("dhaka_recommend_hotels.json", "w", encoding="utf-8") as f:
                            json.dump(dhaka_hotels_list, f, ensure_ascii=False, indent=4)
                        self.logger.info("Saved Dhaka recommendHotels data to dhaka_recommend_hotels.json")
                    else:
                        self.logger.warning("No hotels found for Dhaka")
                
                except json.JSONDecodeError as e:
                    self.logger.error(f"Failed to parse JSON: {e}")
                except Exception as e:
                    self.logger.error(f"An unexpected error occurred: {e}")