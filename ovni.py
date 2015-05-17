# -*- coding: utf-8 -*-
import kivy
kivy.require('1.8.0')
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.loader import Loader
from kivy.properties import ObjectProperty
import random
import __main__
import tanque
import soundlib

class Ovni (Widget):
    explosion=ObjectProperty(None)
    def __init__(self, **kwargs):
        super(Ovni, self).__init__(**kwargs)
        self.explosion=Loader.image("images/explosion.png")

    def impacto(self, *args):
        if self.parent:
            soundlib.s['explosion'].play()
            for ch in self.parent.children:
                if isinstance (ch,tanque.Tanque):
                    ch.ids.base.ids.img.texture=self.explosion.texture
                    ch.remove_widget(ch.ids.radar)
                    ch.remove_widget(ch.ids.torreta)
                if isinstance (ch,tanque.TanqueMovil):
                    ch.ids.base.ids.img.texture=self.explosion.texture
                    ch.remove_widget(ch.ids.radar)
                    ch.remove_widget(ch.ids.canon)
                if isinstance(ch,Ovni):
                    Animation.cancel_all(ch)
            #Clock.schedule_once(__main__.GameScreen.fin,1)
            Clock.schedule_once(self.parent.parent.fin,1)
            self.borrar()

    def borrar(self, *args):
        if self.parent:
            self.parent.remove_widget(self)


class Ovni1(Ovni):
    def __init__(self, **kwargs):
        super(Ovni1, self).__init__(**kwargs)
        velocidad=random.choice([2,3.5,5])
        anim=Animation(x=Window.center[0],y=Window.center[1],duration=velocidad)
        anim.start(self)
        anim.bind(on_complete=self.impacto)

    def on_touch_down(self,touch):
        if self.collide_point(touch.pos[0],touch.pos[1]):
            Animation.cancel_all(self)
            self.ids.imagen.texture=self.explosion.texture
            for ch in self.parent.children:
                if isinstance(ch,__main__.Score):
                    ch.incrementar()
            Clock.schedule_once(self.borrar,0.5)


class Ovni2 (Ovni):
    def __init__(self, **kwargs):
        super(Ovni2, self).__init__(**kwargs)
        velocidad=random.choice([2,3.5,5])
        anim=Animation(x=self.x,y=0,duration=velocidad)
        anim.start(self)
        anim.bind(on_complete=self.impacto)
