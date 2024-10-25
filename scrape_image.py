from bs4 import BeautifulSoup
import requests
from PIL import Image
from io import BytesIO
import re
import schedule
import time
import argparse
from partition import partition_into_six #from partition.py

def scrape_image():
    
    # link to rambles webcam (not a live feed, just pictures taken roughly every 45 mins)
    link = 'https://www.3cat.cat/el-temps/port-olimpic-barcelona/camera/53/'
    response = requests.get(link, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'html.parser')

    img = soup.select_one('img.F-imatge:nth-child(1)')
    datetime = soup.select_one('.R-info__data')['datetime'].replace(' ','_').replace(':','-')


    # gets the temperature, humidity and keeps only the number
    temp_text = soup.select_one('.temperature').get_text()
    humidity_text = soup.select_one('.humidity').get_text()
    temp = re.search(r'\d+', temp_text).group()
    humidity = re.search(r'\d+', humidity_text).group()

    # gets image url
    img_url = img['data-src']

    if img_url.startswith('//'):
        img_url = 'https:' + img_url

        try:
            # downloads image, saves raw
            img_response = requests.get(img_url)

            img = Image.open(BytesIO(img_response.content))

            filename = f'rambles_{datetime}_{temp}_{humidity}.png'

            img.save('images/raw/'+filename)

            # partition into six

            image = Image.open('images/raw/' + filename)
            partition_into_six(img=image)

            print(f"Success! Saved image from: {datetime.split('_')[0]} at {datetime.split('_')[1].replace('-', ':')}")
        
        except Image.UnidentifiedImageError as e:
            print(e)

        except FileExistsError:
            print("The most recent image already is in the folder.")

def run_scheduled():
    """Run the image scraping every 30mins."""
    # schedules the task to run every hour
    schedule.every(30).minutes.do(scrape_image)

    # keep the script running and check for scheduled jobs
    while True:
        schedule.run_pending()
        time.sleep(30)


if __name__ == "__main__":
    
    # some arguments to determine whether its run just once or set up to run hourly (--schedule flag)
    parser = argparse.ArgumentParser(description="Scrape and process either one image or schedule it to scrape every x minutes.")

    parser.add_argument('--schedule', action='store_true', help="Run the script with hourly scheduling")

    args = parser.parse_args()

    # Check if the --schedule flag is set
    if args.schedule:
        print(f"Running with 30 min intervals.")
        run_scheduled()
    else:
        print("Running the script once...")
        scrape_image()