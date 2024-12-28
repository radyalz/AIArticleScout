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
import os
from readme_updater import update_readme

readme_path = './README.md'  # Correct relative path
websites_path = './websites'  # Correct relative path
config_path = './scripts/config.json'  # Correct relative path
images_path = './images'  # Correct relative path
gifs_path = './gifs'  # Correct relative path

if __name__ == "__main__":
    # Call your update_readme function
    new_entries = update_readme(readme_path, websites_path, config_path, images_path, gifs_path)

    # Set the 'new-entries' environment variable
    if new_entries:
        os.environ['new-entries'] = 'true'
    else:
        os.environ['new-entries'] = 'false'

    # Optionally print for debugging
    print(f"new-entries set to {os.environ['new-entries']}")