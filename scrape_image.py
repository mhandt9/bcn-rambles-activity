from bs4 import BeautifulSoup
import requests
from PIL import Image
from io import BytesIO
import re
from partition import *


link = 'https://www.3cat.cat/el-temps/port-olimpic-barcelona/camera/53/'
response = requests.get(link, timeout=10)
response.raise_for_status()

soup = BeautifulSoup(response.content, 'html.parser')

img = soup.select_one('img.F-imatge:nth-child(1)')
datetime = soup.select_one('.R-info__data')['datetime'].replace(' ','_').replace(':','-')

temp_text = soup.select_one('.temperature').get_text()
humidity_text = soup.select_one('.humidity').get_text()
temp = re.search(r'\d+', temp_text).group()
humidity = re.search(r'\d+', humidity_text).group()

img_url = img['data-src']

if img_url.startswith('//'):
    img_url = 'https:' + img_url

    try:

        img_response = requests.get(img_url)

        img = Image.open(BytesIO(img_response.content))

        filename = f'rambles_{datetime}_{temp}_{humidity}.png'

        img.save('images/raw/'+filename)

        print(f"Success! Saved image from: {datetime.split('_')[0]} at {datetime.split('_')[1].replace('-', ':')}")
    
    except Image.UnidentifiedImageError as e:
        print(e)

print('Now partitioning:')

image = Image.open('images/raw/'+filename)

partition_into_six(img=image)

    