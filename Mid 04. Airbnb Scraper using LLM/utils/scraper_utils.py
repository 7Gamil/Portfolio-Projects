import json
import os
from typing import List, Set, Tuple
from pydantic import BaseModel

from crawl4ai import AsyncWebCrawler

from crawl4ai.async_configs import (
    BrowserConfig,
    CacheMode,
    CrawlerRunConfig,
    LLMExtractionStrategy,
    LLMConfig,
)

from utils.data_utils import save_listing_data_to_csv, save_images

class scrape_schema(BaseModel):
    """
    Represents the data structure of a scrape schema.
    """
    Title: str
    price: str
    rating: float
    reviews: int
    description: str
    maxGuestCapacity: str
    bedrooms: str
    beds: str
    baths: str
    address: str
    thumbnail: str # found in ogImage
    mapLat: str
    mapLng: str
    Highlights: list[str] # found in PdpHighlight only main titles 
    amenities: list[str] 
    galleryImagesURL: list[str] # found in baseUrl collect up to 15 urls
    

def get_browser_config() -> BrowserConfig:
    """
    Returns the browser configuration for the crawler.

    Returns:
        BrowserConfig: The configuration settings for the browser.
    """
    # https://docs.crawl4ai.com/core/browser-crawler-config/
    return BrowserConfig(
        browser_type="chromium",  # Type of browser to simulate
        headless=True,  # Whether to run in headless mode (no GUI)
        verbose=True,  # Enable verbose logging
    )


def get_llm_strategy() -> LLMExtractionStrategy:
    """
    Returns the configuration for the language model extraction strategy.

    Returns:
        LLMExtractionStrategy: The settings for how to extract data using LLM.
    """
    # https://docs.crawl4ai.com/api/strategies/#llmextractionstrategy
    strategy = LLMExtractionStrategy(
        llm_config=LLMConfig(provider="gemini/gemini-2.0-flash", api_token=os.getenv('GEMINI_API_KEY')),
        schema=scrape_schema.model_json_schema(),  # JSON schema of the data model
        extraction_type="schema",  # Type of extraction to perform
        instruction=(
            "Extract all property objects with"
            "'title'"
            "'price' (will be in ج.م convert it to USD by divine by 50)"
            "'rating', 'reviews' , 'description', 'maxGuestCapacity', 'bedrooms', 'beds', 'baths'"
            "'address' (area, state, city, country)"
            "'thumbnail' (can be found in ogImage)"
            "'mapLat' (can be found in mapLat)"
            "'mapLng' (can be found in mapLng)"
            "'highlights' (can be found in PdpHighlight only main titles)"
            "'amenities'"
            "'galleryImagesURL' (can be found in baseUrl collect up to 15 urls)"
            "from the content."
        ),  # Instructions for the LLM
        #input_format="markdown",  # Format of the input content
        #input_format="cleaned_html",  # Format of the input content
        input_format="html",  # Format of the input content
        chunk_token_threshold=500000,  # Token limit for LLM input
        verbose=True,  # Enable verbose logging
    )
    #print("LLM Strategy Responder:", vars(strategy))
    return strategy


async def fetch_and_process_listing_page(
    crawler: AsyncWebCrawler,
    listing_url: str,
    css_selector: str,
    llm_strategy: LLMExtractionStrategy,
    session_id: str,
    area: str,
    listing_id: str,
    next_id: int,
) -> bool:
    """
    Fetches and processes a single page of listing data.

    Args:
        crawler (AsyncWebCrawler): The web crawler instance.
        listing_url (str): The URL of the Airbnb listing.
        css_selector (str): The CSS selector to target the content.
        llm_strategy (LLMExtractionStrategy): The LLM extraction strategy.
        session_id (str): The unique session identifier for the crawl.
        area (str): The geographical area of the listing (e.g., "Dahab").
        listing_id (str): The unique ID of the Airbnb listing.
        next_id (int): The sequential ID for the current scraping session.

    Returns:
        bool: True if the page was successfully fetched and processed, False otherwise.
    """

    print(f"Processing URL: {listing_url}, Session ID: {next_id}")

    # Fetch page content with the extraction strategy
    result = await crawler.arun(
        url=listing_url,
        config=CrawlerRunConfig(
            cache_mode=CacheMode.BYPASS,  # Don't use cached data
            extraction_strategy=llm_strategy,  # Strategy for data extraction
            css_selector=css_selector,  # Target specific content on the page
            session_id=session_id,  # Unique session ID for the crawl
        ),
    )
    
    if result.success:
        if "No Results Found" in result.cleaned_html:
            print("No Results Found")
    else:
        print(f"Error fetching page for 'No Results Found' check: {result.error_message}")
        return False

    # Save the raw result in a text file
    os.makedirs('raw', exist_ok=True)
    with open(f"raw/raw_extracted_content_{next_id}_{area}_{listing_id}.txt", "w", encoding="utf-8") as file:
        file.write(str(result))

    # Save the extracted JSON content
    os.makedirs('json', exist_ok=True)
    json_file_name = f"json/json_{next_id}_{area}_{listing_id}.json"
    with open(json_file_name, "w", encoding="utf-8") as file:
        file.write(str(result.extracted_content))
        
    if not (result.success and result.extracted_content):
        print(f"Error fetching listing {listing_id}: {result.error_message}")
        return False

    # Parse extracted content
    extracted_data = json.loads(result.extracted_content)

    # Print the extracted data for verification
    print(json.dumps(extracted_data, indent=4))

    print(f"Extracted Listing {listing_id} successfully.")
    
    print("Saving CSV file...")
    csv_file_name = f"csv_main.csv"
    save_listing_data_to_csv(json_file_name, csv_file_name, next_id, listing_id)
    
    image_folder_path = f'images/{area}/{next_id}_{listing_id}'
    save_images(json_file_name, image_folder_path)
    return True  # Indicate successful processing
