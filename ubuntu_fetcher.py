import requests
import os
import hashlib
from urllib.parse import urlparse

def sanitize_filename(url):
    """
    Extract a filename from the URL or generate one using a hash.
    Ensures uniqueness and safety.
    """
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)
    
    if not filename:
        filename = hashlib.md5(url.encode()).hexdigest() + ".jpg"
    return filename

def download_image(url, save_dir="Fetched_Images", seen_hashes=set()):
    try:
        # Ensure directory exists
        os.makedirs(save_dir, exist_ok=True)

        # Add headers (respectful requests)
        headers = {"User-Agent": "UbuntuImageFetcher/1.0"}
        response = requests.get(url, timeout=10, headers=headers)
        response.raise_for_status()

        # Precaution: verify content type is image
        content_type = response.headers.get("Content-Type", "")
        if not content_type.startswith("image/"):
            print(f"✗ Skipping {url} (Not an image: {content_type})")
            return

        # Prevent duplicates (using hash of content)
        file_hash = hashlib.md5(response.content).hexdigest()
        if file_hash in seen_hashes:
            print(f"✗ Skipping {url} (Duplicate image detected)")
            return
        seen_hashes.add(file_hash)

        # Generate filename
        filename = sanitize_filename(url)
        filepath = os.path.join(save_dir, filename)

        # Save image in binary mode
        with open(filepath, "wb") as f:
            f.write(response.content)

        print(f"✓ Successfully fetched: {filename}")
        print(f"✓ Image saved to {filepath}")

    except requests.exceptions.RequestException as e:
        print(f"✗ Connection error while fetching {url}: {e}")
    except Exception as e:
        print(f"✗ Unexpected error with {url}: {e}")

def main():
    print("Welcome to the Ubuntu Image Fetcher")
    print("A tool for mindfully collecting images from the web\n")

    # Support multiple URLs (comma-separated input)
    urls = input("Please enter image URLs (separated by commas): ").split(",")

    seen_hashes = set()
    for url in [u.strip() for u in urls if u.strip()]:
        download_image(url, seen_hashes=seen_hashes)

    print("\nConnection strengthened. Community enriched.")

if __name__ == "__main__":
    main()
