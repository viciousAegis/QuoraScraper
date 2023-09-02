from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import random
from post import Post
from bs4 import BeautifulSoup
from selenium.webdriver.support.wait import WebDriverWait
import os
import csv

class PostScraper():
    def __init__(self, driver, search_query, total_post_count):
        self.driver = driver
        self.scraped_posts = []
        self.visible_posts = []
        self.search_query = search_query
        
        self.total_post_count = total_post_count
        self.scraped_post_count = 0
        self.epoch = 0
    
    def wait(self):
        time.sleep(random.randint(1, 2))
    
    def open_search_page(self):
        while(len(self.visible_posts) == 0):
            try:
                search_url = "https://www.quora.com/search?q="+self.search_query+"&type=post"
                self.driver.get(search_url)
                self.wait()
                self.get_new_posts()
            except:
                print("error opening search page")
                self.wait()
    
    def scrape_single_post(self, post):
        # scroll the page till next post is visible and wait for 2 seconds
        try:
            postElement = Post(post, self.driver)
            postElement.master_scrape()
            self.scraped_posts.append(postElement.get_post_details())
        except:
            print("error scraping post")
            self.wait()
    
    def scrape_visible_posts(self):
        for post in self.visible_posts:
            if self.scraped_post_count >= self.total_post_count:
                break
            self.scrape_single_post(post)
            self.scraped_post_count += 1
            self.remove_post(post)
    
    def remove_post(self, post):
        self.driver.execute_script("""
        var element = arguments[0];
        element.parentNode.removeChild(element);
        """, post)
        self.wait()
    
    def get_new_posts(self):
        # get all the posts on the page
        try:
            all_posts = self.driver.find_elements(By.CSS_SELECTOR, ".q-box.qu-borderBottom.qu-px--medium.qu-pt--medium")
            self.visible_posts = all_posts
        except:
            self.wait()

    def write_to_file(self):
        # create a new folder with the name of the search query
        try:
            os.mkdir("posts/"+self.search_query)
            
            # write the scraped posts to a csv file
            with open("posts/"+self.search_query+"/"+self.search_query+".csv", "w", newline="", encoding="utf-8") as csvfile:
                fieldnames = ["text", "community_name", "author", "commenters", "upvoters"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for post in self.scraped_posts:
                    writer.writerow(post)
        except:
            pass
    
    def run(self):
        self.open_search_page()
        try:
            while(self.scraped_post_count < self.total_post_count):
                self.get_new_posts()
                self.scrape_visible_posts()
                self.epoch += 1
                self.wait()
                print("scraped posts: ", self.scraped_post_count)
        except:
            pass
        self.write_to_file()