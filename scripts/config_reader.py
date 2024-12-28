# config_reader.py
import json

def get_config(config_path):
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error reading {config_path}: {e}")
        return {}
