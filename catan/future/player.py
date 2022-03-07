
from PIL import Image, ImageDraw


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


    def __hash__(self):
        return hash(tuple(self))
    
    
    def __eq__(self, other):
        return isinstance(other, type(self)) and tuple(self) == tuple(other)



class Hexagon:
    def __init__(self, color : tuple):
        self.color = color 
        
        
    def draw(self, image, center_x, center_y, scale):
        #poiint is a the top, sides are flat
        #30, 60, 90 triangle  scale/2 because the shortest size is scale / 2
        coords = (
            (center_x, center_y - scale), #s(north vertex)
            (center_x + 3**.5 * (scale / 2), center_y - (scale / 2)), # (north east vertex)
            (center_x + 3**.5 * (scale / 2), center_y + (scale / 2)), #(south east vertex)
            (center_x, center_y + scale),#(south vertex)
            (center_x - 3**.5 * (scale / 2), center_y + (scale / 2)), #(south west vertex)
            (center_x - 3**.5 * (scale / 2), center_y - (scale / 2)) #(north west vertex)
        )
        
        draw = ImageDraw.Draw(image)
        draw.polygon(coords, fill=self.color, width=3, outline = (0, 0, 0))
    
    
class HexagonalGrid:
    def __init__(self, scale = 100):
        """
        height : number of hexagons 
        width : number of hexagons 
        scale : radius of the hexagons
        """
        #public
        self.scale = scale
        #store mins and maxes to easily figure out the size of the image to fix all the hexagons
        #also used for determining the cartisian coordinates 
        #private
        self.min_center_x = None
        self.max_center_x = None
        self.min_center_y = None
        self.max_center_y = None
        
        #private
        self.hexagons = {}
    
    
    @property
    def width(self):
        """
        public
        """
        #need to convert largest center coordinates to the largest coordinates by adding the scale 
        #to make it fit exactly need to adjust one of these and multiply by the 3**.5 / 2
        return (self.max_center_x + self.scale) - (self.min_center_x - self.scale) 
    
    @property
    def height(self):
        """
        public
        """
        #need to convert largest center coordinates to the largest coordinates by adding the scale 
        #to make it fit exactly need to adjust one of these and multiply by the 3**.5 / 2
        return(self.max_center_y + self.scale) - (self.min_center_y - self.scale)
    
    
    def center_to_cartesian_coordinates(self, x, y):
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
        x_change = 0 - (self.min_center_x - self.scale)
        y_change = 0 - (self.max_center_y + self.scale)
        #y is different than x
        return  (x_change + x, abs(y_change + y))
    
    
    
    def add_hexagon(self, hexagon, location):
        """
        public
        """
        self.hexagons[location] = hexagon
        #adjust the size if this hexagon expands the grid
        self.set_min_and_max(location)
    
    
    def set_min_and_max(self, location):
        """
        private
        """
        x,y = location.get_2d_coordinates(self.scale)

        if self.min_center_x is None or x < self.min_center_x:
            self.min_center_x = x
        if self.max_center_x is None or x > self.max_center_x:
            self.max_center_x = x
            
        if self.min_center_y is None or y < self.min_center_y:
            self.min_center_y = y
        if self.max_center_y is None or y > self.max_center_y:
            self.max_center_y = y

    
    def render(self):
        """
        public
        """
        image = Image.new("RGBA", (self.width, self.height))
        for location, hexagon in self.hexagons.items():
            x, y = location.get_2d_coordinates(self.scale) #x, y = midpoint is origin
            x, y = self.center_to_cartesian_coordinates(x, y) #x, y = top left origin 
            hexagon.draw(image, x, y, self.scale)
        return image
      
      
      
sheep= (88, 209, 106)
wood= (16, 56, 23)
wheat= (227, 209, 48)
ore= (97, 97, 95)
brick= (112, 27, 27)
desert= (112, 92, 27)  


grid = HexagonalGrid()
grid.add_hexagon(Hexagon(desert), HexagonalCoordinates(0, 0, 0))

grid.add_hexagon(Hexagon(brick), HexagonalCoordinates(0, -1, 1))
grid.add_hexagon(Hexagon(wheat), HexagonalCoordinates(1, -1, 0))
grid.add_hexagon(Hexagon(sheep), HexagonalCoordinates(1, 0, -1))
grid.add_hexagon(Hexagon(wood), HexagonalCoordinates(0, 1, -1))
grid.add_hexagon(Hexagon(ore), HexagonalCoordinates(-1, 1, 0))
grid.add_hexagon(Hexagon(wheat), HexagonalCoordinates(-1, 0, 1))

grid.add_hexagon(Hexagon(wood), HexagonalCoordinates(2, -2, 0))
grid.add_hexagon(Hexagon(brick), HexagonalCoordinates(-1, -1, 2))
grid.add_hexagon(Hexagon(ore), HexagonalCoordinates(1, -2, 1))
grid.add_hexagon(Hexagon(sheep), HexagonalCoordinates(0, -2, 2))
grid.add_hexagon(Hexagon(brick), HexagonalCoordinates(2, -1, -1))
grid.add_hexagon(Hexagon(wheat), HexagonalCoordinates(2, 0, -2))


grid.render().show()




#wood: (16, 56, 23)
#wheat: 
#ore:
#brick:
#sheep= (88, 209, 106)