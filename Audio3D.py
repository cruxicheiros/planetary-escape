from pydub import AudioSegment, effects
from pygame import mixer
from pydub.playback import play
import os
from math import hypot, fabs, asin, sin, degrees, log10
from tempfile import mkstemp
from time import sleep
mixer.init()


UNITS_TO_FEET_MULTIPLIER = 2.5 # How long is one step in feet?

def ProcessAudioSegment(sound, source_pos, listener_pos):
    xdist = source_pos[0] - listener_pos[0]
    ydist = source_pos[1] - listener_pos[1]
    hdist = hypot(fabs(xdist), fabs(ydist))
    
    if ydist < 0: #If the sound is behind the listener, invert it in the left speaker.
        sound = sound.from_mono_audiosegments(sound, sound) # Converts mono to stereo first
        sound = effects.invert_phase(sound, channels=(1, 0))    
    
    if hdist != 0: #Calculates adjustments to sound to create the illusion of three dimensions
        vol_sound = sound - 10*(log10((hdist*UNITS_TO_FEET_MULTIPLIER)**2)) #Uses the Inverse Square Rule to semi-accurately calculate drop in db 
        panned_sound = vol_sound.pan(degrees(asin(xdist / hdist) / 90)) #Pans sound based on the sine law.
        return(panned_sound)
    else:
        return(sound)

def ConvertToPygame(audio_seg): #Converts an AudioSegment object to a Pygame mixer sound object.
    mix_obj = mixer.Sound(audio_seg.raw_data)
    return mix_obj

def MakeAudioSegment(filename): #Loads sound for playback
        file_path = os.path.dirname(os.path.abspath(__file__)) + "\\SFX\\" + filename #Locates file
        audio_seg = AudioSegment.from_file(file_path, format="wav") #Opens file, creates audio segment (PyDub wave object)
        print('Loaded ' + filename)
        return audio_seg