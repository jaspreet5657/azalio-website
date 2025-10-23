import re
import os
import subprocess
from urllib.parse import urlparse, unquote
from pathlib import Path

# Read the HTML file
html_file = r"C:\Users\DELL\Desktop\kits.yumnatype.com\kits.yumnatype.com\intelligy\index.html"
with open(html_file, 'r', encoding='utf-8') as f:
    html_content = f.read()

# Extract all URLs starting with https://kits.yumnatype.com/intelligy/
base_url = "https://kits.yumnatype.com/intelligy/"
url_pattern = r'https://kits\.yumnatype\.com/intelligy/[^"\'\s)>]+'
urls = re.findall(url_pattern, html_content)

# Remove duplicates
unique_urls = list(set(urls))

# Filter out non-static resources
excluded_patterns = [
    'xmlrpc.php',
    'wp-json',
    '/feed/',
    '/comments/',
    'embed?url=',
    '/template-kit/',  # These are page URLs, not static assets
    '/single-post',
    '/intelligy/?',
    '/intelligy/#',
]

static_extensions = [
    '.css', '.js', '.png', '.jpg', '.jpeg', '.gif', '.svg',
    '.woff', '.woff2', '.ttf', '.eot', '.ico', '.webp'
]

def is_static_resource(url):
    """Check if URL is a static resource we want to download"""
    # Skip excluded patterns
    for pattern in excluded_patterns:
        if pattern in url:
            return False

    # Check if it has a static extension
    for ext in static_extensions:
        if ext in url.lower():
            return True

    return False

# Filter URLs
downloadable_urls = [url for url in unique_urls if is_static_resource(url)]

# Sort URLs for better organization
downloadable_urls.sort()

print(f"Total unique URLs found: {len(unique_urls)}")
print(f"Static resources to download: {len(downloadable_urls)}")
print("\nDownloadable URLs:")
print("=" * 80)

# Group by type for summary
css_files = [u for u in downloadable_urls if '.css' in u]
js_files = [u for u in downloadable_urls if '.js' in u]
image_files = [u for u in downloadable_urls if any(ext in u.lower() for ext in ['.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp'])]
font_files = [u for u in downloadable_urls if any(ext in u for ext in ['.woff', '.woff2', '.ttf', '.eot'])]

print(f"\nCSS files: {len(css_files)}")
print(f"JS files: {len(js_files)}")
print(f"Image files: {len(image_files)}")
print(f"Font files: {len(font_files)}")

# Create download list with local paths
base_dir = r"C:\Users\DELL\Desktop\kits.yumnatype.com\kits.yumnatype.com\intelligy"
downloads = []

for url in downloadable_urls:
    # Remove base URL and query parameters to get relative path
    relative_path = url.replace(base_url, '')

    # Remove query parameters for file path
    if '?' in relative_path:
        relative_path = relative_path.split('?')[0]

    # Decode URL encoding
    relative_path = unquote(relative_path)

    # Create local file path
    local_path = os.path.join(base_dir, relative_path)

    downloads.append({
        'url': url,
        'local_path': local_path,
        'relative_path': relative_path
    })

# Save download list to file
download_list_file = os.path.join(base_dir, 'download_list.txt')
with open(download_list_file, 'w', encoding='utf-8') as f:
    for item in downloads:
        f.write(f"{item['url']}|{item['local_path']}\n")

print(f"\nDownload list saved to: {download_list_file}")
print(f"Total files to download: {len(downloads)}")

# Print unique directories that will be created
directories = set()
for item in downloads:
    dir_path = os.path.dirname(item['local_path'])
    directories.add(dir_path)

print(f"\nUnique directories to create: {len(directories)}")
print("\nDirectory structure:")
sorted_dirs = sorted(directories)
for dir_path in sorted_dirs[:20]:  # Show first 20
    print(f"  {dir_path}")
if len(sorted_dirs) > 20:
    print(f"  ... and {len(sorted_dirs) - 20} more directories")

# Print some sample URLs
print("\nSample URLs to download:")
for item in downloads[:10]:
    print(f"  {item['relative_path']}")
if len(downloads) > 10:
    print(f"  ... and {len(downloads) - 10} more files")
