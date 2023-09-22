from selenium import webdriver
from msedge.selenium_tools import EdgeOptions

# beautiful suop
from bs4 import BeautifulSoup

import os
import time
import random

# data transformation
import json
import pandas as pd

# get data with pattern
import re


from selenium import webdriver
from selenium.webdriver.edge.service import Service

# initialize edge options
edge_options = webdriver.EdgeOptions()

# add user data directory argument
edge_options.add_argument("--user-data-dir=/tmp/edgeprofile")

# initialize edge driver
driver = webdriver.Edge(service=Service(executable_path="/home/saket/path/msedgedriver"), options=edge_options)


# # # Your existing setup
# # options = webdriver.EdgeOptions()
# # options.add_argument("--user-data-dir=/tmp/edgeprofile")
# # initialize edge options
# edge_options = webdriver.EdgeOptions()

# # add user data directory argument
# edge_options.add_argument("--user-data-dir=/tmp/edgeprofile")

# # initialize edge driver
# driver = webdriver.Edge(service=Service(executable_path="/home/saket/path/msedgedriver"), options=edge_options)

# driver = webdriver.Edge(options=options)

def human_like_scroll(driver, scroll_distance=50, iterations=100):
    """Simulate a human-like scrolling behavior."""
    for _ in range(iterations):
        driver.execute_script(f"window.scrollBy(0, {scroll_distance});")

        sleep_time = random.uniform(0.2, 1.2) 
        time.sleep(sleep_time)
        
        if random.random() < 0.1:
            time.sleep(random.uniform(1.5, 3))

def human_like_scroll(driver, iterations=500):
    """Simulate a human-like scrolling behavior."""
    
    time.sleep(random.gauss(0.5, 0.1))
    
    for _ in range(random.randint(iterations // 2, iterations)):
        scroll_distance = int(random.gauss(100, 30))
        
        for _ in range(random.randint(10, 20)):
            chunk_distance = scroll_distance // 4
            driver.execute_script(f"window.scrollBy(0, {chunk_distance});")
            time.sleep(random.uniform(0.01, 0.05))
        
        time.sleep(random.randint(1, 3))
        
        if random.random() < 0.1:
            driver.execute_script(f"window.scrollBy(0, {-int(random.gauss(30, 10))});")
        
        if random.random() < 0.001:
            time.sleep(random.gauss(4, 2))
        
        if random.randint(1, 5)==1:
            time.sleep(random.uniform(30))
        
        if random.random() < 0.02:
            break

from selenium import webdriver
from msedge.selenium_tools import EdgeOptions
# beautiful suop
from bs4 import BeautifulSoup

import os
import time
import random

# data transformation
import json
import pandas as pd

# get data with pattern
import re


# # Your existing setup
# options = webdriver.EdgeOptions()
# options.add_argument("--user-data-dir=/tmp/edgeprofile")
# initialize edge options
edge_options = webdriver.EdgeOptions()

# add user data directory argument
edge_options.add_argument("--user-data-dir=/tmp/edgeprofile")

# initialize edge driver
driver = webdriver.Edge(service=Service(executable_path="/home/saket/path/msedgedriver"), options=edge_options)

# driver = webdriver.Edge(options=options)


def human_like_scroll(driver, scroll_distance=50, iterations=100):
    """Simulate a human-like scrolling behavior."""
    for _ in range(iterations):
        driver.execute_script(f"window.scrollBy(0, {scroll_distance});")

        sleep_time = random.uniform(0.2, 1.2) 
        time.sleep(sleep_time)
        
        if random.random() < 0.1:
            time.sleep(random.uniform(1.5, 3))



# THIS FUNCTION IS ACCAPTABLE
# function 1.0
def extract_tweet_details(html_content, searchLink, app_name):
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
            "search_link":searchLink,
            "user_name": user_name,
            "user_handle": user_handle,
            "tweet_date": tweet_date,
            "timestamp": timestamp,
            "tweet_content": tweet_content,
            "replies": replies,
            "retweets": retweets,
            "likes": likes,
            "app": app_name
            # "views": views
        }
    except:
        print("Unable to extract tweet details, might not have the text")
        print(html_content)
        return None
    

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

# version 2.0
def twitter_search(hashtags):
    base_url = "https://twitter.com/search?q="
    end_url = "&src=typed_query&f=top"
    
    hashtag_list = hashtags.split()
    formatted_hashtags = "%20".join(["%23" + tag.replace("#", "") for tag in hashtag_list])
    
    return base_url + formatted_hashtags + end_url

# version 3.0
def twitter_search(hashtag):
    base_url = "https://twitter.com/search?q="
    end_url = "&src=typed_query"
    formatted_hashtag = "%23" + hashtag.replace("#", "").replace(" ", "%20")
    return base_url + formatted_hashtag + end_url

def twitter_search(hashtags):
    base_url = "https://twitter.com/search?q="
    end_url = "&src=typed_query&f=top"
    formatted_hashtags = " ".join(["%23" + tag.replace("#", "") for tag in hashtags.split()])
    return base_url + formatted_hashtags.replace(" ", "%20") + end_url


def get_org_comments_for_the_hashtag(hashtag, app_name
                                     ):
    searchLink = twitter_search(hashtag)
    driver.get(searchLink)
    # end_time = time.time() + 60*2

    all_comments_content = set()

    last_height = driver.execute_script("return document.body.scrollHeight")
    
    while True:
        # Scroll down
        for _ in range(500):
            driver.execute_script(f"window.scrollBy(0, {50});")
            
            sleep_time = random.uniform(0.02, 0.0012) 
            time.sleep(sleep_time)
            
            # if random.random() < 0.1:
            #     time.sleep(random.uniform(1.5, 3))
        # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(random.uniform(4, 6))

        # Extract comments after scrolling
        comments_soup_all = set()
        comments_soup = BeautifulSoup(driver.page_source, 'html.parser')
        for comment_element in comments_soup.find_all('article'):
            comment_detail = extract_tweet_details(str(comment_element), searchLink, app_name)
            if comment_detail not in all_comments_content:
                all_comments_content.add(comment_detail)
                with open('data-232.txt', 'a', encoding='utf-8') as file:
                    file.write(str(comment_detail) + ',')

        # logic to scroll till the end
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    
    # Saving to JSON
    with open(f'{hashtag}.json', 'w', encoding='utf-8') as json_file:
        json.dump(all_comments_content, json_file, ensure_ascii=False, indent=4)

    # combined_soup = BeautifulSoup(''.join(all_comments_content), 'html.parser')
    # prettified_content = combined_soup.prettify()

# try:
# SaketThaku5099
# PwM.BhR9-Tkz4CN
input('signed in?: ')

# Hashes_search = "#Adityabirlahealthinsurance"
# org = "Aditya Birla"



""" UPI"""
#UPI

#UPI #Compaint #BHIM --- didn't show my any results

Hashes_search = """
#digitalpayments #risk
"""
organization =  "digitalpayments"
Hashes_search = Hashes_search.strip()

# searchLink = "https://twitter.com/search?q=%23phonepe%20refund&src=typed_query"
#Phonepe #fraud
get_org_comments_for_the_hashtag(Hashes_search, organization)

# # try:
# Hashes_search = input('Hashes Search:')
# org = input('org/company/source')

# get_org_comments_for_the_hashtag(Hashes_search, org)
# except Exception as e:
#     print("An error occurred:", e)
#     time.sleep(1000) 

# THIS FUNCTION IS ACCAPTABLE
# function 1.0
def extract_tweet_details(html_content, searchLink, app_name):
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
            "search_link":searchLink,
            "user_name": user_name,
            "user_handle": user_handle,
            "tweet_date": tweet_date,
            "timestamp": timestamp,
            "tweet_content": tweet_content,
            "replies": replies,
            "retweets": retweets,
            "likes": likes,
            "app": app_name
            # "views": views
        }
    except:
        print("Unable to extract tweet details, might not have the text")
        print(html_content)
        return None
    

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

