'''
    Implements web scrapping methods to search existing images in Docker Hub
'''
__author__ = "Martin A. Guerrero Romero (marguerom1@alum.us.es)"

from bs4 import BeautifulSoup
import requests
import webbrowser

import time
from selenium import webdriver

def getExistingImageNames(pv) -> list:
    '''
        Check if a product image with specific version exist in Docker Hub

        :param pv: dictionary product-version(s) of CVE
    '''
    res = []

    for product in pv.keys():
        
        url = 'https://hub.docker.com/search?q='+product+'&type=image'
        #webbrowser.open(url, new=2)

        # Intento FALLIDO de Web Scrapping
        resp = requests.get(url, timeout=5)
        cont = BeautifulSoup(resp.content,"lxml")
        #print(cont)

        driver = webdriver.Firefox()
        driver.get(url)
        time.sleep(3)
        htmlSource = driver.page_source
        print(htmlSource)

    return res