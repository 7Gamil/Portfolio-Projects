import pandas as pd
import pyautogui
from PIL import Image
import requests
from io import BytesIO
import time
import subprocess
from my_package import utils
from datetime import datetime
from urllib.parse import quote
import os

file_name = "Walmart sample empty.csv" # <-- Edit this
df = pd.read_csv(file_name)

i = 0 # start from index 0
y = 10 # end at index 9

while i < y:
    i += 1
    print("start row", i)

    if not df.isna().iloc[i, 2]:
        continue

    product_name = quote(df.iloc[i, 0], safe='')
    product_url = df.iloc[i, 1]

    # if image URL
    if "http" in product_url or "www" in product_url:
        # Download the reference image
        response = requests.get(product_url)
        reference_image = Image.open(BytesIO(response.content))
        reference_image.save('reference_image.png')
        reference_image = 'reference_image.png'
    # else image path
    else:
        reference_image_cmp = Image.open(product_url)
        reference_image_cmp.save('reference_image.png')


    target_web = "https://www.walmart.ca/" # <-- Edit this
    search_url = "https://www.google.com/search?q=site:" +  target_web + " " + product_name + "&btnI"

    # Open Chrome and show first result in google search
    #subprocess.Popen(['google-chrome', search_url]) # for chrome
    subprocess.Popen(['brave-browser', search_url]) # for Brave
    time.sleep(3)

    title = subprocess.check_output(
        ['xdotool', 'getwindowfocus', 'getwindowname']).decode('utf-8').strip()

    if not "btnI" in title:
        pyautogui.press('tab')
        time.sleep(0.5)
        pyautogui.press('enter')
        time.sleep(7)
    else:
        print("Google Block")
        print("Try to bypass reCHPATCA")

        # bypass reCHPATCA using addon "Buster: Captcha Solver for Humans"
        pyautogui.press('tab')
        time.sleep(0.7)
        pyautogui.press('enter')
        time.sleep(2)
        pyautogui.press('tab')
        time.sleep(0.7)
        pyautogui.press('tab')
        time.sleep(0.7)
        pyautogui.press('enter')
        time.sleep(7)
        pyautogui.hotkey('ctrl', 'w')
        i -= 1  # retry last step again
        continue

    comparator = utils.DeepImageComparator()

    
    max_s = 0.81 # threshold
    product_region = (260, 380, 650, 630)  # Image coordinates (left, top, width, height) # <-- Edit this
    screen_image = utils.take_screenshot(product_region) # Take screenshot
    screen_image.save('screen_image.png')
    result = comparator.compare_images('reference_image.png', 'screen_image.png')
    
    # Only with Walmart
    result_block = comparator.compare_images('reference_image_block.png', 'screen_image.png') 
    if result_block >= 0.99:
        print("walmart======")
        print(result_block)
        df.iloc[i-2, 3] = "walmart Blocked"
        pyautogui.hotkey('ctrl', 'w')
        time.sleep(60)
        i -= 1 # wait 1 minute and retry last step again
        continue

    if result > max_s:
        print("found in===", result, max_s)
        max_s = result
        print("found in", max_s)
        Got_UPC = utils.find_UPC()
        print(Got_UPC)
        df.iloc[i, 2] = Got_UPC
        df.iloc[i, 3] = max_s
    else:
        df.iloc[i, 2] = "Not Found"
        print("Not Found")


    pyautogui.hotkey('ctrl', 'w')

    df.to_csv(file_name, index=False)  # Update the file

    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y_%H-%M-%S")
    if now.minute % 10 == 0:
        # Backup every 10 minutes
        df.to_csv(dt_string + "_" + file_name, index=False)
        # Remove browser cache every 10 minutes for brave browser
        #os.system('rm -r ~/.config/BraveSoftware/Brave-Browser/DeferredBrowserMetrics')

    time.sleep(0.5)
