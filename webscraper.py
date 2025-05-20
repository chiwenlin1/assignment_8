"""
Adapted from: https://www.youtube.com/shorts/D-I_xau0fmQ
"""
import requests as req
from bs4 import BeautifulSoup

# Store all scraped results in a list
scraped_threads = []

def scrape_thread(url):
    try:
        response = req.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        # Scrape title
        title_tag = soup.find("h1", class_="p-title-value")
        title = title_tag.text.strip() if title_tag else "[Unknown Title]"

        # Scrape thread starter (Author)
        thread_starter_span = soup.find("span", string="Thread starter")
        author_tag = thread_starter_span.find_next("a", class_="username") if thread_starter_span else None
        author_name = author_tag.text.strip() if author_tag else "[Unknown Author]"

        # Scrape current page of thread
        current_page = soup.find("li", class_="pageNav-page--current")
        page_number = current_page.text.strip() if current_page else "[Unknown Page]"

        scraped_threads.append({
            "title": title,
            "author": author_name,
            "page": page_number,
            "url": url
        })

        print(f"Scraped: {title} by {author_name} (Page {page_number})\n")

    except Exception as e:
        print(f"[!] Error scraping {url}: {e}\n")

def main():
    print("AlternateHistory Thread Scraper")
    print("Type 'exit' to finish and save alphabetized output.\n")

    while True:
        page_url = input("Enter the full thread URL: ").strip()
        if page_url.lower() in ["exit", "q"]:
            break
        scrape_thread(page_url)

    # Sort threads alphabetically by title
    sorted_threads = sorted(scraped_threads, key=lambda x: x["title"].lower())

    # Write to file
    with open("scraped_threads.txt", "w", encoding="utf-8") as f:
        for entry in sorted_threads:
            f.write(f"Thread Title: {entry['title']}\n")
            f.write(f"Thread Starter: {entry['author']}\n")
            f.write(f"Page Number: {entry['page']}\n")
            f.write(f"URL: {entry['url']}\n")
            f.write("-" * 50 + "\n")

    print(f"\nAlphabetized thread list saved to scraped_threads.txt")

if __name__ == "__main__":
    main()
