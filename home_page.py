"""
Docstring for home_page
This Module is for main menu home screen of Logic Craft.
Directly Navigate user to Setting and Help Utilites;
Also Link to go Git-hub Profile and Youtube Channel of Creator.
Main start button and file list where user can select&open previewsly created craft or create new craft also.
Handle Saving Process of Canvas.
"""

# Here is import usefull Modules for project
# External Libraries
import pygame
import os
import pickle
import webbrowser

# Internal Modules
from core_tools import variables
from load_assets import load_assets
from core_tools import ImageButton, Image, TextBox, TextButton, TextInputField, NumberInputField

# Store Requred assets
assets = load_assets("general") # Load only general assets

# Variables
popup_bg_overlay = pygame.Surface((900, 600), pygame.SRCALPHA) # Fill it with semi-transparent black
popup_bg_overlay.fill((0, 0, 0, 128))  # RGBA — 128 is 50% transparent(range 0-255)
popup_rect = pygame.Rect(225,100,450,400)

# Create image object for draw game main logo(Logic-Craft)
game_logo = Image(160, 50, 600, 250, "general.logiccraft")

# Important Functions
def save_canvas(craft_name:str, columns:int, rows:int):
    """save_canvas Function to Save Canvas as .craft file.
    It Save Empty canvas for new blank canvas file.
    This Function will save file under craft folder of working directory.

    Args:
        craft_name (str): Name of Canvas to save. file name
        columns (int): Number of columns present in Canvas
        rows (int): Number of rows present in Canvas
    """

    # Making Dictionary object to store all canvas class elements info in Future in dictionary for easy save
    canvas_data = {}
    canvas_data["size"] = {"column":columns, "row":rows}
    canvas_data["items"] = None

    # Make File path name for new file to save
    file_path = "craft/" + craft_name + ".craft"

    # Save file in Binary Mode
    try:
        with open(file_path,"wb") as f:
            pickle.dump(canvas_data, f) # Save file using pickle module
        print("File Saved SuccesFully.") # For Debugging Purpose
    except:
        print("File Not Saved.") # For Debugging Purpose

# Important Classes
class CraftItem:
    """
    CraftItem is class to handle GUI representation and user input handling of each item(craft file) with pygame.
    This show rectangle box with craft-name and delete button.
    if user click on craft rectangle anywhere, it open that craft on canvas page.
    if user click on delete button, it delete particular craft.
    """

    def __init__(self, name:str, x:int ,y:int ,width:int ,height:int):
        """__init__ Initialize custom craft-item class

        Args:
            name (str): Name of Craft
            x (int): Top-left X coordinates to draw rectangle
            y (int): Top-left Y coordinates to draw rectangle
            width (int): Width of cradft-item rectangle
            height (int): Height of cradft-item rectangle
        """        

        # Seting up class's properties
        self.rect = pygame.Rect(x,y,width,height)
        self.delete_button_rect = pygame.Rect(x+width-110,y+10,100,30)
        self.delete_text = TextBox("DELETE",x+width-110,y+10,100,30,"Montserrat-ExtraBold.ttf")
        self.title = TextBox(name,x+10,y+10,270,30,"Poppins-Medium.ttf",pad=0,align="left")
        self.hovered = False
        self.path = f"craft/{name}.craft" # Making path of craft actualy saved

    def draw(self,screen:pygame.surface.Surface):
        """draw Draw rectangle GUI for craft.
        Called in every frame for upadate.

        Args:
            screen (pygame.surface.Surface): Main pygame screen/window object
        """

        # Update Things
        self.delete_button_rect.y = self.rect.y + 10
        self.delete_text.text_rect.y = self.rect.y + self.delete_text.pad + 10
        self.title.text_rect.y = self.rect.y + self.title.pad + 10

        # Draw Different version of rectangle based on hovered or not
        if self.hovered:
            pygame.draw.rect(screen,(6, 168, 189),self.rect,border_radius=10)
        else:
            pygame.draw.rect(screen,(2, 56, 63),self.rect,border_radius=10)    

        # Drawing delete button
        pygame.draw.rect(screen,(235, 72, 72),self.delete_button_rect,border_radius=5)
        self.delete_text.draw(screen) # Drawing delete text
        self.title.draw(screen) # Drawing main Craft name

    def handle_event(self,event:pygame.event.Event):
        """handle_event Handle user input events for craft-item.
        handle click to enter on craft-canvas and delete craft event.

        Args:
            event (pygame.event.Event): Pygame event object containing user input event information
        """

        # Use global variables
        global popup, create_new_popup

        pos = pygame.mouse.get_pos() # Get mouse position

        # Check mouse position in under current item rectangle and entire craftlist rectangle
        if self.rect.collidepoint(pos) and CraftList.rect.collidepoint(pos):
            self.hovered = True
            # Check for mouse clicked or not with left-mouse-button
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # handle delete item event
                if self.delete_button_rect.collidepoint(pos):
                    os.remove(self.path)
                    CraftList.generate_items()

                # Go to Canvas page with selected craft
                else:
                    popup = False
                    variables["working_craft"] = self.title.text
                    variables["current_page"] = "canvas"

        else:
            self.hovered = False

