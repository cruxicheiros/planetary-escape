from pydub import AudioSegment, effects
from pygame import mixer
from pydub.playback import play
import os
from math import hypot, fabs, asin, sin, degrees, log10
from tempfile import mkstemp
from time import sleep
mixer.init()

SPOKEN_WORD_DB = 70
SPOKEN_WORD_DIST = 1
UNITS_TO_FEET_MULTIPLIER = 2.5


def ProcessAudioSegment(sound, source_pos, listener_pos):
    xdist = source_pos[0] - listener_pos[0]
    ydist = source_pos[1] - listener_pos[1]
    hdist = hypot(fabs(xdist), fabs(ydist))
    
    if ydist < 0: #If the sound is behind the listener, invert it.
        sound = effects.invert_phase(sound) 
        sound = effects.low_pass_filter(sound, 100)
        pass
    
    if hdist != 0: #Calculates adjustments to sound to create the illusion of three dimensions
        vol_sound = sound - 10*(log10((hdist*UNITS_TO_FEET_MULTIPLIER)**2))#Uses the Inverse Square Rule to semi-accurately calculate drop in db 
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
        print('Loaded ' + filename)
        return audio_seg
        
