from enum import Enum

class ResourceType(Enum):
    WHEAT = "Wheat",
    LUMBER = "Lumber",
    ORE = "Ore",
    BRICK = "Brick",
    SHEEP = "Sheep",
    DESERT = ""

class TileType(Enum):
    FIELDS = ResourceType.WHEAT,
    FORESTS = ResourceType.LUMBER,
    MOUNTAINS = ResourceType.ORE,
    HILLS = ResourceType.BRICK,
    PASTURES = ResourceType.SHEEP,
    DESERT = ResourceType.DESERT
    
class BuildingCost(Enum):
    ROAD = {ResourceType.LUMBER: 2, ResourceType.BRICK: 1},
    SETTLEMENT = {ResourceType.LUMBER: 2, ResourceType.BRICK: 1, ResourceType.WHEAT: 1, ResourceType.SHEEP: 1},
    CITY = {ResourceType.WHEAT: 2, ResourceType.ORE: 3},
    DEVELOPMENT_CARD = {ResourceType.WHEAT: 1, ResourceType.SHEEP: 1, ResourceType.ORE: 1}

class SettlementType(Enum):
    SETTLEMENT = "Settlement",
    CITY = "City"

class Tile:
    def __init__(self, tile_type: TileType, number_marker: int):
        self.tile_type = tile_type
        self.number_marker = number_marker
        self.has_robber = False

    def __str__(self):
        return f"Tile: {self.tile_type}, Number Marker: {self.number_marker}, Robber: {self.has_robber}"
    
class Intersection:
    def __init__(self, settlement_type: SettlementType, terrains: list[Tile]):
        self.settlement_type = settlement_type
        self.terrains = terrains

class Player:
    def __init__(self, settlements: list[Intersection]):
        self.settlements = settlements

class Catan:
    def __init__(self, map: list[Tile], players: list[Player]):
        self.map = map
        self.players = players
    