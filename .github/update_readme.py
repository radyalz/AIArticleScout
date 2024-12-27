import os
import json
from datetime import datetime

# Paths (relative to this script)
BASE_DIR = os.path.dirname(__file__)
README_PATH = os.path.join(BASE_DIR, '..', 'README.md')
CONFIG_PATH = os.path.join(BASE_DIR, 'config.json')
WEBSITES_PATH = os.path.join(BASE_DIR, '..', 'websites')


def load_config():
    """Load contributor tags and full names from config.json."""
    try:
        with open(CONFIG_PATH, 'r', encoding='utf-8') as file:
            config = json.load(file)
            return config.get("contributors", {})  # Default to an empty dict if missing
    except Exception as e:
        print(f"Error loading config: {e}")
        return {}


def parse_metadata(content):
    """Parse metadata from markdown content."""
    metadata = {
        "title": "",
        "description": "",
        "pros": [],
        "cons": [],
        "category": "Uncategorized",
        "tags": "No tags",
        "contributor": "Unknown Contributor",
        "image": "",
        "tutorial_videos": []
    }
    lines = content.splitlines()

    # Extract metadata
    for i, line in enumerate(lines):
        if line.startswith("## "):
            metadata['title'] = line.replace("## ", "").strip()
        elif line.startswith("**Description:"):
            metadata['description'] = lines[i + 1].strip() if i + 1 < len(lines) else ""
        elif line.startswith("![Website Screenshot]") or line.startswith("![Image]"):
            metadata['image'] = extract_image(line)
        elif line.startswith("### **Pros:**"):
            metadata['pros'] = extract_list(lines, i + 1)
        elif line.startswith("### **Cons:**"):
            metadata['cons'] = extract_list(lines, i + 1)
        elif line.startswith("## Tutorial Videos"):
            metadata['tutorial_videos'] = extract_videos(lines, i + 1)
        elif line.startswith("**Category:"):
            metadata['category'] = line.split(":")[1].strip()
        elif line.startswith("**Tags:"):
            metadata['tags'] = line.split(":")[1].strip()
        elif line.startswith("**Contributor:"):
            metadata['contributor'] = line.split(":")[1].strip()

    return metadata


def extract_list(lines, start_index):
    """Extract a list of bullet points."""
    items = []
    for line in lines[start_index:]:
        if line.startswith("- "):
            items.append(line.replace("- ", "").strip())
        elif line.strip() == "":
            break  # Stop at blank line
    return items


def extract_videos(lines, start_index):
    """Extract tutorial videos from the markdown content."""
    videos = []
    for line in lines[start_index:]:
        if "![](gifs/" in line:
            link = extract_image(line)
            videos.append(link)
        elif line.strip() == "":
            break  # Stop at blank line
    return videos


def extract_image(line):
    """Extract image or video path from markdown syntax."""
    if "![" in line and "](" in line:
        return line.split("(")[1].split(")")[0]
    return ""


def get_new_entries(contributor_tags):
    """Find new markdown files to process."""
    entries = []
    readme_content = get_readme_content()

    for root, _, files in os.walk(WEBSITES_PATH):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, os.path.dirname(README_PATH))

                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if content not in readme_content:  # Only process new entries
                            metadata = parse_metadata(content)
                            metadata['contributor'] = contributor_tags.get(metadata['contributor'], metadata['contributor'])
                            metadata['path'] = relative_path
                            entries.append(metadata)
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
    return entries


def get_readme_content():
    """Read the current README content."""
    try:
        with open(README_PATH, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"Error reading README.md: {e}")
        return ""


def update_readme():
    """Update README.md with new entries."""
    # Load contributors
    contributor_tags = load_config()
    entries = get_new_entries(contributor_tags)

    if entries:
        try:
            with open(README_PATH, 'a', encoding='utf-8') as readme_file:
                current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                for entry in entries:
                    section = f"### {entry['title']}\n---\n"
                    section += f"## [{entry['title']}]({entry['path']})\n\n"
                    section += f"**Description:**  \n{entry['description']}\n\n"

                    if entry['image']:
                        section += f"![Website Screenshot]({entry['image']})\n\n"

                    section += "### Pros and Cons\n\n#### **Pros:**\n"
                    for pro in entry['pros']:
                        section += f"- {pro}\n"

                    section += "\n#### **Cons:**\n"
                    for con in entry['cons']:
                        section += f"- {con}\n"

                    if entry['tutorial_videos']:
                        section += "\n---\n## Tutorial Videos\n"
                        for video in entry['tutorial_videos']:
                            section += f"[![Click to View Video]({video})]({video})\n\n"

                    section += "---\n"
                    section += f"**Category:** {entry['category']}\n"
                    section += f"**Tags:** {entry['tags']}\n"
                    section += f"**Contributor:** {entry['contributor']}\n\n"

                    readme_file.write(section)

        except Exception as e:
            print(f"Error updating README.md: {e}")


if __name__ == "__main__":
    update_readme()
