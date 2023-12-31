from selenium import webdriver

# beautiful suop
from bs4 import BeautifulSoup

import os
import time
import random

# data transformation
import json
import csv

# get data with pattern
import re



# Your existing setup
options = webdriver.EdgeOptions()
options.add_argument("--user-data-dir=/tmp/edgeprofile")

driver = webdriver.Edge(options=options)


def human_like_scroll(driver, scroll_distance=50, iterations=100):
    """Simulate a human-like scrolling behavior."""
    for _ in range(iterations):
        driver.execute_script(f"window.scrollBy(0, {scroll_distance});")

        sleep_time = random.uniform(0.2, 1.2) 
        time.sleep(sleep_time)
        
        if random.random() < 0.1:
            time.sleep(random.uniform(1.5, 3))

def human_like_scroll(driver, iterations=10):
    """Simulate a human-like scrolling behavior."""

    time.sleep(abs(random.gauss(0.5, 0.1)))

    for _ in range(random.randint(iterations // 2, iterations)):
        scroll_distance = int(abs(random.gauss(100, 30)))
        
        for _ in range(random.randint(10, 20)):
            chunk_distance = scroll_distance // 4
            driver.execute_script(f"window.scrollBy(0, {chunk_distance});")
            time.sleep(random.uniform(0.01, 0.05))
        
        time.sleep(random.randint(1, 3))
        
        if random.random() < 0.1:
            driver.execute_script(f"window.scrollBy(0, {-int(random.gauss(30, 10))});")
        
        if random.random() < 0.001:
            time.sleep(abs(random.gauss(4, 2)))
        
        if random.randint(1, 5)==1:
            time.sleep(random.randint(1, 4))
        
        if random.randint(1, 10000)==1:
            time.sleep(random.randint(30, 60*2))

        if random.random() < 0.02:
            break

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
        # print(html_content)
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
def twitter_search_v2(hashtags):
    base_url = "https://twitter.com/search?q="
    end_url = "&src=typed_query&f=top"
    
    hashtag_list = hashtags.split()
    formatted_hashtags = "%20".join(["%23" + tag.replace("#", "") for tag in hashtag_list])
    
    return base_url + formatted_hashtags + end_url

def get_org_comments_for_the_hashtag(hashtag, app_name):
    # searchLink = twitter_search(hashtag)
    # searchLink = "https://twitter.com/search?q=%23upipin&src=typed_query"
    searchLink = twitter_search_v2(hashtag)
    driver.get(searchLink)
    # end_time = time.time() + 60*2

    all_comments_content = []
    # all_comments_content_no_dublicates = set()
    fields = ['search_link', 'user_name', 'user_handle', 'tweet_date', 'timestamp', 'tweet_content', 'replies', 'retweets', 'likes', 'app']

    # last_height = driver.execute_script("return document.body.scrollHeight")
    # ran = random.uniform(1, 2)
    ran = 1328123918231
    with open(f'twitter_comments_csv{hashtag} from {technology}.csv','a', newline='', encoding='utf-8') as csvfile:
        csvWriter = csv.DictWriter(csvfile, fieldnames=fields)
        csvWriter.writeheader()
        while True:
            # Scroll down
            time.sleep(random.uniform(2, 4))
            comments_soup = BeautifulSoup(driver.page_source, 'html.parser')
            # print('finaly working')
            # print(comments_soup)
            for comment_element in comments_soup.find_all('article'):
                comment_detail = extract_tweet_details(str(comment_element), searchLink, app_name)
                print(comment_element)
                if comment_detail not in all_comments_content:
                        print('got a comment') 
                        # try:
                        #     open(f'twitter_comments_data-{ran}.csv', 'a', encoding='utf-8')
                        # except:
                        #     open(f'twitter_comments_data-{ran}.csv', 'x', encoding='utf-8')

                        # with open(f'twitter_comments_csv{hashtag}.csv','a', newline='', encoding='utf-8') as csvfile:
                            
                        if comment_detail != None:
                            csvWriter.writerow(comment_detail)
                        # if comment_detail not in all_comments_content_no_dublicates:
                        with open(f'twitter_comments_data-{ran}hindi.txt', 'a', encoding='utf-8') as file:
                            file.write(str(comment_detail) + ',\n')
                        # all_comments_content_no_dublicates.add(comment_detail)
                        all_comments_content.append(comment_detail)
            human_like_scroll(driver)

    # while True:
                    # with open('data-232.txt', 'a', encoding='utf-8') as file:
                        # file.write(str(comment_detail) + ',')

        # logic to scroll till the end
        # new_height = driver.execute_script("return document.body.scrollHeight")
        # if new_height == last_height:
        #     break
        # last_height = new_height
    
    # Saving to JSON
    # with open(f'{hashtag}.json', 'w', encoding='utf-8') as json_file:
    #     json.dump(all_comments_content, json_file, ensure_ascii=False, indent=4)

    # combined_soup = BeautifulSoup(''.join(all_comments_content), 'html.parser')
    # prettified_content = combined_soup.prettify()

# try:
# input('signed in?: ')

# Hashes_search = "#Adityabirlahealthinsurance"
# org = "Aditya Birla"

# SaketThaku5099
# PwM.BhR9-Tkz4CN

# Hashes_search = "
technology =  "Net Banking"
hashtag = "#digitalbanking"
get_org_comments_for_the_hashtag(hashtag, technology)

# # try:
# Hashes_search = input('Hashes Search:')
# org = input('org/company/source')

# get_org_comments_for_the_hashtag(Hashes_search, org)
# except Exception as e:
#     print("An error occurred:", e)
#     time.sleep(1000) 


#netbanking #internetbanking
#phonebanking
#mobilebanking
#onlinebanking
#digitalbanking


# Technology payment hashtags
#
# UPI
#
# upi, upitransaction, upitransactions, upipayment, upipayments, upiindia, upipin
#
# Net Banking
#
# netbanking, internetbanking, phonebanking, mobilebanking, onlinebanking, digitalbanking
#
# Debit Card / Credit Card
#
# card, debitcard, creditcard, cardpayment, cardpayments, atm, atmcard, atmcards
#
# Point of Sale (PoS)
#
# pos, posmachine, retail
#
# Contactless
#
# tapandpay, taptopay, tappayment, contactless, contactlesspayment, tapandgo, contactlesspurchase, nfc, contactlesscard
#
# Payment Wallets
#
# paytmwallet, paymentbank, wallet, digitalwallet, onlinewallet, mobilewallet, phonewallet
#
# Cheques
#
# chequepayment, cheque, chequebounce, chequefraud
#
# AEPS
#
# aeps, aepsfraud, aadharpay, aadharbanking, aadharbiometric, biometricpayment, csc, aadharenabledpaymentsystem, cscpayment, cscfraud, doorstepbanking, miniatm
#
# NETC Fastag
#
# fastag, tolltax, nhaitoll, toll, fastagfraud, fastagscam, netcfastag
#
# QR
#
# qr, qrfail, qrcode, qrpayment, qrtransaction, qrsticker, qrscan, qrscam, scanandpay
#
# Others
#
# cashless, cashlessindia, digitalindia, digitalbharat, payments, paymentgateway, cybercribe, bankingfraud, paymentfraud, paymentsuccess, onlinepayment, onlinepayments, digitalpayment, digitalpayments, digipay, moneytransfer, remittance, remit, cashdeposit, cashwithdrawal, cashwithdraw, paymenttransaction
# Blueprint a ship with a graphene-titanium hull and ornate patterns. Include retractable solar sail wings, dual chemical-ion thrusters, and bird-like landing pods. Da Vinci's Vitruvian Man inspires the cockpit layout.