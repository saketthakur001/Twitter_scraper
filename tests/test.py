from selenium import webdriver
from selenium.webdriver.chrome.options import Options as chromeOptions
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import os
import time
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import re
import pandas as pd

# Your existing setup
options = webdriver.ChromeOptions()
options.add_argument("--user-data-dir=C:\\Temp\\ChromeProfile")
driver = webdriver.Chrome(options=options)

def smooth_scroll(driver, scroll_distance=50, iterations=40):
    """Smoothly scroll the page by a certain distance."""
    for _ in range(iterations):
        driver.execute_script(f"window.scrollBy(0, {scroll_distance});")
        time.sleep(0.005)  # Reduced sleep to make scrolling faster

def get_org_comments(org_id):

    #org url
    org_url = f"https://twitter.com/{org_id}"

    # Open the provided URL
    driver.get(org_url)
    
    # Define the end time for scrolling
    end_time = time.time() + 20  # 20 seconds from now
    
    seen_articles = set()  # To keep track of articles we've already seen
    all_articles_content = []  # To store all the articles' content

    # Scroll until the end time is reached
    while time.time() < end_time:
        # Smoothly scroll a bit
        smooth_scroll(driver)
        
        # Wait for a random duration between scrolls to mimic human behavior
        time.sleep(random.uniform(1, 2))  # Reduced sleep between scrolls for faster scrolling
        
        # Extract article data using BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        articles = soup.find_all('article')
        
        # Check for new articles and extract the specified part
        for article in articles:
            target_div = article.find('div', class_='css-1dbjc4n r-18u37iz r-1q142lx')
            if target_div:
                target_a = target_div.find('a', href=re.compile(f"/{org_id}/status/"))
                if target_a:
                    target_str = str(target_div)
                    if target_str not in seen_articles:
                        seen_articles.add(target_str)
                        all_articles_content.append(target_str)

    # Prettify the combined articles content using BeautifulSoup
    combined_soup = BeautifulSoup(''.join(all_articles_content), 'html.parser')
    prettified_content = combined_soup.prettify()

    # Save the prettified content to the HTML file
    with open('articles.html', 'w', encoding='utf-8') as file:
        file.write(prettified_content)

    # Pause (you can adjust the duration as needed)
    time.sleep(random.uniform(5, 10))  # Reduced pausing time after scrolling

# Test the function
get_org_comments('NASA')
