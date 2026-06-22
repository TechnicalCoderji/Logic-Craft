"""
Docstring for core_tools
This module is core tools for GUI representation. it is not about project logic but reusable pygame GUI components classes and global project level dictionary for storing variables.

Here is list of classes this module provide.
(1) TextButton : To make simple button with text in pygame
(2) TextBox : To make simple text label in pygame
(3) ImageButton : To make simple button with image in pygame
(4) Image : To just Draw image on screen in pygame
(5) TextInputField : For input Text from user (manages IO and GUI for it)
(6) NumeberInputField : For input Number only from user (manages IO and GUI for it)
"""

# External Libraries
import pygame
# Internal Modules
from load_assets import load_assets

# Make sure pygame and font module is initialized
pygame.init() 
pygame.font.init()

# This is gloabal project level dictionary to store and share common information across different modules, read and write by different modules in this project.
variables = {
    "current_page":"home",
    "working_craft":None
}

assets = load_assets("general") # load only general folder assets

# Simulator Related Classes uses for making Pygame reusable GUI and IO base code
class TextButton:
    """ This is used to draw Button with text in pygame window with User input handling.

    Methods
    draw : For Draw UI on screen
    is_clicked : For User input handling
    """

    # Properties of Button
    border_radius = 7

    def __init__(self, text:str, x:int, y:int, width:int, height:int, bg_color:tuple, font_color:tuple, font_path:str):
        """__init__ Used to set custom GUI TextButton using Pygame

        Args:
            text (str): Main Text to display
            x (int): x position of text-button box top-left
            y (int): y position of text-button box top-left
            width (int): Width of text-button box
            height (int): Height of text-button box
            bg_color (tuple): Background box color of the box
            font_color (tuple): Font color for the text
            font_path (str): Font path for the text
        """

        self.text = TextBox(text,x,y,width,height,font_path,font_color) # Creating text object for drawing
        self.rect = pygame.Rect(x, y, width, height) # Creating rect object for user input detection

        self.bg_color = bg_color
    
    def draw(self, screen:pygame.surface.Surface):
        """draw Draw your custom Text Button on the screen.
        call inside your main-loop.

        Args:
            screen (pygame.surface.Surface): Your main pygame screen object
        """
        pygame.draw.rect(screen,self.bg_color,self.rect,0,self.border_radius) # for drawing button box
        self.text.draw(screen) # For Drawing Text

    def is_clicked(self, event:pygame.event.Event):
        """is_clicked Used to check wheather user clicked on button or not.
        Call inside your Main-loop, inside your event loop.

        Args:
            event (pygame.event.Event): detailes of user input

        Returns:
            bool: tell wheather user clicked button or not.
        """
        
        pos = pygame.mouse.get_pos() # get mouse position x and y as tuple (x,y)

        # check for mouse position under button rect and mouse clicked or not.
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(pos):
            return True
            
        return False

