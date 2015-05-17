# -*- coding: utf-8 -*-
import kivy
from kivy.clock import Clock
from kivy.properties import NumericProperty
from kivy.uix.widget import Widget
from kivy.animation import Animation
import math
from pygame import mixer
from pygame.mixer import Sound
from kivy.properties import ObjectProperty
from kivy.loader import Loader
import ovni
import soundlib
import __main__
kivy.require('1.8.0')


class Tanque (Widget):
    pass


class TanqueMovil (Widget):
    pass



class Base (Widget):
    pass


class Torreta (Widget):
    rotation = NumericProperty(0)
    mixer.init()
    snd = Sound("sounds/shot.ogg")
    snd.set_volume(3)

    def __init__(self, **kwargs):
        super(Torreta, self).__init__(**kwargs)

    def on_touch_down(self, touch):
        y = (touch.y - self.center[1])
        x = (touch.x - self.center[0])
        calc = math.degrees(math.atan2(y, x))
        new_angle = calc if calc > 0 else 360+calc
        self.ids.sc.rotation= new_angle -90
        self.snd.play()


class Radar (Widget):
    rotation = NumericProperty(45)
    def __init__(self, **kwargs):
        super(Radar, self).__init__(**kwargs)
        Clock.schedule_interval(self.update, 1/60.)

    def update(self, *args):
        self.rotation = self.rotation + 3


class Canon (Widget):
    def on_touch_down(self, touch):
        self.parent.pos[0]=touch.x
        self.parent.parent.add_widget(Disparo(pos=self.center))
        soundlib.s['shot'].play()


class Disparo(Widget):
    explosion=ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Disparo, self).__init__(**kwargs)
        self.explosion=Loader.image("images/explosion.png")
        Clock.schedule_interval(self.update, 1/60.)

    def borrar(self, *args):
        if self.parent:
            self.parent.remove_widget(self)

    def update(self, *args):
        self.pos[1] = self.pos[1] + 3
        if self.parent:
            for ch in self.parent.children:
                if self.collide_widget(ch) & isinstance(ch,ovni.Ovni2):
                    Animation.cancel_all(ch)
                    ch.ids.imagen.texture=self.explosion.texture
                    Clock.schedule_once(ch.borrar,0.5)
                    for ch in self.parent.children:
                        if isinstance(ch,__main__.Score):
                            ch.incrementar()
                    self.borrar()
