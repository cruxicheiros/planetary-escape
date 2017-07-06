import os 
import creatures
import VectorMaps
from random import randint, choice, uniform
from math import hypot, fabs
import Audio3D
import json
import pygame
import menu_elements

dir_path = os.path.dirname(os.path.realpath(__file__))

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Planetary Escape')

#A bunch of custom events
change_palette_event = pygame.USEREVENT + 1 #Posted when the user crosses between two palette zones. Triggers switching the ambient noises played.
interaction_event = pygame.USEREVENT + 2 #Posted when the user interacts with the arrow keys. Used to trigger thud_sound and footstep sfx.

#Static sound effects
thud_sound = pygame.mixer.Sound(dir_path + '\\SFX\\static\\thud\\thud.wav')
takeoff_sound = pygame.mixer.Sound(dir_path + '\\SFX\\static\\takeoff\\takeoff.wav')
chomp_sound = pygame.mixer.Sound(dir_path + '\\SFX\\static\\chomp\\chomp.wav')
lose_sound = pygame.mixer.Sound(dir_path + '\\SFX\\static\\lose\\lose.wav')
win_sound = pygame.mixer.Sound(dir_path + '\\SFX\\static\\win\\win.wav')

#Initalize mixer Channels
ambient_channel_0 = pygame.mixer.Channel(0)
ambient_channel_1 = pygame.mixer.Channel(1)
avatar_channel = pygame.mixer.Channel(2)
vocal_channel = pygame.mixer.Channel(3)
menu_channel = pygame.mixer.Channel(4)


#Set up mixer channels
ambient_channel_0.set_volume(0.3)
ambient_channel_1.set_volume(0.3)
vocal_channel.set_volume(0.4)
menu_channel.set_volume(0.4)
    
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
    for e in entities:
        if e.name not in entity_sounds:
            entity_sounds[e.name] = []
            sound_names = os.listdir(dir_path + '\\SFX\\3d\\entities\\' + e.name)
          
            for i in sound_names:
                new_sound = Audio3D.MakeAudioSegment('\\3d\\entities\\' + e.name + '\\' + i)
                entity_sounds[e.name].append(new_sound)
                
    return entity_sounds

# Vocals (eg announcements)

def LoadVocalSounds():
    vocals = {}
    sound_names = os.listdir(dir_path + '\\SFX\\3d\\vocals\\')
  
    for i in sound_names:
        new_sound = pygame.mixer.Sound(dir_path + '\\SFX\\3d\\vocals\\' + i)
        vocals[i] = new_sound
        
    return vocals
        
        
#Play looped sounds
def PlayAmbientSounds(current_palette):
    ambient_channel_0.play(current_palette.ambient[0], loops = -1)
    ambient_channel_1.play(current_palette.ambient[1], loops = -1)

