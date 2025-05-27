# Airbnb Scraper
Utilizes crawl4ai for web crawling and an LLM (Gemini Flash) for extracting Airbnb room data based on a defined schema. The extracted data includes listing titles, prices, ratings, reviews, descriptions, capacities, room details, addresses, images, and amenities.

## Setup

1.  **Clone the repository (if you haven't already):**
    ```bash
    git clone repository_url / downlaod it as zip file
    ```
2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## How to Use This Project

Follow these steps to use the Airbnb scraper:

### 1. Extract Listing IDs from an Airbnb Search Page

To get the IDs of Airbnb listings you want to scrape, you first need to extract them from an Airbnb search results page.

*   **Get a Search Page URL:** Go to Airbnb.com, perform a search for your desired location (e.g., "Dahab"), and copy the URL from the search results page.
*   **Update `get_rooms_ids_from_search_page.py`:** Open the [`get_rooms_ids_from_search_page.py`](get_rooms_ids_from_search_page.py) file. Replace the existing URL in the `URL_list` with the Airbnb search page URL you copied.
*   **Run the Extraction Script:** Execute the script from your terminal:
    ```bash
    python get_rooms_ids_from_search_page.py
    ```
    This script will crawl the search page and print a list of extracted Airbnb listing IDs to your console.
*   **Copy IDs to `config.py`:** Copy the extracted listing IDs from the console output. Open [`config.py`](config.py) and paste these IDs into the `URL_list` dictionary under the appropriate key (e.g., `"Dahab"`).

### 2. Run the Main Scraper

Once you have populated `config.py` with listing IDs, you can run the main scraper to fetch detailed information for each listing.

*   **Execute `main.py`:** Run the main scraping script from your terminal:
    ```bash
    python main.py
    ```
*   **Rate Limit Awareness:** Please be aware that the scraper is configured to pause for 90 seconds between requests to avoid hitting Airbnb's rate limits. You can modify this delay in the `main.py` file if needed, but be cautious not to set it too low to prevent your IP from being blocked.

The scraped data will be saved in `json/` and `raw/` directories, and a summary CSV file (`csv_main.csv`) will be generated. Images will be downloaded to the `images/` directory.
---

## ⚠️ Important Disclaimer for Educational Purposes: ⚠️

This tutorial demonstrates how to use Crawl4AI for web scraping. Please be aware that scraping content from websites, especially those that explicitly disallow it via their robots.txt file (like Airbnb for `/rooms/` pages), may violate their Terms of Service and could lead to your IP being blocked, or even legal action. This tutorial is for educational purposes only and does not endorse or encourage scraping against a website's policies. Always respect a website's robots.txt and Terms of Service.