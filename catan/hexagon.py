import math

from PIL import Image



class SideCoordinates:
    pass


class HexagonalCoordinates:
    def __init__(self, r = 0, g = 0, b = 0):
        """
        cube coordinates system
        """
        self.r = r
        self.g = g
        self.b = b 
        
        
    def __iter__(self):
        yield self.r 
        yield self.g
        yield self.b
    
    
    def get_2d_coordinates(self, scale):
        """
        https://stackoverflow.com/questions/2459402/hexagonal-grid-coordinates-to-pixel-coordinates
        """
        y = 3/2 * scale * self.b
        x = 3**.5 * scale * (self.b/2 + self.r)
        return (round(x), round(y))


class CornerCoordinates(HexagonalCoordinates):
    def __init__(self, r : int, g : int, b : int, direction : str):
        """
        how coordinates relate to the tiles
        
        http://www-cs-students.stanford.edu/~amitp/game-programming/grids/hexagon-grid-vertex-coordinates.png?2010-09-04-08-01-34
        (im thinking of this top to bottom, not left to right. SO mine will be a bit different)
        https://en.wikipedia.org/wiki/Body_relative_direction    
    
        coordinates: hexagonal coordiantes
        direction: t or b (top or bottom)
        """  
        super().__init__(r, g, b)
        self.direction = direction
        

    
    def get_2d_coordinates(self, scale):
        """
        """
        x, y = super().get_2d_coordinates(scale)
        if self.direction == "t":
            
            return (x, y + scale)
        
        return (x, y - scale)
        


class Hexagonable:
    def __init__(self, coordinates : HexagonalCoordinates | CornerCoordinates | SideCoordinates):
        """
        why is it like this? to know the actual x, y the objects will be rendered at before knowing 
        all of the objects is impossible because adding hexagons to the grid changes where the objects 
        are in relation to (0,0) top left corner. 
        So they all need to be looked at holistically and then rendered so that the x,y locations can be determined
        
        Object that can be rendered to the hexagon grid
        
        to be hexagonable, must meet these requirements:
            - must have coordinates attribute. Either HexagonalCoordinates or CornerCoordinates or SideCoordinates
            - must have a draw method that takes in image, x, y, and scale
            - must have a size method that returns the expected size of the hexagonable
        
        things that are hexagonable: tiles, settlements, roads, citties
        """
        self.location = coordinates
    
    
    def get_size(self, scale):
        """
        for determining mins and maxes, need to know this to prevent things from rendering off of the screen
        
        return -> tuple (width, height)
        """
        return ()


    def draw(self, image : Image.Image, x : int, y : int, scale : int):
        """
        image: image to be drawn to
        x: center x of the object
        y: center y of the object
        scale : scale
        
        draws the object to the image
        
        return -> None
        """
        pass
    
    
class HexagonalGrid:
    def __init__(self, scale = 100):
        """
        height : number of hexagons 
        width : number of hexagons 
        scale : side length of a hexagon (everything else is rendered in regards to this) 
        """
        self.scale = scale 
        self.elements = [] 
    
    
    def get_size(self, min_x, min_y, max_x, max_y):
        """
        public
        """
        #these are probabaly gone 
        #need to convert largest center coordinates to the largest coordinates by adding the scale 
        #to make it fit exactly need to adjust one of these and multiply by the 3**.5 / 2
        return (max_x - min_x, max_y - min_y)

    
    def get_primary_monitor_coordinates(self, location, min_x, min_y):
        """
        private
        converts regular cartesian coordinates (negatives and positives) to the cartesian pixel coordinate system 
        (only positives) origin in the upper lefthand corner 
        
        coverts (0,0) center midpoint originas with negative and positive x,y's to 
        top left center origin with all positive x,y
        """
        #(0,0) is the current origin. need to change it so that the minimums are now the origin
        #might not need to adjust by the scale here... not sre but were talkign about the center so it seems a bit strange to be changing that
        #actual i think it is fine so that the adjustment is made 
        
        #need to chaange the x and the y change
        old_x, old_y = location.get_2d_coordinates(self.scale)
        return  (old_x - min_x, abs(old_y + min_y))
    
    
    def get_range(self):
        """
        loops through the elements
        returns the lowest low x and y and the highesst x and y
        
        returns a nested tuple : ( (min x, min y), (max x, max y) )

        """
        overall_min_x = None
        overall_min_y = None
        
        overall_max_x = None
        overall_max_y = None
        
        for element in self.elements:
            x, y = element.location.get_2d_coordinates(self.scale)
            width, height = element.get_size(self.scale)
            
            low_y = math.floor(y - height / 2)
            high_y = math.ceil(y + height / 2)
            left_x = math.floor(x - width / 2)
            right_x = math.ceil(x + width / 2)
            
            if overall_min_y is None or low_y < overall_min_y:
                overall_min_y = low_y
            
            if overall_min_x is None or left_x < overall_min_x:
                overall_min_x = left_x
            
            if overall_max_y is None or high_y > overall_max_y:
                overall_max_y = high_y
                
            if overall_max_x is None or right_x > overall_max_x:
                overall_max_x = right_x
                
        return ((overall_min_x, overall_min_y), (overall_max_x, overall_max_y))
            

    def add_hexagonable(self, element : Hexagonable):
        """
        add hexagonable to the grid
        
        if remove is added to to recalculate the size on remove with new adjust_min_max
        """
        self.elements.append(element)    

        
    def render(self, width = None, height = None):
        """
        shrink to width and height
        shrink (borrow from brickpy utils) shrink longest side to fit and then center it within the final
        public
        """
        min_xy, max_xy = self.get_range()
        image = Image.new("RGBA", self.get_size(*min_xy, *max_xy))
        for element in self.elements:
            x, y = self.get_primary_monitor_coordinates(element.location, *min_xy)
            element.draw(image, x, y, self.scale)
        return image
    


