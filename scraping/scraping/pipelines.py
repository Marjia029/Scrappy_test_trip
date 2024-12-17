import os
from scrapy.pipelines.images import ImagesPipeline
from urllib.parse import urlparse
from scrapy import Request
from sqlalchemy import Column, String, Float, Integer, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define the database model
Base = declarative_base()

class Hotel(Base):
    __tablename__ = 'hotels'

    id = Column(Integer, primary_key=True, autoincrement=True)
    city_name = Column(String, nullable=True)
    property_title = Column(String, nullable=True)
    hotel_id = Column(String, nullable=True)
    price = Column(String, nullable=True)
    rating = Column(String, nullable=True)
    address = Column(String, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    room_type = Column(String, nullable=True)
    image_path = Column(String, nullable=True)


# Database Pipeline
class DatabasePipeline:
    def __init__(self, postgresql_uri):
        self.postgresql_uri = postgresql_uri
        self.engine = None
        self.Session = None

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            postgresql_uri=crawler.settings.get('POSTGRESQL_URI', 'postgresql://Marjia:Marjia029@localhost:5432/trip')
        )

    def open_spider(self, spider):
        self.engine = create_engine(self.postgresql_uri)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def close_spider(self, spider):
        if self.engine:
            self.engine.dispose()

    def process_item(self, item, spider):
        session = self.Session()
        try:
            hotel = Hotel(
                city_name=item.get('city_name'),
                property_title=item.get('property_title'),
                hotel_id=item.get('hotel_id'),
                price=item.get('price'),
                rating=item.get('rating'),
                address=item.get('address'),
                latitude=float(item.get('latitude')) if item.get('latitude') else None,
                longitude=float(item.get('longitude')) if item.get('longitude') else None,
                room_type=item.get('room_type'),
                image_path=item.get('image_local_path')  # Image path saved
            )
            session.add(hotel)
            session.commit()
        except Exception as e:
            spider.logger.error(f"Error processing item: {e}")
            session.rollback()
        finally:
            session.close()
        return item


# Images Pipeline
class HotelImagesPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None, item=None):
        # Get the hotel_id and city_name from the item for organizing images
        hotel_id = item.get('hotel_id', 'unknown_id')  # Fallback if hotel_id missing
        city_name = item.get('city_name', 'unknown_city').lower().replace(' ', '_')
        
        # Get the image file extension, default to .jpg if not available
        ext = os.path.splitext(urlparse(request.url).path)[1] or '.jpg'
        
        # Log the file path for debugging purposes
        self.logger.info(f"Saving image for hotel {hotel_id} in city {city_name} as {city_name}/{hotel_id}{ext}")

        # Return the file path where the image will be saved
        return f'{city_name}/{hotel_id}{ext}'

    def get_media_requests(self, item, info):
        # Check if image URL exists in the item and yield the request for the image
        if item.get('image'):
            yield Request(item['image'])

    def item_completed(self, results, item, info):
        # Check if image download is successful and update the image_local_path field
        image_paths = [x['path'] for ok, x in results if ok]
        if image_paths:
            item['image_local_path'] = image_paths[0]  # Set the local image path
        else:
            item['image_local_path'] = None
        return item
