
class CellType:
    def __init__(self, name, color, nutrient_level, regions, cluster):
        self.name = name
        self.color = color
        self.nutrient_level = nutrient_level
        self.regions = regions
        self.cluster = cluster
        
        
class Cell(CellType):
    
    def __init__(self, x, y, name, color, nutrient_level, regions, cluster):
        super().__init__(name, color, nutrient_level, regions, cluster)
        self.x = x
        self.y = y
