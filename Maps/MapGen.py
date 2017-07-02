import VectorMaps, json, sys
from os import system, path


#Used instead of print() and input() for purposes of accessibility to screenreaders
def dual_print(string):
    system("title "+string)
    print(string + '\n')
    
def dual_input(string):
    system("title "+string)
    return input(string)
    
#Utility functions
    
def get_commands():
    command = dual_input('Please enter a command: ')
    return command
    
def validate_position(position, bound):
    if position not in range(bound):
        return False
    else:
        return True
        
def export(data):
    with open('export.json', 'w') as outfile:
        json.dump(data, outfile)
        outfile.close()
    
#Commands that can be used in tile edit mode

def list_fields(tile): #Lists fields within a tile
    if tile.fields == []:
        dual_print('There are no fields in this tile.')
    else:
        dual_print('There are ' + str(len(tile.fields)) + ' fields. In order of addition: ')
        
        for f in tile.fields:
            dual_print(f.name + ',')
            
            
    return

def create_field(tile):
    field_name = str(dual_input('Enter a name for the new field: '))
    for f in tile.fields:
        if f.name == field_name:
            dual_print('Error: Field named ' + field_name + ' already exists in this tile. Exiting field creation.')
            return
    
    while True:
        try:
            anchor_x = dual_input('Enter the x-position of the field\'s anchor (upper left corner): ')
            anchor_x = int(anchor_x)
        except:
            dual_print('Error: ' + str(anchor_x) + ' is not a number.')
            continue
        else:
            if validate_position(anchor_x, tile.width):
                break
            else:
                dual_print('Error: ' + str(anchor_x) + ' is out of bounds.')
        
    while True:
        try:
            anchor_y = dual_input('Enter the y-position of the field\'s anchor (upper left corner): ')
            anchor_y = int(anchor_y)
        except:
            dual_print('Error: ' + str(anchor_y) + ' is not a number.')
            continue
        else:
            if validate_position(anchor_y, tile.height):
                break
            else:
                dual_print('Error: ' + str(anchor_y) + ' is out of bounds.')
                
    while True:
        try:
            field_width = dual_input('Enter the width of the field: ')
            field_width = int(field_width)
        except:
            dual_print('Error: ' + str(field_width) + ' is not a number.')
            continue
        else:
            if validate_position(field_width + anchor_x, tile.width + 1):
                break
            else:
                dual_print('Error: the edge of the field is out of bounds.')
        
    while True:
        try:
            field_height = dual_input('Enter the height of the field: ')
            field_height = int(field_height)
        except:
            dual_print('Error: ' + str(field_height) + ' is not a number.')
            continue
        else:
            if validate_position(field_height + anchor_y, tile.height + 1):
                break
            else:
                dual_print('Error: the edge of the field is out of bounds. Try shortening it.')
                
    while True:
        field_clips = dual_input('Can entities pass through this field? Y/n: ')
        if field_clips.lower() == 'y':
            field_clips = True
            break
        elif field_clips.lower() == 'n':
            field_clips = False
            break
        else:
            dual_print('Invalid input.')
            
    
    dual_print('Creating field...')
    
    tile.fields.append(VectorMaps.Field([field_width, field_height],[anchor_x, anchor_y], name=field_name, clipping=field_clips))
    dual_print('Done. Returning to tile edit mode.')
    return tile
    
    
