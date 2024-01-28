from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time
import random
from bs4 import BeautifulSoup

class AnswerPost:
    def __init__(self, post_element, driver):
        self.post_element = post_element
        self.driver = driver
        self.question = None
        self.answer = []
        self.image_urls = []
        self.video_urls = []
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
            # get src of image
            src = image.get_attribute("src")
            if src != None:
                self.image_urls.append(src)
            
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

    def scrape_question(self):
        question_div = self.post_element.find_element(By.CSS_SELECTOR, "div.q-flex.qu-flexDirection--row")
        # get all inner texts in the div
        question_text = question_div.text
        self.question = question_text
        self.wait()

    
    def scrape_text(self):
        WebDriverWait(self.driver, timeout=10).until(lambda d: d.find_element(By.CSS_SELECTOR,".q-text.qu-display--block.qu-wordBreak--break-word.qu-textAlign--start")) # this is the p tag containing the text
        
        # get the text from the p tag
        text_boxes = self.post_element.find_elements(By.CSS_SELECTOR, ".q-text.qu-display--block.qu-wordBreak--break-word.qu-textAlign--start")
        self.answer = [text_box.text for text_box in text_boxes]
        self.answer = ' '.join(self.answer)
        self.wait()
    
    def master_scrape(self):
        self.move_into_view()
        self.remove_videos()
        self.click()
        self.remove_images()
        self.scrape_question()
        self.scrape_text()        

    def get_post_details(self):
        return {
            "question": self.question,
            "answer": self.answer,
            "image_urls": self.image_urls,
        }