import asyncio

from crawl4ai import AsyncWebCrawler
from dotenv import load_dotenv

from config import CSS_SELECTOR, URL_list

from utils.scraper_utils import (
    fetch_and_process_listing_page,
    get_browser_config,
    get_llm_strategy,
)

load_dotenv()

async def run_airbnb_scraper():
    """
    Main asynchronous function to run the Airbnb web scraping process.
    Initializes the crawler, fetches room data, and saves it.
    """
    # Initialize configurations
    browser_config = get_browser_config()
    llm_strategy = get_llm_strategy()

    # Load the next available ID for scraping sessions
    with open('next_ID.txt', 'r') as file:
        next_ID = int(file.read())
        
    # Start the web crawler context
    # Documentation: https://docs.crawl4ai.com/api/async-webcrawler/#asyncwebcrawler
    
    for room_id_from_list in URL_list["Dahab"]:
        async with AsyncWebCrawler(config=browser_config) as crawler:
            room_id_str = str(room_id_from_list)
            
            # Check if the room ID has already been processed
            with open('checked_ID.txt', 'r') as file:
                checked_ids = file.read().splitlines()
            if room_id_str in checked_ids:
                print(f"Room ID {room_id_str} already checked. Skipping...")
                continue
        
            next_ID += 1
            listing_url = f"https://www.airbnb.com/rooms/{room_id_str}"
            
            # Fetch and process data from the current page
            await fetch_and_process_listing_page(
                crawler,
                listing_url,
                CSS_SELECTOR,
                llm_strategy,
                "crawl_session_" + str(next_ID),
                "Dahab", # area name
                room_id_str,
                next_ID
            )

            # Update next_ID for the next session
            with open("next_ID.txt", "w") as file:
                file.write(str(next_ID))
            
            # Mark the current room ID as checked
            with open("checked_ID.txt", "a") as file:
                file.write(room_id_str + "\n")
                
            # Pause between requests to be respectful and avoid rate limits.
            print("Pausing for 90 seconds...")
            await asyncio.sleep(90)

    # Display usage statistics for the LLM strategy
    llm_strategy.show_usage()


if __name__ == "__main__":
    asyncio.run(run_airbnb_scraper())

