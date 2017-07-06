from random import randint
from math import hypot, fabs, ceil

class AudioSource:
    def __init__(self, pos, tile):
        self.pos = pos
        self.tile = tile

    def ValidatedMove(self, velocity, map):
            new_location = {'tile' : [self.tile.pos[0], self.tile.pos[1]], 'position' : [0, 0]}
            if velocity[1] < 0:
                if self.pos[1] + velocity[1] >= 0:
                    new_location['position'][1] = self.pos[1] + velocity[1]
                elif self.tile.pos[1] > 0:
                    new_location['position'][1] = (self.tile.height + velocity[1])
                    new_location['tile'][1] = self.tile.pos[1] - 1
                else:
                    return False
                    
            elif velocity[1] > 0:
                if self.pos[1] + velocity[1] <= self.tile.height - 1:
                    new_location['position'][1] = self.pos[1] + velocity[1]
                elif self.tile.pos[1] < map.height - 1:
                    new_location['position'][1] = velocity[1] - 1
                    new_location['tile'][1] = self.tile.pos[1] + 1
                else:
                    return False
    
            elif velocity[1] == 0:
                new_location['position'][1] = self.pos[1]
                new_location['tile'][1] = self.tile.pos[1]

            if velocity[0] > 0:
                if self.pos[0] + velocity[0] <= self.tile.width - 1:
                    new_location['position'][0] = self.pos[0] + velocity[0]
                elif self.tile.pos[0] < map.width - 1:
                    new_location['position'][0] = velocity[0] - 1
                    new_location['tile'][0] = self.tile.pos[0] + 1
                else:
                    return False

                
            elif velocity[0] < 0:
                if self.pos[0] + velocity[0] >= 0:
                    new_location['position'][0] = self.pos[0] + velocity[0]
                elif self.tile.pos[0] > 0:
                    new_location['position'][0] = map.width + velocity[0]
                    new_location['tile'][0] = self.tile.pos[0] - 1
                else:
                    return False

            elif velocity[0] == 0:
                new_location['position'][0] = self.pos[0]
                new_location['tile'][0] = self.tile.pos[0]
            
            print(new_location)
            
            for field in map.tiles[(new_location['tile'][0], new_location['tile'][1])].FieldsAtLocation(new_location['position']):
                if field.clipping == False:
                    return False
                    
              
            print('moving')
            self.pos = new_location['position']
            self.tile = map.tiles[(new_location['tile'][0], new_location['tile'][1])]
            return True

    def Move(self, velocity):
        self.pos[0] = self.pos[0] + velocity[0]
        self.pos[1] = self.pos[1] + velocity[1]
        
    def DistanceFrom(self, coords):
        self.xdist = self.pos[0] - coords[0]
        self.ydist = self.pos[1] - coords[1]
        self.hdist = hypot(fabs(xdist), fabs(ydist))
        return self.hdist 
        
        

class NamedSource(AudioSource):
    def __init__(self, pos, tile, name):
        AudioSource.__init__(self, pos, tile)
        self.name = name
            

class Zombie(NamedSource):
    def __init__(self, pos, tile):
        NamedSource.__init__(self, pos, tile, 'zombie')
        self.state = "wander"
        
    def behave(self, target, map):
        if self.state == "wander":
            if self.sense(target):
                self.state = "follow"
                
        elif self.state == "follow":
            absolute_self_position = ((self.tile.pos[0]*self.tile.width + self.pos[0]), (self.tile.pos[1]*self.tile.height + self.pos[1]))
            absolute_target_position = ((target.tile.pos[0]*target.tile.width + target.pos[0]), (target.tile.pos[1]*target.tile.height + target.pos[1]))
            
            xdist = absolute_target_position[0] - absolute_self_position[0]
            ydist = absolute_target_position[1] - absolute_self_position[1]
            hdist = hypot(fabs(xdist), fabs(ydist))
           
            if hdist == 0 and xdist == 0 and ydist == 0:
                self.state = 'kill'
            else:
                velocity = (ceil(xdist/hdist), ceil(ydist/hdist))
                self.ValidatedMove(velocity, map)
            
            if not self.sense(target):
                self.state = "lost"
                
        elif self.state == "lost":
            if self.sense(target):
                self.state = "follow"
            else:
                self.state = "wander"
                
        elif self.state == "kill":
            self.pos = target.pos
            self.tile = target.tile
    
    def sense(self, target):
        hdist = hypot(fabs(self.pos[0] - target.pos[0]), fabs(self.pos[1] - target.pos[1]))

        if hdist > 7:
            return False
        else:
            return True
"""
        
class Monster(Creature):
    def __init__(self, pos, aggression_sfx, sensory_sfx, footstep_sfx):
        Creature.__init__(self, pos)
        self.cries = {'aggression' : aggression_sfx, 'sensory' : sensory_sfx, 'footstep' : footstep_sfx}
        
    def aggress(self, listener_pos):
        sound_name = self.cries['aggression'] + str(randint(1, 3))
        self.MakeNoise(sound_name, listener_pos)
        
    def sense(self, listener_pos):
        sound_name = self.cries['sensory'] + str(randint(1, 3))
        self.MakeNoise(sound_name, listener_pos)
        
    def step(self, listener_pos, velocity):
        self.Move(velocity[0], velocity[1])
        sound_name = self.cries['footstep'] + str(randint(1, 3))
        self.MakeNoise(sound_name, listener_pos)
        
"""
class Player(AudioSource):
    def __init__(self, pos):
        AudioSource.__init__(self, pos)