def edit_field(tile):
    found = False
    
    field_name = str(dual_input('Enter the name of the field you wish to edit. '))
    for f in tile.fields:
        if f.name == field_name:
            dual_print('Now editing field "' + field_name + '" in tile ' + str(tile.pos) + '.')
            found = True
            active_field_index = tile.fields.index(f)
    
    if not found:
        dual_print('Field "' + field_name + '" was not found. Returning to tile edit mode.')
        return
        
    while 1:
        option = str(dual_input('Enter the name of the variable you want to edit. Options are: \'anchorX\', \'anchorY\', \'width\', \'height\', and \'name\'. To exit, use \'save\' to save changes and exit or \'cancel\' to revert changes and exit: ')).lower().strip()
        if option == 'anchorx':
            dual_print('The anchor\'s current coordinates are ' + str(tile.fields[active_field_index].anchor) + '.')
            try:
                new_x = int(dual_input('Enter the new value for the anchor\'s position on the X axis: '))
            except:
                dual_print('Error: Not a Number')
                continue
            else:
                if validate_position(new_x + tile.fields[active_field_index].dimensions[0], tile.width):
                    tile.fields[active_field_index].anchor[0] = new_x
                    dual_print('Done. The anchor\'s coordinates are now ' + str(tile.fields[active_field_index].anchor) + '.')
                else:
                    dual_print('Error: the edge of the field is now out of bounds. Cancelling action.')
                
        elif option == 'anchory':
            try:
                new_y = int(dual_input('Enter the new value for the anchor\'s position on the Y axis: '))
            except:
                dual_print('Error: Not a Number')
                continue
            else:
                if validate_position(new_y + tile.fields[active_field_index].dimensions[1], tile.height):
                    tile.fields[active_field_index].anchor[1] = new_y
                    dual_print('Done. The anchor\'s coordinates are now ' + str(tile.fields[active_field_index].anchor) + '.')
                else:
                    dual_print('Error: the edge of the field is now out of bounds. Cancelling action.')
                    
        elif option == 'name':
            try:
                new_name = str(dual_input('Enter the new name for the field: '))
            except:
                dual_print('Something went wrong. Please report this error.')
                continue
            else:
                tile.fields[active_field_index].name = new_name
                dual_print('New name has been set.')
                    
                    
        elif option == 'width':
            try:
                new_width = int(dual_input('Enter the new value for the field\'s width: '))
            except:
                dual_print('Error: Not a Number')
                continue
            else:
                if validate_position(new_width + tile.fields[active_field_index].anchor[0], tile.width):
                    tile.fields[active_field_index].dimensions[0] = new_width
                    dual_print('Done. The field\'s dimensions are now' + str(tile.fields[active_field_index].dimensions) + '.')
                else:
                    dual_print('Error: the edge of the field is now out of bounds. Cancelling action.')
                    
        elif option == 'height':
            try:
                new_height = int(dual_input('Enter the new value for the field\'s height: '))
            except:
                dual_print('Error: Not a Number')
                continue
            else:
                if validate_position(new_height + tile.fields[active_field_index].anchor[1], tile.height):
                    tile.fields[active_field_index].dimensions[1] = new_height
                    dual_print('Done. The field\'s dimensions are now' + str(tile.fields[active_field_index].dimensions) + '.')
                else:
                    dual_print('Error: the edge of the field is now out of bounds. Cancelling action.')

        elif option == 'clipping':
            field_clips = dual_input('Can entities pass through this field? Y/n: ')
            if field_clips.lower() == 'y':
                tile.fields[active_field_index].clipping = False
                dual_print('Clipping set to False')
                break
            elif field_clips.lower() == 'n':
                tile.fields[active_field_index].clipping = True
                dual_print('Clipping set to True')
                break
            else:
                dual_print('Invalid input. Cancelling action.')
        
        elif option == 'cancel':
            dual_print('Cancelling all changes. Exiting to tile edit mode.')
            return
            
        elif option == 'save':
            dual_print('Saving all changes. Exiting to tile edit mode. Note that to save to a file you must export.')
            return tile
        
        
    
def delete_field(tile):
    found = False
    
    field_name = str(dual_input('Enter the name of the field you wish to delete. '))
    for f in tile.fields:
        if f.name == field_name:
            dual_print('Deleting field...')
            found = True
            tile.fields.remove(f)
            dual_print('Field deleted. Returning to tile edit mode.')
            return tile
    
    if not found:
        dual_print('Field "' + field_name + '" was not found. Returning to tile edit mode.')
        return
        
def view_field(tile):
    found = False
    
    field_name = str(dual_input('Enter the name of the field you wish to view. '))
    for f in tile.fields:
        if f.name == field_name:
            dual_print('Now viewing field "' + field_name + '" in tile ' + str(tile.pos) + '.')
            dual_print('anchor: ' + str(f.anchor) + '\ndimensions: ' + str(f.dimensions) + '\nclips: ' + str(f.clipping) )
            found = True
            return
    
    if not found:
        dual_print('Field "' + field_name + '" was not found. Returning to tile edit mode.')
        return

def parse_command(command, tile):
    command_dict = {
    'field' : {'list' : list_fields, 'new' : create_field, 'delete' : delete_field, 'edit' : edit_field, 'view' : view_field},
    'goto' : [],
    'help' : ['field', 'goto'],
    'save' : [],
    'exit' : []
    }
    
    
    
    commands = command.split(' ')
    try:
        options = command_dict[commands[0]]
    except:
        dual_print('Error, invalid command.')
    else:
        if commands[0] == 'field':
            try:
                if commands[1] in options:
                    tile = options[commands[1]](tile)
                    return tile
                else:
                    dual_print('Error, invalid argument')
            except:
                dual_print('You need to provide an argument. Try \'list\', \'new\', \'delete\', \'edit\', or \'view\'.')
                #raise
        
        elif commands[0] == 'help':
            try:
                if commands[1] not in options:
                    raise Error
                else:
                    dual_print('Extended help menu is coming soon')
                    dual_print('Valid arguments are \'field\', \'help\', \'goto\', \'save\', \'exit\'.')
            
            except:
                dual_print('Valid commands and arguments are \'field\', \'help\', \'goto\', \'save\', \'exit\'.')            
                #raise
                
        elif commands[0] == 'save':
            return 'save'

        elif commands[0] == 'exit':
            dual_print('Exiting program.')
            sys.exit()
            
        elif commands[0] == 'goto':        
            while 1:
                try:
                    new_x = int(dual_input('Enter the X-position of the tile you wish to view: '))
                except:
                    dual_print('Error: Not a Number.')
                    continue
                else:
                    if validate_position(new_x, map.width):
                        break
                    else:
                        dual_print('Error: That position is out of bounds.')
                        continue
                        
            while 1:
                try:
                    new_y = int(dual_input('Enter the Y-position of the tile you wish to view: '))
                except:
                    dual_print('Error: Not a Number.')
                    continue
                else:
                    if validate_position(new_y, map.height):
                        break
                    else:
                        dual_print('Error: That position is out of bounds.')
                        continue
                    
            return((new_x, new_y))                            
                        
                
                
                
            
            
        
            

