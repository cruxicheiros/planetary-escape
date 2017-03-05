from random import randint

class AudioSource:
    def __init__(self, pos, tile):
        self.pos = pos
        self.tile = tile

    def ValidatedMove(self, velocity, map):
            move_to = {'tile' : [self.tile.pos[0], self.tile.pos[1]], 'position' : self.pos}

            if velocity[1] < 0:
                if self.pos[1] + velocity[1] >= 0:
                    move_to['position'][1] = self.pos[1] + velocity[1]
                elif self.tile.pos[1] > 0:
                    move_to['position'][1] = (self.tile.height - velocity[1])
                    move_to['tile'][1] = self.tile.pos[1] - 1
                else:
                    print('Could not move to that position')
                    return
                    

            elif velocity[1] > 0:
                if self.pos[1] + velocity[1] <= self.tile.height - 1:
                    move_to['position'][1] = self.pos[1] + velocity[1]
                elif self.tile.pos[1] < map.height - 1:
                    move_to['position'][1] = velocity[1] - 1
                    move_to['tile'][1] = self.tile.pos[1] + 1
                else:
                    print('Could not move to that position')
                    return
            
            if velocity[0] > 0:
                if self.pos[0] + velocity[0] <= self.tile.width - 1:
                    move_to['position'][0] = self.pos[0] + velocity[0]
                elif self.tile.pos[0] < map.width - 1:
                    move_to['position'][0] = velocity[0] - 1
                    move_to['tile'][0] = self.tile.pos[0] + 1
                else:
                    print('Could not move to that position')
                    return

            elif velocity[0] < 0:
                if self.pos[0] + velocity[0] >= 0:
                    move_to['position'][0] = self.pos[0] + velocity[0]
                elif self.tile.pos[0] > 0:
                    move_to['position'][0] = velocity[0] - 1
                    move_to['tile'][0] = self.tile.pos[0] - 1
                else:
                    print('Could not move to that position')
                    return

            for i in map.tiles[(move_to['tile'][0], move_to['tile'][1])].FieldsAtLocation(move_to['position']):
                if i.clipping == True:
                    print('Could not move to that position (clipping)')
                    return
            
            self.pos = move_to['position']
            self.tile = map.tiles[(move_to['tile'][0], move_to['tile'][1])]


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
    
    def behave(self, tick):
        if tick % 20 == 0:
            pass
            
        
        

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
