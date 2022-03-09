import math

from PIL import ImageDraw

from hexagon import (
    Hexagonable, 
    HexagonalGrid,
    HexagonalCoordinates, 
    CornerCoordinates, 
    SideCoordinates
)


class Tile(Hexagonable):
    def __init__(self, coordinates : HexagonalCoordinates, color):
        super().__init__(coordinates)
        self.color = color
    
    def get_size(self, scale : int):
        """
        returns width, height of the hexagon 
        assumes pointy edges are on top and bottom
        """
        return (scale * 3**.5, scale * 2) 
    
    
    def draw(self, image, center_x, center_y, scale):
        #poiint is a the top, sides are flat
        #30, 60, 90 triangle  scale/2 because the shortest size is scale / 2
        coords = (
            (center_x, center_y - scale), #s(north vertex)
            (center_x + 3**.5 * (scale / 2), center_y - (scale / 2)), # (north east vertex)
            (center_x + 3**.5 * (scale / 2), center_y + (scale / 2)), #(south east vertex)
            (center_x, center_y + scale), #(south vertex)
            (center_x - 3**.5 * (scale / 2), center_y + (scale / 2)), #(south west vertex)
            (center_x - 3**.5 * (scale / 2), center_y - (scale / 2)) #(north west vertex)
        )
        
        draw = ImageDraw.Draw(image)
        draw.polygon(coords, fill=self.color, width=3, outline = (0, 0, 0))




class Settlement(Hexagonable):
    pass


    def __init__(self, coordinates : CornerCoordinates, color):
        super().__init__(coordinates)
        self.color = color

    
    def get_size(self, scale):
        radius = math.ceil(scale / 10)
        return (radius * 2, radius * 2)
    
    
    def draw(self, image, center_x, center_y, scale):
        """
        change scale to a percentage of width and height
        don't pass in scale, pass in width and height. 
        """
        radius = math.ceil(scale / 10)
        draw = ImageDraw.Draw(image)
        draw.ellipse( ( (center_x - radius, center_y - radius), (center_x + radius, center_y + radius) ), fill=self.color)



sheep= (88, 209, 106)
wood= (16, 56, 23)
wheat= (227, 209, 48)
ore= (97, 97, 95)
brick= (112, 27, 27)
desert= (112, 92, 27)  

red = (255, 0, 0)

grid = HexagonalGrid(100)

grid.add_hexagonable(Tile(HexagonalCoordinates(0, 0, 0), desert))
grid.add_hexagonable(Tile(HexagonalCoordinates(0, -1, 1), wood))
grid.add_hexagonable(Tile(HexagonalCoordinates(1, -1, 0), sheep))
grid.add_hexagonable(Tile(HexagonalCoordinates(1, 0, -1), wheat))
grid.add_hexagonable(Tile(HexagonalCoordinates(0, 1, -1), brick))
grid.add_hexagonable(Tile(HexagonalCoordinates(-1, 1, 0), ore))
grid.add_hexagonable(Tile(HexagonalCoordinates(-1, 0, 1), ore))

grid.add_hexagonable(Settlement(CornerCoordinates(-1, 1, -1, "t"), red))
grid.render().show()

