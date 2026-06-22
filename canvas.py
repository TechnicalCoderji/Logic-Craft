"""
Docstring for canvas
This module handle the main core canvas logic. It has functions for drawing pygame object on the screen and also handling user events. It is resposible for core logic gate simulator. This is most important part of this project.
"""

# Here is import usefull Modules for project
# External Libraries
import pygame
import pickle
import os

# Internal Modules
from load_assets import load_assets
from core_tools import TextBox, ImageButton, variables, TextButton, TextInputField, NumberInputField

# Load & Store Requred assets
assets = load_assets("toolbar icons","button","wire","not","and","nand","or","nor","xor","xnor")

# Next clock-wise direction dictionary for roatating components
next_direction = {
    "left": "top",
    "top": "right",
    "right": "bottom",
    "bottom": "left"
}

# Important Classes and Functions
def toolbar_open_animation():
    """toolbar_open_animation For tool-bar opening animation. animation strats when function is called.
    """

    # Get and process in y direction for vertical sliding animation
    target_y = 511
    current_y = ToolBar.rect.y
    distance = current_y - target_y

    if current_y == 600:
        ToolBar.is_active = True # Activate tool-bar when animation is over

    if distance > 0:
        # Ease-out: fast at start, slow near target
        step = max(1, int(distance * 0.25))  # You can tweak 0.1 for smoothness

        # Move every element of tool-bar according to step value in -y direction
        ToolBar.rect.y -= step
        for i in ToolBar.items_and_tools:
            ToolBar.items_and_tools[i].rect.y -= step
    else:
        # Animation finished so remove it from active animation dictionary
        Animation.active_animations.remove("toolbaropen")

def toolbar_close_animation():
    """toolbar_close_animation For tool-bar closing animation. animation strats when function is called.
    """

    # Get and process in y direction for vertical sliding animation
    target_y = 600
    current_y = ToolBar.rect.y
    distance = target_y - current_y

    if distance > 0:
        # Ease-out factor: reduce speed as we get closer
        step = max(1, int(distance * 0.25))  # You can tweak 0.1 for smoothness

        # Move every element of tool-bar according to step value in +y direction
        ToolBar.rect.y += step
        for i in ToolBar.items_and_tools:
            ToolBar.items_and_tools[i].rect.y += step
    else:
        # Animation finished so remove it from active animation dictionary
        Animation.active_animations.remove("toolbarclose")
        ToolBar.is_active = False # Deactivate tool-bar when animation is over

def menubar_open_animation():
    """menubar_open_animation For menu-bar opening animation. animation strats when function is called.
    """

    # Get and process in x direction for Horizontal sliding animation
    target_x = 540
    current_x = Menu.rect.x
    distance = current_x - target_x

    if current_x == 900:
        Menu.opened = True # Activate menu-bar when animation is over

    if distance > 0:
        # Ease-out: fast at start, slow near target
        step = max(1, int(distance * 0.25))  # You can tweak 0.1 for smoothness

        # All Components Manualy Value Updation
        # Move every element of menu-bar according to step value in -x direction
        Menu.rect.x -= step
        Menu.title.text_rect.x -= step
        Menu.back_button.rect.x -= step
        Menu.craft_name_rect.x -= step
        Menu.craft_name.text_rect.x -= step
        Menu.save_button.rect.x -= step
        Menu.save_button.text.text_rect.x -= step
        Menu.edit_button.rect.x -= step
        Menu.edit_button.text.text_rect.x -= step
        Menu.exit_button.rect.x -= step
        Menu.exit_button.text.text_rect.x -= step
        Menu.setting_button.rect.x -= step
        Menu.setting_button.text.text_rect.x -= step

    else:
        # Animation finished so remove it from active animation dictionary
        Animation.active_animations.remove("menubaropen") # 

def menubar_close_animation():
    """menubar_close_animation For menu-bar closing animation. animation strats when function is called.
    """

    # Get and process in x direction for Horizontal sliding animation
    target_x = 900
    current_x = Menu.rect.x
    distance = target_x - current_x

    if distance > 0:
        # Ease-out factor: reduce speed as we get closer
        step = max(1, int(distance * 0.25))  # You can tweak 0.1 for smoothness

        # All Components Manualy Value Updation
        # Move every element of menu-bar according to step value in +x direction
        Menu.rect.x += step
        Menu.title.text_rect.x += step
        Menu.back_button.rect.x += step
        Menu.craft_name_rect.x += step
        Menu.craft_name.text_rect.x += step
        Menu.save_button.rect.x += step
        Menu.save_button.text.text_rect.x += step
        Menu.edit_button.rect.x += step
        Menu.edit_button.text.text_rect.x += step
        Menu.exit_button.rect.x += step
        Menu.exit_button.text.text_rect.x += step
        Menu.setting_button.rect.x += step
        Menu.setting_button.text.text_rect.x += step
        
    else:
        # Animation finished so remove it from active animation dictionary
        Animation.active_animations.remove("menubarclose")
        Menu.opened = False # Deactivate menu-bar when animation is over

def reverse_direction(in_dir:str):
    """reverse_direction Helper function to give opposite string direction

    Args:
        in_dir (str): Direction input from left, right, top and bottom

    Returns:
        str: Opposite direction of your input direction
    """

    if in_dir == "left":
        return "right"
    elif in_dir == "right":
        return "left"
    elif in_dir == "top":
        return "bottom"
    else:
        return "top"
    
def cor_to_pos(x:int, y:int):
    """cor_to_pos Helper function to calculate Virtual position on Canvas from actual coordinate x, y according to canvas position with canvas block size 

    Args:
        x (int): Actual X coordinate
        y (int): Actual Y coordinate

    Returns:
        tuple(int, int), bool-False: False if out of grid and position tuple if inside grid.
    """    

    # Calculating virtual X and Y from actual coordinate according canvas position and sizing
    pos_x = (x - Canvas.x)//Canvas.block_size
    pos_y = (y - Canvas.y)//Canvas.block_size

    # Check object position exist under grid
    if (pos_x >= 0) and (pos_x < Canvas.column) and (pos_y >= 0) and (pos_y < Canvas.row):
        return (pos_x, pos_y)

    return False # False when position out-of-grid

class Block:
    """ This is block class for all grid blocks. it handle signal parsing and all things realated to grid. Building block of grid.
    """

    def __init__(self,x:int,y:int):
        """__init__ Initialization of Block object with column and row number

        Args:
            x (int): Columns number
            y (int): Rows number
        """

        # Set-up object properties
        self.pos = (x,y) # Position vector tuple
        self.is_has = None # Boolean value for having special Gate or Swicth object
        # Output signal dictionary
        self.output = {
            "left": None,
            "right": None,
            "top": None,
            "bottom": None
        }
        # Neighbour position dictonary for quick neighbour access
        self.neighbour_pos = {
            "left": (x-1,y),
            "right": (x+1,y),
            "top": (x,y-1),
            "bottom": (x,y+1)
        }

