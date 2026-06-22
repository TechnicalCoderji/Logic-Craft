"""
Docstring for help
This Module is for Helping Documentation about how to use Logic Craft. Just dummy page for now.
Implementation Coming soon
scrollable layout for each tab control, use and navigations.
"""

# Import usefull Modules
# External Libraries
import pygame

# Internal Modules
from core_tools import TextBox, ImageButton, variables

# Creating objects for GUI
# Back-Button
back_button = ImageButton(20,20,30,30,"general.back","general.back")
# Comming Soon Text
comming_soon_text = TextBox("Comming Soon.... ^_____^",150,250,600,100,"Poppins-Medium.ttf")

def draw_screen(screen:pygame.Surface):
    """draw_screen Handle GUI drawing for help screen

    Args:
        screen (pygame.Surface): Main pygame window or screen object
    """

    # Drawing elements on screen
    back_button.draw(screen)
    comming_soon_text.draw(screen)

def handle_event(event:pygame.event.Event):
    """handle_event For handle pygame user IO event for interactive elements like input-fields and buttons for help screen

    Args:
        event (pygame.event.Event): User input object provided by pygame
    """    
    
    # Checking events for interactive elements
    if back_button.is_clicked(event):
        variables["current_page"] = "home"