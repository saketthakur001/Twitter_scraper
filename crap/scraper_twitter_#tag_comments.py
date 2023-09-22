import json
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

def save_to_json_for_post(data, post_link):
    """Save the given data to a JSON file named after the post's link."""
    print(data) 
    # Convert the post link to a suitable filename
    filename = post_link.split('/')[-1] + '.json'
    
    # Write data to the JSON file
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

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


def save_to_json(data, filename='data.json'):
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as file:
            existing_data = json.load(file)
    else:
        existing_data = []

    existing_data.extend(data)

    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(existing_data, file, ensure_ascii=False, indent=4)


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
    time.sleep(random.uniform(5, 10))  # Reduced pausing time after scrolling

# THIS FUNCTION IS ACCAPTABLE
# function 1.0
def extract_tweet_details(html_content, link, org_id):
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
            "post_link":link,
            "user_name": user_name,
            "user_handle": user_handle,
            "tweet_date": tweet_date,
            "timestamp": timestamp,
            "tweet_content": tweet_content,
            "replies": replies,
            "retweets": retweets,
            "likes": likes,
            "org": org_id
            # "views": views
        }
    except:
        print("Unable to extract tweet details, might not have the text")
        print(html_content)
        return None

def save_to_json(data, filename='data.json'):
    """Save the given data to a JSON file."""
    # Load existing data, if the file exists
    # file_name = str(random.uniform(0,100))
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as file:
            existing_data = json.load(file)
    else:
        existing_data = []

    # Append new data to existing data
    existing_data.extend(data)

    # Write combined data to the JSON file
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(existing_data, file, ensure_ascii=False, indent=4)

def twitter_search(query, filter_by="top"):
    base_url = "https://twitter.com/search?q="
    
    if not query.startswith('#'):
        query = "%23" + query
    else:
        query = "%23" + query[1:]
    
    end_url = "&src=typed_query"
    if filter_by == "latest":
        end_url += "&f=live"
    elif filter_by == "top":
        end_url += "&f=top"
    
    return base_url + query + end_url

def twitter_search(hashtag):
    base_url = "https://twitter.com/search?q=%23"
    end_url = "&src=typed_query&f=top"
    
    return base_url + hashtag + end_url

def twitter_search(hashtags):
    base_url = "https://twitter.com/search?q="
    end_url = "&src=typed_query&f=top"
    formatted_hashtags = " ".join(["%23" + tag.replace("#", "") for tag in hashtags.split()])
    return base_url + formatted_hashtags.replace(" ", "%20") + end_url

def twitter_search(hashtags):
    base_url = "https://twitter.com/search?q="
    end_url = "&src=typed_query&f=top"
    formatted_hashtags = " ".join(["%23" + tag.replace("#", "") for tag in hashtags.split()])
    return base_url + formatted_hashtags.replace(" ", "%20") + end_url

# search_url = twitter_search("hdfcloan")

import json

def get_org_comments_for_the_hashtag(hashtag):
    driver.get()
    end_time = time.time() + 60*2

    all_comments_content = []

    last_height = driver.execute_script("return document.body.scrollHeight")
    
    while True:
        # Scroll down
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(random.uniform(4, 6))

        # Extract comments after scrolling
        comments_soup = BeautifulSoup(driver.page_source, 'html.parser')
        for comment_element in comments_soup.find_all('article'):
            comment_detail = extract_tweet_details(str(comment_element), f"https://twitter.com{href_link}", org_id)
            if comment_detail not in all_comments_content:
                all_comments_content.append(comment_detail)
                with open('data-232.txt', 'a', encoding='utf-8') as file:
                    file.write(str(comment_detail) + ',')
                
        # Check if the scroll height remains unchanged after scrolling (indicating end of page)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    
    # Saving to JSON
    with open('comments_data.json', 'w', encoding='utf-8') as json_file:
        json.dump(all_comments_content, json_file, ensure_ascii=False, indent=4)

    combined_soup = BeautifulSoup(''.join(all_comments_content), 'html.parser')
    prettified_content = combined_soup.prettify()



                        # print("  Done  "**100)
    # save_to_json(all_comments_content)

    # combined_soup = BeautifulSoup(''.join(all_articles_content), 'html.parser')
    # prettified_content = combined_soup.prettify()

    # with open('articles.html', 'w', encoding='utf-8') as file:
    #     file.write(prettified_content)

    # combined_comments_soup = BeautifulSoup(''.join(all_comments_content), 'html.parser')
    # prettified_comments = combined_comments_soup.prettify()

    # with open('comments.html', 'w', encoding='utf-8') as file:
    #     file.write(prettified_comments)
    # time.sleep(random.uniform(30, 40))

# Test the function
# get_org_comments('Cbse_official')
get_org_comments_for_the_hashtag('IRDA')
