import scrapy

class HotelItem(scrapy.Item):
    city_name = scrapy.Field()
    property_title = scrapy.Field()
    hotel_id = scrapy.Field()
    price = scrapy.Field()
    rating = scrapy.Field()
    address = scrapy.Field()
    latitude = scrapy.Field()
    longitude = scrapy.Field()
    room_type = scrapy.Field()
    image = scrapy.Field()
    image_path = scrapy.Field()
    image_url = scrapy.Field()