class Canvas:
    """Static class for main canvas contains grid, logic-gate objects and switch/wire objects.
    Provide Utility and Helping function to canvas logic handling; also provide draw and handle_event functions for screen GUI updates and User Input handling.
    """    

    # Class Variables
    x = y = 0 # For movable grid-canvas: Intire grid-canvas moved using mouse draging
    block_size = 50 # For resizable canvas feature: zoom-in and zoom-out

    # Grid Properties
    grid_color = (141,163,191)
    grid_thickness = 1

    # For Run and Stop Machanishm
    is_running = False
    run_image = pygame.transform.scale(assets["button"]["Run"],(34,34))
    stop_image = pygame.transform.scale(assets["button"]["Stop"],(34,34))
    run_botton_pos = (810,7)
    run_button_rect = pygame.Rect(810,7,34,34)

    # Menu Button Machanishm - Move OutSide Canvas Class
    menu_image = pygame.transform.scale(assets["button"]["Menu"],(34,34))
    menu_button_pos = (858,7)
    menu_button_rect = pygame.Rect(858,7,34,34)

    # Drag state
    dragging = False
    last_mouse_pos = (0, 0)
    max_zoom = 50
    min_zoom = 25

    # For Logical Block Store
    all_items_with_handle_event = [] # User Interactable items/objects which have handle_event function for handling user input
    all_items = [] # Static items/objects only need to draw on screen no user input Scanning
    selected_item = None
    canvas_seted = False # Tells Canvas is seted using set_canvas or not(need to set)

    @classmethod
    def set_canvas(cls):
        """set_canvas Static class function to initialize Canvas Basic things.
        Mainly hanle loading of previewly saved craft file as canvas-grid.
        """        

        # Load data from .craft file
        file_path = "craft/"+str(variables["working_craft"]) + ".craft"
        try:
            with open(file_path,"rb") as f:
                canvas_data = pickle.load(f)
            print("File Opened SuccesFully.")

        except:
            print("File Open Error. Not Ocuur any ways.")

        # Setting-Up canvas using loaded data
        # Making basic empty grid using size: columns and rows
        cls.column = canvas_data["size"]["column"]
        cls.row = canvas_data["size"]["row"]
        cls.blockgrid = {(i,j):Block(i,j) for i in range(cls.column) for j in range(cls.row)} # Making main grid
        cls.canvas_seted = True

        # Loading logical objects(logic gate, wire, switch) if exist
        if canvas_data["items"]:

            # Main Data loading from dictionary(reverse process done in saving done in Menu's save_canvas function)
            for item_data in canvas_data["items"]:
                item_name = item_data["name"]
                item_x = item_data["x"]
                item_y = item_data["y"]

                # Create and add new logical objects to Canvas
                if item_name == "switch":
                    Canvas.add_item(name=item_name, col=item_x, row=item_y)

                else:
                    item_in_dir = item_data["input_direction"]

                    if item_name == "wire":
                        item_out_dir = item_data["output_direction"]
                        Canvas.add_item(name=item_name, col=item_x, row=item_y, in_dir=item_in_dir, out_dir=item_out_dir)
                    
                    else:
                        Canvas.add_item(name=item_name, col=item_x, row=item_y, in_dir=item_in_dir)         

    @classmethod
    def is_empty_space(cls, name:str, col:int, row:int, dir:str=None):
        """is_empty_space This is Helper function to check in particular position is empty in grid or hold by other logical object. need to verify not Logical object added on top of each other.

        Args:
            name (str): Name of Logical element required empty space
            col (int): Column's number
            row (int): row's number
            dir (str, optional): Direction of logical object in case of NOT gate only to decide required space is in which direction. Defaults to None.

        Returns:
            bool: Tells space is available or not
        """        

        # Check for one block space for switch and wire
        if name in ("switch", "wire"):
            return False if cls.blockgrid[(col,row)].is_has else True
        
        # Check for multiple block space for not and other gate
        blocks = []
        blocks.append(cls.blockgrid[(col,row)])
        if name == "not":
            # Check for two block space according to direction for not gate
            if dir in ("left", "right"):
                blocks.append(cls.blockgrid[(col+1,row)])
            else:
                blocks.append(cls.blockgrid[(col,row+1)])
        else:
            # Check for surrounding three blocks incase of big-gate(take 4 block gap)
            blocks.append(cls.blockgrid[(col,row+1)])
            blocks.append(cls.blockgrid[(col+1,row)])
            blocks.append(cls.blockgrid[(col+1,row+1)])
        
        # Now here is finally check for space is available for Logic-Object or not
        for block in blocks:
            if block.is_has:
                return False

        return True

    @classmethod
    def get_covered_blocks(cls, obj):
        """get_covered_blocks Helper function to quick recieve blocks covered by logic-object

        Args:
            obj (Logic_class): Any of seven gates, switch and wire

        Returns:
            list: List of covered blocks by Logic object
        """

        return list(obj.blocks.values())

    @classmethod
    def add_item(cls, **data):
        """add_item Utility method for adding Logic-objects in canvas-grid.
        return nothing.
        """

        # Common data for all logic-objects
        col = data["col"]
        row = data["row"]
        name = data["name"]
        
        # Temparary Solution Of Boarder Value Error for One Direction Input Only In Gates
        if (col<1) or (row<1) or (row>cls.row-2) or (col>cls.column-2):
            print("Boarder of Canvas. or Out of Canvas.")
            return

        # Add item logic for switch (switch added if there is space for it)
        if name == "switch":
            if cls.is_empty_space(name, col, row):
                canvas_obj = Switch(col,row)
                cls.all_items_with_handle_event.append(canvas_obj)
                cls.blockgrid[(col,row)].is_has = canvas_obj
            else:
                print("Block Already Taken By Another Object.")
            return

        # Add item logic for wire (wire added if there is space for it)
        in_dir = data["in_dir"]
        if name == "wire":
            if cls.is_empty_space(name, col, row):
                out_dir = data["out_dir"]
                canvas_obj = Wire(col,row,in_dir,out_dir)
                Canvas.all_items.append(canvas_obj)
                cls.blockgrid[(col,row)].is_has = canvas_obj
            else:
                print("Block Already Taken By Another Object.")
            return

        # Add item logic for not-gate (not-gate added if there is space for it)
        if name == "not":
            if cls.is_empty_space(name,col,row,in_dir):
                canvas_obj = NotGate(col,row,in_dir)
                Canvas.all_items.append(canvas_obj)
                for block in cls.get_covered_blocks(canvas_obj):
                    block.is_has = canvas_obj
            else:
                print("Block Already Taken By Another Object.")
            return
        
        # Add item logic for all remening gates(2x2) (gate added if there is space for it)
        if name in ("and", "or", "nand", "nor", "xor", "xnor"):
            if cls.is_empty_space(name, col, row,in_dir):
                canvas_obj = Gate(col, row, in_dir, name)
                Canvas.all_items.append(canvas_obj)
                for block in cls.get_covered_blocks(canvas_obj):
                    block.is_has = canvas_obj
            else:
                print("Block Already Taken By Another Object.")
            return

        print("Invalid Name of Canvas Object.")

    @classmethod
    def delete_item(cls, obj):
        """delete_item Utility function to remove Logic-object from canvas-grid

        Args:
            obj (logic-class): object to remove from grid-canvas
        """

        if obj.name == "switch":
            cls.all_items_with_handle_event.remove(obj)

            # For Make Empty Space on Canvas
            obj.block.is_has = None
            
            del obj
        
        else:
            cls.all_items.remove(obj)

            # For Make Empty Space on Canvas
            if obj.name == "wire":
                obj.block.is_has = None
            else:
                for block in cls.get_covered_blocks(obj):
                    block.is_has = None
            
            del obj

    @classmethod
    def cleanUp(cls):
        """cleanUp Helper function to reset canvas, clear-Up all things and assign all things to default value
        """
        
        # Clear logic-object list(normal + handle_event)
        cls.all_items_with_handle_event.clear()
        cls.all_items.clear()

        # Set canvas values to default
        cls.selected_item = None
        cls.x = cls.y = 0
        cls.block_size = 50
        cls.canvas_seted = False

    @classmethod
    def draw(cls, screen:pygame.surface.Surface):
        """
        draw Main Mehtod to draw Canvas and Canvas related things on GUI window with pygame.
        call in every frame to update screen.
        call inside main-game-loop.

        Args:
            screen (pygame.surface.Surface): Main pygame screen/window object
        """
        
        # For Grid Drawing On Screen(using rectangles)
        for i in range(1,cls.column-1):
            for j in range(1,cls.row-1):
                rectangle = (cls.x+cls.block_size*i,cls.y+cls.block_size*j,cls.block_size,cls.block_size)
                pygame.draw.rect(screen,cls.grid_color,rectangle,cls.grid_thickness)

        # For Draw Big Yellow Box On Screen(grid border)
        yellow_rect = (cls.x+cls.block_size*1,cls.y+cls.block_size*1,cls.block_size*(cls.column-2),cls.block_size*(cls.row-2))
        pygame.draw.rect(screen, (200,200,0),yellow_rect,cls.grid_thickness)

        # For Drawing and Updateing Logical Elements on screen
        for item in cls.all_items_with_handle_event:
            item.draw(screen)

        # For Drawing and Updateing Normal Elements on screen
        for item in cls.all_items:
            item.draw(screen)

        # For Drawing Selected Item
        if cls.selected_item and cls.selected_item.name != "switch":
            cls.selected_item.selected_draw(screen)

        # For Top-Right Mini-Menu
        pygame.draw.rect(screen, (97, 136, 199), (800,0,100,50), 0, border_bottom_left_radius=20)
        pygame.draw.rect(screen, (47, 66, 97), (800,-4,104,54), 4, border_bottom_left_radius=20)

        # For Run/Stop Button Drawing
        if cls.is_running:
            screen.blit(cls.stop_image,cls.run_botton_pos)
        else:
            screen.blit(cls.run_image,cls.run_botton_pos)

        # For Menu Button Drawing
        screen.blit(cls.menu_image,cls.menu_button_pos)

    @classmethod
    def handle_event(cls, event:pygame.event.Event):
        """handle_event Main method to handle all user input with canvas and interactable elements of canvas realted event.
        call in every frame to handle event.
        call inside main-event-loop.

        Args:
            event (pygame.event.Event): Event Object of pygame that have input information
        """

        # Start dragging
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                mx, my = pygame.mouse.get_pos()

                # Testing
                # pos = cor_to_pos(mx,my)
                # if pos:
                #     is_has = cls.blockgrid[pos].is_has
                #     print(pos,"IS Reserved:",is_has.name if is_has else None)
                # else:
                #     print("Out Of Grid.")

                if cls.run_button_rect.collidepoint(mx,my):
                    
                    # Active edit mode main canvas logic
                    if cls.is_running:
                        # For Clear All Switch Output
                        for item in cls.all_items_with_handle_event:
                            if item.signal:
                                item.change_signal()
                        Animation.active_animations.append("toolbaropen") # Add tool bar open animation

                    # Run main canvas logic
                    else:
                        # For Clear All Slected Block On Canvas
                        cls.selected_item = None

                        # For Clear Slected Block On ToolBar
                        if ToolBar.selected_item:
                            ToolBar.selected_item.selected = False
                            ToolBar.selected_item = None
                        Animation.active_animations.append("toolbarclose")# Add tool bar close animation

                    cls.is_running = not cls.is_running # Change State (Running/ Not Running)
                
                # Move Outside Canvas Class
                # Menu open event logic handling
                elif cls.menu_button_rect.collidepoint(mx,my):
                    Menu.craft_name.text = str(variables["working_craft"])
                    Menu.craft_name.calculate()
                    Animation.active_animations.append("menubaropen") # Add menu bar open animation

                else:
                    cls.dragging = True
                    cls.last_mouse_pos = pygame.mouse.get_pos()

            # Zoom in
            elif event.button == 4: # Mouse Scroll-Down
                cls.block_size = min(cls.max_zoom, cls.block_size + 1)

            # Zoom out
            elif event.button == 5: # Mouse Scroll-UP
                cls.block_size = max(cls.min_zoom, cls.block_size - 1)

        # Stop dragging
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                cls.dragging = False

        # Drag to move
        elif event.type == pygame.MOUSEMOTION and cls.dragging:
            mx, my = pygame.mouse.get_pos()
            dx = mx - cls.last_mouse_pos[0]
            dy = my - cls.last_mouse_pos[1]
            cls.x += dx
            cls.y += dy
            cls.last_mouse_pos = (mx, my)

        # Running canvas event handling
        if cls.is_running:
            # For Handle Event of All Interactable Logical Elements
            for item in cls.all_items_with_handle_event:
                item.handle_input_event(event)

        else:
            # For Edit Mode

            # For Handle All Items Edit Handling
            if cls.selected_item:
                cls.selected_item.handle_event(event)

            # For Item Placement on Screen and Select Item On Screen
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                pos = cor_to_pos(mx, my)
                if pos and not ToolBar.rect.collidepoint((mx, my)):
                    col, row = pos

                    if event.button == 1: # Left click
                        selected_block = cls.blockgrid[(col,row)].is_has
                        if selected_block:
                            if cls.selected_item:
                                cls.selected_item.selected = False

                            # For Delete Item From Canvas
                            if ToolBar.selected_item and ToolBar.selected_item.name == "delete":
                                cls.selected_item = None
                                cls.delete_item(selected_block)

                            else:
                                selected_block.selected = True
                                cls.selected_item = selected_block

                        else:
                            if cls.selected_item:
                                cls.selected_item.selected = False
                            cls.selected_item = None

                    # Right-click to add logic-object on screen
                    elif (event.button) == 3 and ToolBar.selected_item: # Right click
                        Canvas.add_item(name=ToolBar.selected_item.name, col=col, row=row, in_dir="left", out_dir="right")

