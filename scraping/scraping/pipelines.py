import os
import sqlalchemy
from sqlalchemy import Column, String, Float, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from urllib.parse import urlparse

# Create SQLAlchemy Base
Base = declarative_base()

class Hotel(Base):
    __tablename__ = 'hotels'

    id = Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
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

class DatabasePipeline:
    def __init__(self, postgresql_uri):
        self.postgresql_uri = postgresql_uri
        self.engine = None
        self.Session = None

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            postgresql_uri=crawler.settings.get('POSTGRESQL_URI', 
                                                'postgresql://Marjia:Marjia029@localhost:5432/ecommerce')
        )

    def open_spider(self, spider):
        # Create engine and create tables
        self.engine = create_engine(self.postgresql_uri)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def close_spider(self, spider):
        # Close the database connection
        if self.engine:
            self.engine.dispose()

    def process_item(self, item, spider):
        session = self.Session()
        
        try:
            # Convert nullable fields, handle missing values
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
                image_path=item.get('image_local_path')
            )
            
            session.add(hotel)
            session.commit()
        except Exception as e:
            spider.logger.error(f"Error processing item: {e}")
            session.rollback()
        finally:
            session.close()
        
        return item

class HotelImagesPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None, item=None):
        # Generate unique filename based on hotel ID and original extension
        url = request.url
        hotel_id = item.get('hotel_id', 'unknown')
        city_name = item.get('city_name', 'unknown').lower().replace(' ', '_')
        ext = os.path.splitext(urlparse(url).path)[1]
        
        # Create a folder for each city
        return f'{city_name}/{hotel_id}{ext}'

    def get_media_requests(self, item, info):
        # Check if image URL exists
        if item.get('image'):
            yield scrapy.Request(item['image'])

    def item_completed(self, results, item, info):
        # Add local image path to item
        image_paths = [x['path'] for ok, x in results if ok]
        item['image_local_path'] = image_paths[0] if image_paths else None
        return item