from random import randint


class AudioSource:
    def __init__(self, pos):
        self.pos = pos
        
    def Move(self, velocity):
        self.pos[0] = self.pos[0] + velocity[0]
        self.pos[1] = self.pos[1] + velocity[1]
        
    def DistanceFrom(self, coords):
        self.xdist = self.pos[0] - coords[0]
        self.ydist = self.pos[1] - coords[1]
        self.hdist = hypot(fabs(xdist), fabs(ydist))
        return self.hdist 
        
class Human(AudioSource):
    def __init__(self, pos):
        AudioSource.__init__(self, pos)
        self.name = name

        
        
class NPC(Human):
    def __init__(self, pos):
        Creature.__init__(self, pos)
        
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
