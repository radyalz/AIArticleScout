import os

# Path to the README.md file
readme_path = 'README.md'

# Path to the websites folder
websites_path = 'websites'

def get_new_entries():
    new_entries = []
    for root, dirs, files in os.walk(websites_path):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    entry = f"## {content.splitlines()[0][3:]}\n"  # Extracting the website name
                    new_entries.append(entry)
    return new_entries

def update_readme():
    new_entries = get_new_entries()

    if new_entries:
        with open(readme_path, 'r+', encoding='utf-8') as readme_file:
            content = readme_file.read()
            for entry in new_entries:
                if entry not in content:
                    readme_file.write(f"\n---\n{entry}\n")

if __name__ == "__main__":
    update_readme()
