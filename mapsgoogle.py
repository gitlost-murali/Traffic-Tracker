import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from datetime import datetime
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import sys, os
from glob import glob
# Reference : 
# https://stackoverflow.com/questions/41340792/change-google-map-web-page-with-selenium-python
# https://stackoverflow.com/questions/18869365/a-watermark-inside-a-rectangle-which-filled-the-certain-color

images_folder = 'images/'
if not os.path.exists(images_folder):os.mkdir(images_folder)
# Load the page
driver = webdriver.Chrome()

locations = dict()
locations['Yousufguda'] = 'https://www.google.com/maps/@17.4374383,78.4322134,16.75z/data=!5m1!1e1' 
locations['HSR Layout'] = 'https://www.google.com/maps/@12.9185707,77.6398468,17z/data=!5m1!1e1' 
locations['Ameerpet'] = 'https://www.google.com/maps/@17.4350442,78.4339125,15.5z/data=!5m1!1e1'
locations['Mehdipatnam'] = 'https://www.google.com/maps/@17.391764,78.4354326,15.75z/data=!5m1!1e1'

location = 'Mehdipatnam'
locationurl = locations[location]

import imageio 
def make_gif(imagesli,datepath):
    with imageio.get_writer(f'analysis_{datepath}.gif', mode='I',duration=0.1) as writer: 
        # image = imageio.imread(filename)
        # writer.append_data(image) 
        for filename in imagesli: 
            image = imageio.imread(filename)
            writer.append_data(image) 

def initiate():

    '''
    yousufguda_location 
    'https://www.google.com/maps/@17.4374383,78.4322134,16.75z/data=!5m1!1e1'
    HSR Layout location
    https://www.google.com/maps/@12.9185707,77.6398468,17z/data=!5m1!1e1
    Jubilee
    https://www.google.com/maps/@17.4350442,78.4339125,15.5z/data=!5m1!1e1
    Mehdipatnam
    https://www.google.com/maps/@17.391764,78.4354326,15.75z/data=!5m1!1e1
    '''
    
    driver.get(locationurl)

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
    wait2 = WebDriverWait(driver, 10)
    elem2 = wait2.until(EC.element_to_be_clickable((By.XPATH, '//button[contains(@class, "maps-sprite-settings-chevron-left")]')))
    time.sleep(10)
    elem2.click()
    time.sleep(10)

def write_on_image(text,imgname):
    img = Image.open(imgname)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', 40)
    draw.rectangle((0, 0, 400, 80), fill='black')
    draw.text((0, 0), text, (512, 512, 255), font=font)
    img.save(imgname)

while True:
    # timenow = datetime.now().strftime("%d-%b (%H:%M:%S.%f)")
    timenow = datetime.now().strftime("%H:%M_%b-%dth")
    datepath = datetime.now().strftime("%b-%dth")
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
    make_gif(sorted(glob(f'{img_storefolder}/*')),f'{datepath}_{location}')
    # make_gif(f"{images_folder}{datepath}/{timenow}.png",datepath)

    time.sleep(240)
