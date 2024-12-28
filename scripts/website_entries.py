import os
import json

def get_new_entries(websites_path, readme_content):
    new_entries = []
    for root, dirs, files in os.walk(websites_path):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        website_data = json.load(f)

                        # Add type attribute based on the example flag
                        if website_data.get('example', True):
                            website_data['type'] = 'example'
                        else:
                            website_data['type'] = 'entry'

                        # Skip if 'example' is False but still add type
                        if website_data.get('show', True):
                            if file_path not in readme_content:
                                new_entries.append((file_path, website_data))
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
    return new_entries
