import json
import tiktoken
import undetected_chromedriver as uc
import time
from bs4 import BeautifulSoup, NavigableString, Tag
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyautogui
from PIL import Image
from typing import List
from bs4 import BeautifulSoup
import os
import requests
import base64
from openai import OpenAI
from pydantic import BaseModel
from selenium.webdriver.common.action_chains import ActionChains
import random



def skip_cloudflare(url:str= 'https://www.quora.com/',  ):


    driver = uc.Chrome(headless=False,use_subprocess=False,)

    driver.get(url)
    time.sleep(4)
    try:
        location = pyautogui.locateOnScreen('/Users/chenzi/project/zcbc/mofa/python/examples/search/scripts/agent_core/cloudflare_checkbox.png', confidence=0.8)  #
        if location:
            center = pyautogui.center(location)
            print(center)
            pyautogui.click(center)

            # pyautogui.click(center)
        else:
            print("Can't find location")
        print('end skip Cloudflare')
    except Exception as e:
        print(e)
        pass

    actions = ActionChains(driver)
    actions.move_by_offset(center.x, center.y).click().perform()

    wait = WebDriverWait(driver, 30)

    iframe = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, 'iframe[allow*="cross-origin-isolated"]')
    ))
    iframe = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, 'iframe[title="包含 Cloudflare 安全质询的小组件"]')
    ))
    driver.refresh()


    return driver



if __name__ == '__main__':
    search_text = 'qwen'
    html_source = skip_cloudflare(url='https://www.quora.com/')




