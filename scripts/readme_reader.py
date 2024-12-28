# readme_reader.py
import os

def get_readme_content(readme_path):
    try:
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading {readme_path}: {e}")
        return ""
