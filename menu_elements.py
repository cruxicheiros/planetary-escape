from pygame import image, mixer
import os

class Page:
    def __init__(self, name, buttons):
        path = os.path.dirname(os.path.abspath(__file__))
        self.name = name
        self.heading = Title(name)
        
        self.audio_heading = mixer.Sound(path + '\\menu\\audio_headings\\' + self.name + '.wav')
        
        self.buttons = []
        
        for i in buttons:
            self.buttons.append(Button(i))
        
            
class Title:
    def __init__(self, name):
        self.name = name
        path = os.path.dirname(os.path.abspath(__file__))
        
        self.image = image.load(path + '\\menu\\' + self.name + '-heading.png')

class Button:
    def __init__(self, name):
        path = os.path.dirname(os.path.abspath(__file__))
        
        self.name = name
        
        self.default = image.load(path + '\\menu\\' + self.name + '-default.png')
        self.selected = image.load(path + '\\menu\\' + self.name + '-selected.png')
        
        self.current = self.default
        
        self.audio_label = mixer.Sound(path + '\\menu\\audio_labels\\' + self.name + '.wav')
                
        
    def select(self):
        self.current = self.selected
    
    def deselect(self):
        self.current = self.default
        