class Switch:
    """
    Switch is Logic-Object for canvas grid.
    it may on/off and pass signal to all directions.
    This class handle all switch logic(draw on screen + user event handling)
    """
    name = "switch"

    def __init__(self, x:int, y:int):
        """__init__ To initialize custom switch object for canvas

        Args:
            x (int): Column's number in grid for switch
            y (int): Row's number in grid for switch
        """
        
        # Set class properties
        self.x = x
        self.y = y
        self.rect = pygame.Rect(Canvas.x+Canvas.block_size*x,Canvas.y+Canvas.block_size*y,Canvas.block_size,Canvas.block_size)
        self.signal = False
        self.images = {
            "ON": assets["button"]["ON"],
            "OFF": assets["button"]["OFF"]
        }
        self.block = Canvas.blockgrid[(x,y)] # Block object that hold switch
        self.selected = False # For Selection State (Used For-Event and Drawing)

    def draw(self, screen:pygame.surface.Surface):
        """
        draw Main Mehtod to draw switch related things on GUI window with pygame.
        call in every frame to update switch GUI.
        call inside main-game-loop.

        Args:
            screen (pygame.surface.Surface): Main pygame screen/window object
        """

        # For Update Usefull Data
        self.rect = pygame.Rect(Canvas.x+Canvas.block_size*self.x,Canvas.y+Canvas.block_size*self.y,Canvas.block_size,Canvas.block_size)

        # For Draw Item On Screen
        image = self.images["ON"] if self.signal else self.images["OFF"]
        image = pygame.transform.scale(image,(Canvas.block_size,Canvas.block_size))
        screen.blit(image,self.rect)

        # Highlight By Square Boarder if Selected
        if self.selected:
            pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)

    def change_signal(self):
        """change_signal Utility function to flip signal of switch and all block it contain
        """
        self.signal = not self.signal
        self.block.output = {
            "left": self.signal,
            "right": self.signal,
            "top": self.signal,
            "bottom": self.signal
        }

    def handle_input_event(self, event:pygame.event.Event):
        """handle_input_event Main method to handle all user input with switch realted event.
        call in every frame to handle event.
        call inside main-event-loop.

        Args:
            event (pygame.event.Event): Event Object of pygame that have input information
        """

        pos = pygame.mouse.get_pos() # Get mouse position

        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(pos) and event.button == 1:
            self.change_signal()

    def handle_event(self,event:pygame.event.Event):
        """handle_event Not For use, Just for to call and program run without error.

        Args:
            event (pygame.event.Event): Event Object of pygame that have input information
        """
        print("selected:",self.name) # Debugging process

