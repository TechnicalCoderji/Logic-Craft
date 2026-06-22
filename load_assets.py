"""
This file is used to load specific assets images form whole Assets Folder.
Efficient to load needed only Asssets to save memory space and time.

Main function of this file is load_assets, that load specific asset image file in pygame
object and return it.
"""

import os
import pygame

def load_assets(*folders:str):
    """This function takes Array of Strings that is subfolder name inside assets folder.
    used you load specific assets folder.

    Returns:
        dictionary of dictionary of pygame.image object: that cointain Pygame Image object with image name without .png for easy access
    """

    assets_dir = "Assets"
    assets = {}
    # for folder in os.listdir(assets_dir):
    for folder in folders: # Loop for list of assets folder needed
        
        folder_path = os.path.join(assets_dir, folder) # Create Path of that Folder
        if os.path.isdir(folder_path):
            image_dict = {} # making image dict to store pygame image object as value with image file name as path without .extention_name
            for file in os.listdir(folder_path): # Loop through all files in particular folder
                if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')): # Condition for checking only images
                    image_name = os.path.splitext(file)[0] # get Image name without extension
                    image_path = os.path.join(folder_path, file) # make full path of image for pygame
                    image_dict[image_name] = pygame.image.load(image_path) # create and add pygame image object to dictionary
            assets[folder] = image_dict # add to main assets dictionary
    return assets # Returning that asset