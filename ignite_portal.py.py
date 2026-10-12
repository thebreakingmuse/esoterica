import os
import sys
import json
import shutil
import subprocess
import time

# Base Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BRANCHES_JSON = os.path.join(BASE_DIR, 'branches.json')
PORTALS_DIR = os.path.join(BASE_DIR, 'portals')

THUMBNAILS = [
    "01-hexagonal-gate.webp", "02-lunar-oracle.webp", "03-metatron-bloom.webp",
    "04-alchemical-conjunction.webp", "05-eightfold-compass.webp", "06-vesica-tide.webp",
    "07-triple-ouroboros.webp", "08-black-sun-mandala.webp"
]

def main():
    print("✦ CONIUNCTIO PORTAL IGNITION ✦\n")
    
    # Accept folder drop via terminal argument, or manual prompt
    if len(sys.argv) > 1:
        source_folder = sys.argv[1]
    else:
        source_folder = input("Drag and drop the image folder here and press Enter: ").strip().strip("'\"")

    if not os.path.isdir(source_folder):
        print("Error: Invalid folder path.")
        return

    folder_name = os.path.basename(os.path.normpath(source_folder))
    branch_name = input(f"Name this portal branch (Default: {folder_name}): ").strip()
    if not branch_name:
        branch_name = folder_name

    # Load existing branches
    if os.path.exists(BRANCHES_JSON):
        with open(BRANCHES_JSON, 'r') as f:
            branches = json.load(f)
    else:
        branches = []

    # Create unique ID and destination folder
    branch_id = str(int(time.time()))
    dest_dir = os.path.join(PORTALS_DIR, branch_id)
    os.makedirs(dest_dir, exist_ok=True)

    # Copy standard web images into the local project directory
    valid_exts = ('.jpg', '.jpeg', '.png', '.gif', '.webp')
    image_urls = []
    
    for file in os.listdir(source_folder):
        if file.lower().endswith(valid_exts):
            shutil.copy2(os.path.join(source_folder, file), dest_dir)
            image_urls.append(f"portals/{branch_id}/{file}")

    if not image_urls:
        print("No valid images found. Aborting.")
        os.rmdir(dest_dir)
        return

    # Assign thumbnail sequentially and package data
    thumbnail = THUMBNAILS[len(branches) % len(THUMBNAILS)]
    branches.append({
        "id": branch_id,
        "name": branch_name.upper(),
        "thumbnail": thumbnail,
        "images": image_urls
    })

    # Write the updated data to the JSON manifest
    with open(BRANCHES_JSON, 'w') as f:
        json.dump(branches, f, indent=4)

    print(f"\nBranch '{branch_name}' manifested locally with {len(image_urls)} images.")
    
    # Optional: Automate the Netlify Deploy via Git
    push = input("\nPush to GitHub/Netlify now? (y/n): ").strip().lower()
    if push == 'y':
        print("Committing and pushing...")
        subprocess.run(["git", "add", "."])
        subprocess.run(["git", "commit", "-m", f"Manifested new portal: {branch_name}"])
        subprocess.run(["git", "push"])
        print("Push complete. Netlify is building.")

if __name__ == "__main__":
    main()