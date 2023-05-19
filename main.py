import numpy as np
from catan import ResourceType, TileType, BuildingCost, Tile
import matplotlib.pyplot as plt

PLAYERS = 4
class Analyzer:
    def __init__(self):
        self.prob_of_dice_sum = lambda x: {2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6, 8: 5, 9: 4, 10: 3, 11: 2, 12: 1}[x] / 36
        self.prob_of_robber = lambda x: 1 - (5/6)**x

    def calculate_resource_probability(self, tiles: list[Tile]):
        resource_dict = {tile_type: [] for tile_type in TileType}
        prob_dict = {tile_type: 0 for tile_type in TileType}
        for tile in tiles:
            if (tile.has_robber): continue
            for tile_type in TileType:
                if (tile.tile_type == tile_type):
                    resource_dict[tile_type].append(tile)
                    prob_dict[tile_type] += self.prob_of_dice_sum( tile.number_marker)
                    break
        unnormalized = np.array(list(prob_dict.values()))
        normalized = unnormalized / np.sum(unnormalized)
        return dict(zip(list(prob_dict.keys()), normalized))

if __name__ == "__main__":
    analyzer = Analyzer()
    tiles = [Tile(TileType.MOUNTAINS,10), Tile(TileType.MOUNTAINS,12), Tile(TileType.FIELDS,6), Tile(TileType.HILLS,3)]
    resource_distribution = analyzer.calculate_resource_probability(tiles)
    print(resource_distribution)
