# update_readme.py
from readme_updater import update_readme

readme_path = '../README.md'
websites_path = '../websites'
config_path = './config.json'
images_path = '../images'
gifs_path = '../gifs'

if __name__ == "__main__":
    update_readme(readme_path, websites_path, config_path, images_path, gifs_path)
