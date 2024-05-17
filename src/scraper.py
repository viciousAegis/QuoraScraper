from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from postScraper import PostScraper
from userScraper import UserScraper
from answerScraper import AnswerScraper
import sys
import argparse
import chromedriver_autoinstaller

if __name__ == "__main__":
    search_queries = []

    with open('./search.terms', 'r') as f:
        for line in f:
            search_queries.append(line.strip())

    parser = argparse.ArgumentParser()
    
    parser.add_argument("-t", "--type", dest="type", help="type of scrape: post, user or answer", required=True)
    
    # if user scrape
    parser.add_argument("-u", "--user", dest="user_url", help="user profile link")
    
    # if post scrape
    parser.add_argument("-c", "--count", dest="total_post_count", help="number of posts or users to scrape", default=50)
    
    parser.add_argument('--timeline', type=str, help='timeline to scrape', default='week', choices=['all', 'year', 'month', 'week', 'day', 'hour'])

    args = parser.parse_args()

    chromedriver_autoinstaller.install()
        

    
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument('--disable-popup-blocking')
    # Overcomes limited resource problems
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")  # Applicable to windows os only
    chrome_options.add_argument(
        "--remote-debugging-port=9222")  # This is important
    # Disable sandboxing that Chrome runs in.
    chrome_options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=chrome_options)
    
    if(args.type == "user"):
        for search_term in search_queries:
            user_scraper = UserScraper(driver, search_term)
            user_scraper.run()
    elif(args.type == "answer"):
        for search_term in search_queries:
            answer_scraper = AnswerScraper(driver, search_term, int(args.total_post_count))
            answer_scraper.run()
    else:
        for search_term in search_queries:
            post_scraper = PostScraper(driver, search_term, int(args.total_post_count), args.timeline)
            post_scraper.run()
    driver.quit()
