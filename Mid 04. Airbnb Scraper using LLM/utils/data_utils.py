import csv
import json
import os

def save_listing_data_to_csv(json_file_name: str, csv_file_name: str, session_id: int, listing_id: str):
    """
    Saves extracted listing data from a JSON file to a CSV file.

    Args:
        json_file_name (str): Path to the JSON file containing listing data.
        csv_file_name (str): Path to the CSV file to save the data.
        session_id (int): The session ID associated with the scraped data.
        listing_id (str): The unique ID of the Airbnb listing.
    """
    with open(json_file_name, 'r', encoding='utf-8') as f:
        json_string = f.read()
    
    json_content = json.loads(json_string)
    
    # Ensure json_content is always a list of dictionaries
    if isinstance(json_content, dict):
        json_content = [json_content]

    fieldnames = ["ID", "Title", "Address", "URL"]
    csv_rows = []

    for item in json_content:
        title = item.get("Title")
        address = item.get("address", "")

        if not title:
            print(f"No listing title found in {json_file_name}")
            return

        listing_url = f"https://www.airbnb.com/rooms/{listing_id}"
        
        csv_rows.append({
            "ID": session_id,
            "Title": title,
            "Address": address,
            "URL": listing_url
        })

    if not csv_rows:
        print("No valid items with 'Title' found to save to CSV.")
        return

    file_exists = os.path.exists(csv_file_name)
    with open(csv_file_name, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        
        # Write header only if the file is new or empty
        if not file_exists or os.stat(csv_file_name).st_size == 0:
            writer.writeheader()
        
        writer.writerows(csv_rows)
    print(f"Successfully appended rows to '{csv_file_name}'.")
    
    
def save_images(json_file_name: str, image_folder_path: str):
    """
    Downloads images specified in a JSON file to a local folder.

    Args:
        json_file_name (str): Path to the JSON file containing image URLs.
        image_folder_path (str): Local path where images will be saved.
    """
    import time
    
    with open(json_file_name, 'r', encoding='utf-8') as f:
        json_string = f.read()
    
    json_content = json.loads(json_string)
    
    # Ensure json_content is always a list of dictionaries
    if isinstance(json_content, dict):
        json_content = [json_content]

    images_list = []
    for item in json_content:
        if "galleryImagesURL" in item:
            images_list.extend(item["galleryImagesURL"])

    if not images_list:
        print(f"No images found in {json_file_name}")
        return

    output_folder = os.path.join(image_folder_path)
    os.makedirs(output_folder, exist_ok=True)

    for idx, image_url in enumerate(images_list, start=1):
        image_name = f"Pic{idx:03}.jpeg"
        image_path = os.path.join(output_folder, image_name)

        # Check if image already exists
        if os.path.exists(image_path):
            print(
                f"{image_name} already exists in {output_folder}, skipping download")
            continue

        try:
            print("Downloading image:", image_url)
            # Download image using curl:
            curl_command = f'curl -L "{image_url}" -o "{image_path}"'
            os.system(curl_command)
            print(f"Downloaded {image_name} to {output_folder} using curl")
        except Exception as e:
            print(f"Failed to download {image_url}: {e}")
        time.sleep(0.25)
    print("Finished image downloading.")


