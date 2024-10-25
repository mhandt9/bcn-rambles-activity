FROM python:3.11-slim

WORKDIR /image-scraper

RUN pip install requests pillow beautifulsoup4 schedule

COPY scrape_image.py partition.py /image-scraper/

RUN mkdir -p /image-scraper/images/raw && mkdir -p /image-scraper/images/partitioned

ENTRYPOINT [ "python", "-u", "scrape_image.py"]