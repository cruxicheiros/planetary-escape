import os 
import creatures
import VectorMaps
from random import randint, choice, random
import Audio3D
import json
import pygame

dir_path = os.path.dirname(os.path.realpath(__file__))

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((100, 100))

#A bunch of custom events
change_palette_event = pygame.USEREVENT + 1
crash_event = pygame.USEREVENT + 2
interaction_event = pygame.USEREVENT + 3

#TEMPORARY THUD SOUND
thud_sound = pygame.mixer.Sound(dir_path + '\\SFX\\3d\\interactions\\thud\\thud.wav')

#Initalize mixer Channels
ambient_channel_0 = pygame.mixer.Channel(0)
ambient_channel_1 = pygame.mixer.Channel(1)
avatar_channel = pygame.mixer.Channel(2)

#Set up mixer channels
ambient_channel_0.set_volume(0.3)
ambient_channel_1.set_volume(0.3)


#Sound Palette

with open('palettes.json', 'r') as f: #Dict where data for loading palettes is stored
    palette_dict = json.load(f)
    
class palette:
    def __init__(self, name, ambient, footsteps):
        self.name = name
        self.ambient = ambient
        self.footsteps = footsteps
        
def load_palette(palette_name):
    ambient = [pygame.mixer.Sound(dir_path + '\\SFX\\palette\\ambient\\' + palette_dict[palette_name]['AMBIENT'][0] + '.wav'), pygame.mixer.Sound(dir_path + '\\SFX\\palette\\ambient\\' + palette_dict[palette_name]['AMBIENT'][1] + '.wav')]
    footsteps = []
    
    footstep_names = os.listdir(dir_path + '\\SFX\\palette\\footsteps\\' + palette_dict[palette_name]['FOOTSTEP'])
    for i in footstep_names:
        footstep = pygame.mixer.Sound(dir_path + '\\SFX\\palette\\footsteps\\' + palette_dict[palette_name]['FOOTSTEP'] + '\\' + i)
        footsteps.append(footstep)
    
    
    new_palette = palette(palette_name, ambient, footsteps)
    return new_palette
    
#Map related


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
    if event.type == interaction_event:
        if event.action == 'crash':
            avatar_channel.play(thud_sound)
        elif event.action == 'step':
            footstep = choice(current_palette.footsteps)
            avatar_channel.play(footstep)

    if event.type == change_palette_event:
        PlayAmbientSounds(current_palette)
        

def LoadEntitySounds(entities):
    entity_sounds = {}
    for entity in entities:
        if entity.name not in entity_sounds:
            entity_sounds[entity.name] = []
            sound_names = os.listdir(dir_path + '\\SFX\\3d\\entities\\' + entity.name)
          
            for i in sound_names:
                new_sound = Audio3D.MakeAudioSegment('\\3d\\entities\\' + entity.name + '\\' + i)
                entity_sounds[entity.name].append(new_sound)
                
    return entity_sounds
            
#Play looped sounds
def PlayAmbientSounds(current_palette):
    ambient_channel_0.play(current_palette.ambient[0], loops = -1)
    ambient_channel_1.play(current_palette.ambient[1], loops = -1)


#Populate field with entities
def PopulateFields(map, field_name, spawn_chance):
    entities = []
    
    for key in map.tiles:
        for field in map.tiles[key].fields:
            print(field)
            if field.name == field_name:
                for row in range(field.dimensions[0]):
                    for col in range(field.dimensions[1]):
                        if random() < spawn_chance:
                            entities.append(creatures.Zombie([field.anchor[0] + col, field.anchor[1] + col], map.tiles[key]))
    print(len(entities), 'entities spawned')
    return entities
                            
def check_palette_zone(current_fields):
    new_palette = 'OutsidePalette'
    for field in current_fields:
        if field.name == 'shack':
            new_palette = 'ShedPalette'
        elif field.name == 'ship':
            new_palette = 'ShipPalette'            
            
    return new_palette
    
    
#### Main Loop
        
def MainLoop():    
    map = LoadMap('zombie')
    avatar = creatures.AudioSource([3,14], map.tiles[(0, 3)])
    clock = pygame.time.Clock()
    
    current_palette = load_palette(check_palette_zone(avatar.tile.FieldsAtLocation(avatar.pos)))
    PlayAmbientSounds(current_palette)


    entities = PopulateFields(map, 'zombie_spawn', 0.01)
    entity_sounds = LoadEntitySounds(entities)
    
    
    while 1:
        clock.tick(30)
        
        for entity in entities:
            if random() > 0.95:
                absolute_entity_position = ((entity.tile.pos[0]*avatar.tile.width + entity.pos[0]), (entity.tile.pos[1]*avatar.tile.height + entity.pos[1]))
                absolute_avatar_position = ((avatar.tile.pos[0]*avatar.tile.width + avatar.pos[0]), (avatar.tile.pos[1]*avatar.tile.height + avatar.pos[1]))
                
                Audio3D.ConvertToPygame(Audio3D.ProcessAudioSegment(choice(entity_sounds[entity.name]), absolute_entity_position, absolute_avatar_position)).play()
                
                entity.behave(avatar)
                
        current_fields = avatar.tile.FieldsAtLocation(avatar.pos) 
        

        events = pygame.event.get()
        for event in events:
            PlayEventSounds(event, current_palette)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    failure = avatar.ValidatedMove([-1, 0], map)
                    print(failure)
                    if failure == True:
                        pygame.event.post(pygame.event.Event(interaction_event, action='crash'))                
                    else:
                        pygame.event.post(pygame.event.Event(interaction_event, action='step'))
                if event.key == pygame.K_RIGHT:
                    failure = avatar.ValidatedMove([1, 0], map)
                    if failure == True:
                        pygame.event.post(pygame.event.Event(interaction_event, action='crash'))
                    else:
                        pygame.event.post(pygame.event.Event(interaction_event, action='step'))
                        
                if event.key == pygame.K_UP:
                    failure = avatar.ValidatedMove([0, -1], map)
                    if failure == True:
                        pygame.event.post(pygame.event.Event(interaction_event, action='crash'))
                    else:
                        pygame.event.post(pygame.event.Event(interaction_event, action='step'))
                        
                if event.key == pygame.K_DOWN:
                    failure = avatar.ValidatedMove([0, 1], map)
                    if failure == True:
                        pygame.event.post(pygame.event.Event(interaction_event, action='crash'))
                    else:
                        pygame.event.post(pygame.event.Event(interaction_event, action='step'))
                        
                if event.key == pygame.K_p:
                    pygame.quit()
                                
                if check_palette_zone(current_fields) != current_palette.name:
                    current_palette = load_palette(check_palette_zone(current_fields))
                    PlayAmbientSounds(current_palette)
                    
                print(avatar.pos, avatar.tile.pos, map.width, map.height)
                                    
                    
                

                    
MainLoop()
