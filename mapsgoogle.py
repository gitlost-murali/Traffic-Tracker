import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from datetime import datetime
import pytz
import json
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import sys, os
from glob import glob
import moviepy.editor as mp
# Reference : 
# https://stackoverflow.com/questions/41340792/change-google-map-web-page-with-selenium-python
# https://stackoverflow.com/questions/18869365/a-watermark-inside-a-rectangle-which-filled-the-certain-color

images_folder = 'images/'
if not os.path.exists(images_folder):os.mkdir(images_folder)
videos_folder = 'videos/'
if not os.path.exists(videos_folder):os.mkdir(videos_folder)
gifs_folder = 'gifs/'
if not os.path.exists(gifs_folder):os.mkdir(gifs_folder)


# Load the page
options = FirefoxOptions()
options.add_argument("--headless")
driver = webdriver.Firefox(options=options)
width = 1920
height = 1080
driver.set_window_size(width, height)
#driver = webdriver.Chrome()

locations = dict()
with open('locations.json') as json_file: 
    locations = json.load(json_file) 

location = 'NH27-Part2'
timeinterval = 550
locationurl = locations[location]

import imageio 
def make_gif(imagesli,datepath):
    with imageio.get_writer(f'{gifs_folder}analysis_{datepath}.gif', mode='I',duration=0.1) as writer: 
        for filename in imagesli: 
            image = imageio.imread(filename)
            writer.append_data(image) 

    return f'{gifs_folder}analysis_{datepath}.gif'

def make_video(gifname,datepath):
    clip = mp.VideoFileClip(f"{gifname}")
    clip.write_videofile(f"{videos_folder}vid_{datepath}.mp4")

def initiate():

    '''
    # Majestic https://www.google.com/maps/@12.9752159,77.5762682,14.75z/data=!5m1!1e1 
    # Brooklyn https://www.google.com/maps/@40.6516003,-73.9438822,13.25z/data=!5m1!1e1
    yousufguda_location 
    'https://www.google.com/maps/@17.4374383,78.4322134,16.75z/data=!5m1!1e1'
    HSR Layout location
    https://www.google.com/maps/@12.9185707,77.6398468,17z/data=!5m1!1e1
    Jubilee
    https://www.google.com/maps/@17.4350442,78.4339125,15.5z/data=!5m1!1e1
    Mehdipatnam
    https://www.google.com/maps/@17.391764,78.4354326,15.75z/data=!5m1!1e1
    '''
    
    driver.get(f'https://www.google.com/maps/@{",".join(locations[location][0:3])}/data=!5m1!1e1' )

    try:
        waitgot = WebDriverWait(driver, 10)
        elem_gotit = waitgot.until(EC.element_to_be_clickable((By.XPATH, '//a[contains(@class, "gb_Kd gb_kd")]')))
        time.sleep(10)
        elem_gotit.click()
    except:
        print("Got it _ Not present")

    # Wait and click the menu button
    wait = WebDriverWait(driver, 10)
    elem1 = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[contains(@class, "searchbox-button")]')))
    time.sleep(10)
    elem1.click()
    # Wait and close the menu button
    wait2 = WebDriverWait(driver, 10)
    elem2 = wait2.until(EC.element_to_be_clickable((By.XPATH, '//button[contains(@class, "maps-sprite-settings-chevron-left")]')))
    time.sleep(10)
    elem2.click()
    time.sleep(10)

def write_on_image(text,imgname):
    img = Image.open(imgname)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', 40)
    draw.rectangle((0, 0, 460, 120), fill='black')
    draw.text((0, 0), text, (512, 512, 255), font=font)
    img.save(imgname)

while True:
    # timenow = datetime.now().strftime("%d-%b (%H:%M:%S.%f)")
    timenow = datetime.now().astimezone(pytz.timezone(f'{locations[location][-1]}')).strftime("%b %dth %H:%M")
    datepath = datetime.now().astimezone(pytz.timezone(f'{locations[location][-1]}')).strftime("%b-%dth")
    print('Current Timestamp : ', timenow)
    try:
        initiate()
    except:
        print("Problem loading the page. Timeout exception")
        time.sleep(120)
        continue

    img_storefolder =  f'{images_folder}{datepath}_{location}'
    if not os.path.exists(img_storefolder):os.mkdir(img_storefolder)
    driver.save_screenshot(f"{img_storefolder}/{timenow}.png"); time.sleep(2)
    write_on_image(timenow+f'\n{location}',f"{img_storefolder}/{timenow}.png")
    gifname = make_gif(sorted(glob(f'{img_storefolder}/*')),f'{datepath}_{location}')
    make_video(gifname,f'{datepath}_{location}')
    time.sleep(timeinterval)
