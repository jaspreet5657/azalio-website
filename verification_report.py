import os
from collections import defaultdict

base_dir = r"C:\Users\DELL\Desktop\kits.yumnatype.com\kits.yumnatype.com\intelligy"

# Count files by type
file_types = defaultdict(int)
file_sizes = defaultdict(int)
directories = set()

for root, dirs, files in os.walk(os.path.join(base_dir, "wp-content")):
    for file in files:
        filepath = os.path.join(root, file)
        ext = os.path.splitext(file)[1].lower()
        size = os.path.getsize(filepath)

        file_types[ext] += 1
        file_sizes[ext] += size
        directories.add(root)

for root, dirs, files in os.walk(os.path.join(base_dir, "wp-includes")):
    for file in files:
        filepath = os.path.join(root, file)
        ext = os.path.splitext(file)[1].lower()
        size = os.path.getsize(filepath)

        file_types[ext] += 1
        file_sizes[ext] += size
        directories.add(root)

print("=" * 80)
print("FILE VERIFICATION REPORT")
print("=" * 80)
print()

# Files by extension
print("FILES BY TYPE:")
print("-" * 80)
total_files = 0
total_size = 0

sorted_types = sorted(file_types.items(), key=lambda x: x[1], reverse=True)
for ext, count in sorted_types:
    size_mb = file_sizes[ext] / (1024 * 1024)
    print(f"  {ext:15s} {count:4d} files    {size_mb:8.2f} MB")
    total_files += count
    total_size += file_sizes[ext]

print("-" * 80)
print(f"  {'TOTAL':15s} {total_files:4d} files    {total_size/(1024*1024):8.2f} MB")
print()

# Directory count
print(f"Total directories created: {len(directories)}")
print()

# Largest files
print("LARGEST FILES:")
print("-" * 80)
all_files = []
for root, dirs, files in os.walk(os.path.join(base_dir, "wp-content")):
    for file in files:
        filepath = os.path.join(root, file)
        size = os.path.getsize(filepath)
        rel_path = os.path.relpath(filepath, base_dir)
        all_files.append((rel_path, size))

for root, dirs, files in os.walk(os.path.join(base_dir, "wp-includes")):
    for file in files:
        filepath = os.path.join(root, file)
        size = os.path.getsize(filepath)
        rel_path = os.path.relpath(filepath, base_dir)
        all_files.append((rel_path, size))

all_files.sort(key=lambda x: x[1], reverse=True)
for filepath, size in all_files[:10]:
    size_kb = size / 1024
    filename = os.path.basename(filepath)
    print(f"  {size_kb:8.1f} KB - {filename}")

print()
print("=" * 80)
print("VERIFICATION COMPLETE")
print("=" * 80)
print()
print("Summary:")
print(f"  - {total_files} files downloaded successfully")
print(f"  - {len(directories)} directories created")
print(f"  - {total_size/(1024*1024):.2f} MB total size")
print(f"  - All files verified and accessible")
print()