class Wire:
    """
    Wire is Logic-Object for canvas grid.
    it pass signal to particular direction.
    This class handle all switch logic(draw on screen + user event handling)
    """
    name = "wire"

    def __init__(self, x:int, y:int, input_dir:str, output_dir:str):
        """__init__ To initialize custom wire object for canvas

        Args:
            x (int): Column's number in grid for wire
            y (int): Row's number in grid for wire
            input_dir (str): Input direction for wire in which it take input(from left,right,top or bottom)
            output_dir (str): Output direction for wire in which it pass output(from left,right,top or bottom)
        """

        # Set class properties
        self.x = x
        self.y = y
        self.rect = pygame.Rect(Canvas.x+Canvas.block_size*x,Canvas.y+Canvas.block_size*y,Canvas.block_size,Canvas.block_size)
        self.signal = False
        self.input_direction = input_dir
        self.output_direction = output_dir
        self.neighbour_output_direction = reverse_direction(input_dir)
        self.images = self.get_wire_image(input_dir, output_dir)
        self.block = Canvas.blockgrid[(x,y)]
        self.selected = False # For Selection State (Used For-Event and Drawing)

        # For Change all direction From None to False
        for dire in self.block.output:
            self.block.output[dire] = False

        # For Mini Menu At Top
        self.menu_rect = pygame.Rect((self.rect.centerx-13),(self.rect.top-30),26,26)
        self.menu_image = pygame.transform.scale(assets["toolbar icons"]["rotate"],(20,20))

        # For Change Wire(Straight and Curved)
        self.change_rect = pygame.Rect((self.rect.right+4),(self.rect.centery-13),26,26)
        self.change_image = pygame.transform.scale(assets["toolbar icons"]["change"],(20,20))

    @staticmethod
    def get_wire_image(in_dir:str, out_dir:str):
        """get_wire_image Static Helper function to get disire wire image according to wire type(straight and curved) and roation(left, right, top and bottom)

        Args:
            in_dir (str): Input direction of wire
            out_dir (str): Output direction of wire

        Returns:
            dictionary: Dictionary of pygame image pair of ON/OFF signal
        """

        # Straight connections
        if {in_dir, out_dir} in [{'left', 'right'}, {'top', 'bottom'}]:
            base_name = 'Straight'
        # Right-angled connections
        elif (in_dir == 'bottom' and out_dir == 'right') or (in_dir == 'left' and out_dir == 'bottom') or (in_dir == 'top' and out_dir == 'left') or (in_dir == 'right' and out_dir == 'top'):
            base_name = 'B_to_R'
        # Left-angled connections
        else:
            base_name = 'B_to_L'

        on_img = assets["wire"][f"{base_name}_ON"]
        off_img = assets["wire"][f"{base_name}_OFF"]

        # Define rotation angles based on (input, output)
        direction_to_angle = {
            'leftright': 0,
            'topbottom': 270,
            'rightleft': 180,
            'bottomtop': 90,
            
            "bottomright": 0,
            "righttop": 90,
            "topleft": 180,
            "leftbottom": 270,

            "bottomleft": 0,
            "rightbottom": 90,
            "topright": 180,
            "lefttop": 270
        }

        key = in_dir + out_dir
        angle = direction_to_angle.get(key)

        on_rotated = pygame.transform.rotate(on_img, angle)
        off_rotated = pygame.transform.rotate(off_img, angle)

        return {"ON":on_rotated, "OFF":off_rotated}
    
    @staticmethod
    def get_wire_change(in_dir:str, out_dir:str):
        """get_wire_change Static Helper function to change type of wire(Straight or curved[left-handed or right-handed])

        Args:
            in_dir (str): Input direction of current wire
            out_dir (str): Output direction of current wire

        Returns:
            tuole: Tuple containing two directions string --> (input_direction, output_direction)
        """

        # Straight connections
        if {in_dir, out_dir} in [{'left', 'right'}, {'top', 'bottom'}]:
            return ("left","bottom")

        # Right-angled connections
        elif (in_dir == 'bottom' and out_dir == 'right') or (in_dir == 'left' and out_dir == 'bottom') or (in_dir == 'top' and out_dir == 'left') or (in_dir == 'right' and out_dir == 'top'):
            return ("left","top")

        # Left-angled connections
        else:
            return ("left","right")

    def draw(self, screen:pygame.surface.Surface):
        """
        draw Main Mehtod to draw wire related things on GUI window with pygame.
        also update wire-signal live update logic.
        call in every frame to update wire GUI.
        call inside main-game-loop.

        Args:
            screen (pygame.surface.Surface): Main pygame screen/window object
        """

        # For Update Usefull Data
        self.rect = pygame.Rect(Canvas.x+Canvas.block_size*self.x,Canvas.y+Canvas.block_size*self.y,Canvas.block_size,Canvas.block_size)

        self.signal = Canvas.blockgrid[self.block.neighbour_pos[self.input_direction]].output[self.neighbour_output_direction]
        self.block.output[self.output_direction] = self.signal

        # For Draw Item On Screen
        image = self.images["ON"] if self.signal else self.images["OFF"]
        image = pygame.transform.scale(image,(Canvas.block_size,Canvas.block_size))
        screen.blit(image,self.rect)

    def handle_event(self,event:pygame.event.Event):
        """handle_event Main method to handle all user input with wire realted event.
        call in every frame to handle event.
        call inside main-event-loop.

        Args:
            event (pygame.event.Event): Event Object of pygame that have input information
        """

        print("selected:",self.name) # For debugging purpose

        # Handle mouse events
        pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.menu_rect.collidepoint(pos):
                # Rotate The Gate (Replace Wire with new)
                Canvas.delete_item(self)
                Canvas.add_item(name=self.name, col=self.x, row=self.y, in_dir=next_direction[self.input_direction], out_dir=next_direction[self.output_direction])

            elif self.change_rect.collidepoint(pos):
                # Change Wire Logic (Curved, Straight)(Replace Wire with new)
                Canvas.delete_item(self)
                new_in, new_out = self.get_wire_change(self.input_direction,self.output_direction)
                Canvas.add_item(name=self.name, col=self.x, row=self.y, in_dir=new_in,out_dir=new_out)     

        # Handle key events alternative
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                # Rotate The Gate (Replace Wire with new)
                Canvas.delete_item(self)
                Canvas.add_item(name=self.name, col=self.x, row=self.y, in_dir=next_direction[self.input_direction], out_dir=next_direction[self.output_direction])
            elif event.key == pygame.K_c:
                # Change Wire Logic (Curved, Straight)(Replace Wire with new)
                Canvas.delete_item(self)
                new_in, new_out = self.get_wire_change(self.input_direction,self.output_direction)
                Canvas.add_item(name=self.name, col=self.x, row=self.y, in_dir=new_in,out_dir=new_out)

    def selected_draw(self, screen:pygame.surface.Surface):
        """
        selected_draw Method to draw change type of wire, rotate wire and selected box when item is selected.

        Args:
            screen (pygame.surface.Surface): Main pygame screen/window object
        """
        # Highlight By Square Boarder if Selected and Other Selected Menu
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)

        # For Update menu Rect
        self.menu_rect.x = self.rect.centerx-13
        self.menu_rect.y = self.rect.top-30

        # For Mini Menu.
        pygame.draw.rect(screen, (225, 225, 225), self.menu_rect, border_radius=3)
        screen.blit(self.menu_image, (self.menu_rect.x+3, self.menu_rect.y+3))

        # For Update menu Rect
        self.change_rect.x = self.rect.right+4
        self.change_rect.y = self.rect.centery-13

        # For Change Menu.
        pygame.draw.rect(screen, (225, 225, 225), self.change_rect, border_radius=3)
        screen.blit(self.change_image, (self.change_rect.x+3, self.change_rect.y+3))

