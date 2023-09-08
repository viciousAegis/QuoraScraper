from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from postScraper import PostScraper
import sys

if __name__ == "__main__":
    search_term = sys.argv[1]
    total_post_count = int(sys.argv[2])
    options = ChromeOptions()
    options.add_argument("--window-size=1005,9999")
    driver = webdriver.Chrome(options=options)
    post_scraper = PostScraper(driver, search_term, total_post_count)
    post_scraper.run()