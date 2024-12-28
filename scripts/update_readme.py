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
import sys
readme_path = './README.md'  # Correct relative path
websites_path = './websites'  # Correct relative path
config_path = './scripts/config.json'  # Correct relative path
images_path = './images'  # Correct relative path
gifs_path = './gifs'  # Correct relative path

if __name__ == "__main__":
    # Call your update_readme function and capture the result (True/False)
    new_entries = update_readme(readme_path, websites_path, config_path, images_path, gifs_path)
    new_entries = True  
    # After performing actions, output the result
    if new_entries:
        print("::set-output name=new-entries::true")
    else:
        print("::set-output name=new-entries::false")