def setup():
    while 1:
        try:
            MAP_NAME = str(dual_input('Please name the map: '))
        except:
            print("Invalid name.")
            continue
        else:
            break
            
    while 1:
        try:
            TILE_WIDTH = int(dual_input('What should the width of each tile be?: '))
        except:
            print("Error: Not a Number")
            continue
        else:
            break
            
    while 1:
        try:
            TILE_HEIGHT = int(dual_input('What should the height of each tile be?: '))
        except:
            print("Error: Not a Number")
            continue
        else:
            break
            
    while 1:
        try:
            MAP_WIDTH = int(dual_input('How wide should the map be (in tiles)?: '))
        except:
            print("Error: Not a Number")
            continue
        else:
            break
            
    while 1:
        try:
            MAP_HEIGHT = int(dual_input('How tall should the map be (in tiles)?: '))
        except:
            print("Error: Not a Number")
            continue
        else:
            break
            


    map = VectorMaps.Map(MAP_WIDTH, MAP_HEIGHT, name=MAP_NAME)
    
    dual_print('Map object created. Propagating...')
    map.propagate(tile_width=TILE_WIDTH, tile_height=TILE_HEIGHT)
    dual_print('Done. Now entering tile edit mode.')
    return map

def edit_tile(pos):
    dual_print('Now editing tile' + str(pos) + '. Type \'help\' for a list of commands.')
    while 1:
        command = get_commands()
        parsed_data = parse_command(command, map.tiles[(pos[0], pos[1])])

        if type(parsed_data) == type(map.tiles[(0, 0)]):
            map.tiles[(pos[0], pos[1])] = parsed_data
            
        elif type(parsed_data) == type(()):
            edit_tile(parsed_data)
            break
            
        elif parsed_data == 'exit':
            dual_print('Closing program.')
            sys.exit()
            
        elif parsed_data == 'save':
            dual_print('Saving...')
            data = {'CONSTANTS' : {'MAP_NAME' : map.name, 'MAP_HEIGHT' : map.height, 'MAP_WIDTH' : map.width, 'TILE_HEIGHT' : map.tiles[(0, 0)].height, 'TILE_WIDTH' : map.tiles[(0, 0)].width},
                    'TILES' : {}}
            for key, tile in map.tiles.items():
                json_tile = {'FIELDS' : []}
                for field in tile.fields:
                    json_field = {'NAME' : field.name, 'DIMENSIONS' : field.dimensions, 'ANCHOR' : field.anchor, 'CLIPPING' : field.clipping}
                    json_tile['FIELDS'].append(json_field)
            
                data['TILES'][str(key)] = json_tile
                
            export(data)
            dual_print('Saved!')




if __name__ == '__main__':
    dual_print('Welcome to the VectorMaps Editor.')
    
    while 1:
        choice = str(dual_input('To create a new map, enter \'new\'. To load a map, enter \'load\'. To exit, enter \'exit\'.'))
        if choice == 'new':
            map = setup()
            edit_tile((0,0))
            break
    
        elif choice == 'load':
            fname = str(dual_input('What is the name of the file you want to open?'))
            if path.isfile(fname):
                with open(fname, 'r') as infile:
                    data = json.load(infile)
                    infile.close()

                map = VectorMaps.Map(data['CONSTANTS']['MAP_WIDTH'], data['CONSTANTS']['MAP_HEIGHT'], name=data['CONSTANTS']['MAP_NAME'])
                
                for i in data['TILES']:
                    coords = i.strip('(').strip(')').split(',')
                    key = (int(coords[0]), int(coords[1]))
                    map.tiles[key] = VectorMaps.Tile(key, data['CONSTANTS']['TILE_WIDTH'], data['CONSTANTS']['TILE_HEIGHT'])
                    
                    for j in data['TILES'][i]['FIELDS']:
                        map.tiles[key].fields.append(VectorMaps.Field(j['DIMENSIONS'], j['ANCHOR'], clipping=j['CLIPPING'], name=j['NAME']))
                    
                edit_tile((0,0))
                break
                
        
        elif choice == 'exit':
            dual_print('Exiting program.')
            sys.exit()
            
        else:
            dual_print('Invalid input.')
            continue
        
        
