import os
import subprocess
import json
from datetime import datetime

# Paths to the necessary files and directories
readme_path = '../README.md'  # Adjusted path to README.md
websites_path = '../websites'  # Adjusted path to websites folder containing JSON files
images_path = '../images'  # Folder where images are stored
gifs_path = '../gifs'  # Folder where GIFs are stored
config_path = './config.json'  # config.json is in the same folder as the script

def get_readme_content():
    try:
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading {readme_path}: {e}")
        return ""

def get_config():
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error reading {config_path}: {e}")
        return {}

def get_new_entries():
    readme_content = get_readme_content()  # Read the current README.md content
    new_entries = []
    for root, dirs, files in os.walk(websites_path):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        website_data = json.load(f)
                        # Check if the entry should be included (show is true or not set)
                        if website_data.get('show', True):
                            # Check if the entry is not already in README
                            if file_path not in readme_content:
                                new_entries.append((file_path, website_data))
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
    return new_entries

def get_commit_author(file_path):
    # Extract the last commit's author for the given file
    try:
        result = subprocess.run(
            ['git', 'log', '-1', '--format=%an', '--', file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
            text=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error getting commit author for {file_path}: {e}")
        return "Unknown Contributor"

def update_readme():
    config = get_config()
    new_entries = get_new_entries()

    if new_entries:
        try:
            with open(readme_path, 'r+', encoding='utf-8') as readme_file:
                readme_content = readme_file.read()  # Read current content
                entry_number = 1  # Initialize the entry numbering
                for file_path, website_data in new_entries:
                    # Ensure the entry does not already exist in the README
                    if file_path not in readme_content:
                        author = get_commit_author(file_path)

                        # Prepare entry title
                        entry_title = f"## {entry_number}️⃣"

                        # Prepare website link
                        entry_link = f"[{website_data['website']}]({website_data['link']})"
                        
                        # Add Description
                        content = f"**Description:** 📝 {website_data['Description']}\n\n"
                        
                        # Prepare image path (assuming images are in the ../images directory)
                        image_filename = website_data.get("image", "")
                        image_path = os.path.join(images_path, image_filename)
                        if os.path.exists(image_path):
                            content += f"![Website Screenshot]({image_path})\n\n"
                        
                        # Prepare GIF path (assuming gifs are in the ../gifs directory)
                        gif_filename = website_data.get("gif", "")
                        gif_path = os.path.join(gifs_path, gif_filename)
                        if os.path.exists(gif_path):
                            content += f"![GIF Tutorial]({gif_path})\n\n"

                        # Add Pros and Cons with emojis
                        if website_data.get("attributes", {}).get("pros"):
                            content += "#### 🌟 Pros:\n"
                            for pro in website_data["attributes"]["pros"]:
                                content += f"- ✅ **{pro}:** Add pros as bullet points here\n"  # Emoji and description

                        if website_data.get("attributes", {}).get("cons"):
                            content += "#### ❌ Cons:\n"
                            for con in website_data["attributes"]["cons"]:
                                content += f"- 🚫 **{con}:** Add cons as bullet points here\n"  # Emoji and description

                        # Add Video Section
                        content += "\n### 🎥 Tutorial Videos\n"
                        for video in website_data.get("videos", []):
                            content += f"#### 📹 {video['title']}:\n"
                            content += f"**Description:** 🎬 {video['Description']}\n"
                            content += f"[![Click to View Video]({video['thumbnail']})]({video['link']})\n"
                            content += "---\n"
                        
                        # Add Category and Tags
                        content += f"\n**🔖 Category:** {', '.join(website_data.get('Category', []))}\n"
                        content += f"**🏷️ Tags:** {', '.join(website_data.get('Tags', []))}\n"
                        content += f"**🤝 Contributor:** 🎤 {config.get('contributors', {}).get(website_data.get('Contributor'), website_data.get('Contributor'))}\n"

                        # Full Example JSON Code Block
                        content += f"\n```json\n{json.dumps(website_data, indent=2)}\n```\n"

                        # Add entry to the README
                        numbered_entry = f"{entry_title} {entry_link}\n{content}\n**Contributor:** {author}\n"
                        readme_file.write(f"\n---\n{numbered_entry}\n")
                        entry_number += 1  # Increment the entry number

                # Replace the placeholder with the current date
                current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                readme_file.seek(0)  # Move to the start of the file
                updated_content = readme_file.read().replace("{{ update_date }}", f"Last Updated: {current_date}")
                readme_file.seek(0)
                readme_file.write(updated_content)
                readme_file.truncate()
        except Exception as e:
            print(f"Error writing to {readme_path}: {e}")

if __name__ == "__main__":
    update_readme()
