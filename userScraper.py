import time
import random
from selenium.webdriver.common.by import By
import csv

class UserScraper():
    def __init__(self, driver, profile_link):
        self.driver = driver
        self.profile_link = profile_link
        self.followers = []
        self.following = []
        self.creds = []
        self.epochs = 100
        self.error_margin = 3
        self.driver.get(self.profile_link)
    
    def wait(self):
        time.sleep(random.randint(1,2))
        
    def scrape_linked_users(self, type):
        print("scraping linked users: ", type)
        try:
            user_text = self.driver.find_elements(By.CSS_SELECTOR, ".q-text.qu-dynamicFontSize--small.qu-color--gray")[type]
            
            user_text.click()

            time.sleep(2)

            user_popup = self.driver.find_element(By.CSS_SELECTOR, "div.q-box.qu-overflowY--auto.qu-display--flex.qu-flexDirection--column.ScrollBox___StyledBox-sc-1t8bc7j-0.eEjJKQ")
            
            epoch = 0
            last_count = 0
            curr_count = 0
            error_count = 3
            while epoch < self.epochs:
                try:
                    self.driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight)", user_popup)
                    time.sleep(4)
                    
                    if(epoch == 0):
                        last_count = len(user_popup.find_elements(By.XPATH, ".//a[@href]"))
                        curr_count = last_count
                        epoch += 1
                        continue
                    
                    # check if we got more upvoters, if not, break
                    curr_count = len(user_popup.find_elements(By.XPATH, ".//a[@href]"))
                    if(curr_count == last_count):
                        if(error_count == 0):
                            break
                        else:
                            error_count -= 1
                    else:
                        last_count = curr_count

                    epoch += 1
                    print("epoch: ", epoch)
                except:
                    break
            
            # get all the links in the popup
            user_links = user_popup.find_elements(By.XPATH, ".//a[@href]")
            user_links = [link.get_attribute("href") for link in user_links if "profile" in link.get_attribute("href")]
            user_links = list(set(user_links))
            
            time.sleep(random.randint(5,10))

            # close the popup
            close_button = self.driver.find_element(By.CLASS_NAME, "q-click-wrapper")
            close_button.click()

            self.wait()
        except Exception as e:
            print(e)
            user_links = []
        print(len(user_links))
        if type == 0:
            self.followers = user_links
        else:
            self.following = user_links
        print("set linked users: ", type)
    
    def scrape_credentials(self):
        main_div = self.driver.find_elements(By.CSS_SELECTOR, ".q-text.qu-dynamicFontSize--small.qu-mt--small")
        for div in main_div:
            self.creds.append(div.text)
    
    def save_to_csv(self):
        with open("users/users.csv", "a+") as f:
            writer = csv.writer(f)
            writer.writerow([self.profile_link, self.followers, self.following, self.creds])
    
    def run(self):
        self.scrape_linked_users(0)
        self.scrape_linked_users(1)
        self.scrape_credentials()
        self.save_to_csv()
        self.driver.quit()