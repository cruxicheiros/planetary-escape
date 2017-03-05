import os 
import creatures
import VectorMaps
from random import randint, choice
import Audio3D
import json
import pygame

dir_path = os.path.dirname(os.path.realpath(__file__))

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((100, 100))

#A bunch of custom events
change_palette_event = pygame.USEREVENT + 1

#Initalize mixer Channels
ambient_channel = pygame.mixer.Channel(0)
environmental_channel = pygame.mixer.Channel(1)

#Set up mixer channels
ambient_channel.set_volume(0.3)
environmental_channel.set_volume(0.3)


#Sound Palette

with open('palettes.json', 'r') as f: #Dict where data for loading palettes is stored
    palette_dict = json.load(f)
    
class palette:
    def __init__(self, ambient, footsteps, environmental):
        self.ambient = ambient
        self.footsteps = footsteps
        self.environmental = environmental

        
def load_palette(palette_name):
    ambient = pygame.mixer.Sound(dir_path + '\\SFX\\palette\\ambient\\' + palette_dict[palette_name]['AMBIENT'] + '.wav')
    environmental = pygame.mixer.Sound(dir_path + '\\SFX\\palette\\environmental\\' + palette_dict[palette_name]['ENVIRONMENTAL'] + '.wav')
    footsteps = []
    
    footstep_names = os.listdir(dir_path + '\\SFX\\palette\\footsteps\\' + palette_dict[palette_name]['FOOTSTEP'])
    for i in footstep_names:
        footstep = pygame.mixer.Sound(dir_path + '\\SFX\\palette\\footsteps\\' + palette_dict[palette_name]['FOOTSTEP'] + '\\' + i)
        footsteps.append(footstep)
        
    
    new_palette = palette(ambient, footsteps, environmental)
    return new_palette
    
#Map related


def GetFieldsAtLocation(tile, pos):
    fields_at_location = []
    
    for field in tile.fields:
        if pos[0] in range(field.anchor[0], field.anchor[0] + field.dimensions[0]) and pos[1] in range(field.anchor[1], field.anchor[1] + field.dimensions[1]):
            fields_at_location.append(field)
            
    return fields_at_location
            

def LoadMap(fname):
    with open(dir_path + '\\Maps\\' + fname + '.json', 'r') as infile:
        data = json.load(infile)
        infile.close()

    map = VectorMaps.Map(data['CONSTANTS']['MAP_WIDTH'], data['CONSTANTS']['MAP_HEIGHT'], name=data['CONSTANTS']['MAP_NAME'])
    
    for i in data['TILES']:
        coords = i.strip('(').strip(')').split(',')
        key = (int(coords[0]), int(coords[1]))
        map.tiles[key] = VectorMaps.Tile(key, data['CONSTANTS']['TILE_WIDTH'], data['CONSTANTS']['TILE_HEIGHT'])
        
        for j in data['TILES'][i]['FIELDS']:
            map.tiles[key].fields.append(VectorMaps.Field(j['DIMENSIONS'], j['ANCHOR'], clipping=j['CLIPPING'], name=j['NAME']))
            
    
    return map

#### Sound Playback
#Play sounds when events happen
        
def PlayEventSounds(event, current_palette):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
            footstep = choice(current_palette.footsteps)
            footstep.play()
            
    if event.type == change_palette_event:
        
        PlayAmbientSounds(current_palette)
        

def LoadEntitySounds(entities):
    entity_sounds = {}
    for entity in entities:
        if entity not in entity_sounds:
            entity_sounds[entity.name] = []
            front_sound_names = os.listdir(dir_path + '\\SFX\\3d\\entities\\' + entity.name + '\\front')
            back_sound_names = os.listdir(dir_path + '\\SFX\\3d\\entities\\' + entity.name + '\\back')
            
            for i in range(len(front_sound_names) - 1):
                front_sound = Audio3D.MakeAudioSegment('\\3d\\entities\\' + entity.name + '\\front\\' + front_sound_names[i])
                back_sound = Audio3D.MakeAudioSegment('\\3d\\entities\\' + entity.name + '\\back\\' + back_sound_names[i])
                entity_sounds[entity.name].append([front_sound, back_sound])
                
    return entity_sounds
        
#Play looped sounds
def PlayAmbientSounds(current_palette):
    ambient_channel.play(current_palette.ambient, loops = -1)
    environmental_channel.play(current_palette.environmental, loops = - 1)
    
#### Main Loop
        
def MainLoop():    
    map = LoadMap('data')
    avatar = creatures.AudioSource([0,0], map.tiles[(0, 0)])
    current_palette = load_palette('TidalPlainPalette')
    PlayAmbientSounds(current_palette)
    clock = pygame.time.Clock()

    entities = [creatures.Zombie([0, 0], map.tiles[(0, 0)]), creatures.Zombie([3, 3], map.tiles[(3, 3)])]
    entity_sounds = LoadEntitySounds(entities)
        

    while 1:
        clock.tick(30)
        
        for entity in entities:
            if randint(1, 10) > 9:
                absolute_entity_position = ((entity.tile.pos[0]*avatar.tile.width + entity.pos[0]), (entity.tile.pos[1]*avatar.tile.height + entity.pos[1]))
                absolute_avatar_position = ((avatar.tile.pos[0]*avatar.tile.width + avatar.pos[0]), (avatar.tile.pos[1]*avatar.tile.height + avatar.pos[1]))
                
                Audio3D.ConvertToPygame(Audio3D.ProcessAudioSegment(choice(entity_sounds[entity.name]), absolute_entity_position, absolute_avatar_position)).play()
            
        current_fields = GetFieldsAtLocation(avatar.tile, avatar.pos)
        
        events = pygame.event.get()
        for event in events:
            PlayEventSounds(event, current_palette)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    avatar.ValidatedMove([-1, 0], map)
                        
                if event.key == pygame.K_RIGHT:
                    avatar.ValidatedMove([1, 0], map)
                                        
                if event.key == pygame.K_UP:
                    avatar.ValidatedMove([0, -1], map)
                
                if event.key == pygame.K_DOWN:
                    avatar.ValidatedMove([0, 1], map)
                
                if event.key == pygame.K_p:
                    pygame.quit()
                    
                print(avatar.pos, avatar.tile.pos, map.width, map.height)

                    
                

                    
MainLoop()
