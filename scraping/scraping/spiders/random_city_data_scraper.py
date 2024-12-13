import scrapy
import json
import re
import random


class RandomCityHotelsSpider(scrapy.Spider):
    name = "random_city_hotels_scraper"
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
                    
                    # Randomly select a city with recommendHotels
                    valid_cities = [
                        city for city in inbound_cities 
                        if city.get("recommendHotels") and len(city.get("recommendHotels", [])) > 0
                    ]
                    
                    if not valid_cities:
                        self.logger.warning("No cities with recommend hotels found")
                        return
                    
                    # Randomly select a city
                    selected_city = random.choice(valid_cities)
                    
                    # Extract city details
                    city_name = selected_city.get("name", "Unknown")
                    city_hotels = selected_city.get("recommendHotels", [])
                    
                    self.logger.info(f"Selected city: {city_name}")
                    
                    # Process and yield each hotel
                    random_city_hotels = []
                    for hotel in city_hotels:
                        hotel_info = {
                            "city_name": city_name,
                            "hotel_name": hotel.get("hotelName", ""),
                            "hotel_id": hotel.get("hotelId", ""),
                            "price": hotel.get("price", ""),
                            "star_rating": hotel.get("starRating", ""),
                            "district": hotel.get("district", ""),
                            "address": hotel.get("address", "")
                        }
                        random_city_hotels.append(hotel_info)
                        yield hotel_info
                    
                    # Save to a JSON file
                    if random_city_hotels:
                        output_filename = f"{city_name.lower().replace(' ', '_')}_recommend_hotels.json"
                        with open(output_filename, "w", encoding="utf-8") as f:
                            json.dump(random_city_hotels, f, ensure_ascii=False, indent=4)
                        self.logger.info(f"Saved recommendHotels data for {city_name} to {output_filename}")
                
                except json.JSONDecodeError as e:
                    self.logger.error(f"Failed to parse JSON: {e}")
                except Exception as e:
                    self.logger.error(f"An unexpected error occurred: {e}")