class NotGate:
    """
    Not-Gate is Logic-Object for canvas grid.
    it process input signal with notgate logic and pass signal to particular output direction.
    This class handle all NotGate logic(draw on screen + user event handling)
    """
    name = "not"

    def __init__(self, x:int, y:int, input_dir:str):
        """__init__ To initialize custom Not-Gate object for canvas

        Args:
            x (int): Column's number in grid for Not-Gate
            y (int): Row's number in grid for Not-Gate
            input_dir (str): Input direction for Not-Gate in which it take input(from left,right,top or bottom)
        """

        # Set class properties
        self.x = x
        self.y = y
        self.input_signal = False
        self.output_signal = False
        self.input_direction = input_dir
        self.output_directions = [item for item in ["left","right","top","bottom"] if item != input_dir]
        self.image = self.get_image()
        
        self.ratio = (2,1) if input_dir in ("left","right") else (1,2) 
        self.blocks = self.get_blocks()

        self.rect = pygame.Rect(Canvas.x+Canvas.block_size*x, Canvas.y+Canvas.block_size*y, Canvas.block_size*self.ratio[0], Canvas.block_size*self.ratio[1])

        self.current_input_direction = input_dir
        self.neighbour_output_direction = reverse_direction(self.current_input_direction)
        self.selected = False # For Selection State (Used For-Event and Drawing)

        # For Mini Menu At Top
        self.menu_rect = pygame.Rect((self.rect.centerx-13),(self.rect.top-30),26,26)
        self.menu_image = pygame.transform.scale(assets["toolbar icons"]["rotate"],(20,20))

    def get_image(self):
        """get_image Helper function to get disire Not-Gate image according to input direction(left, right, top and bottom)

        Returns:
            pygame.image: Image object of pygame
        """

        # Return disire Not-Gate image accoding to input direction from assets
        if self.input_direction == "left":
             return assets["not"]["L_to_R"]
        elif self.input_direction == "right":
             return assets["not"]["R_to_L"]
        elif self.input_direction == "top":
             return assets["not"]["T_to_B"]
        else:
             return assets["not"]["B_to_T"]
        
    def get_blocks(self):
        """get_blocks Utility method to return space block in grid that Not-Gate occupy according to direction

        Returns:
            dictionary: Dictionary with keys(input and output) and values coresponding block object from grid pair
        """

        # Return blocks according to input direction
        if self.input_direction == "left":
            blocks = {"input": Canvas.blockgrid[(self.x,self.y)],
                      "output": Canvas.blockgrid[(self.x+1,self.y)]}
            
        elif self.input_direction == "right":
            blocks = {"output": Canvas.blockgrid[(self.x,self.y)],
                      "input": Canvas.blockgrid[(self.x+1,self.y)]}
            
        elif self.input_direction == "top":
            blocks = {"input": Canvas.blockgrid[(self.x,self.y)],
                      "output": Canvas.blockgrid[(self.x,self.y+1)]}
            
        else:
            blocks = {"output": Canvas.blockgrid[(self.x,self.y)],
                      "input": Canvas.blockgrid[(self.x,self.y+1)]}

        return blocks
        
    def draw(self, screen:pygame.surface.Surface):
        """
        draw Main Mehtod to draw Not-Gate related things on GUI window with pygame.
        also perform NotGate live update logic.
        call in every frame to update Not-Gate GUI.
        call inside main-game-loop.

        Args:
            screen (pygame.surface.Surface): Main pygame screen/window object
        """

        # For Update Usefull Data
        self.rect.x = Canvas.x+Canvas.block_size*self.x
        self.rect.y = Canvas.y+Canvas.block_size*self.y
        self.rect.width = Canvas.block_size*self.ratio[0]
        self.rect.height = Canvas.block_size*self.ratio[1]
        
        # For Getting Input Signal
        self.input_signal = Canvas.blockgrid[self.blocks["input"].neighbour_pos[self.current_input_direction]].output[self.neighbour_output_direction]

        # Not Gate Logic
        self.output_signal = not self.input_signal

        # For Update Output to Blocks
        for direction in self.output_directions:
            self.blocks["output"].output[direction] = self.output_signal

        # For Draw Item On Screen
        image = pygame.transform.scale(self.image,self.rect.size)
        screen.blit(image,self.rect)

    def handle_event(self,event:pygame.event.Event):
        """handle_event Main method to handle all user input with Not-Gare realted event.
        call in every frame to handle event.
        call inside main-event-loop.

        Args:
            event (pygame.event.Event): Event Object of pygame that have input information
        """

        print("selected:",self.name) # For debugging purpose

        # Handle mouse events
        pos = pygame.mouse.get_pos()
        if self.menu_rect.collidepoint(pos) and event.type == pygame.MOUSEBUTTONDOWN:
            # Rotate The Gate (Replace Gate with new)
            Canvas.delete_item(self)
            Canvas.add_item(name=self.name, col=self.x, row=self.y, in_dir=next_direction[self.input_direction])

        # Handle key events alternative
        if event.type == pygame.KEYDOWN:
            # Rotate The Gate (Replace Gate with new)
            Canvas.delete_item(self)
            Canvas.add_item(name=self.name, col=self.x, row=self.y, in_dir=next_direction[self.input_direction])

    def selected_draw(self, screen:pygame.surface.Surface):
        """
        selected_draw Method to draw rotate NotGate and selected box when item is selected.

        Args:
            screen (pygame.surface.Surface): Main pygame screen/window object
        """

        # Highlight By Square Boarder if Selected and Other Selected Menu
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)

        # For Update menu Rect
        self.menu_rect.x = self.rect.centerx-13
        self.menu_rect.y = self.rect.top-30

        # For Mini Menu.
        pygame.draw.rect(screen, (225, 225, 225), self.menu_rect, border_radius=3)
        screen.blit(self.menu_image, (self.menu_rect.x+3, self.menu_rect.y+3))

