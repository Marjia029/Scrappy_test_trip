# 🏨 Scrapy Hotel Scraper Project

This project is a **web scraping** solution built with **Scrapy** to scrape hotel data from **Trip.com**. The scraped data includes hotel details like name, price, rating, address, and image. It also stores the information in a **PostgreSQL** database and saves hotel images to a local folder.

## 🛠️ Technologies Used

- **Scrapy**: Framework used for scraping the data.
- **PostgreSQL**: Database to store scraped hotel data.
- **Docker**: Containerization for easy deployment.
- **SQLAlchemy**: ORM for interacting with the PostgreSQL database.
- **Twisted**: Asynchronous networking engine used in Scrapy.
- **Docker Compose**: To manage multi-container Docker applications.

## 📁 Project Structure

```plaintext
Scrapy_test_trip/
├── scraping/
│   ├── scraping/
│   │   ├── settings.py
│   │   ├── spiders/
│   ├── scrapy.cfg
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── pipelines.py
├── items.py
└── README.md
```
- **scraping/spiders**: Contains the spiders for scraping hotel data.
- **scraping/settings.py**: Scrapy settings and configurations.
- **Dockerfile**: Docker configuration for the project.
- **docker-compose.yml**: Docker Compose file to run the project with dependencies.
- **requirements.txt**: Python dependencies.
- **pipelines.py**: Custom pipelines for handling images and storing data in PostgreSQL.

## 📋 Prerequisites
Before running the project, ensure you have the following installed:

- **Docker**: [Install Docker](https://docs.docker.com/get-docker/)

- **Python (optional)**: If you want to run the spider outside Docker, ensure you have Python 3.9+ installed along with the required dependencies in `requirements.txt`.

Make sure you have a stable internet connection to download Docker images and dependencies.


⚙️ **Setup & Installation**

1. **Clone the repository**
   ```bash
   git clone https://github.com/Marjia029/Scrappy_test_trip.git
   cd Scrapy_test_trip
2. **Create a new virtual environment**
    ```bash
    python -m venv venv #or
    python3 -m venv venv
    ```
3. **Activate the virtual environment**
    ```bash
    \venv\Scripts\activate # for windows
    source venv/bin/activate # for linux
    ```
4. **Go to project Directory**
    ```bash
    cd scraping
    ```
5. **Build Docker containers**

    Ensure you have Docker and Docker Compose installed. Then, run the following commands to build the containers:
    ```bash
    docker-compose build
    ```
6. **Start the containers**

    ```bash
    docker-compose up
    ```
    This will start the Scrapy spider, the PostgreSQL database, and pgAdmin for managing the database.

7. **Access pgAdmin**

    After starting the containers, you can access pgAdmin at:

    - **URL**: [http://localhost:5050](http://localhost:5050)
    - **Username**: `admin@admin.com`
    - **Password**: `admin`

8. **Register the databade**

After accessing the pgAdmin database, you should register the database in server section with providing a database name, and proper database container name, username and password. After that, you should see you database, now go to trip named database --> Schemas --> public --> Tables --> hotels. Now right click and select view/edit, then select All rows. You can see your database table.

## 📚 Features
- **Scraping**: Extracts hotel data like name, price, rating, and images from Trip.com.
- **Database Storage**: Stores the scraped data in a PostgreSQL database.
- **Image Storage**: Downloads hotel images and saves them locally.
- **Dockerized**: Easy to deploy and run in a containerized environment.

## 📝 Notes
- You can customize the spider to scrape additional data or modify the settings as needed.
- The data is saved in PostgreSQL and can be viewed through pgAdmin.
- Image paths are stored in the database, and the images themselves are saved in the `images` directory.

## 📈 To Do
- Add support for more websites.
- Improve the spider to handle edge cases (e.g., empty hotel listings).
- Add more advanced data validation and processing.

## 🙌 Contributing
Contributions are welcome! Feel free to fork this project, open issues, and submit pull requests.
