import os
import subprocess

# Path to the README.md file
readme_path = './README.md'

# Path to the websites folder
websites_path = 'websites'

def get_readme_content():
    try:
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading {readme_path}: {e}")
        return ""

def get_new_entries():
    readme_content = get_readme_content()  # Read the current README.md content
    new_entries = []
    for root, dirs, files in os.walk(websites_path):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        # Check if the entry is not already in README
                        if content not in readme_content:
                            new_entries.append((file_path, content))
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
    new_entries = get_new_entries()

    if new_entries:
        try:
            with open(readme_path, 'a+', encoding='utf-8') as readme_file:
                readme_content = readme_file.read()  # Read current content to check for duplicates
                entry_number = 1  # Initialize the entry numbering
                for file_path, entry in new_entries:
                    # Ensure the entry does not already exist in the README
                    if entry not in readme_content:
                        author = get_commit_author(file_path)
                        numbered_entry = f"## #{entry_number}\n{entry}\n**Contributor:** {author}\n"
                        readme_file.write(f"\n---\n{numbered_entry}\n")
                        entry_number += 1  # Increment the entry number
        except Exception as e:
            print(f"Error writing to {readme_path}: {e}")

if __name__ == "__main__":
    update_readme()
