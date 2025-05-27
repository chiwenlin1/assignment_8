# scraper_service.py
import requests as req
from bs4 import BeautifulSoup
import time
import os

REQUEST_FILE = "scraper_request.txt"
RESPONSE_FILE = "scraper_response.txt"

def scrape_thread(url):
    try:
        response = req.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        title_tag = soup.find("h1", class_="p-title-value")
        title = title_tag.text.strip() if title_tag else "[Unknown Title]"

        thread_starter_span = soup.find("span", string="Thread starter")
        author_tag = thread_starter_span.find_next("a", class_="username") if thread_starter_span else None
        author_name = author_tag.text.strip() if author_tag else "[Unknown Author]"

        current_page = soup.find("li", class_="pageNav-page--current")
        page_number = current_page.text.strip() if current_page else "[Unknown Page]"

        return {
            "title": title,
            "author": author_name,
            "page": page_number,
            "url": url
        }

    except Exception as e:
        return {
            "error": f"[!] Error scraping {url}: {e}"
        }

def main():
    print("Scraper Microservice Running...")
    while True:
        if os.path.exists(REQUEST_FILE):
            with open(REQUEST_FILE, "r") as f:
                url = f.read().strip()
            if url:
                result = scrape_thread(url)

                with open(RESPONSE_FILE, "w", encoding="utf-8") as f:
                    for key, value in result.items():
                        f.write(f"{key}:{value}\n")

                # Reset request file to signal job is complete
                with open(REQUEST_FILE, "w") as f:
                    f.write("")

        time.sleep(1)

if __name__ == "__main__":
    main()

