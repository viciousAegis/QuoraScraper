from selenium import webdriver
from postScraper import PostScraper

if __name__ == "__main__":
    driver = webdriver.Chrome()
    post_scraper = PostScraper(driver, "jeeadvanced", 2)
    post_scraper.run()