# version 2.0
def twitter_search(hashtags):
    base_url = "https://twitter.com/search?q="
    end_url = "&src=typed_query&f=top"
    
    hashtag_list = hashtags.split()
    formatted_hashtags = "%20".join(["%23" + tag.replace("#", "") for tag in hashtag_list])
    
    return base_url + formatted_hashtags + end_url

# version 3.0
def twitter_search(hashtag):
    base_url = "https://twitter.com/search?q="
    end_url = "&src=typed_query"
    formatted_hashtag = "%23" + hashtag.replace("#", "").replace(" ", "%20")
    return base_url + formatted_hashtag + end_url

def twitter_search(hashtags):
    base_url = "https://twitter.com/search?q="
    end_url = "&src=typed_query&f=top"
    formatted_hashtags = " ".join(["%23" + tag.replace("#", "") for tag in hashtags.split()])
    return base_url + formatted_hashtags.replace(" ", "%20") + end_url


def get_org_comments_for_the_hashtag(hashtag, app_name):
    searchLink = twitter_search(hashtag)
    driver.get(searchLink)
    # end_time = time.time() + 60*2

    all_comments_content = set()

    last_height = driver.execute_script("return document.body.scrollHeight")
    
    while True:
        # Scroll down
        for _ in range(500):
            driver.execute_script(f"window.scrollBy(0, {50});")
            
            sleep_time = random.uniform(0.02, 0.0012) 
            time.sleep(sleep_time)
            
            # if random.random() < 0.1:
            #     time.sleep(random.uniform(1.5, 3))
        # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(random.uniform(4, 6))

        # Extract comments after scrolling
        comments_soup_all = set()
        comments_soup = BeautifulSoup(driver.page_source, 'html.parser')
        for comment_element in comments_soup.find_all('article'):
            comment_detail = extract_tweet_details(str(comment_element), searchLink, app_name)
            if comment_detail not in all_comments_content:
                all_comments_content.add(comment_detail)
                with open('data-232.txt', 'a', encoding='utf-8') as file:
                    file.write(str(comment_detail) + ',')

        # logic to scroll till the end
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    
    # Saving to JSON
    with open(f'{hashtag}.json', 'w', encoding='utf-8') as json_file:
        json.dump(all_comments_content, json_file, ensure_ascii=False, indent=4)

    # combined_soup = BeautifulSoup(''.join(all_comments_content), 'html.parser')
    # prettified_content = combined_soup.prettify()

# try:
# SaketThaku5099
# PwM.BhR9-Tkz4CN
input('signed in?: ')

# Hashes_search = "#Adityabirlahealthinsurance"
# org = "Aditya Birla"



""" UPI"""
#UPI

#UPI #Compaint #BHIM --- didn't show my any results

Hashes_search = """
#digitalpayments #risk
"""
organization =  "digitalpayments"
Hashes_search = Hashes_search.strip()

# searchLink = "https://twitter.com/search?q=%23phonepe%20refund&src=typed_query"
#Phonepe #fraud
get_org_comments_for_the_hashtag(Hashes_search, organization)

# # try:
# Hashes_search = input('Hashes Search:')
# org = input('org/company/source')

# get_org_comments_for_the_hashtag(Hashes_search, org)
# except Exception as e:
#     print("An error occurred:", e)
#     time.sleep(1000) 

