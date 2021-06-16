'''
    Implements web scrapping method to search existing images in Docker Hub
'''
__author__ = "Martin A. Guerrero Romero (marguerom1@alum.us.es)"

import time
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from selenium import webdriver
from selenium.webdriver.common.by import By

def getExistingImageNames(product,pv) -> list:
    '''
        Check if a product image with specific version exist in Docker Hub

        :param product: product of for in main.py execution

        :param pv: dictionary product-version(s) of CVE
    '''
    res = []

    windowS = Toplevel()
    windowS.title("Searching images")
    windowS.geometry('450x100')
    iconPath = "./img/iconMOZART.jpg"
    icon = ImageTk.PhotoImage(Image.open(iconPath))
    windowS.wm_iconphoto(False, icon)

    my_progress = ttk.Progressbar(windowS, orient=HORIZONTAL, length=300, mode='indeterminate')
    my_progress.pack(pady=20)
    my_progress.start(20)

    # Options modification to not open the browser
    options = webdriver.FirefoxOptions()
    options.headless = True
    options.add_argument('--no-sandbox')

    # Initialize driver
    driver = webdriver.Firefox(options=options)

    url = 'https://hub.docker.com/search?q='+product+'&type=image'
    index = 1
    values = pv.get(product)  
        
    # Get web page search of product, first page and total pages
    driver.get(url)
    time.sleep(3) # Browser needs time to load the page information
    pagination = driver.find_element(By.CSS_SELECTOR, ".styles__currentSearch___35kW_ > div:nth-child(1)").text
    totalPage = pagination.split()[4]
    actualPage = pagination.split()[2]

    while actualPage != totalPage and int(actualPage) <= 1000:
            
        for i in range(1,26):
            imageName = driver.find_element(By.CSS_SELECTOR, ".imageSearchResult:nth-child("+str(i)+") .styles__name___2198b").text
            if not ('/' in imageName and product in imageName.split('/')[0]):
                try:
                    description = driver.find_element(By.CSS_SELECTOR, ".imageSearchResult:nth-child("+str(i)+") .styles__description___1jeSI").text
                    # Checking if description has the version used
                    if any(value in description for value in values):
                        res.append(imageName)
                # Not all images have a description
                except: 
                    pass

        # Advance to the next page
        index += 1
        pagesUrl = 'https://hub.docker.com/search?q='+product+'&type=image&page='+str(index)
        driver.get(pagesUrl)
        time.sleep(3)
        actualPage = driver.find_element(By.CSS_SELECTOR, ".styles__currentSearch___35kW_ > div:nth-child(1)").text.split()[2]

        # Last page
        lastPage = driver.find_element(By.CSS_SELECTOR, ".styles__currentSearch___35kW_ > div:nth-child(1)").text.split()[0]
        gap = int(actualPage) - int(lastPage) + 1 # Increment by one because max_value of range is excluding

        for i in range(1,gap):
            try:
                description = driver.find_element(By.CSS_SELECTOR, ".imageSearchResult:nth-child("+str(i)+") .styles__description___1jeSI").text
                # Checking if description has the version used
                if any(value in description for value in values):
                    imageName = driver.find_element(By.CSS_SELECTOR, ".imageSearchResult:nth-child("+str(i)+") .styles__name___2198b").text
                    res.append(imageName)
            # Not all images have a description
            except: 
                pass
    
    # Closing driver
    driver.quit()

    windowS.destroy()

    return res