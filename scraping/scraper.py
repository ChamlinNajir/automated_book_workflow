import os
import time
import json
from pathlib import Path
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

# create these folders if they don't exist
def create_folders():
    os.makedirs('screenshots', exist_ok=True)
    os.makedirs('scraping', exist_ok=True)

# save reward data to a JSON file
def save_rewards(success, message):
    reward = 1 if success else -1 
    log_entry = {
        "time": time.strftime("%Y-%m-%d %H:%M:%S"),
        "success": success,
        "reward": reward,
        "message": message
    }

    log_file = "scraping/reward_log.json"

    if os.path.exists(log_file):
        with open(log_file, "r") as file:
            logs = json.load(file)
    else:
        logs = []

    logs.append(log_entry)

    with open(log_file, "w") as file:
        json.dump(logs, file, indent=2)

# this function visits the webpage and does the scraping
def scrape_page(url):
    try:
        # start the browser using Playwright
        with sync_playwright() as sp:
            browser = sp.chromium.launch()
            page = browser.new_page()
            
            # go to the url
            page.goto(url)
            page.wait_for_timeout(3000)  # wait 3 seconds for everything to load

            # take a screenshot of the whole page
            screenshot_path = 'screenshots/chapter1.png'
            page.screenshot(path=screenshot_path, full_page=True)

            # get all the text content from the page
            html_content = page.content()
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # find the main content area
            content_div = soup.find('div', class_='mw-parser-output')

            # extract the text and clean it up
            paragraphs = content_div.find_all('p')
            clean_text = "\n".join([p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)]) 

            # save the text into a file
            with open('scraping/chapter_text.txt', 'w', encoding="utf-8") as file:
                file.write(clean_text)

            # close the browser
            browser.close()

            # log a successful reward
            save_rewards(True, "Scraping completed successfully")
            print("Scraping completed successfully. Data saved.")
    except Exception as error:
            save_rewards(False, f"Error during scraping : {error}")
            print("Error during scraping :",error)

# main function
if __name__ == "__main__":
    create_folders()  # ensure folders exist
    url = "https://en.wikisource.org/wiki/The_Gates_of_Morning/Book_1/Chapter_1 "  
    scrape_page(url)  # start the scraping process