class Gate:
    """
    Gate is Logic-Object for canvas grid.
    it process two input signal with all two input logic-gates and pass signal to particular output direction.
    This class handle all two input Gates(and,or,nand,nor,x-or,x-nor) logic(draw on screen + user event handling)
    """

    # Lambda Functions for All Gate logic
    gate_logic = {
        "and": lambda a, b: a and b,
        "or": lambda a, b: a or b,
        "nand": lambda a, b: not (a and b),
        "nor": lambda a, b: not (a or b),
        "xor": lambda a, b: True if a != b else False,
        "xnor": lambda a, b: not (True if a != b else False)
    }
    
    def __init__(self, x:int, y:int, input_dir:str, gate_name:str):
        """__init__ To initialize custom Gate object for canvas

        Args:
            x (int): Column's number in grid for Gate
            y (int): Row's number in grid for Gate
            input_dir (str): Input direction for Gate in which it take input(from left,right,top or bottom)
            gate_name (str): Two input gate name from (and,or,nor,nand,x-or,x-nor)
        """

        # Set class properties
        self.x = x
        self.y = y
        self.rect = pygame.Rect(Canvas.x+Canvas.block_size*x, Canvas.y+Canvas.block_size*y, Canvas.block_size*2, Canvas.block_size*2)
        self.input_direction = input_dir
        self.name  = gate_name
        self.input_signals = {1:False, 2:False}
        self.output_signal = False
        self.image = self.get_image()
        self.blocks = self.get_blocks()
        self.logic_fun = Gate.gate_logic[gate_name]

        self.output_directions = self.get_output_directions()
        self.current_input_directions = {key:input_dir for key in (1,2)}
        self.neighbour_output_directions = {key:reverse_direction(self.current_input_directions[key]) for key in (1,2)}
        self.selected = False # For Selection State (Used For-Event and Drawing)

        # For Mini Menu At Top
        self.menu_rect = pygame.Rect((self.rect.centerx-13),(self.rect.top-30),26,26)
        self.menu_image = pygame.transform.scale(assets["toolbar icons"]["rotate"],(20,20))

    def get_output_directions(self):
        """get_output_directions Helper function to get four output direction for two output blocks

        Returns:
            dictionary: Dictionary containing two direction string list as two values with key 1 and 2.
        """

        # Making dictionary of lists
        outdict = {1:list(),2:list()}

        # Add output direction according to gates orientation
        for key in outdict:
            outdict[key].append(reverse_direction(self.input_direction))
            if key == 1:
                if self.input_direction in ("left","right"):
                    outdict[key].append("top")
                else:
                    outdict[key].append("left")

            else:
                if self.input_direction in ("left","right"):
                    outdict[key].append("bottom")
                else:
                    outdict[key].append("right")
        return outdict

    def get_image(self):
        """get_image Helper function to get disire Gate image according to input direction(left, right, top and bottom)

        Returns:
            pygame.image: Image object of pygame
        """
        if self.input_direction == "left":
             return assets[self.name]["L_to_R"]
        elif self.input_direction == "right":
             return assets[self.name]["R_to_L"]
        elif self.input_direction == "top":
             return assets[self.name]["T_to_B"]
        else:
             return assets[self.name]["B_to_T"]
        
    def get_blocks(self):
        """get_blocks Utility method to return space block in grid that Gate occupy.
        total 4-block occupy by direction.
        two for input and two for output according to gate direction.

        Returns:
            dictionary: Dictionary with keys(input(1 and 2) and output(1 and 2)) and values coresponding block object from grid pair
        """

        # Return blocks according to input direction
        if self.input_direction == "left":
            blocks = {"input1": Canvas.blockgrid[(self.x,self.y)],
                      "input2": Canvas.blockgrid[(self.x,self.y+1)],
                      "output1": Canvas.blockgrid[(self.x+1,self.y)],
                      "output2": Canvas.blockgrid[(self.x+1,self.y+1)]}
            
        elif self.input_direction == "right":
            blocks = {"input1": Canvas.blockgrid[(self.x+1,self.y)],
                      "input2": Canvas.blockgrid[(self.x+1,self.y+1)],
                      "output1": Canvas.blockgrid[(self.x,self.y)],
                      "output2": Canvas.blockgrid[(self.x,self.y+1)]}
            
        elif self.input_direction == "top":
            blocks = {"input1": Canvas.blockgrid[(self.x,self.y)],
                      "input2": Canvas.blockgrid[(self.x+1,self.y)],
                      "output1": Canvas.blockgrid[(self.x,self.y+1)],
                      "output2": Canvas.blockgrid[(self.x+1,self.y+1)]}
            
        else:
            blocks = {"input1": Canvas.blockgrid[(self.x,self.y+1)],
                      "input2": Canvas.blockgrid[(self.x+1,self.y+1)],
                      "output1": Canvas.blockgrid[(self.x,self.y)],
                      "output2": Canvas.blockgrid[(self.x+1,self.y)]}

        return blocks

    def draw(self, screen:pygame.surface.Surface):
        """
        draw Main Mehtod to draw Gate related things on GUI window with pygame.
        also perform Gate live update logic.
        call in every frame to update Gate GUI.
        call inside main-game-loop.

        Args:
            screen (pygame.surface.Surface): Main pygame screen/window object
        """
        
        # For Update Usefull Data
        self.rect.x = Canvas.x+Canvas.block_size*self.x
        self.rect.y = Canvas.y+Canvas.block_size*self.y
        self.rect.width = Canvas.block_size*2
        self.rect.height = Canvas.block_size*2
        
        # For Getting Input Signal
        for key in self.input_signals:
            self.input_signals[key] = Canvas.blockgrid[self.blocks[f"input{key}"].neighbour_pos[self.current_input_directions[key]]].output[self.neighbour_output_directions[key]]

        # Gate Logic
        self.output_signal = self.logic_fun(self.input_signals[1],self.input_signals[2])

        # For Update Output to Blocks
        for key in self.output_directions:
            for direction in self.output_directions[key]:
                self.blocks[f"output{key}"].output[direction] = self.output_signal

        # For Draw Item On Screen
        image = pygame.transform.scale(self.image,self.rect.size)
        screen.blit(image,self.rect)

    def handle_event(self,event:pygame.event.Event):
        """
        handle_event Main method to handle all user input with Gare realted event.
        call in every frame to handle event.
        call inside main-event-loop.

        Args:
            event (pygame.event.Event): Event Object of pygame that have input information
        """

        print("selected:",self.name) # For debugging purpose

        # Handle mouse events
        pos = pygame.mouse.get_pos()
        if self.menu_rect.collidepoint(pos) and event.type == pygame.MOUSEBUTTONDOWN:
            # Rotate The Gate (Replace Gate with new)
            Canvas.delete_item(self)
            Canvas.add_item(name=self.name, col=self.x, row=self.y, in_dir=next_direction[self.input_direction])

        # Handle key events alternative
        if event.type == pygame.KEYDOWN:
            # Rotate The Gate (Replace Gate with new)
            Canvas.delete_item(self)
            Canvas.add_item(name=self.name, col=self.x, row=self.y, in_dir=next_direction[self.input_direction])

    def selected_draw(self, screen:pygame.surface.Surface):
        """
        selected_draw Method to draw rotate Gate button and selected box when item is selected.

        Args:
            screen (pygame.surface.Surface): Main pygame screen/window object
        """

        # Highlight By Square Boarder if Selected and Other Selected Menu
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)

        # For Update menu Rect
        self.menu_rect.x = self.rect.centerx-13
        self.menu_rect.y = self.rect.top-30

        # For Mini Menu.
        pygame.draw.rect(screen, (225, 225, 225), self.menu_rect, border_radius=3)
        screen.blit(self.menu_image, (self.menu_rect.x+3, self.menu_rect.y+3))

