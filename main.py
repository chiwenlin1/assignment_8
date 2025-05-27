# main_program.py
import os
import time

REQUEST_FILE = "scraper_request.txt"
RESPONSE_FILE = "scraper_response.txt"
scraped_threads = []

def get_scraper_response():
    while True:
        if os.path.exists(RESPONSE_FILE):
            with open(RESPONSE_FILE, "r", encoding="utf-8") as f:
                content = f.read().strip()
            if content:
                result = {}
                for line in content.splitlines():
                    if ":" in line:
                        key, val = line.split(":", 1)
                        result[key.strip()] = val.strip()
                return result
        time.sleep(0.5)

def main():
    print("AlternateHistory Thread Scraper - Main Program")
    print("Type 'exit' to finish and save alphabetized output.\n")

    while True:
        page_url = input("Enter the full thread URL: ").strip()
        if page_url.lower() in ["exit", "q"]:
            break

        # Write URL to request file
        with open(REQUEST_FILE, "w") as f:
            f.write(page_url)

        print("Waiting for scraper response...")
        result = get_scraper_response()
        if "error" in result:
            print(result["error"])
        else:
            scraped_threads.append(result)
            print(f"Scraped: {result['title']} by {result['author']} (Page {result['page']})\n")

        # Clear response file
        with open(RESPONSE_FILE, "w") as f:
            f.write("")

    # Sort threads alphabetically by title
    sorted_threads = sorted(scraped_threads, key=lambda x: x["title"].lower())

    with open("scraped_threads.txt", "w", encoding="utf-8") as f:
        for entry in sorted_threads:
            f.write(f"Thread Title: {entry['title']}\n")
            f.write(f"Thread Starter: {entry['author']}\n")
            f.write(f"Page Number: {entry['page']}\n")
            f.write(f"URL: {entry['url']}\n")
            f.write("-" * 50 + "\n")

    print("\nAlphabetized thread list saved to scraped_threads.txt")

if __name__ == "__main__":
    main()