class TextBox:
    """This is Class for drawing custom Text on screen in pygame.
    Methods
    draw : For Draw UI on screen
    """    

    def __init__(self, text:str, x:int, y:int, width:int, height:int, font_path:str, font_color:tuple=(255, 255, 255),pad:int = 5, align:str='center'):
        """__init__ set your custom text box object.

        Args:
            text (str): main text to show on screen
            x (int): top-left cordinate for text-box to draw
            y (int): top-left cordinate for text-box to draw
            width (int): Width of text-box
            height (int): Height of text-box
            font_path (str): your custom font path exist in font folder
            font_color (tuple, optional): font color in RGB value. Defaults to (255, 255, 255).
            pad (int, optional): inner padding between text and rect box. Defaults to 5.
            align (str, optional): text alignment in box.it may 'left','right'or 'center'. Defaults to 'center'.
        """        
        
        # seting properties value
        self.text = text
        self.font_color = font_color
        self.font_path = font_path
        self.align = align.lower() # convert in lower case for conditions
        self.pad = pad
        self.rect = pygame.Rect(x, y, width, height) # creating pygame rect object for drawing

        # This calculates original text position form box position in addition to padding and alignment
        self.calculate()

    def calculate(self):
        """calculate Method to calculate orignal text position from padding and alignment
        """        
        # Calculate area for text after padding
        inner_width = self.rect.width - 2 * self.pad
        inner_height = self.rect.height - 2 * self.pad

        # Start with large font size and reduce until it fits
        font_size = min(inner_height, 100)
        font_path = f"font/{self.font_path}"
        font = pygame.font.Font(font_path, font_size)

        while font.size(self.text)[0] > inner_width or font.size(self.text)[1] > inner_height:
            font_size -= 1
            if font_size <= 5:
                break
            font = pygame.font.Font(font_path, font_size)

        self.font = font
        self.text_surface = font.render(self.text, True, self.font_color)

        # Align text
        self.text_rect = self.text_surface.get_rect()
        if self.align == 'left':
            self.text_rect.midleft = (self.rect.x + self.pad, self.rect.y + self.rect.height // 2)
        elif self.align == 'right':
            self.text_rect.midright = (self.rect.x + self.rect.width - self.pad, self.rect.y + self.rect.height // 2)
        else:  # default center
            self.text_rect.center = self.rect.center

    def draw(self, screen:pygame.surface.Surface):
        """draw for drawing text on screen in every frame.
        call in main loop of pygame.

        Args:
            screen (pygame.surface.Surface): Pygame window object where all things already drawed
        """

        # for drawing text-surface in screen
        screen.blit(self.text_surface, self.text_rect)

class ImageButton:
    """ This is used to draw Button with Image in pygame window with User input handling.

    Methods
    draw : For Draw UI on screen
    is_clicked : For User input handling
    """

    def __init__(self, x:int, y:int, width:int, height:int, image_path:str, hovered_image_path:str):
        """__init__ Used to set custom GUI ImageButton using Pygame

        Args:
            x (int): x position of text-button box top-left
            y (int): y position of text-button box top-left
            width (int): Width of text-button box
            height (int): Height of text-button box
            image_path (str): Image path present in assets folder
            hovered_image_path (str): Image's path, that shows when user hovered on button
        """

        # seting up properties
        self.x = x
        self.y = y
        self.hovered = False
        self.rect = pygame.Rect(x, y, width, height) # Creating pygame rect object for user input detection

        # making list of path points to access from assets dictionary
        path = image_path.split(".")
        hpath = hovered_image_path.split(".")

        # Resized image object for directly draw on screen
        self.image = pygame.transform.scale(assets[path[0]][path[1]],(width,height))
        self.hovered_image = pygame.transform.scale(assets[hpath[0]][hpath[1]],(width,height))

    def draw(self, screen:pygame.surface.Surface):
        """draw Draw your custom Image-Button on the screen.
        call inside your main loop.

        Args:
            screen (pygame.surface.Surface): Your main pygame screen object
        """

        # draw different images based on user hovered on button or not
        if self.hovered:
            screen.blit(self.hovered_image,(self.rect.x,self.rect.y))
        else:
            screen.blit(self.image,(self.rect.x,self.rect.y))

    def is_clicked(self, event:pygame.event.Event):
        """is_clicked Used to check wheather user clicked on button or not.
        Call inside your Main-loop, inside your event loop.

        Args:
            event (pygame.event.Event): detailes of user input

        Returns:
            bool: tell wheather user clicked button or not.
        """

        pos = pygame.mouse.get_pos() # get mouse position x and y as tuple (x,y)

        # check for mouse position under button rect
        if self.rect.collidepoint(pos):
            self.hovered = True # seting hovered true if mouse cordinates under rect
            if event.type == pygame.MOUSEBUTTONDOWN: # check mouse clicked or not.
                return True
        else:
            self.hovered = False

        return False
    
class Image:
    """ Class used for Drawing image on pygame screen.
    """

    def __init__(self, x:int, y:int, width:int, height:int, image_path:str):
        """__init__ For setup Your custom Image class

        Args:
            x (int): top-left x coordinate to draw image
            y (int): top-left y coordinates to draw image
            width (int): Width of image
            height (int): Height of image
            image_path (str): image path exist in assets folder
        """

        # seting properties of object
        self.x = x
        self.y = y

        # making list of path points to access from assets dictionary
        path = image_path.split(".")
        self.image = pygame.transform.scale(assets[path[0]][path[1]],(width,height)) # Resized image object for directly draw on screen

    def draw(self, screen:pygame.surface.Surface):
        """draw Draw your Image on the screen.
        call inside your main loop.

        Args:
            screen (pygame.surface.Surface): Your main pygame screen object
        """  
        
        # for drawing image on screen
        screen.blit(self.image, (self.x, self.y))

class TextInputField:
    """ Class for making custom Text-Input-Field in pygame and handle drawing GUI and user event IO handling.
    Used for GUI text input in pygame.
    Methods
    draw : For Draw UI on screen
    handle_event : For User input handling
    """

    def __init__(self, x:int, y:int, width:int, height:int, place_holder:str, bg_color:tuple, font_path:str, font_color:tuple, font_size:int, border_color:tuple,max_len:int=50):
        """__init__ for set-up custom Text-Input-Field according to your requirement

        Args:
            x (int): Top-left x coordinate of field box
            y (int): Top-left y coordinate of field box
            width (int): Width of Field-box
            height (int): Height of Field-box
            place_holder (str): Text Defalt place holder
            bg_color (tuple): Back-ground color of Field-box
            font_path (str): Font for text
            font_color (tuple): Font-color for text
            font_size (int): Font size for Text-field
            border_color (tuple): Border color for Field-box (if not want border set same as bg_color)
            max_len (int, optional): Maximum length of valid text. Defaults to 50.
        """

        # seting up properties of Text-Input-Field
        self.text = ""
        self.max_len = max_len
        self.rect = pygame.Rect(x,y,width,height)
        self.place_holder = place_holder
        self.bg_color = bg_color
        self.font_color = font_color
        self.border_color = border_color
        self.border_radius = 5
        self.font = pygame.font.Font("font/"+font_path, font_size)

        # For Deselect border color
        self.deselected_font_color = (max(font_color[0]-100,0),max(font_color[1]-100,0),max(font_color[2]-100,0))
        self.deselected_border_color = (max(border_color[0]-100,0),max(border_color[1]-100,0),max(border_color[2]-100,0))
        self.selected = False

    def draw(self, screen:pygame.surface.Surface):
        """draw Draw your custom Text-Input-Field on the screen.
        call inside your main loop.

        Args:
            screen (pygame.surface.Surface): Your main pygame screen object
        """

        pygame.draw.rect(screen, self.bg_color,self.rect,border_radius=self.border_radius)

        # draw differete for selected and not selected; in text available and place holder empty text
        if self.selected:
            pygame.draw.rect(screen,self.border_color,self.rect,7,self.border_radius)
            if self.text:
                text_surf = self.font.render(self.text, True, self.font_color)
            else:
                text_surf = self.font.render(self.place_holder, True, self.deselected_font_color)

        else:
            pygame.draw.rect(screen,self.deselected_border_color,self.rect,5,self.border_radius)
            if self.text:
                text_surf = self.font.render(self.text, True, self.font_color)
            else:
                text_surf = self.font.render(self.place_holder, True, self.deselected_font_color)

        screen.blit(text_surf, (self.rect.x+12,self.rect.y+5))

    def handle_event(self, event:pygame.event.Event):
        """handle_event Handling pygame IO events for Text-Input-Field

        Args:
            event (pygame.event.Event): detailes of user input pygame object
        """
        
        # for selecting text field if not selected and deselect if user clicked outside textfield
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(*pos):
                self.selected = True
            else:
                self.selected = False

        # Gather keyboard events for Text-Field
        if self.selected:
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_BACKSPACE:
                    if self.text:
                        self.text = self.text[:-1]
                elif len(self.text)<self.max_len and event.unicode.isalnum():
                    self.text += event.unicode

                # Deselct if enter pressed
                elif event.key == pygame.K_RETURN:
                    self.selected = False

class NumberInputField:
    """ Class for making custom Number-Input-Field in pygame and handle drawing GUI and user event IO handling.
    Used for GUI Number input in pygame.
    Methods
    draw : For Draw UI on screen
    is_clicked : For User input handling
    """

    def __init__(self, x:int, y:int, width:int, height:int, default_value:int, bg_color:tuple, font_path:str, font_color:tuple, font_size:int, border_color:tuple,max_num:int=500,min_num:int=20):
        """__init__ for set-up custom Number-Input-Field according to your requirement

        Args:
            x (int): Top-left x coordinate of field box
            y (int): Top-left y coordinate of field box
            width (int): Width of Field-box
            height (int): Height of Field-box
            default_value (int): Number defalt value
            bg_color (tuple): Back-ground color of Field-box
            font_path (str): Font for text
            font_color (tuple): Font-color for text
            font_size (int): Font size for Text-field
            border_color (tuple): Border color for Field-box (if not want border set same as bg_color)
            max_num (int, optional): Maximum valid input number. Defaults to 500.
            min_num (int, optional): Minimum valid input number. Defaults to 20.
        """

        # setting up properties
        self.text = str(default_value)
        self.max_num = max_num
        self.min_num = min_num
        self.rect = pygame.Rect(x,y,width,height)
        self.bg_color = bg_color
        self.font_color = font_color
        self.border_color = border_color
        self.border_radius = 5
        self.font = pygame.font.Font("font/"+font_path, font_size)

        # For Deselect border color
        self.deselected_border_color = (max(border_color[0]-100,0),max(border_color[1]-100,0),max(border_color[2]-100,0))
        self.selected = False

    def apply_limit(self):
        """apply_limit Helper function to set max and min value for out of range input
        """
        if not self.text or int(self.text) < self.min_num:
            self.text = str(self.min_num)
        elif int(self.text) > self.max_num:
            self.text = str(self.max_num)

    def draw(self, screen:pygame.surface.Surface):
        """draw Draw your custom Number-Input-Field on the screen.
        call inside your main loop.

        Args:
            screen (pygame.surface.Surface): Your main pygame screen object
        """

        pygame.draw.rect(screen, self.bg_color,self.rect,border_radius=self.border_radius)

        # draw different things based on selected or not
        if self.selected:
            pygame.draw.rect(screen,self.border_color,self.rect,7,self.border_radius)
            text_surf = self.font.render(self.text, True, self.font_color)

        else:
            pygame.draw.rect(screen,self.deselected_border_color,self.rect,5,self.border_radius)
            text_surf = self.font.render(self.text, True, self.font_color)

        screen.blit(text_surf, (self.rect.x+12,self.rect.y+5))

    def handle_event(self, event:pygame.event.Event):
        """handle_event Handling pygame IO events for Number-Input-Field

        Args:
            event (pygame.event.Event): detailes of user input pygame object
        """
        
        # for selecting number field if not selected and deselect if user clicked outside number field
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(*pos):
                self.selected = True
            else:
                self.selected = False
                self.apply_limit()

        # Gather keyboard events for Number-Field
        if self.selected:
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_BACKSPACE:
                    if self.text:
                        self.text = self.text[:-1]

                elif event.unicode.isdigit():
                    self.text += event.unicode

                # Deselct if enter pressed
                elif event.key == pygame.K_RETURN:
                    self.selected = False
                    self.apply_limit()