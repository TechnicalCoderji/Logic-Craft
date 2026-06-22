"""
This is main Entery point of project Logic-Craft(logic gate simulator).

This file containing main game-loop and event loop for handling user events and drawing and updating things on screen.
All other page called from here, this run tills program run. Consider root file of program running.
"""

# Here is import usefull Modules for project
# External Libraries
import pygame

# Internal Modules
import home_page
import setting
import canvas
import help
from core_tools import variables

# Initialize Pygame basic set-up
pygame.init()

# For Screen/Window Basic
WIDTH = 900
HEIGHT = 600
RES = WIDTH,HEIGHT # Screen resolution
win = pygame.display.set_mode(RES,pygame.SCALED) # Pygame main window/screen object
pygame.display.set_caption("Logic-Craft by Technical Coderji") # Set title of window
clock = pygame.time.Clock() # Clock for FPS(frame per second)
FPS = 60 # Limit FPS(Targeted)

def main():
    """main Entry point function for logic-craft/logic-gate-simulator.
    Contains main-GUI loop and event loop.
    """

    # Simulator Related Varibles
    # All page function as dict of key-value function to easily navigate between different pages and intire program can run on single game loop
    pages = {"home":{"event":home_page.handle_event, "draw":home_page.draw_screen},
             "setting":{"event":setting.handle_event, "draw":setting.draw_screen},
             "help":{"event":help.handle_event, "draw":help.draw_screen},
             "canvas":{"event":canvas.handle_event, "draw":canvas.draw_screen}
             }

    # For Gameloop/Mainloop
    while True:

        # For Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            
            # For Different Page Event Handling
            pages[variables["current_page"]]["event"](event)
            
        # For Drawing Things on Screen
        win.fill((46, 52, 64)) # Fil Background with custom (RGB)color

        # Draw Different Pages GUI on Screen
        pages[variables["current_page"]]["draw"](win)

        pygame.display.flip() # Update screen on every frame
        clock.tick(FPS) # limit FPS(achive targeted FPS)

# Running and Quiting program
if __name__=="__main__":
    main() # Entry point of intire project-program
    pygame.quit() # Close pygame GUI window
    exit() # Close terminal code running CLI