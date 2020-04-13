import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from datetime import datetime
import numpy as np
import pandas as pd
import pytz
import json
import matplotlib.pyplot as plt
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import sys, os
from glob import glob
import moviepy.editor as mp
from moviepy.editor import *

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
pixels = {
    'low': [99, 214, 104],
    'med': [255, 151, 77],
    'high': [242, 60, 50],
    'vhigh': [129, 31, 31]
}
basepixels = {
    'roads':[255,255,255],
    'highways':[255,242,175]
}

driver.set_window_size(width, height)
#driver = webdriver.Chrome()

locations = dict()
with open('locations.json') as json_file:
    locations = json.load(json_file)


location = sys.argv[1] #'NH27-Part2'

log = 'log/' + location
if not os.path.exists(log):os.makedirs(log, exist_ok=True)
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

def make_mp4(imgli,datepath,bar=False):
    if bar==False:clips = [ImageClip(m).set_duration(0.1) for m in imgli if not (os.path.basename(m)).startswith('bar_') ]
    else:clips = [ImageClip(m).set_duration(0.1) for m in imgli]
    concat_clip = concatenate_videoclips(clips, method="compose")
    if bar: concat_clip.write_videofile(f"{videos_folder}barvid_{datepath}.mp4", fps=24) 
    else: concat_clip.write_videofile(f"{videos_folder}vid_{datepath}.mp4", fps=24)

def make_bar_graph(logfilename,storedbarname):
    df = pd.read_csv(f"{logfilename}")
    vals = df.values.tolist()
    num_bars = df.shape[0]
    heads = ['notraffic','mild','med','high','vhigh']
    for ix in range(num_bars):
        fig = plt.figure()
        emptyroads = vals[ix][1] - sum(vals[ix][2:])
        data = [emptyroads] + vals[ix][2:]
        plt.bar(heads,data)
        plt.title(f"{vals[ix][0]}")
        plt.savefig(storedbarname)
        plt.close()

def initiate(baseimage=False):

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
    if baseimage:
        driver.get(f'https://www.google.com/maps/@{",".join(locations[location][0:3])}' )
    else:
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

baseimagedict={}
totalroadpixels = 0

def pixel_density(path, pixels, timestamp,datepath):
    img = np.array(Image.open(path).convert('RGB'))
    w,h,_ = img.shape
    d = {
            'pixels': totalroadpixels,
            'ts': timestamp
        }

    for n,v in pixels.items():
        d[n] = (np.all(img == v, axis=2)).sum()

    imgpath = os.path.basename(path).replace(".png","")

    headerflag = False
    if not os.path.exists(f'{log}/{datepath}_log.csv'): headerflag = True

    logfilename = f'{log}/{datepath}_log.csv'
    with open(logfilename, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['ts', 'pixels', 'low', 'med', 'high', 'vhigh'])
        if headerflag:  writer.writeheader()
        writer.writerow(d)
    
    return logfilename

basecheck = True

while True:
    # timenow = datetime.now().strftime("%d-%b (%H:%M:%S.%f)")
    timenow = datetime.now().astimezone(pytz.timezone(f'{locations[location][-1]}')).strftime("%b %dth %H:%M")
    datepath = datetime.now().astimezone(pytz.timezone(f'{locations[location][-1]}')).strftime("%b-%dth")
    print('Current Timestamp : ', timenow)
    try:
        if basecheck: initiate(baseimage=True)
        else: initiate()
    except:
        print("Problem loading the page. Timeout exception")
        time.sleep(120)
        continue

    img_storefolder =  f'{images_folder}{datepath}_{location}'
    
    if not os.path.exists(img_storefolder):os.mkdir(img_storefolder)
    
    if basecheck: storedimagename = f"{img_storefolder}/baseimage.png"
    else:storedimagename = f"{img_storefolder}/{timenow}.png"
    driver.save_screenshot(storedimagename); time.sleep(2)
    
    write_on_image(timenow+f'\n{location}',storedimagename)
    
    if basecheck: 
        img = np.array(Image.open(f"{img_storefolder}/baseimage.png").convert('RGB'))

        for n,v in basepixels.items():
            baseimagedict[n] = (np.all(img == v, axis=2)).sum()
            totalroadpixels += baseimagedict[n]

        basecheck=False
    else:
        logfilename = pixel_density(f"{img_storefolder}/{timenow}.png", pixels, timenow, datepath)
        storedbarname = f"{img_storefolder}/bar_{timenow}.png"
        make_bar_graph(logfilename,storedbarname)
        # gifname = make_gif(sorted(glob(f'{img_storefolder}/*')),f'{datepath}_{location}')
        # make_video(gifname,f'{datepath}_{location}')
        make_mp4(sorted(glob(f'{img_storefolder}/bar_*')),f'{datepath}_{location}',bar=True)
        make_mp4(sorted(glob(f'{img_storefolder}/*')),f'{datepath}_{location}')


    time.sleep(timeinterval)
