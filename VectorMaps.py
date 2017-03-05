class Field: #Not like a field of a grass; more like an electromagnetic field. Can have multiple properties that activate when you're in it. More than one field can be in the same area.
    def __init__(self, dimensions, anchor, clipping=False, teleport=False, name = 'unnamed field'):
        self.dimensions = dimensions
        self.anchor = anchor #The anchor is the upper left corner of the field.
        
        # Various properties
        self.clipping = clipping # Can you walk through it? If clipping = True, no.
        self.teleport = teleport # Will you be transported to a different map? If teleport = False, no. Not currently implemented
        self.name = name # For human identification

        
class Tile:
    def __init__(self, pos, width, height, name='unnamed tile'):
        self.width = width
        self.height = height
        self.fields = [] #Not an argument to avoid issues with python and mutable default arguments
        self.pos = pos
        self.name = name
        
    def text_display(self):
        for f in self.fields:
            for i in range(self.width):
                row = ''
                
                for j in range(self.height):
                    append = ' -'
                    
                    if j in range(f.anchor[0], f.anchor[0] + f.dimensions[0]) and i in range(f.anchor[1], f.anchor[1] + f.dimensions[1]):
                        append = ' F'
                
                    row = row + append
                print(row)
                    
            print(f.name + ', clipping =', f.clipping, ', teleport =', f.teleport)
            print('\n\n\n')

    def FieldsAtLocation(self, pos):
        fields_at_location = []
    
        for field in self.fields:
            if pos[0] in range(field.anchor[0], field.anchor[0] + field.dimensions[0]) and pos[1] in range(field.anchor[1], field.anchor[1] + field.dimensions[1]):
                fields_at_location.append(field)
            
        return fields_at_location

class Map:
    def __init__(self, width = 4, height = 4, name='unnamed map'):
        self.width = width
        self.height = height
        self.tiles = {}
        self.name = name
                        
    def propagate(self, tile_width=20, tile_height=20):
        for i in range(self.width):
            for j in range(self.height):
                self.tiles[(i, j)] = Tile((i, j), width=tile_width, height=tile_height)
        
    def text_display(self, pos):
        t = self.tiles[(pos[0], pos[1])]
        t.text_display()
                      
                      