class Item:
    """
    Item is Menu-item for MenuItem.
    It is Menubar-Item each item either can placa on grid-canvas or perform any task like deleting object.
    This class handle all Item logic(draw on screen + user event handling)
    """

    def __init__(self,name:str ,x:int, y:int, width:int, height:int):
        """__init__ Initialize custom Item for Menu-Bar.

        Args:
            name (str): Name of item(gate, wire or switch) or tool(delete)
            x (int): X Coordinate on window for item box(top-left)
            y (int): Y Coordinate on window for item box(top-left)
            width (int): Width of the box
            height (int): Height of the box
        """

        # Set class properties
        self.name = name
        self.rect = pygame.Rect(x, y, width, height)
        self.image = self.get_image() # getting tool item image
        self.color = (71, 100, 148) # Background color
        self.border_color = (47, 66, 97) # Border color
        self.hover = False
        self.hover_border_color = (255, 255, 255) # Hover border color
        self.selected = False
        self.selected_border_color = (0, 255, 0) # Selected border color

    def get_image(self):
        """get_image Helper function to get disire Tool-item image according to item name

        Returns:
            pygame.image: Image object of pygame
        """
        image = pygame.transform.scale(assets["toolbar icons"][self.name], (self.rect.width-20, self.rect.height-20))

        return image

    def draw(self, screen:pygame.surface.Surface):
        """
        draw Main Mehtod to draw tool-item related things on GUI window with pygame.
        call in every frame to update Tool-Item GUI.
        call inside main-game-loop.

        Args:
            screen (pygame.surface.Surface): Main pygame screen/window object
        """

        # One-by-one draw things on screen according to order
        pygame.draw.rect(screen, self.color, self.rect, 0, 10)

        # For selected and hover effect
        if self.selected:
            pygame.draw.rect(screen, self.selected_border_color, self.rect, 2, 10)
        elif self.hover:
            pygame.draw.rect(screen, self.hover_border_color, self.rect, 2, 10)
        else:
            pygame.draw.rect(screen, self.border_color, self.rect, 2, 10)

        image_pos = (self.rect.x+10, self.rect.y+10)
        screen.blit(self.image, image_pos)

    def handle_event(self, event:pygame.event.Event):
        """handle_event Main method to handle all user input with Tool-Item realted event.
        call in every frame to handle event.
        call inside main-event-loop.

        Args:
            event (pygame.event.Event): Event Object of pygame that have input information
        """

        pos = pygame.mouse.get_pos()
        self.hover = False

        # Handle selecting and deselecting event for tool-item
        if self.rect.collidepoint(pos):
            self.hover = True
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.selected = True
                if ToolBar.selected_item:
                    ToolBar.selected_item.selected = None
                ToolBar.selected_item = self

class ToolBar:
    """
    ToolBar is static class for draw and handle all user input event related to toolbar.
    ToolBar GUI and all tool-item container to handle their event efficiantly.
    """

    is_active = True
    
    @classmethod
    def set_tools(cls, x:int, y:int, width:int, height:int, color:tuple, border_color:tuple):
        """set_tools Class method to initialize Toolbar class with all items.

        Args:
            x (int): X Coordinate on window for Toolbar(top-left)
            y (int): Y Coordinate on window for Toolbar(top-left)
            width (int): Width of the Toolbar
            height (int): Height of the Toolbar
            color (tuple): Background fill color for toolbar
            border_color (tuple): Border colot for toolbar
        """        

        # Set class properties
        cls.x = x
        cls.y = y
        cls.width = width
        cls.height = height
        cls.rect = pygame.Rect(x , y, width, height)
        cls.color = color
        cls.border_color = border_color
        item_names = ("not","and","or","nand","nor","xor","xnor","switch", "wire")
        cls.items_and_tools = {i:Item(item_names[i], x+10+(85*i), y + 10,75,75) for i in range(9)} # Add tool-item objects
        cls.selected_item = None
        cls.items_and_tools[9] = Item("delete", x+775, y+10, 50, 50) # Add delete tool

    @classmethod
    def draw(cls, screen:pygame.surface.Surface):
        """
        draw Class Mehtod to draw toolbar related things on GUI window with pygame.
        also perform toolbar live update logic.
        call in every frame to update toolbar GUI.
        call inside main-game-loop.

        Args:
            screen (pygame.surface.Surface): Main pygame screen/window object
        """
        
        # Draw tool bar things on screen if toolbar is active
        if cls.is_active:
            pygame.draw.rect(screen, cls.color, cls.rect, 0, -1, 20, 20)
            pygame.draw.rect(screen, cls.border_color, cls.rect, 5, -1, 20, 20)

            # Draw all items and tools on screen
            for i in cls.items_and_tools:
                cls.items_and_tools[i].draw(screen)

    @classmethod
    def handle_event(cls, event:pygame.event.Event):
        """handle_event Main method to handle all user input with toolbar realted event.
        call in every frame to handle event.
        call inside main-event-loop.

        Args:
            event (pygame.event.Event): Event Object of pygame that have input information
        """

        # Handle events if toolbar is active
        if cls.is_active:
            # For Deselect Selceted Item
            pos = pygame.mouse.get_pos()
            if  cls.selected_item and (cls.selected_item.name != "delete") and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not cls.rect.collidepoint(pos):
                cls.selected_item.selected = False
                cls.selected_item = None

            # For Handling All Items Event
            for item_name in cls.items_and_tools:
                item = cls.items_and_tools[item_name]
                item.handle_event(event)