class CraftList:
    """
    CraftList is class to handle GUI representation and user input handling of list item(craft file) with pygame.
    This show rectangle box with  list of craft-item with scrollable layout.
    """

    # Common class  variables
    folder_path = "craft/"
    file_list = []
    craft_items = []

    # For scrolling list of craft-item logic
    scroll_offset = 0
    scroll_speed = 5
    item_height = 50 # Each craft-item height
    padding = 10 # padding between craft items

    @classmethod
    def set_rect(cls ,x:int ,y:int ,width:int ,height:int):
        """set_rect Initializing custom class list according to user need

        Args:
            x (int): Top-left X coordinate of list rectangle
            y (int): Top-left Y coordinate of list rectangle
            width (int): Width of list rectangle
            height (int): Height of list rectangle
        """

        # Seting properties
        cls.rect = pygame.Rect(x,y,width,height)
        cls.visible_area_height = height
        cls.inner_width = width - 10
        cls.generate_items()

    @classmethod
    def generate_items(cls):
        """generate_items Internal Helper function to crate list of CraftItem onject according to saved craft files present in craft folder.
        """
        cls.get_file_list()
        cls.craft_items = []
        for i, name in enumerate(cls.file_list):
            item_y = cls.rect.y + i * (cls.item_height + cls.padding)
            item = CraftItem(name, cls.rect.x, item_y, cls.inner_width, cls.item_height)
            cls.craft_items.append(item)

    @staticmethod
    def get_file_list():
        """get_file_list Internal Helper function to listout saved craft files in craft folder.
        """
        CraftList.file_list = [os.path.splitext(f)[0] for f in os.listdir(CraftList.folder_path) if f.endswith(".craft")]

    @staticmethod
    def get_craftname():
        """get_craftname Auto-Incramented craft name for newly generated craft

        Returns:
            str: Defualt craft name
        """        
        files = CraftList.file_list
        next_file_number = 1
        for file_name in files:
            words = file_name.split()
            if len(words) == 2 and words[0] == "Craft" and words[1].isdigit():
                next_file_number = max(next_file_number,int(words[1])+1)
                
        return "Craft " + str(next_file_number)

    @classmethod
    def draw(cls ,screen:pygame.surface.Surface):
        """draw Draw rectangle GUI for craft-list.
        Called in every frame for upadate.
        Drawing vertiacal scrollbar in right side if Items over-flow screen 

        Args:
            screen (pygame.surface.Surface): Main pygame screen/window object
        """
        
        # Scrollable list of craft-item rectangle drawing logic
        clip = screen.get_clip()
        screen.set_clip(cls.rect)

        step = cls.item_height + cls.padding
        start_index = cls.scroll_offset // step
        y_offset = cls.rect.y - (cls.scroll_offset % step)

        for i in range(start_index, len(cls.craft_items)):
            item = cls.craft_items[i]
            item.rect.y = y_offset + (i - start_index) * step
            if item.rect.bottom < cls.rect.top:
                continue
            if item.rect.top > cls.rect.bottom:
                break
            item.draw(screen)

        # Scrollbar
        total_height = len(cls.craft_items) * (cls.item_height + cls.padding)

        if total_height > cls.visible_area_height:
            scroll_height = max(cls.visible_area_height * cls.visible_area_height // total_height, 20)
            scroll_y = cls.rect.y + (cls.scroll_offset / total_height) * cls.visible_area_height
            scrollbar_rect = pygame.Rect(cls.rect.right - 6, scroll_y, 4, scroll_height)
            scrollbar_bg_rect = pygame.Rect(cls.rect.right - 6, cls.rect.y, 4, cls.visible_area_height)

            # For Bg of Scrollbar
            pygame.draw.rect(screen, (6, 34, 40), scrollbar_bg_rect,border_radius=7)
            # For Scrollbar
            pygame.draw.rect(screen, (0, 230, 230), scrollbar_rect,border_radius=7)

        screen.set_clip(clip)

    @classmethod
    def handle_event(cls ,event:pygame.event.Event):
        """handle_event Handle user input events for craft-list.
        handle scroll and click events.

        Args:
            event (pygame.event.Event): Pygame event object containing user input event information
        """

        # For handling click on craft-item and scroll event
        total_height = len(cls.craft_items) * (cls.item_height + cls.padding)
        max_scroll = max(0, total_height - cls.rect.height)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # Scroll up
                cls.scroll_offset = max(cls.scroll_offset - cls.scroll_speed, 0)
            elif event.button == 5:  # Scroll down
                cls.scroll_offset = min(cls.scroll_offset + cls.scroll_speed, max_scroll)

        # For event handle for each item
        for item in cls.craft_items:

            # Handling edge-case conditions
            if item.rect.bottom < cls.rect.top:
                continue
            if item.rect.top > cls.rect.bottom:
                break

            # Handle craft-item event
            item.handle_event(event)

# GUI Objects
# Image button objects
start_button = ImageButton(300,325,300,100,"general.start","general.start_hovered")
setting_button = ImageButton(25,525,50,50,"general.settings","general.settings")
help_button = ImageButton(100,525,50,50,"general.help","general.help")
github_button = ImageButton(750,525,50,50,"general.github","general.github")
youtube_button = ImageButton(825,525,50,50,"general.youtube","general.youtube")
create_new_button = ImageButton(350,435,200,50,"general.create_new","general.create_new_hovered")
create_craft_button = TextButton("Create Craft",330,435,240,50,(33,167,51),(230,230,230),"Montserrat-ExtraBold.ttf")

CraftList.set_rect(250,165,400,255) # Initializing CraftList

# Textbox objects
popup_title = TextBox("YOUR CRAFT",225,100,450,50,"Montserrat-ExtraBold.ttf",(255, 221, 77))
create_new_popup_title = TextBox("Create New Craft",225,100,450,50,"Montserrat-ExtraBold.ttf",(255, 221, 77))
craft_name_text = TextBox("Craft Name",250,155,400,50,"Poppins-Medium.ttf",(211,222,233),5,"left")
canvas_size_text = TextBox("Canvas Size",250,265,400,50,"Poppins-Medium.ttf",(211,222,233),5,"left")
column_text = TextBox("Column",250,300,195,45,"Poppins-Medium.ttf",(3,199,199))
x_text = TextBox("X",425,300,50,50,"Montserrat-ExtraBold.ttf",(3,199,199),10)
row_text = TextBox("Row",455,300,195,45,"Poppins-Medium.ttf",(3,199,199))

# For Credit and Version info
credit_text = TextBox("Developed by Technical Coderji",300,525,300,50,"Poppins-Medium.ttf",(255,255,255))
version_text = TextBox("version 1.0",400,550,100,50,"Poppins-Medium.ttf",(255,255,255))

# Social Media Links Variables
github_url = "https://github.com/TechnicalCoderji"
youtube_url = "https://www.youtube.com/@TechnicalCoderji"

# Pop-up boolean value
popup = False # For open-file pop-up
create_new_popup = False # For create new file pop-up

# Input Field Objects
craft_name_input = TextInputField(250,205,400,50,"Enter Canvas Name Here...",(10, 116, 110),"Poppins-Medium.ttf",(211,222,233),27,(211,222,233),15)
column_input = NumberInputField(250,340,195,50,30,(10, 116, 110),"Poppins-Medium.ttf",(211,222,233),27,(211,222,233),200,10)
row_input = NumberInputField(455,340,195,50,20,(10, 116, 110),"Poppins-Medium.ttf",(211,222,233),27,(211,222,233),200,10)

# For Draw Home Screen GUI
def draw_screen(screen:pygame.Surface):
    """draw_screen Handle GUI drawing for Home screen

    Args:
        screen (pygame.Surface): Main pygame window or screen object
    """
    
    # Draw all things on screen one-by-one in order with depth
    game_logo.draw(screen) # For Blit Game Logo On Screen
    start_button.draw(screen) # For Start Button
    help_button.draw(screen) # For Help Button
    setting_button.draw(screen) # For Setting Button
    github_button.draw(screen) # For Github Button
    youtube_button.draw(screen) # For youtube Button

    # For Credit and Version
    credit_text.draw(screen)
    version_text.draw(screen)

    # For Pop-Up Screen Things  if pop-up is opened
    if popup or create_new_popup:

        # Common pop-up things for both pop-ups
        screen.blit(popup_bg_overlay,(0,0)) # For semi-Transparent Background

        # For rectangle pop-up box in center of the screen with heading diffrent background
        pygame.draw.rect(screen,(4, 84, 89),popup_rect,border_radius=20)
        pygame.draw.rect(screen,(1, 106, 110),(225,100,450,50),border_top_left_radius=20,border_top_right_radius=20)

        # Special for file list pop-up
        if popup:
            popup_title.draw(screen) # For Header pop-up title
            create_new_button.draw(screen) # For Create New Button
            CraftList.draw(screen) # For Craft List

        # Special for create new pop-up
        elif create_new_popup:
            create_new_popup_title.draw(screen) # For Header pop-up title

            # For different types of texts, buttons and input-fields
            craft_name_text.draw(screen) 
            craft_name_input.draw(screen)
            canvas_size_text.draw(screen)
            column_text.draw(screen)
            x_text.draw(screen)
            row_text.draw(screen)
            column_input.draw(screen)
            row_input.draw(screen)
            create_craft_button.draw(screen)

# For Handle Pygame Events
def handle_event(event:pygame.event.Event):
    """handle_event For handle pygame user input event for interactive elements like input-fields and buttons for home screen

    Args:
        event (pygame.event.Event): User input object provided by pygame
    """

    global popup, create_new_popup # accessing global varibles
    
    # Special event-handling for create new pop-up
    if create_new_popup:

        # Input-Field event handling
        craft_name_input.handle_event(event)
        column_input.handle_event(event)
        row_input.handle_event(event)

        if create_craft_button.is_clicked(event):
            craft_name = craft_name_input.text if craft_name_input.text else CraftList.get_craftname()
            variables["working_craft"] = craft_name
            column_input.apply_limit()
            columns = int(column_input.text)
            row_input.apply_limit()
            rows = int(row_input.text)
            save_canvas(craft_name, columns, rows)
            create_new_popup = False
            variables["current_page"] = "canvas"

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if not popup_rect.collidepoint(pos):
                create_new_popup = False
                popup = True

    # Special event-handling for file-list pop-up
    elif popup:

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if not popup_rect.collidepoint(pos):
                popup = False

        if create_new_button.is_clicked(event):
            create_new_popup = True
            popup = False

        CraftList.handle_event(event)

    # Basic event handling
    else:

        # All button event handling
        if start_button.is_clicked(event):
            popup = True
            CraftList.generate_items()

        if help_button.is_clicked(event):
            variables["current_page"] = "help"

        if setting_button.is_clicked(event):
            variables["current_page"] = "setting"

        if github_button.is_clicked(event):
            webbrowser.open(github_url)

        if youtube_button.is_clicked(event):
            webbrowser.open(youtube_url)