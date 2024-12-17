import os
from pathlib import Path
import scrapy
from urllib.parse import urlparse
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from scrapy.pipelines.images import ImagesPipeline
from itemadapter import ItemAdapter

# Define SQLAlchemy Base
Base = declarative_base()

# Define the Hotel model directly in pipelines.py
class Hotel(Base):
    __tablename__ = 'hotels'
    
    id = Column(Integer, primary_key=True)
    city_name = Column(String)
    property_title = Column(String)
    hotel_id = Column(String)
    price = Column(String)
    rating = Column(Float)
    address = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    room_type = Column(String)
    image_path = Column(String)
    image_url = Column(String)

    def __repr__(self):
        return f"<Hotel(city_name={self.city_name}, property_title={self.property_title})>"


# Image Download Pipeline
class HotelImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        # Check if image URL exists and is not empty
        image_url = item.get('image')
        if image_url and image_url.strip():
            yield scrapy.Request(image_url, meta={'item': item})

    def file_path(self, request, response=None, info=None, item=None):
        # Ensure the 'images' directory exists
        Path('/app/images').mkdir(parents=True, exist_ok=True)

        # Extract the filename from the URL
        parsed_url = urlparse(request.url)
        image_name = os.path.basename(parsed_url.path)

        # Sanitize the filename
        safe_name = "".join(c for c in image_name if c.isalnum() or c in ('.', '_')).rstrip()

        # Use a default filename if the name is empty
        if not safe_name:
            safe_name = 'hotel_image.jpg'

        return os.path.join('images', safe_name)

    def item_completed(self, results, item, info):
        # Use ItemAdapter to handle both Scrapy Item and dict
        adapter = ItemAdapter(item)

        # Check if image was downloaded successfully
        for success, result in results:
            if success:
                # Update item with image path
                image_path = result['path']
                adapter['image_path'] = image_path
                adapter['image_url'] = result.get('url', '')
            else:
                # Log any download failures
                info.spider.logger.warning(f"Image download failed for item: {item}")

        return item

    

# PostgreSQL Pipeline
class PostgreSQLPipeline:
    def __init__(self, postgresql_uri):
        # Set up SQLAlchemy engine and session
        self.engine = create_engine(postgresql_uri)
        
        # Drop existing table (if it exists)
        Base.metadata.drop_all(self.engine, tables=[Hotel.__table__])
        
        # Create tables
        Base.metadata.create_all(self.engine)
        
        # Create session
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    @classmethod
    def from_crawler(cls, crawler):
        postgresql_uri = crawler.settings.get('POSTGRESQL_URI')
        return cls(postgresql_uri)

    def process_item(self, item, spider):
        # Ensure all required fields are present
        try:
            # Convert rating to float, defaulting to None if not possible
            rating = None
            try:
                rating = float(item.get('rating')) if item.get('rating') else None
            except (TypeError, ValueError):
                spider.logger.warning(f"Could not convert rating to float: {item.get('rating')}")

            # Convert latitude and longitude to float, defaulting to None if not possible
            latitude = None
            longitude = None
            try:
                latitude = float(item.get('latitude')) if item.get('latitude') else None
                longitude = float(item.get('longitude')) if item.get('longitude') else None
            except (TypeError, ValueError):
                spider.logger.warning(f"Could not convert coordinates to float. Latitude: {item.get('latitude')}, Longitude: {item.get('longitude')}")

            # Save the item to the database
            hotel = Hotel(
                city_name=str(item.get('city_name', '')),
                property_title=str(item.get('property_title', '')),
                hotel_id=str(item.get('hotel_id', '')),
                price=str(item.get('price', '')),
                rating=rating,
                address=str(item.get('address', '')),
                latitude=latitude,
                longitude=longitude,
                room_type=str(item.get('room_type', '')),
                image_path=str(item.get('image_path', '')),
                image_url=str(item.get('image', ''))
            )
            
            # Add and commit the hotel
            self.session.add(hotel)
            self.session.commit()
            
            return item
        
        except Exception as e:
            spider.logger.error(f"Error processing item: {e}")
            self.session.rollback()
            raise

    def close_spider(self, spider):
        # Close the database session
        self.session.close()