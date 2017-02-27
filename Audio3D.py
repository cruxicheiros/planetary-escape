from pydub import AudioSegment, effects
from pygame import mixer
from pydub.playback import play
import os
from math import hypot, fabs, asin, sin, degrees
from tempfile import mkstemp
from time import sleep
mixer.init()



def ProcessAudioSegment(sound_name, source_pos, listener_pos):
    xdist = source_pos[0] - listener_pos[0]
    ydist = source_pos[1] - listener_pos[1]
    hdist = hypot(fabs(xdist), fabs(ydist))
    
    if ydist >= 0: #Is the sound in front of the listener or behind?
        sound = MakeAudioSegment(sound_name)
    else:
        sound = MakeAudioSegment(sound_name + "-b")
    
    
    if hdist != 0:
        vol_sound = effects.low_pass_filter(sound - hdist, 10000 / hdist) #Applies a low-pass filter based on distance & adjusts volume
        panned_sound = vol_sound.pan(degrees(asin(xdist / hdist) / 90)) #Pans sound based on the sine law.
        return(panned_sound)
    else:
        return(sound)

def ConvertToPygame(audio_seg): #Converts an AudioSegment object to a Pygame mixer sound object.
    fd, temp_path = mkstemp()    
    file = open(temp_path, 'wb+')
    audio_seg.export(temp_path, "wav")
    file.close()
    os.close(fd)
    mix_obj = mixer.Sound(temp_path)
    os.remove(temp_path)
    return mix_obj

def MakeAudioSegment(filename): #Loads sound for playback
        file_path = os.path.dirname(os.path.abspath(__file__)) + "\\SFX\\" + filename #Locates file
        audio_seg = AudioSegment.from_file(file_path, format="wav") #Opens file, creates audio segment (PyDub wave object)
        print('Loaded ' + filename + '.wav')
        return audio_seg
        


## testing code below this line
"""
for i in [[-1, -1], [0, -1], [1, -1], [1, 0], [1, 1], [0, 1], [-1, 1], [-1, 0], [-1, -1]]:
    ReturnSound('roar-01', i, [0, 0])
    print(i)
    sleep(3)
"""