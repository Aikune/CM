# -*- coding: utf-8 -*-
import kivy
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.loader import Loader
from kivy.properties import ObjectProperty
import random
import __main__

kivy.require('1.6.0')
class Ovni (Widget):
    explosion=ObjectProperty(None)
    def __init__(self, **kwargs):
        super(Ovni, self).__init__(**kwargs)
        self.explosion=Loader.image("images/explosion.png")
        #print self.tanque_explosion.source
        velocidad=random.choice([2,3.5,5])
        anim=Animation(x=Window.center[0],y=Window.center[1],duration=velocidad)
        anim.start(self)
        anim.bind(on_complete=self.impacto)

    def impacto(self, *args):
        if self.parent:
            for ch in self.parent.children:
                try:
                    #ch.ids.base.ids.img.source="images/explosion.png"
                    ch.ids.base.ids.img.texture=self.explosion.texture
                    ch.remove_widget(ch.ids.radar)
                    ch.remove_widget(ch.ids.torreta)
                    Clock.unschedule(__main__.TanqueApp.lanzar)
                    if isinstance(ch,Ovni):
                        Animation.cancel_all(ch)
                    Clock.schedule_once(__main__.TanqueApp.fin,1)
                except KeyError:
                    pass
            self.borrar()

    def on_touch_down(self,touch):
        if self.collide_point(touch.pos[0],touch.pos[1]):
            Animation.cancel_all(self)
            #self.ids.imagen.source="images/explosion.png"
            self.ids.imagen.texture=self.explosion.texture
            #print self.parent.children
            for ch in self.parent.children:
                #print ch
                if isinstance(ch,__main__.Score):
                    ch.incrementar()
            #main.Score.incrementar()
            Clock.schedule_once(self.borrar,0.5)

    def borrar(self, *args):
        if self.parent:
            self.parent.remove_widget(self)

    #def fin(self, *args):
        #popup = Popup(attach_to=self, title='', size_hint=(0.3, 0.5))
        #go = __main__.GameOver()
        #if self.parent:
            #for ch in self.parent.children:
                    ##print ch
                    #if isinstance(ch,__main__.Score):
                        #punt=ch.puntuacion()
            #go.ids.score_f.text=str(punt)
        #popup.content=go
        #popup.open()

class Ovni2 (Widget):
    explosion=ObjectProperty(None)
    def __init__(self, **kwargs):
        super(Ovni2, self).__init__(**kwargs)
        self.explosion=Loader.image("images/explosion.png")
        velocidad=random.choice([2,3.5,5])
        anim=Animation(x=self.x,y=0,duration=velocidad)
        anim.start(self)
        anim.bind(on_complete=self.impacto)

    def impacto(self, *args):
        if self.parent:
            for ch in self.parent.children:
                try:
                    ch.ids.base.ids.img.texture=self.explosion.texture
                    #ch.ids.base.ids.img.source="images/explosion.png"
                    ch.remove_widget(ch.ids.radar)
                    ch.remove_widget(ch.ids.canon)
                    #Clock.schedule_once(self.fin,2)
                except KeyError:
                    pass
            self.borrar()

    def borrar(self, *args):
        if self.parent:
            self.parent.remove_widget(self)

    def fin(self, *args):
        popup = Popup(title='',
            content=Label(text='Game Over'),
            size_hint=(None, None), size=(200, 100))
        popup.open()