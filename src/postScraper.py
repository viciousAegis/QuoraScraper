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

def format_query(query):
    return query.replace(" ", "%20")

class PostScraper:
    def __init__(self, driver, search_query, total_post_count, timeline):
        self.driver = driver
        self.scraped_posts = []
        self.visible_posts = []
        self.search_query = format_query(search_query)
        
        self.total_post_count = total_post_count
        self.scraped_post_count = 0
        self.epoch = 0
        self.consecutive_error_count = 0

        self.timeline = timeline
        if timeline == "all":
            self.timeline = ""
    
    def wait(self):
        time.sleep(random.randint(1, 2))
    
    def login(self):
        # get email input
        email_input = self.driver.find_element(By.NAME, "email")
        email_input.send_keys("email")
        self.wait()
        # get password input
        password_input = self.driver.find_element(By.NAME, "password")
        password_input.send_keys("password")
        self.wait()
        # click enter
        password_input.send_keys(Keys.RETURN)
    
    def open_search_page(self):
        while(len(self.visible_posts) == 0):
            try:
                search_url = f"https://www.quora.com/search?q={self.search_query}&type=post&time={self.timeline}"
                self.driver.get(search_url)
                self.wait()
                # check if url is actually the search url
                if self.driver.current_url != search_url:
                    print("not a search url")
                    if self.driver.current_url == "https://www.quora.com/":
                        # login page
                        self.login()
                        time.sleep(5)
                        self.driver.get(search_url)
                        self.wait()
                        self.get_new_posts()
                else:
                    self.get_new_posts()
            except:
                print("error opening search page")
                self.wait()
    
    def check_paid_post_error(self):
        paid_post_popup = self.driver.find_elements(By.CSS_SELECTOR, "div.q-flex.ModalContainerInternal___StyledFlex-s8es4q-2.gXhqYs.modal_content_inner.qu-flexDirection--column.qu-bg--white.qu-overflowY--auto.qu-borderAll.qu-alignSelf--center")
        print('paid post')
        if len(paid_post_popup) > 0:
            # close the popup
            close_button = self.driver.find_element(By.CLASS_NAME, "q-click-wrapper")
            close_button.click()
            self.wait()
            print("closed paid post popup")

    def check_upvote_popup_error(self):
        # get the upvote popup
        upvote_popup = self.driver.find_elements(By.CSS_SELECTOR, "div.q-box.qu-overflowY--auto.qu-display--flex.qu-flexDirection--column.ScrollBox___StyledBox-sc-1t8bc7j-0.eEjJKQ")
        if len(upvote_popup) > 0:
            # close the popup
            close_button = self.driver.find_element(By.CLASS_NAME, "q-click-wrapper")
            close_button.click()
            self.wait()
            print("closed upvote popup")
        else:
            print("no upvote popup. some other error")
    
    def scrape_single_post(self, post):
        # scroll the page till next post is visible and wait for 2 seconds
        try:
            postElement = Post(post, self.driver)
            postElement.master_scrape()
            self.scraped_posts.append(postElement.get_post_details())
            if self.consecutive_error_count > 0:
                self.consecutive_error_count = 0
        except:
            print("error scraping post")
            self.check_upvote_popup_error()
            self.check_paid_post_error()
            self.wait()
            self.consecutive_error_count += 1
    
    def scrape_visible_posts(self):
        for post in self.visible_posts:
            if self.scraped_post_count >= self.total_post_count:
                break
            self.scrape_single_post(post)
            self.scraped_post_count += 1
            print("scraped post: ", self.scraped_post_count)
            self.remove_post(post)
            # check consecutive errors
            if self.consecutive_error_count > 5:
                print("too many consecutive errors")
                return -1
        return 0
    
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
            print("got posts")
        except:
            self.wait()

    def write_to_file(self):
        # create a new folder with the name of the search query
        try:
            if not os.path.exists("./posts/"+self.search_query.replace("%20", "")):
                os.makedirs("./posts/"+self.search_query.replace("%20", ""))
            
            # write the scraped posts to a csv file
            with open("posts/"+self.search_query.replace("%20", "")+"/"+self.search_query.replace("%20", "")+".csv", "w", newline="", encoding="utf-8") as csvfile:
                fieldnames = ["text", "community_name", "author", "commenters", "upvoters", "comments"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for post in self.scraped_posts:
                    writer.writerow(post)
        except Exception as e:
            print(e)
            pass
    
    def run(self):
        self.open_search_page()
        print("Opened search page")
        try:
            while(self.scraped_post_count < self.total_post_count):
                self.get_new_posts()
                flag = self.scrape_visible_posts()
                if flag == -1:
                    break
                self.epoch += 1
                self.wait()
                print("scraped posts: ", self.scraped_post_count)
        except Exception as e:
            print(e)
            pass
        self.write_to_file()