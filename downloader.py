import os
import subprocess
import time
from pathlib import Path

# Read download list
base_dir = r"C:\Users\DELL\Desktop\kits.yumnatype.com\kits.yumnatype.com\intelligy"
download_list_file = os.path.join(base_dir, 'download_list.txt')

downloads = []
with open(download_list_file, 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if line:
            url, local_path = line.split('|')
            downloads.append({'url': url, 'local_path': local_path})

print(f"Total files to download: {len(downloads)}")
print("=" * 80)

# Create all necessary directories first
print("\nCreating directory structure...")
directories_created = set()
for item in downloads:
    dir_path = os.path.dirname(item['local_path'])
    if dir_path not in directories_created:
        os.makedirs(dir_path, exist_ok=True)
        directories_created.add(dir_path)

print(f"Created {len(directories_created)} directories")

# Download files
successful = []
failed = []
skipped = []

print("\nDownloading files...")
print("=" * 80)

for i, item in enumerate(downloads, 1):
    url = item['url']
    local_path = item['local_path']

    # Skip if file already exists
    if os.path.exists(local_path):
        skipped.append(item)
        print(f"[{i}/{len(downloads)}] SKIP: {os.path.basename(local_path)} (already exists)")
        continue

    # Download using curl
    try:
        # Use curl with follow redirects and silent mode
        result = subprocess.run(
            ['curl', '-L', '-o', local_path, url, '--create-dirs', '--silent', '--show-error', '--max-time', '30'],
            capture_output=True,
            text=True,
            timeout=35
        )

        if result.returncode == 0 and os.path.exists(local_path) and os.path.getsize(local_path) > 0:
            file_size = os.path.getsize(local_path)
            successful.append(item)
            print(f"[{i}/{len(downloads)}] OK: {os.path.basename(local_path)} ({file_size} bytes)")
        else:
            failed.append({'item': item, 'error': result.stderr or 'Unknown error'})
            print(f"[{i}/{len(downloads)}] FAIL: {os.path.basename(local_path)}")
            if result.stderr:
                print(f"    Error: {result.stderr[:100]}")

    except subprocess.TimeoutExpired:
        failed.append({'item': item, 'error': 'Timeout'})
        print(f"[{i}/{len(downloads)}] FAIL: {os.path.basename(local_path)} (timeout)")
    except Exception as e:
        failed.append({'item': item, 'error': str(e)})
        print(f"[{i}/{len(downloads)}] FAIL: {os.path.basename(local_path)} ({str(e)})")

    # Small delay to avoid overwhelming the server
    time.sleep(0.1)

# Summary
print("\n" + "=" * 80)
print("DOWNLOAD SUMMARY")
print("=" * 80)
print(f"Total files: {len(downloads)}")
print(f"Successfully downloaded: {len(successful)}")
print(f"Skipped (already exist): {len(skipped)}")
print(f"Failed: {len(failed)}")

if failed:
    print("\nFailed downloads:")
    for item in failed[:20]:  # Show first 20 failures
        print(f"  - {item['item']['url']}")
        print(f"    Error: {item['error'][:100]}")
    if len(failed) > 20:
        print(f"  ... and {len(failed) - 20} more failures")

# Save results
results_file = os.path.join(base_dir, 'download_results.txt')
with open(results_file, 'w', encoding='utf-8') as f:
    f.write("DOWNLOAD RESULTS\n")
    f.write("=" * 80 + "\n\n")
    f.write(f"Total files: {len(downloads)}\n")
    f.write(f"Successfully downloaded: {len(successful)}\n")
    f.write(f"Skipped (already exist): {len(skipped)}\n")
    f.write(f"Failed: {len(failed)}\n\n")

    if successful:
        f.write("\nSuccessful downloads:\n")
        for item in successful:
            f.write(f"  {item['local_path']}\n")

    if skipped:
        f.write("\nSkipped files:\n")
        for item in skipped:
            f.write(f"  {item['local_path']}\n")

    if failed:
        f.write("\nFailed downloads:\n")
        for item in failed:
            f.write(f"  {item['item']['url']}\n")
            f.write(f"    Error: {item['error']}\n")

print(f"\nDetailed results saved to: {results_file}")

# Directory structure summary
print("\nDirectory structure created:")
sorted_dirs = sorted(directories_created)
for dir_path in sorted_dirs[:10]:
    rel_path = os.path.relpath(dir_path, base_dir)
    file_count = len([s for s in successful + skipped if os.path.dirname(s['local_path']) == dir_path])
    print(f"  {rel_path} ({file_count} files)")
if len(sorted_dirs) > 10:
    print(f"  ... and {len(sorted_dirs) - 10} more directories")
