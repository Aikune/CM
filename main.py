# -*- coding: utf-8 -*-
import kivy
kivy.require('1.8.0')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.utils import boundary
from kivy.properties import ObjectProperty, NumericProperty
from pygame import mixer
#from pygame.mixer import Sound
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from kivy.core.audio import SoundLoader
import sys
import random
#import math
import tanque
import main
import ovni

class Opciones(BoxLayout):
    root=ObjectProperty(None)
    volumen = ObjectProperty(None)
    def __init__(self, **kwargs):
        super(Opciones, self).__init__(**kwargs)
        self.volumen.bind(value=self.update_sound_volume)

    def check1(self,cb):
        if cb.active:
            self.root.app.config.set('GamePlay', 'Modo', '1')
    def check2(self,cb):
        if cb.active:
            self.root.app.config.set('GamePlay', 'Modo', '2')
    def dismiss_parent(self):
        self.root.opciones_popup.dismiss()

    def update_sound_volume(self, instance, value):
        # write to app configs
        self.root.app.config.set('General', 'Sound', str(int(value)))
        self.root.app.config.write()
        for item in self.root.app.sound:
            self.root.app.sound[item].volume = value / 100.0

class Menu(Widget):
    opciones_popup=ObjectProperty(None)
    app = ObjectProperty(None)

    def exit(self):
        sys.exit(0)

    def jugar(self):
        App.stop(App.get_running_app())
        self.modo = self.app.config.get('GamePlay', 'Modo')
        if self.modo=='1':
            TanqueApp(app=self.app).run()
        if self.modo=='2':
            Tanque2App(app=self.app).run()

    def opciones(self):
        if self.opciones_popup is None:
            self.opciones_popup = Popup(attach_to=self, title='Opciones', size_hint=(0.3, 0.5))
            self.opciones_popup.content = Opciones(root=self)
            #self.setting_dialog.music_slider.value = boundary(self.app.config.getint('General', 'Music'), 0, 100)
            self.opciones_popup.content.volumen.value = boundary(self.app.config.getint('General', 'Sound'), 0, 100)
            #self.opciones_popup.content.modo_slider.value = boundary(self.app.config.getint('GamePlay', 'Modo'), 1, 2)
        self.opciones_popup.open()

class GameOver (BoxLayout):

    def __init__(self):
        super(GameOver , self).__init__()
        pass

class Score(Widget):
    score=NumericProperty(0)
    def __init__(self):
        super(Score, self).__init__()
        self.score=0
        #self.ids.score.text=str(self.score)

    def incrementar(self):
        self.score=self.score+10
    def puntuacion (self):
        return self.score

class TanqueApp(App):
    app = ObjectProperty(None)
    tanque= ObjectProperty(None)
    score= ObjectProperty(None)
    def build(self):
        mixer.init()
        #snd = Sound("sounds/environment.ogg")
        #snd.set_volume(0.1)
        #snd.play(loops=-1)
        print self.app.sound
        self.app.sound['environment'].play()
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self.root= FloatLayout(size=Window.size)
        self.num=1
        main.TanqueApp.tanque=tanque.Tanque(center=(Window.center[0],Window.center[1]))
        self.root.add_widget(main.TanqueApp.tanque)
        main.TanqueApp.score=Score()
        self.root.add_widget(main.TanqueApp.score)
        self.iniciar()
        return self.root

    #Posicion inicial de los ovnis en cualquiera de los cuatro borders de la pantalla
    def posicion(self,*args):
        x=random.randint(1,Window.height)
        y=random.randint(1,Window.width)
        return random.choice([(x,0),(x,Window.height),(0,y),(Window.width,y)])

    def iniciar(self,*args):
        Clock.schedule_interval(self.lanzar,3)

    def lanzar(self,*args):
        for x in range (0,self.num):
                self.root.add_widget(ovni.Ovni(pos=self.posicion()))
        self.num=self.num+1

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        App.stop(App.get_running_app())
        main.JuegoApp().run()
        return True

    @staticmethod
    def fin(self):
        popup = Popup(title='', size_hint=(0.3, 0.5))
        go = GameOver()
        go.ids.score_f.text=str(main.TanqueApp.score.score)
        popup.content=go
        popup.open()
        popup.content.ids.cerrar_go.bind (on_press=main.TanqueApp.enviar)

    def enviar(self):
        App.stop(App.get_running_app())
        main.JuegoApp().run()
class Tanque2App(App):
    app = ObjectProperty(None)
    #def __init__(self):
        #super(Tanque2App,self).__init__()
        #self.root= FloatLayout(size=Window.size)
        #self.num=1

    def build(self):
        mixer.init()
        #snd = Sound("sounds/environment.ogg")
        #snd.set_volume(0.1)
        #snd.play(loops=-1)
        self.app.sound['environment'].play()
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self.root= FloatLayout(size=Window.size)
        self.num=1
        self.root.add_widget(tanque.TanqueMovil(pos=(Window.width/2,0)))
        self.iniciar()
        return self.root

    #Posicion inicial de los ovnis
    def posicion(self,*args):
        return (random.randint(1,Window.width),Window.height)

    def iniciar(self,*args):
        Clock.schedule_interval(self.lanzar,3)

    def lanzar(self,*args):
        for x in range (0,self.num):
                self.root.add_widget(ovni.Ovni2(pos=self.posicion()))
        self.num=self.num+1

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None
    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        App.stop(App.get_running_app())
        main.JuegoApp().run()
        return True

class JuegoApp(App):

    sound = {}
    def build(self):

        self.sound['environment'] = SoundLoader.load('sounds/environment.ogg')
        self.sound['shot'] = SoundLoader.load('sounds/shot.ogg')
        sound_volume = self.config.getint('General', 'Sound') / 100.0
        for item in self.sound:
            self.sound[item].volume = sound_volume
        return Menu(size=(Window.width,Window.height),app=self)

    def build_config(self, config):
        config.adddefaultsection('General')
        config.setdefault('General', 'Music', '100')
        config.setdefault('General', 'Sound', '100')

        config.adddefaultsection('GamePlay')
        config.setdefault('GamePlay', 'Modo', '1')
        config.setdefault('GamePlay', 'Dificultad', '3')



if __name__=='__main__':
    JuegoApp().run()

