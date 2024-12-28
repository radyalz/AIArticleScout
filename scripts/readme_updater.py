import json
import os
from datetime import datetime
from readme_reader import get_readme_content
from config_reader import get_config
from commit_author import get_commit_author
from contributors_formatter import format_contributors
from website_entries import get_new_entries

def update_readme(readme_path, websites_path, config_path, images_path, gifs_path):
    config = get_config(config_path)
    readme_content = get_readme_content(readme_path)  # Read current content
    new_entries = get_new_entries(websites_path, readme_content)
    print(f"New Entries: {new_entries}") 
    # Find the line numbers (or approximate)
    lines = readme_content.splitlines()
    # Section line numbers
    section_line = next(i for i, line in enumerate(lines) if "## 📖 All updates of resource list" in line)
    example_line = next(i for i, line in enumerate(lines) if "## 🛠️ Example Entry:" in line)
    license_line = next(i for i, line in enumerate(lines) if "## 📜 License" in line)
    json_example_line = next(i for i, line in enumerate(lines) if "## 📇 here is the example of a json file" in line)
    section_four_line = next(i for i, line in enumerate(lines) if "### 4️⃣ Add an Image or gifs" in line)
    
    # Remove content after "## 📖 All updates of resource list"
    lines = lines[:section_line + 1]
    # Remove content between "## 🛠️ Example Entry:" and ## 📜 License  
    lines = lines[:example_line + 1] + lines[license_line - 4:]

    if new_entries:
        try:
            with open(readme_path, 'r+', encoding='utf-8') as readme_file:
                readme_content = readme_file.read()
                # Initialize the entries
                entry_number = 1
                example_number = 1
                example_entries_content = ""  # To store formatted example entries
                regular_entries_content = ""  # To store regular entries

                # Find the last non-empty line to insert new content
                last_non_empty_line = len(lines) - 1
                while last_non_empty_line >= 0 and not lines[last_non_empty_line].strip():
                    last_non_empty_line -= 1

                # Flag to track if changes were made
                changes_made = False

                for file_path, website_data in new_entries:
                    if file_path not in readme_content:
                        author = get_commit_author(file_path)
                        contributors = format_contributors(website_data, config)
                        entry_link = f"🌐 [{website_data['website']}]({website_data['link']})"
                        content = f"**Description:** 📝 {website_data['Description']}\n\n"
                        
                        # Get the image filename from the website data
                        image_filename = website_data.get("image", "")
                        # Construct the full image path using os.path.join
                        image_path = os.path.join(images_path, image_filename)
                        # Normalize the image path (ensure consistent path format with forward slashes)
                        image_path = image_path.replace("\\", "/")  # Ensure forward slashes are used in the path
                        # Check if the image exists and add it to the content
                        if os.path.exists(image_path):
                            content += f"![{website_data['website']}]({image_path})\n\n"

                        if website_data.get("attributes", {}).get("pros"):
                            content += "#### 🌟 Pros:\n"
                            for pro in website_data["attributes"]["pros"]:
                                content += f"- ✅ **{pro}:** Add pros as bullet points here\n"

                        if website_data.get("attributes", {}).get("cons"):
                            content += "#### ❌ Cons:\n"
                            for con in website_data["attributes"]["cons"]:
                                content += f"- 🚫 **{con}:** Add cons as bullet points here\n"

                        content += "\n### 🎥 Tutorial Videos\n"
                        for video in website_data.get("videos", []):
                            content += f"#### 📹 {video['title']}:\n"
                            content += f"**Description:** 🎬 {video['Description']}\n"
                            content += f"[![Click to View Video]({video['thumbnail']})]({video['link']})\n"
                            content += "\n"
                        
                        content += f"\n**🔖 Category:** {', '.join(website_data.get('Category', []))}\n"
                        content += f"**🏷️ Tags:** {', '.join(website_data.get('Tags', []))}\n"
                        content += f"**🤝 Contributor:** 🎤 {contributors}\n"
                        print(f"Adding entry: {website_data['type']}")

                        if website_data['type'] == 'example':
                            # Format example entries for the example section
                            example_title = f"## {example_number}️⃣"
                            example_entry = f"{example_title} {entry_link}\n{content}\n**Contributor:** {author}"
                            example_entries_content += f"\n{example_entry}\n"
                            # Add the formatted example entries json in the correct section
                            lines = lines[:json_example_line + 1] + [f"\n```json\n{json.dumps(website_data, indent=2)}\n```"] + lines[section_four_line - 1:]
                            # Add the example entries under the "Example Entry" section
                            lines = lines[:example_line + 1] + [f"{example_entries_content}"] + lines[license_line - 2:]
                            example_number += 1
                        elif website_data['type'] == 'entry':
                            # Format regular entries for the resource list
                            entry_title = f"## {entry_number}️⃣"
                            numbered_entry = f"{entry_title} {entry_link}\n{content}\n**Contributor:** {author}"
                            regular_entries_content += f"\n{numbered_entry}\n"
                            # Add the regular entries under the "All updates" section
                            lines.insert(last_non_empty_line + 2, f"{regular_entries_content}")
                            entry_number += 1
                        else:
                            # Handle any other cases
                            pass
                        
                        changes_made = True  # Mark changes as made

                # If changes were made, update the file
                if changes_made:
                    current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    readme_content = "\n".join(lines).replace("{{ update_date }}", f"Last Updated: {current_date}")
                    # Write the updated content back to the README file
                    readme_file.seek(0)
                    readme_file.write(readme_content)
                    readme_file.truncate()
                with open(readme_path, 'r+', encoding='utf-8') as readme_file:
                    # Read content and make modifications
                    readme_content = readme_file.read()
                    # Perform modifications as needed...
                    
                    # Debug: Print changes before writing back
                    print("Changes made to README.md:")
                    print("\n".join(lines))  # or just print the modified lines
                    
                    # After modification, write back
                    readme_file.seek(0)
                    readme_file.write(readme_content)
                    readme_file.truncate()
                # Output the result
                return changes_made  

        except Exception as e:
            print(f"Error writing to {readme_path}: {e}")
            return False
    return False
