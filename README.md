# 🔍 Website Crawler Script

A simple Python-based website crawler that recursively visits every internal link on a specified domain, counts the number of unique pages, and optionally exports the results in various formats (CSV, XLSX, JSON).

## 📦 Features

- Recursively crawls all internal pages on a given website
- Skips:
  - External domains
  - URLs with `#fragment` identifiers
  - Media file URLs (`.pdf`, `.mp3`, `.jpg`, etc.)
  - Pagination-style links (e.g., `/page/2/`)
- Tracks total number of pages visited
- Command-line flags for exporting results:
  - `-cv` : Export as CSV
  - `-xl` : Export as Excel
  - `-j`  : Export as JSON
- Color-coded terminal output for better readability
- Exports saved in an `exports` directory

## 🚀 How to Use

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```
### 2. Run the Crawler

```bash
python crawler.py -w https://example.com
```

### Optional Export flags

```bash
python crawler.py -w https://example.com -cv   # Export to CSV
python crawler.py -w https://example.com -xl   # Export to Excel
python crawler.py -w https://example.com -j    # Export to JSON

```

### 3. ⚙️ Example Output

```bash
✅ Crawled: https://example.com
✅ Crawled: https://example.com/about
⏩ Skipped media file: https://example.com/logo.png
⏩ Skipped pagination link: https://example.com/page/2/
Crawling complete. Total pages found: 18
✅ Exported as CSV to exports/crawl_results.csv
```

### 4. 📁 Directory Structure

```java
crawler/
│
├── crawler.py
├── requirements.txt
├── exports/
│   └── crawl_results.csv (or .json / .xlsx)
└── README.md

```

### 5. 🧱 Dependencies

- requests

- beautifulsoup4

- openpyxl

- colorama

- pandas


### 6. ✨ Author
Crafted with ❤️ by [Gaddiel](https://iamgaddiel.netlify.app/)
