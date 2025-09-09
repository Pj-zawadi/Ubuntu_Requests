import requests
import os
from urllib.parse import urlparse
import hashlib

def get_filename_from_url(url):
    """Extract filename from URL or generate a unique one."""
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)
    
    # If no filename, generate one using a hash
    if not filename:
        filename = hashlib.md5(url.encode()).hexdigest()[:10] + ".jpg"
    return filename

def download_image(url, folder="Fetched_Images"):
    """Download a single image with error handling and duplicate prevention."""
    try:
        # Create directory if not exists
        os.makedirs(folder, exist_ok=True)

        # Fetch the image
        response = requests.get(url, timeout=10, stream=True)
        response.raise_for_status()  # Raise error for bad status codes

        # Extract filename
        filename = get_filename_from_url(url)
        filepath = os.path.join(folder, filename)

        # Prevent duplicates
        if os.path.exists(filepath):
            print(f"⚠ Skipping duplicate: {filename}")
            return

        # Check headers (safety precaution)
        content_type = response.headers.get("Content-Type", "")
        if not content_type.startswith("image/"):
            print(f"✗ Not an image: {url}")
            return

        # Save image in binary mode
        with open(filepath, "wb") as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)

        print(f"✓ Successfully fetched: {filename}")
        print(f"✓ Image saved to {filepath}")

    except requests.exceptions.RequestException as e:
        print(f"✗ Connection error: {e}")
    except Exception as e:
        print(f"✗ Unexpected error: {e}")

def main():
    print("🌍 Welcome to the Ubuntu Image Fetcher")
    print("A tool for mindfully collecting images from the web\n")
    print("💡 Tip: You can enter multiple URLs separated by spaces.\n")

    # Get URLs from user
    urls = input("Please enter image URL(s): ").split()

    for url in urls:
        download_image(url)

    print("\nConnection strengthened. Community enriched. ✨")

if __name__ == "__main__":
    main()
