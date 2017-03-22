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
                    print('Could not move to that position')
                    return False
                    
            elif velocity[1] > 0:
                if self.pos[1] + velocity[1] <= self.tile.height - 1:
                    new_location['position'][1] = self.pos[1] + velocity[1]
                elif self.tile.pos[1] < map.height - 1:
                    new_location['position'][1] = velocity[1] - 1
                    new_location['tile'][1] = self.tile.pos[1] + 1
                else:
                    print('Could not move to that position')
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

                    print(new_location)
                
            elif velocity[0] < 0:
                if self.pos[0] + velocity[0] >= 0:
                    new_location['position'][0] = self.pos[0] + velocity[0]
                elif self.tile.pos[0] > 0:
                    new_location['position'][0] = map.width + velocity[0]
                    new_location['tile'][0] = self.tile.pos[0] - 1
                else:
                    print('Could not move to that position')
                    return False

            elif velocity[0] == 0:
                new_location['position'][0] = self.pos[0]
                new_location['tile'][0] = self.tile.pos[0]
            
            print(new_location)
            
            for field in map.tiles[(new_location['tile'][0], new_location['tile'][1])].FieldsAtLocation(new_location['position']):
                if field.clipping == False:
                    print('Could not move to that position (clipping)')
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
        
class Human(AudioSource):
    def __init__(self, pos, tile):
        AudioSource.__init__(self, pos, tile)
        self.name = name

class Enemy(AudioSource):
    def __init__(self, pos, tile, name):
        AudioSource.__init__(self, pos, tile)
        self.name = name

class Zombie(Enemy):
    def __init__(self, pos, tile):
        Enemy.__init__(self, pos, tile, 'zombie')
        self.state = "wander"
        
    def behave(self, target):
        if self.state == "wander":
            if self.sense(target):
                self.state == "follow"
                
        elif self.state == "follow":
            xdist = self.pos[0] - target.pos[0]
            ydist = self.pos[1] - target.pos[1]
            hdist = hypot(fabs(xdist), fabs(ydist))
            self.ValidatedMove((ceil(xdist/hdist), ceil(ydist/hdist)))
            
            if not self.sense(target):
                self.state = "lost"
                
        elif self.state == "lost":
            if self.sense(target):
                self.state = "follow"
            else:
                self.state = "wander"
    
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
class Player(Human):
    def __init__(self, pos):
        Creature.__init__(self, pos)
