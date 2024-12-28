# commit_author.py
import subprocess

def get_commit_author(file_path):
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
        return "Anonymous"
