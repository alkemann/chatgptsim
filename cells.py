
class CellType:
    def __init__(self, name, color, regions, cluster):
        self.name = name
        self.color = color
        self.regions = regions
        self.cluster = cluster
        
        
class Cell(CellType):
    
    def __init__(self, x, y, name, color, regions, cluster):
        super().__init__(name, color, regions, cluster)
        self.x = x
        self.y = y