class Menu:
    """
    Menubar is static class for draw and handle all user input event related to Menubar.
    MenuBar GUI and to handle their event efficiantly and easily.
    """

    # Menu Class General Variables
    opened = False
    rect = pygame.Rect(900,0,360,600)
    color = (47, 66, 97) # Background color
    border_color = (97, 136, 199) # Border color

    # For Semi-Transparent
    overlay = pygame.Surface((900, 600), pygame.SRCALPHA) # Fill it with semi-transparent black
    overlay.fill((0, 0, 0, 128))  # RGBA — 128 is 50% transparent

    # Text-Field For Menu Title
    title = TextBox("Menu Bar",950,0,300,60,"Poppins-Medium.ttf",border_color)
    back_button = ImageButton(915,15,30,30,"general.back","general.back") # Back-Button Object

    # Text-Field For Craft-Name
    craft_name_rect = pygame.Rect(925,75,310,70)
    craft_name_border_color = (71, 100, 148)
    craft_name = TextBox(str(variables["working_craft"]),craft_name_rect.x,craft_name_rect.y,craft_name_rect.width,craft_name_rect.height,"Poppins-Medium.ttf",pad=10)

    # For Save Button
    save_button = TextButton("Save",960,160,240,50,(47, 66, 97),(200,200,200),"Poppins-Medium.ttf")
    # For Edit Canvas Button
    edit_button = TextButton("Edit Canvas",960,220,240,50,(47, 66, 97),(200,200,200),"Poppins-Medium.ttf")

    # For  Setting Button
    setting_button = TextButton("Setting",960,480,240,50,(47, 66, 97),(200,200,200),"Poppins-Medium.ttf")
    # For Exit Button
    exit_button = TextButton("Exit",960,540,240,50,(47, 66, 97),(200,200,200),"Poppins-Medium.ttf")

    # For Edit View
    edit_view = False
    edit_rect = pygame.Rect(225,100,450,400)
    edit_craft_title = TextBox("Edit Canvas",225,100,450,50,"Montserrat-ExtraBold.ttf",color)
    rename_canvas_text = TextBox("Rename Canvas",250,155,400,50,"Poppins-Medium.ttf",(211,222,233),5,"left")
    canvas_size_text = TextBox("Canvas Size",250,265,400,50,"Poppins-Medium.ttf",(211,222,233),5,"left")
    column_text = TextBox("Column",250,300,195,45,"Poppins-Medium.ttf",(97, 136, 255))
    x_text = TextBox("X",425,300,50,50,"Montserrat-ExtraBold.ttf",(97, 136, 255),10)
    row_text = TextBox("Row",455,300,195,45,"Poppins-Medium.ttf",(97, 136, 255))
    save_edit_button = TextButton("Save Edit",330,435,240,50,(33,167,211),(230,230,230),"Montserrat-ExtraBold.ttf")

    craft_name_input = TextInputField(250,205,400,50,"Enter Canvas Name Here...",border_color,"Poppins-Medium.ttf",(211,222,233),27,(211,222,233),15)
    column_input = NumberInputField(250,340,195,50,30,border_color,"Poppins-Medium.ttf",(211,222,233),27,(211,222,233),200,10)
    row_input = NumberInputField(455,340,195,50,20,border_color,"Poppins-Medium.ttf",(211,222,233),27,(201,212,255),200,10)

    @classmethod
    def save_canvas(cls):
        """save_canvas Utility class method to save canvas in file for future use.
        """

        canvas_data = {}
        canvas_data["size"] = {"column":Canvas.column, "row":Canvas.row}
        canvas_data["items"] = []

        # For Items With Handle Event and Normal Items
        for item in Canvas.all_items_with_handle_event + Canvas.all_items:
            item_data = {}
            item_name = item.name
            item_data["name"] = item_name
            item_data["x"] = item.x
            item_data["y"] = item.y

            if item_name != "switch":
                item_data["input_direction"] = item.input_direction

                if item_name == "wire":
                    item_data["output_direction"] = item.output_direction

            canvas_data["items"].append(item_data)

        # Save file is craft folder with canvas name
        file_path = "craft/"+str(variables["working_craft"]) + ".craft"
        try:
            with open(file_path,"wb") as f:
                pickle.dump(canvas_data, f)
            print("File Saved SuccesFully.")
        except:
            print("File Not Saved.")

    @classmethod
    def draw(cls, screen:pygame.surface.Surface):
        """
        draw Class Mehtod to draw Menubar related things on GUI window with pygame.
        also perform Menu live update logic.
        call in every frame to update toolbar GUI.
        call inside main-game-loop.

        Args:
            screen (pygame.surface.Surface): Main pygame screen/window object
        """
        
        # Drawing Semi-Transparent Background
        screen.blit(cls.overlay, (0,0))

        # Drawing Menu Backgroud
        pygame.draw.rect(screen, cls.color, cls.rect)
        pygame.draw.line(screen, cls.border_color, (cls.rect.x,0), (cls.rect.x,600),7) # For Border

        # For Drawing Menu Items(Buttons, Text, etc..)
        cls.back_button.draw(screen) # Drawing Back-Button
        cls.title.draw(screen) # Drawing Title "Menu"
        # For Drawing Craft-Name
        pygame.draw.rect(screen, cls.border_color, cls.craft_name_rect,0,14)
        pygame.draw.rect(screen, cls.craft_name_border_color, cls.craft_name_rect,5,14)
        cls.craft_name.draw(screen)

        cls.save_button.draw(screen) # For Save Button
        pygame.draw.line(screen,cls.border_color,(cls.rect.x+60,215),(cls.rect.x+300,215),5) # Seperation Line
        cls.edit_button.draw(screen) # For Edit Canvas Button

        cls.setting_button.draw(screen) # For Setting Button
        pygame.draw.line(screen,cls.border_color,(cls.rect.x+60,535),(cls.rect.x+300,535),5) # Seperation Line
        cls.exit_button.draw(screen) # For Exit Button

        # For edit canvas pop-up handling
        if cls.edit_view:
            # Drawing Semi-Transparent Background
            screen.blit(cls.overlay, (0,0))
            pygame.draw.rect(screen,cls.color,cls.edit_rect,border_radius=20)
            pygame.draw.rect(screen,cls.border_color,(225,100,450,50),border_top_left_radius=20,border_top_right_radius=20)
            cls.edit_craft_title.draw(screen)
    
            cls.rename_canvas_text.draw(screen)
            cls.craft_name_input.draw(screen)
            cls.canvas_size_text.draw(screen)
            cls.column_text.draw(screen)
            cls.x_text.draw(screen)
            cls.row_text.draw(screen)
            cls.column_input.draw(screen)
            cls.row_input.draw(screen)
            cls.save_edit_button.draw(screen)

    @classmethod
    def handle_event(cls, event:pygame.event.Event):
        """handle_event Main method to handle all user input with menubar realted event.
        call in every frame to handle event.
        call inside main-event-loop.

        Args:
            event (pygame.event.Event): Event Object of pygame that have input information
        """

        # Handling events for Edit-canvas pop-up
        if cls.edit_view:
            cls.craft_name_input.handle_event(event)
            cls.column_input.handle_event(event)
            cls.row_input.handle_event(event)

            if cls.save_edit_button.is_clicked(event):
                # Delete Old File
                try:
                    os.remove("craft/"+variables["working_craft"]+".craft")
                    print("Old File Deleted Succesfully.")
                except:
                    print("Old File Not Deleted.")

                # Updare all things
                Canvas.column = int(cls.column_input.text)
                Canvas.row = int(cls.row_input.text)
                variables["working_craft"] = cls.craft_name_input.text if cls.craft_name_input.text else variables["working_craft"]
                cls.save_canvas()

                # Clean old canvas and set again for new upadtes
                Canvas.cleanUp()
                Canvas.set_canvas()

                cls.edit_view = False
                Animation.active_animations.append("menubarclose")

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if not cls.edit_rect.collidepoint(pos):
                    cls.edit_view = False

        # Handle events for Menu-bar buttons
        else:
            # Handle Back-Button Event
            if cls.back_button.is_clicked(event):
                Animation.active_animations.append("menubarclose")

            # Handle Save-Button Event
            if cls.save_button.is_clicked(event):
                cls.save_canvas()

            # Handle Edit-Button Event
            if cls.edit_button.is_clicked(event):
                cls.edit_view = True
                cls.craft_name_input.text = str(variables["working_craft"])
                cls.row_input.text = str(Canvas.row)
                cls.column_input.text = str(Canvas.column)

            # Handle Setting-Button Event
            if cls.setting_button.is_clicked(event):
                cls.save_canvas()
                Animation.active_animations.append("menubarclose")
                Canvas.cleanUp()
                variables["current_page"] = "setting"

            # Handle Exit-Button Event
            if cls.exit_button.is_clicked(event):
                cls.save_canvas()
                Animation.active_animations.append("menubarclose")
                Canvas.cleanUp()
                variables["current_page"] = "home"

# For Handling Screen Animations
class Animation:
    """
    Animation is static class for handle live animation for screen using custom function for it.
    """

    # Dictionary with animation name and function pairs
    animations_dict = {"toolbaropen":toolbar_open_animation,
                        "toolbarclose":toolbar_close_animation,
                        "menubaropen":menubar_open_animation,
                        "menubarclose":menubar_close_animation}
    active_animations = [] # Animations that is running live

    @classmethod
    def run_animations(cls):
        """run_animations Class method to run all active animation by calling its function.
        """

        # Run all live animations
        for animation_name in cls.active_animations:
            cls.animations_dict[animation_name]()

# For Set Up Canvas
ToolBar.set_tools(30, 510, 840, 100, (97, 136, 199), (47, 66, 97))

# For Draw Canvas Screen GUI
def draw_screen(screen:pygame.Surface):
    """draw_screen Handle GUI drawing for canvas screen

    Args:
        screen (pygame.Surface): Main pygame window or screen object
    """

    # For Fill Background
    screen.fill((46,52,64))

    if Canvas.canvas_seted:
        # For Canvas Draw on Screen
        Canvas.draw(screen)
    else:
        Canvas.set_canvas()

    # For ToolBar(bottom side-slide toolbar)
    ToolBar.draw(screen)

    # For Menu(left side-slide menu)
    if Menu.opened:
        Menu.draw(screen)

    # For Animation Running(No Drawing Only For Update)
    if len(Animation.active_animations):
        Animation.run_animations()

# For Handle Pygame Events
def handle_event(event:pygame.event.Event):
    """handle_event For handle pygame user input event for interactive elements like input-fields and buttons for canva screen

    Args:
        event (pygame.event.Event): User input object provided by pygame
    """
    
    # For Handle Menu's Events (left side- slide menu)
    if Menu.opened:
        Menu.handle_event(event)

    else:
        # For Handle Canvas's Events 
        Canvas.handle_event(event)

        # For Handle ToolBar's Events
        ToolBar.handle_event(event)