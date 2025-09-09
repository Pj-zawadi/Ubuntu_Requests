import requests
import os
from urllib.parse import urlparse
import hashlib

def main():
    """
    Main function to run the Ubuntu Image Fetcher program.
    """
    print("Welcome to the Ubuntu Image Fetcher")
    print("A tool for mindfully collecting images from the web\n")
    
    # Get URLs from user, allowing multiple entries
    urls = []
    while True:
        url = input("Please enter an image URL (or 'done' to finish): ")
        if url.lower() == 'done':
            break
        urls.append(url)
    
    # Create directory for images
    image_dir = "Fetched_Images"
    os.makedirs(image_dir, exist_ok=True)
    
    for url in urls:
        fetch_and_save_image(url, image_dir)
    
    print("\nConnection strengthened. Community enriched.")

def fetch_and_save_image(url, directory):
    """
    Fetches and saves a single image, handling errors and duplicates.
    
    Args:
        url (str): The URL of the image to download.
        directory (str): The directory to save the image in.
    """
    try:
        # Precaution 1: Validate URL and check HTTP headers
        parsed_url = urlparse(url)
        if not all([parsed_url.scheme, parsed_url.netloc]):
            print(f"✗ Invalid URL: {url}")
            return
            
        print(f"Attempting to fetch: {url}")
        
        # Precaution 2: Use a timeout for the request
        response = requests.get(url, timeout=10)
        
        # Check important HTTP headers before processing
        content_type = response.headers.get('Content-Type')
        content_length = response.headers.get('Content-Length')

        # Check for non-image content types.
        if not content_type or not content_type.startswith('image/'):
            print(f"✗ Skipped. URL does not point to an image. (Content-Type: {content_type})")
            return

        # Check for large files to avoid unexpected downloads.
        if content_length and int(content_length) > 10 * 1024 * 1024: # 10MB limit
            print(f"✗ Skipped. File is too large. (Size: {int(content_length) / 1024 / 1024:.2f} MB)")
            return

        response.raise_for_status()  # Raise an exception for bad status codes
        
        # Implement duplicate check using a hash of the content
        image_content = response.content
        image_hash = hashlib.md5(image_content).hexdigest()
        
        # Check if the image hash already exists
        duplicate_found = False
        for root, _, files in os.walk(directory):
            for filename in files:
                filepath = os.path.join(root, filename)
                with open(filepath, 'rb') as f:
                    existing_hash = hashlib.md5(f.read()).hexdigest()
                    if image_hash == existing_hash:
                        print(f"✓ Duplicate image found. Skipped saving: {filename}")
                        duplicate_found = True
                        break
            if duplicate_found:
                break
        
        if duplicate_found:
            return
            
        # Extract filename from URL or generate one if not available
        filename = os.path.basename(parsed_url.path)
        if not filename:
            filename = f"downloaded_image_{image_hash}.jpg"
        else:
            # Append hash to filename to prevent filename collisions
            name, ext = os.path.splitext(filename)
            filename = f"{name}_{image_hash}{ext}"
            
        filepath = os.path.join(directory, filename)
        
        # Save the image in binary mode
        with open(filepath, 'wb') as f:
            f.write(image_content)
            
        print(f"✓ Successfully fetched: {filename}")
        print(f"✓ Image saved to {filepath}")
        
    except requests.exceptions.RequestException as e:
        print(f"✗ Connection error for {url}: {e}")
    except Exception as e:
        print(f"✗ An error occurred for {url}: {e}")

if __name__ == "__main__":
    main()
