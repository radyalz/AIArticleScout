# # update_readme.py
# from readme_updater import update_readme

# readme_path = '../README.md'
# websites_path = '../websites'
# config_path = './config.json'
# images_path = '../images'
# gifs_path = '../gifs'

# if __name__ == "__main__":
#     update_readme(readme_path, websites_path, config_path, images_path, gifs_path)

# update_readme.py
from readme_updater import update_readme

# Use paths relative to the root of the repository
readme_path = './README.md'  # This assumes README.md is at the root
websites_path = './websites'  # Assuming websites is a folder at the root
config_path = './scripts/config.json'  # Assuming config.json is at the root
images_path = './images'  # Assuming images is a folder at the root
gifs_path = './gifs'  # Assuming gifs is a folder at the root

if __name__ == "__main__":
    update_readme(readme_path, websites_path, config_path, images_path, gifs_path)
