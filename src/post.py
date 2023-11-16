from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time
import random
from bs4 import BeautifulSoup

class Post:
    def __init__(self, post_element, driver):
        self.post_element = post_element
        self.driver = driver
        self.text = None
        self.community_name = None
        self.author = None
        self.commenters = None
        self.upvoters = None
        self.upvote_epoch_limit = 100
    
    def wait(self):
        time.sleep(random.randint(1,2))
    
    def move_into_view(self):
        self.driver.execute_script("arguments[0].scrollIntoView();", self.post_element)
        self.wait()
    
    def remove_videos(self):
        videos = self.post_element.find_elements(By.CSS_SELECTOR, "div.q-box.qu-mt--small.standalone_featurable")
        for video in videos:
            self.driver.execute_script("""
            var element = arguments[0];
            element.parentNode.removeChild(element);
            """, video)
            self.wait()
    
    def remove_images(self):
        images = self.post_element.find_elements(By.TAG_NAME, "img")
        for image in images:
            self.driver.execute_script("""
            var element = arguments[0];
            element.parentNode.removeChild(element);
            """, image)
            self.wait()
    
    def click(self):
        # click on the post to get expanded view
        actions = webdriver.ActionChains(self.driver)
        # click on top
        actions.move_to_element_with_offset(self.post_element, 0, self.post_element.size["height"]/2-10)
        actions.click()
        actions.perform()
        self.wait()
    
    def scrape_text(self):
        WebDriverWait(self.driver, timeout=10).until(lambda d: d.find_element(By.CSS_SELECTOR,".q-text.qu-display--block.qu-wordBreak--break-word.qu-textAlign--start")) # this is the p tag containing the text
        
        # get the text from the p tag
        self.text = self.driver.find_element(By.CSS_SELECTOR, ".q-text.qu-display--block.qu-wordBreak--break-word.qu-textAlign--start").text
        self.wait()
    
    def scrape_community_name(self):
        # get the community name
        WebDriverWait(self.driver, timeout=10).until(lambda d: d.find_element(By.CSS_SELECTOR, ".q-text.puppeteer_test_tribe_name"))
        self.community_name = self.driver.find_element(By.CSS_SELECTOR, ".q-text.puppeteer_test_tribe_name").text
        self.wait()
    
    def scrape_author(self):
        # get all the links in the post
        all_links = self.post_element.find_elements(By.XPATH, ".//a[@href]")
        
        # get the link to the profile. The href should contain the word profile
        profile_link = ""
        for link in all_links:
            if "profile" in link.get_attribute("href"):
                profile_link = link.get_attribute("href")
                break
        self.author = profile_link
    
    def scrape_upvotes(self):
        # find upvote text and click on it
        try:
            error_count = 3
            upvote_popup = None
            print(error_count, upvote_popup)
            while error_count > 0 and upvote_popup is None:
                print("Clicking on upvote text")
                upvote_text = self.post_element.find_element(By.XPATH, "//*[text()='View upvotes']")
               
                print(upvote_text)
                if upvote_text is None:
                    print("No upvote text")
                else:
                    print("Upvote text found")

                upvote_text.click()


                # wait for the upvote popup to load 
                time.sleep(2)

                # get the upvote popup
                upvote_popup = self.driver.find_element(By.CSS_SELECTOR, "div.q-box.qu-overflowY--auto.qu-display--flex.qu-flexDirection--column.ScrollBox___StyledBox-sc-1t8bc7j-0.fRHsQI")

                error_count-=1

            # scroll the modal to the bottom to load next batch of upvoters until the end
            epoch = 0
            last_count = 0
            curr_count = 0
            error_count = 3
            while epoch < self.upvote_epoch_limit:
                try:
                    print("Scrolling")
                    self.driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight)", upvote_popup)
                    time.sleep(4)
                    
                    if(epoch == 0):
                        last_count = len(upvote_popup.find_elements(By.XPATH, ".//a[@href]"))
                        curr_count = last_count
                    
                    # check if we got more upvoters, if not, break
                    curr_count = len(upvote_popup.find_elements(By.XPATH, ".//a[@href]"))
                    if(curr_count == last_count):
                        if error_count == 0:
                            break
                        error_count-=1
                    else:
                        last_count = curr_count

                    epoch += 1
                except:
                    break
            
            # select all links in the popup
            upvoter_links = upvote_popup.find_elements(By.XPATH, ".//a[@href]")
            upvoter_links = [link.get_attribute("href") for link in upvoter_links if "profile" in link.get_attribute("href")]
            upvoter_links = list(set(upvoter_links))
            
            time.sleep(random.randint(5,10))
            
            # close the popup
            close_button = self.driver.find_element(By.CLASS_NAME, "q-click-wrapper")
            close_button.click()

            self.wait()
        except:
            upvoter_links = []
        self.upvoters = upvoter_links

    def scrape_comments(self):
        comments_container = self.post_element.find_element(By.CLASS_NAME, "comment_and_ad_container")
        comments_container.click()
        
        # now, comments container is expanded. Click on view more comments
        self.wait()
        
        try:
            view_more_comments = comments_container.find_element(By.XPATH, "//*[text()='View more comments']")
            self.wait()
            view_more_comments.click()
            self.wait()
        except:
            pass
        
        # now get the profile links of all the commenters        
        comment_links = comments_container.find_elements(By.XPATH, ".//a[@href]")
        comment_links = [link.get_attribute("href") for link in comment_links if "profile" in link.get_attribute("href")]
        comment_links = list(set(comment_links))
        
        # remove the profile link of the post author
        self.commenters = [link for link in comment_links if link != self.author]
        
        self.wait()
    
    def master_scrape(self):
        self.move_into_view()
        self.remove_videos()
        self.click()
        self.remove_images()
        self.scrape_community_name()
        self.scrape_author()
        self.scrape_text()
        self.scrape_upvotes()
        self.scrape_comments()        

    def get_post_details(self):
        return {
            "text": self.text,
            "community_name": self.community_name,
            "author": self.author,
            "commenters": self.commenters,
            "upvoters": self.upvoters
        }