import asyncio
from crawl4ai import AsyncWebCrawler
from crawl4ai.async_configs import BrowserConfig, CrawlerRunConfig, CacheMode
import re

URL_list = [
    "https://www.airbnb.com/s/Dahab/homes?refinement_paths%5B%5D=%2Fhomes&place_id=ChIJic1hu2gsVRQRI76ZDuHslNM&date_picker_type=calendar&source=structured_search_input_header&search_type=AUTOSUGGEST&query=Dahab&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2025-06-01&monthly_length=3&monthly_end_date=2025-09-01&search_mode=regular_search&price_filter_input_type=2&channel=EXPLORE&pagination_search=true&price_filter_num_nights=5&federated_search_session_id=15c90daa-e48f-4aff-a5af-8ecab96c8588&cursor=eyJzZWN0aW9uX29mZnNldCI6MCwiaXRlbXNfb2Zmc2V0IjowLCJ2ZXJzaW9uIjoxfQ%3D%3D",
]


def extract_listing_ids(html_content):
    """
    Extracts unique numbers following "listingId":" from HTML content.

    Args:
        html_content (str): The HTML content to search within.

    Returns:
        list: A list of unique integers found after "listingId":".
              Returns an empty list if no matches are found.
    """

    # Regular expression to find "listingId":" followed by one or more digits
    pattern = r"listingId\":\"(\d+)"

    # Find all matches in the HTML content
    matches = re.findall(pattern, html_content)

    # Convert the extracted strings to integers and remove duplicates
    unique_numbers = list(set(map(int, matches)))

    return unique_numbers


async def main():
    # Configure browser settings
    browser_config = BrowserConfig(
        headless=True,  # Run in headless mode
        #stealth=True,   # Enable stealth mode to avoid detection
        verbose=True    # Enable verbose logging
    )

    # Configure crawler run settings
    run_config = CrawlerRunConfig(
        word_count_threshold=1,        # Minimum words per content block
        cache_mode=CacheMode.ENABLED   # Use cached data if available
    )

    all_html_content = ""
    # Initialize the crawler
    async with AsyncWebCrawler(config=browser_config) as crawler:
        for url in URL_list:
            print(f"Crawling URL: {url}")
            result = await crawler.arun(
                url=url,
                config=run_config
            )
            
            if result.success and result.cleaned_html:
                all_html_content += str(result)
            elif result.error_message:
                print(f"Error crawling {url}: {result.error_message}")
            
            await asyncio.sleep(5) # Pause between requests

    if all_html_content:
        listing_ids = extract_listing_ids(all_html_content)
        print(f"\nFound {len(listing_ids)} unique listing IDs:")
        print(listing_ids)
    else:
        print("No HTML content was successfully crawled to extract listing IDs.")

# Run the asynchronous main function
if __name__ == "__main__":
    asyncio.run(main())
