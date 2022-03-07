from utils import roll_dice, simulate_dice_rolls

#
#https://i.stack.imgur.com/n9nmA.jpg
#https://catlikecoding.com/unity/tutorials/hex-map/part-1/hexagonal-coordinates/cube-diagram.png
#http://www-cs-students.stanford.edu/~amitp/game-programming/grids/



#http://www-cs-students.stanford.edu/~amitp/game-programming/grids/hexagon-grid-vertex-coordinates.png?2010-09-04-08-01-34



#https://i.stack.imgur.com/n9nmA.jpg




#need to be able to render the robber onto a hexagon 


class Settlement:
    pass


class City:
    pass



class HexagonalGrid:
    def __init__(self):
        pass
    pass


class HexagonCoordinate:
    def __init__(self):
        pass
    
    def __hash__(self):
        return False

    def __eq__(self, other):
        return False



class SideCoordinate:
    def __init__(self):
        pass


class CornerCoordinate:
    def __init__(self):
        pass

class Hexagon:

    def __init__(self):
        """
        the actual coordinates will probabaly be stores somewhere else
        
        Resources:
        
        https://www.redblobgames.com/grids/hexagons/
        **https://i.stack.imgur.com/n9nmA.jpg
        https://catlikecoding.com/unity/tutorials/hex-map/part-1/hexagonal-coordinates/cube-diagram.png
        """
        self.position = (0, 0, 0)
        
        self.resource = "" #maybe a class, not sure 
        
    
    def draw(self):
        """
        https://www.blog.pythonlibrary.org/2021/02/23/drawing-shapes-on-images-with-python-and-pillow/
        """
        pass



"""
from PIL import Image, ImageDraw
def polygon(output_path):
    image = Image.new("RGB", (400, 400), "grey")
    draw = ImageDraw.Draw(image)
    draw.polygon(((100, 100), (200, 50), (125, 25)), fill="green")
    draw.polygon(((175, 100), (225, 50), (200, 25)),
                  outline="yellow")
    image.save(output_path)
if __name__ == "__main__":
    polygon("polygons.jpg")
    """

class Corner:
    def __init__(self, building = None):
        """
        vertex / corner of a hexagon
        where settlements and cities can be placed
        
        storage of the actual coordinate and left and right should go somewhere else
        for easy index 
        """
        self.position = "" #where the corner is in relation to everything else
        self.building = building #either a settlement or a city 
    
    def has_settlement(self):
        return self.building and isinstance(self.building, Settlement)
    
    def has_city(self):
        return self.building and isinstance(self.building, City)

    def undeveloped(self):
        if self.building is None:
            return True
        return False
            
        
class Side:
    """
    side of a hexagon. Roads can be placed here
    """
    pass





"""
Game:
get_corners(Tile)
returns 6 corners
tile.get_corners() -> reutrns 6 corners 

Game:
get_adjacent_tiles(corner)

"""





"""

#http://www-cs-students.stanford.edu/~amitp/game-programming/grids/hexagon-grid-vertex-coordinates.png?2010-09-04-08-01-34
each hexagon has a left and a right corner coordinate
all corners will be covered that way

place_settlement(tile1, tile2, tile3):
each corner is surrounded by 3 tiles. 
e


How to store settlemtn and road positiosn 

corners 6:
north, south, north-east, south-east, north-west, south-west

edges:
west, east, north-west, south-west, north-east, south-east


add_something (adjacent tiles)


settlement stores the tiles it is adjacent to?


stores it as dictionary 



"""


"""
each tile stores all the information about the corners and edges 
on 

settlements = {
    hexCord : settlement 
}


on roll logic: 

"""




roll_values = {
    6 : ["Tile", "Tile"]
}