def ConvertFromAbsolutePosition(map, absolute_x, absolute_y):
    tile_width = map.tiles[(0, 0)].width # accesses tile (0,0) (Which will ALWAYS exist in a non-malformed map) to get its height and width
    tile_height = map.tiles[(0, 0)].height
    
    tile_location = (absolute_x // tile_width, absolute_y // tile_height)
    sub_location = [absolute_x - (tile_width * tile_location[0]), absolute_y - (tile_height * tile_location[0])]

    return tile_location, sub_location
    

#Populates map with entities
def SpawnZombies(map, quantity):
    entities = []
    
    tile_width = map.tiles[(0, 0)].width # accesses tile (0,0) (Which will ALWAYS exist in a non-malformed map) to get its height and width
    tile_height = map.tiles[(0, 0)].height
    
    while len(entities) != quantity:        
        spawn_tile_pos = (randint(0, map.width - 1), randint(0, map.height - 1))
        spawn_pos = [randint(0, tile_width - 1), randint(0, tile_height - 1)]
        
        spawn_tile = map.tiles[spawn_tile_pos]
        
        valid_position = True
        
        for i in spawn_tile.FieldsAtLocation(spawn_pos):
            if 'ship' in i.name or 'shed' in i.name:
                valid_position == False
                
        for i in entities:
            if spawn_tile == i.tile:
                if spawn_pos == i.pos:
                    valid_position == False
                
                else:
                    hdist = hypot(fabs(i.pos[0] - spawn_pos[0]), fabs(i.pos[1] - spawn_pos[1]))
                    if hdist < 4:
                        valid_position == False
                
        if valid_position:
            entities.append(creatures.Zombie(spawn_pos, spawn_tile))
        
    return entities
                            
def check_palette_zone(current_fields):
    new_palette = 'OutsidePalette'
    for field in current_fields:
        if field.name == 'shed':
            new_palette = 'ShedPalette'
        elif field.name == 'ship':
            new_palette = 'ShipPalette'            
            
    return new_palette
    

def Menu():
    PressedPlay = False
    
    clock = pygame.time.Clock()
    pages = {
            'main' : menu_elements.Page('main', ['instructions', 'play', 'credits', 'exit']),
            'credits' : menu_elements.Page('credits', ['main']),
            'instructions' : menu_elements.Page('instructions', ['main'])
            }
    
    current_page = 'main'
    cursor_pos = 0
    
    menu_channel.play(pages[current_page].audio_heading)

    
    while not PressedPlay:
        events = pygame.event.get()
        screen.blit(pages[current_page].heading.image, (10, 0))
                
        button_count = -1
        
        for i in pages[current_page].buttons:
            button_count += 1
            
            if button_count == cursor_pos:
                i.select()
            else:
                i.deselect()
                
            screen.blit(i.current, (0, pages[current_page].heading.image.get_height() + (80 * button_count)))
            
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if cursor_pos == 0:
                        cursor_pos = len(pages[current_page].buttons) - 1
                    else:
                        cursor_pos -= 1
                        
                    menu_channel.play(pages[current_page].buttons[cursor_pos].audio_label)
                        
                elif event.key == pygame.K_DOWN:
                    if cursor_pos == len(pages[current_page].buttons) - 1:
                        cursor_pos = 0
                    else:
                        cursor_pos += 1
                        
                    menu_channel.play(pages[current_page].buttons[cursor_pos].audio_label)

                elif event.key == pygame.K_RETURN:
                    next_page = pages[current_page].buttons[cursor_pos].name
                    screen.fill((0,0,0))
                    if next_page == 'play':
                        PressedPlay = True
                        return 0
                        
                    if next_page == 'exit':
                        return 1
                    else:
                        current_page = next_page
                        cursor_pos = 0
                    
                        menu_channel.play(pages[current_page].audio_heading)
                    
                        
        
        pygame.display.update()
        clock.tick(30)
    
    
#### Main Loop
        
def MainLoop():
    screen.fill((0,0,0))
    pygame.display.update()
    
    map = LoadMap('zombie')
    avatar = creatures.AudioSource([3,14], map.tiles[(0, 3)])
    clock = pygame.time.Clock()
    
    current_palette = load_palette(check_palette_zone(avatar.tile.FieldsAtLocation(avatar.pos)))
    PlayAmbientSounds(current_palette)


    entities = SpawnZombies(map, 5)
    entities.append(creatures.NamedSource((2, 7), map.tiles[(1, 0)], 'beacon'))
    entity_sounds = LoadEntitySounds(entities)
    
    vocals = LoadVocalSounds()
    
    end_condition_met = False
    
    
    vocal_channel.play(vocals['please_evacuate.wav'])
    
    while not end_condition_met:
        clock.tick(30)
        
        for e in entities:     
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if e.tile.pos == (avatar.tile.pos[0] + i, avatar.tile.pos[1] + j):                       
                        if uniform(0, 1) > 0.50:
                            if e.name == "zombie":
                                e.behave(avatar, map)
                                if e.state == 'kill':                                    
                                    player_alive = False
                                    end_condition_met = True
                                    break
                                
                            absolute_entity_position = ((e.tile.pos[0]*avatar.tile.width + e.pos[0]), (e.tile.pos[1]*avatar.tile.height + e.pos[1]))
                            absolute_avatar_position = ((avatar.tile.pos[0]*avatar.tile.width + avatar.pos[0]), (avatar.tile.pos[1]*avatar.tile.height + avatar.pos[1]))
                            Audio3D.ConvertToPygame(Audio3D.ProcessAudioSegment(choice(entity_sounds[e.name]), absolute_entity_position, absolute_avatar_position)).play()

                                
                                
                        break
                    
        current_fields = avatar.tile.FieldsAtLocation(avatar.pos) 
        

        events = pygame.event.get()
        for event in events:
            PlayEventSounds(event, current_palette)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    success = avatar.ValidatedMove([-1, 0], map)

                    if success == True:
                        pygame.event.post(pygame.event.Event(interaction_event, action='step'))                
                    else:
                        pygame.event.post(pygame.event.Event(interaction_event, action='crash'))
                if event.key == pygame.K_RIGHT:
                    success = avatar.ValidatedMove([1, 0], map)
                    if success == True:
                        pygame.event.post(pygame.event.Event(interaction_event, action='step'))
                    else:
                        pygame.event.post(pygame.event.Event(interaction_event, action='crash'))
                        
                if event.key == pygame.K_UP:
                    success = avatar.ValidatedMove([0, -1], map)
                    if success == True:
                        pygame.event.post(pygame.event.Event(interaction_event, action='step'))
                    else:
                        pygame.event.post(pygame.event.Event(interaction_event, action='crash'))
                        
                if event.key == pygame.K_DOWN:
                    success = avatar.ValidatedMove([0, 1], map)
                    if success == True:
                        pygame.event.post(pygame.event.Event(interaction_event, action='step'))
                    else:
                        pygame.event.post(pygame.event.Event(interaction_event, action='crash'))
                        
                if event.key == pygame.K_p:
                    pygame.quit()
                                
                if check_palette_zone(current_fields) != current_palette.name:
                    current_palette = load_palette(check_palette_zone(current_fields))
                    PlayAmbientSounds(current_palette)
                    
                    for i in current_fields:
                        if i.name == 'ship':
                            player_alive = True
                            end_condition_met = True
                    
                                                        
        if end_condition_met:
            if player_alive:
                vocal_channel.play(win_sound)
                while vocal_channel.get_busy():
                    pygame.event.get()
                vocal_channel.play(takeoff_sound)
                while vocal_channel.get_busy():
                    pygame.event.get()
            else:
                vocal_channel.play(chomp_sound)
                while vocal_channel.get_busy():
                    pygame.event.get()
                
                vocal_channel.play(lose_sound)
                while vocal_channel.get_busy():
                    pygame.event.get()
                    
            ambient_channel_0.stop()
            ambient_channel_1.stop()
      
                    
                    
            

if __name__ == '__main__':
    while True:
        if Menu() == 1:
            break
        else:
            MainLoop()
        
    
