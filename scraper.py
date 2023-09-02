from selenium import webdriver
from postScraper import PostScraper
import sys

if __name__ == "__main__":
    search_term = sys.argv[1]
    total_post_count = int(sys.argv[2]) 
    driver = webdriver.Chrome()
    post_scraper = PostScraper(driver, search_term, total_post_count)
    post_scraper.run()