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
import pandas as pd
import re

# Your existing setup
options = webdriver.ChromeOptions()
options.add_argument("--user-data-dir=C:\\Temp\\ChromeProfile")
driver = webdriver.Chrome(options=options)

def human_like_scroll(driver, scroll_distance=50, iterations=100):
    for _ in range(iterations):
        driver.execute_script(f"window.scrollBy(0, {scroll_distance});")

        sleep_time = random.uniform(0.2, 1.2) 
        time.sleep(sleep_time)
        
        if random.random() < 0.1:
            time.sleep(random.uniform(1.5, 3))

def smooth_scroll(driver, scroll_distance=50, iterations=40):
    for _ in range(iterations):
        driver.execute_script(f"window.scrollBy(0, {scroll_distance});")
        time.sleep(0.005)

def detect_replies(html_content):

    match = re.search(r'aria-label="(\d+) Replies', html_content)

    if match:
        return int(match.group(1))
    else:
        return None

def get_org_comments(org_url):
    # Open the provided URL
    driver.get(org_url)
    
    # Define the end time for scrolling
    end_time = time.time() + 20  # 20 seconds from now
    
    seen_articles = set() 
    
    # Scroll until the end time is reached
    while time.time() < end_time:
        # Smoothly scroll a bit
        smooth_scroll(driver)
        
        # Wait for a random duration between scrolls to mimic human behavior
        time.sleep(random.uniform(1, 2)) 

        # Extract article data using BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        articles = soup.find_all('article')
        
        # Check for new articles and extract the specified part
        for article in articles:
            target_div = article.find('div', class_='css-1dbjc4n r-18u37iz r-1q142lx')
            if target_div:
                target_str = str(target_div)
                if target_str not in seen_articles:
                    seen_articles.add(target_str)
                    # Append new articles to the HTML file
                    with open('articles.html', 'a', encoding='utf-8') as file:
                        file.write(target_str)

    # Pause (you can adjust the duration as needed)
    time.sleep(random.uniform(5, 10))

# THIS FUNCTION IS ACCAPTABLE
# function 1.0
def extract_tweet_details(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract user details
    user_name_element = soup.find("span", {"class": "css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0"})
    user_name = user_name_element.text if user_name_element else None

    user_handle_element = soup.find("a", {"href": True, "role": "link", "tabindex": "-1"})
    user_handle = user_handle_element['href'] if user_handle_element else None

    try:
    # Extract tweet date
        tweet_date = soup.find("time").text
        timestamp = soup.find('time')['datetime']

        # Extract tweet content
        
        tweet_content_div = soup.find('div', {'data-testid': 'tweetText'})
        tweet_content = ' '.join([span.text for span in tweet_content_div.find_all('span', recursive=False)])
        # print(tweet_content)
        
        # tweet_content = soup.find("div", {"lang": "en"}).text

        # Extract tweet statistics
        replies = soup.find("div", {"data-testid": "reply"}).find("span").text
        retweets = soup.find("div", {"data-testid": "retweet"}).find("span").text
        likes = soup.find("div", {"data-testid": "like"}).find("span").text

        # Try to extract views with a more general selector
        views_element = soup.find("div", text=lambda t: "Views" in t if t else False)
        views = views_element.text if views_element else "N/A"
        
        return {
            "user_name": user_name,
            "user_handle": user_handle,
            "tweet_date": tweet_date,
            "timestamp": timestamp,
            "tweet_content": tweet_content,
            "replies": replies,
            "retweets": retweets,
            "likes": likes,
            # "views": views
        }
    except:
        print("Unable to extract tweet details, might not have the text")
        print(html_content)
        return None

def get_org_comments(org_id):
    org_url = f"https://twitter.com/{org_id}"
    driver.get(org_url)
    end_time = time.time() + 60*2

    seen_articles = set()
    all_articles_content = []
    all_comments_content = []
    Post_clicked = []

    while time.time() < end_time:
        smooth_scroll(driver)
        # human_like_scroll(driver)
        time.sleep(random.uniform(1, 2))

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        articles = soup.find_all('article')

        for article in articles:
            user_id_tag = article.find('span', class_='css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0')
            timestamp_tag = article.find('time')

            if user_id_tag and timestamp_tag:
                user_id = user_id_tag.text.strip()
                timestamp = timestamp_tag['datetime']
                print(f"User ID: {user_id}")
                print(f"Timestamp: {timestamp}")

                target_div = article.find('div', class_='css-1dbjc4n r-18u37iz r-1q142lx')
                if target_div:
                    target_a = target_div.find('a', href=re.compile(f"/{org_id}/status/"))
                    if target_a:
                        href_link = target_a['href']
                        if f"https://twitter.com{href_link}" in Post_clicked:
                            continue
                        datetime_str = timestamp
                        datetime_year = int(datetime_str.split('-')[0])
                        datetime_month = int(datetime_str.split('-')[1])

                        if datetime_year == 2023 and datetime_month <= 8:
                            print(f"Link: https://twitter.com{href_link}")
                            print(f"Time: {datetime_str}")
                            target_str = str(target_div)
                            if target_str not in seen_articles:
                                seen_articles.add(target_str)
                                all_articles_content.append(target_str)

                            # Click on the article link
                            try:
                                wait = WebDriverWait(driver, 10)
                                element_to_click = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, f'a[href="{href_link}"]')))
                                Post_clicked.append(f'https://twitter.com{href_link}')
                                element_to_click.click()
                            except:
                                driver.execute_script("arguments[0].click();", element_to_click)
                            time.sleep(2)

                            # Scroll for 10 seconds to gather all the comments
                            # smooth_scroll(driver, iterations=200)
                            # Extract the comments
                            
                            comments = set()
                            for _ in range(20):
                                smooth_scroll(driver)
                                time.sleep(random.uniform(4, 6))
                                comments_soup = BeautifulSoup(driver.page_source, 'html.parser')
                                for comment_element in comments_soup.find_all('article'):
                                    comments.add(comment_element)

                            comments_details = []
                            for comment in comments:
                                if extract_tweet_details(str(comment)) not in comments_details:
                                    comments_details.append(extract_tweet_details(str(comment)))
                            print(comments_details)
                            driver.back()
                            time.sleep(2)
                            break

    combined_soup = BeautifulSoup(''.join(all_articles_content), 'html.parser')
    prettified_content = combined_soup.prettify()

    with open('articles.html', 'w', encoding='utf-8') as file:
        file.write(prettified_content)

    combined_comments_soup = BeautifulSoup(''.join(all_comments_content), 'html.parser')
    prettified_comments = combined_comments_soup.prettify()

    with open('comments.html', 'w', encoding='utf-8') as file:
        file.write(prettified_comments)
    time.sleep(random.uniform(30, 40))

# Test the function
# get_org_comments('Cbse_official')
get_org_comments('')
