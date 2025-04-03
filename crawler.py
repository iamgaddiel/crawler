import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
import argparse
import os
import csv
import json
import re
import pandas as pd
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Set up global variables
visited_pages = set()
page_counter = 0

# File extensions to skip (common media & document types)
SKIPPED_EXTENSIONS = {
    ".mp3", ".wav", ".ogg", ".mp4", ".avi", ".mov", ".mkv",  # Audio & Video
    ".jpg", ".jpeg", ".png", ".gif", ".svg", ".webp",  # Images
    ".pdf", ".doc", ".docx", ".ppt", ".pptx", ".xls", ".xlsx", ".zip", ".rar"  # Documents & Archives
}

def is_media_file(url):
    """Check if a URL ends with a media file extension."""
    return any(url.lower().endswith(ext) for ext in SKIPPED_EXTENSIONS)

def is_pagination_link(url):
    """Check if a URL contains pagination like '/page/2/'."""
    return bool(re.search(r"/page/\d+/?$", url))

def fetch_page(url):
    """Fetches the page and handles request errors with retries."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"Failed to crawl {url}: {e}")
        return None

def crawl_site(start_url, domain):
    """Crawls the website using a queue (iterative) instead of recursion."""
    global page_counter
    queue = [start_url]

    while queue:
        current_url = queue.pop(0)

        # Skip visited pages, anchor links, media files, and pagination links
        if (
            current_url in visited_pages or 
            "#" in current_url or 
            is_media_file(current_url) or 
            is_pagination_link(current_url)
        ):
            continue

        response = fetch_page(current_url)
        if response is None or not response.text.strip():  # Ensure valid response
            print(Fore.RED + f"Skipping {current_url} due to empty or invalid response.")
            continue

        try:
            soup = BeautifulSoup(response.text, "html.parser")
        except Exception as e:
            print(Fore.RED + f"Skipping {current_url} due to parsing error: {e}")
            continue

        visited_pages.add(current_url)
        page_counter += 1
        print(Fore.GREEN + f"Crawled: {current_url} " + Fore.YELLOW + f"(Total: {page_counter})")

        for link in soup.find_all("a", href=True):
            next_url = urljoin(current_url, link["href"])
            parsed_url = urlparse(next_url)

            if (
                parsed_url.netloc and parsed_url.netloc == domain and 
                next_url not in visited_pages and 
                "#" not in next_url and 
                not is_media_file(next_url) and
                not is_pagination_link(next_url)
            ):
                queue.append(next_url)
                time.sleep(1)  # Rate-limiting to avoid overwhelming the server

def export_data(format_type):
    """Exports crawled data in the specified format (CSV, XLSX, JSON)."""
    if not visited_pages:
        print(Fore.YELLOW + "No data to export.")
        return

    os.makedirs("exports", exist_ok=True)
    file_path = f"exports/crawled_data.{format_type}"

    if format_type == "csv":
        with open(file_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["URL"])
            for url in visited_pages:
                writer.writerow([url])
    elif format_type == "xlsx":
        df = pd.DataFrame({"URL": list(visited_pages)})
        df.to_excel(file_path, index=False)
    elif format_type == "json":
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(list(visited_pages), file, indent=4)

    print(Fore.CYAN + f"Data exported successfully: {file_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple Web Crawler")
    parser.add_argument("-w", "--website", required=True, help="The website URL to crawl")
    parser.add_argument("-cv", "--csv", action="store_true", help="Export crawled data as CSV")
    parser.add_argument("-xl", "--xlsx", action="store_true", help="Export crawled data as XLSX")
    parser.add_argument("-j", "--json", action="store_true", help="Export crawled data as JSON")

    args = parser.parse_args()
    start_url = args.website
    domain = urlparse(start_url).netloc

    print(Fore.BLUE + f"Starting crawl on: {start_url}")
    crawl_site(start_url, domain)

    print(Fore.GREEN + f"Crawling complete. Total pages found: {page_counter}")

    # Handle exports
    if args.csv:
        export_data("csv")
    if args.xlsx:
        export_data("xlsx")
    if args.json:
        export_data("json")