class Game:
    def __init__(self):
        """
        Handles board, bank, players, etc...
        Handles all of the play acitons 

        placeSettlement
        playDevCard
        rollDice
        
        
        methods:
        roll_dice
        buy_settlement
        buy_road
        buy_city
        buy_development_card
        claim_longest_road
        claim_largest_army 
        
        get_available_corners() all available corners
        get_available_edges() all available edges
        
        get_adjaced_corners(settlement)
        get_adjaced_edges(settlement)
        
        get_valid_adjaced_corners(settlement) 
        get_valid_adjaced_edges(settlement)
        
        
        
        
        callbacks: 
        on_settlement_placed
        on_road_placed
        on_dice_roll
        on_player_trade
        on_robber_moved
        on_bank_trade  
        on_robber_move
        """
        pass
    

    
    
    
    
class Board:
    """
    cube grid of hexagons 
    """
    pass


class Hexagon:
    """
    Hexagonal Game Tile
    """
    pass


class Edge:
    """
    Edge between two tiles
    DO I NEED THIS? 
    """
    pass


class Corner:
    """
    Corner between hexagons
    DO I NEED THIS? or should redundance placements or is this class shared among tiles? 
    """
    pass


class Trade:
    def __init__(self, offer_resource, offer_resource_qty, recieve_resource, recieve_resource_qty):
        """
        data class for a trade
        maybe make this more functional by actually facilitating the trades through this.
        this honestly could be a function in game though with these same parameters
        """
        self.offer_resource = offer_resource
        self.offer_resource_qty = offer_resource_qty
        self.recieve_resource = recieve_resource
        self.recieve_resource_qty = recieve_resource_qty
        

class Player:
    """
    Dummy player class that controls player strategy and information about what the player has 
    """
    def __init__(self):
        """
        should each player have a bank class that handles transactions for them and stores resource amounts etc...
        """
        self.name = ""
        self.resources = []
        self.settlements = []
        self.cities = []
        self.inactive_dev_cards = []
        self.active_dev_cards = []
        
        #history
        self.roll_history = []
        self.move_history = []
    
    def render(self):
        """
        render the players hand 
        """
        pass
    
    
    def on_initial_turn(self, game):
        """
        initial logic for picking 
        """
        pass
    
    def on_player_turn(self, game):
        """
        logic for when it is the players turn 
        
        options: 
        call from the game object passed as param 
        
        build settlement,
        build city,
        build road
        buy dev card
        send trade 
        
        get players 
            get player settlement positions 
            get player trade history

        get available adjacent settlement spots 
        
        
        """
    

    def on_trade_request(self, player, trade):
        """
        logic for handaling a trade 
        
        a trade maybe should be an object? 
        trade contains information about the player facilitating 
        name, obviously what they're trading, what cities they have 
        actually nvm. trade does not contian any of that
        player can look that up on the board 
        
        return options:
        counter
        accept
        reject
        
        
        get_player_victory_points(player) -> int
        get_player_settlements(player) -> list
        get_player_cities(player) -> list
        get_player_roads(player) -> list
        get_player_card_count(player) -> list
        get_player_development_cards(player) -> (only active dev cards)
        """
        pass


    def buy(self, someobject):
        pass
        
        



class Cost:
    def __init__(self, book = {}):
        """
        Represents the cost to purchase something (number of resources needed)
        Need some way to keep track of what recources something costs
        """
        self.book = book
    
    
    def add_resource(self, resource_type, qty):
        """
        add to the cost of an object
        """
        self.book[resource_type] = qty
        
        

class Buyable:
    def __init__(self, cost):
        """
        includes settlements, devcards, and roads 
        """
        #how much the buyable object costs 


class DevelopmentCard(Buyable):
    
    def __init__(self):
        """
        dev card
        inherited to create the dev cards 
        need custom logic for each card.
        """
        pass

    
class Road(Buyable):
    pass


class Settlement(Buyable):
    pass



class ResourceCard:
    def __init__(self):
        """
        Recource Card 
        inherited for each resource type 
        brick, wheat, ore, lumber, sheep
        """
        self.name = ""
        pass


    def render(self):
        """
        visulization of the card
        """
        pass
    
    
    
class SpecialtyCard:
    def __init__(self):
        """
        longest road, largest army
        """
        pass
    
    
#monopoly, year of plenty, road building, knight, 