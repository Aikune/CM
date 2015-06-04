# -*- coding: utf-8 -*-
import kivy
kivy.require('1.8.0')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty, NumericProperty
from kivy.uix.screenmanager import ScreenManager, Screen, RiseInTransition
from kivy.clock import Clock
from kivy.core.audio import SoundLoader  # lint:ok
import sys
import random
import tanque
import ovni
import soundlib
import socket
import json


class Principal(ScreenManager):
    app = ObjectProperty(None)


class IntroScreen(Screen):

    def on_touch_down(self, touch):
        soundlib.s['menu'].play()
        self.manager.current = 'Menu'

    def on_leave(self):
        soundlib.s['music'].play()


class MenuScreen(Screen):

    def on_enter(self):
        for item in soundlib.s:
            soundlib.s[item].volume = self.manager.app.config.getint('General', 'Sound') / 100.0

    def exit(self):
        sys.exit(0)

    def jugar(self):
        soundlib.s['menu'].play()
        self.modo = self.manager.app.config.get('GamePlay', 'Modo')
        if self.modo == '1':
            self.manager.current = 'Game1'
        if self.modo == '2':
            self.manager.current = 'Game2'

    def opciones(self):
        soundlib.s['menu'].play()
        self.manager.current = 'Opciones'


class OpcionesScreen(Screen):
    modo = ObjectProperty(None)

    def on_pre_enter(self):
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self, 'text')
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self.ids.volumen.value = self.manager.app.config.getint('General', 'Sound')
        self.ids.dificultad.value = self.manager.app.config.getint('GamePlay', 'Dificultad')
        self.modo = self.manager.app.config.get('GamePlay', 'Modo')
        if self.modo == '1':
            self.ids.modo1.active = True
            self.ids.modo2.active = False
        if self.modo == '2':
            self.ids.modo1.active = False
            self.ids.modo2.active = True

    def check1(self, cb):
        soundlib.s['click'].play()
        if cb.active:
            self.modo = '1'

    def check2(self, cb):
        soundlib.s['click'].play()
        if cb.active:
            self.modo = '2'

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        self.manager.current = 'Menu'
        return True

    def on_pre_leave(self):
        soundlib.s['menu'].play()
        self.manager.app.config.set('General', 'Sound', int(self.ids.volumen.value))
        self.manager.app.config.set('GamePlay', 'Dificultad', int(self.ids.dificultad.value))
        self.manager.app.config.set('GamePlay', 'Modo', self.modo)
        self.manager.app.config.write()


class Cuenta(Widget):
    pass

class GameScreen(Screen):
    num = 0
    score = ObjectProperty(None)
    go = None

    def on_pre_enter(self):
        self.ids.layout.clear_widgets()

    def on_enter(self):
        self.num = self.manager.app.config.getint('GamePlay', 'Dificultad')
        self.go = None
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self, 'text')
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        soundlib.s['env'].play()
        self.score = Score()
        self.ids.layout.add_widget(self.score)

    def borrar_cuenta(self,*args):
        self.ids.layout.remove_widget(self.cu)

    def fin(self, args):
        Clock.unschedule(self.lanzar)
        if (self.go is None):
            self.go = GameOver()
            self.go.ids.score_f.text = str(self.score.score)
            self.go.open()

    def iniciar(self, *args):
        Clock.schedule_interval(self.lanzar, 3)

    def on_pre_leave(self):
        Clock.unschedule(self.lanzar)
        self.ids.layout.clear_widgets()
        soundlib.s['env'].stop()

    def on_leave(self):
        Clock.unschedule(self.lanzar)
        self.ids.layout.clear_widgets()

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        self.manager.current = 'Menu'
        return True

    def velocidad(self):
        n = self.manager.app.config.getint('GamePlay', 'Dificultad')
        if n == 1:
            return random.choice([4, 5, 6])
        if n == 2:
            return random.choice([2, 3.5, 5])
        if n == 3:
            return random.choice([1.5, 2.5, 3.5])


class Game1Screen(GameScreen):

    def on_enter(self):
        super(Game1Screen, self).on_enter()
        self.ids.layout.add_widget(tanque.Tanque(center=(Window.center[0], Window.center[1])))
        self.cu=Cuenta(center=(Window.center[0], Window.center[1]))
        self.ids.layout.add_widget(self.cu)
        self.cu.ids.num.center=(Window.center[0], Window.center[1])
        Clock.schedule_once(self.borrar_cuenta, 2.7)
        self.iniciar()

    def posicion(self, *args):
        x = random.randint(1, Window.height)
        y = random.randint(1, Window.width)
        return random.choice([(x, 0), (x, Window.height), (0, y), (Window.width, y)])

    def lanzar(self, *args):
        for x in range(0, self.num):
            self.ids.layout.add_widget(ovni.Ovni1(pos=self.posicion(), vel=self.velocidad()))
        self.num += 1


class Game2Screen(GameScreen):

    def on_enter(self):
        super(Game2Screen, self).on_enter()
        self.ids.layout.add_widget(tanque.TanqueMovil(pos=(Window.width / 2, 0)))
        self.cu=Cuenta(center=(Window.center[0], Window.center[1]))
        self.ids.layout.add_widget(self.cu)
        self.cu.ids.num.center=(Window.center[0], Window.center[1])
        Clock.schedule_once(self.borrar_cuenta, 2.7)
        self.iniciar()

    def posicion(self, *args):
        return random.randint(1, Window.width), Window.height

    def lanzar(self, *args):
        for x in range(0, self.num):
            self.ids.layout.add_widget(ovni.Ovni2(pos=self.posicion(), vel=self.velocidad()))
        self.num += 1


class GameOver (Popup):

    def __init__(self, **kwargs):
        super(GameOver, self).__init__()
        self.title = "Game Over"
        self.auto_dismiss = False

    def enviar(self, **kwargs):
        for ch in self.parent.children:
            if isinstance(ch, ScreenManager):
                HOST = "localhost"
                PORT = 8888
                BUFFER_SIZE = 1024
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                try:
                    s.connect((HOST, PORT))
                    dictData = {}
                    dictData["usuario"] = self.ids.iniciales.text
                    dictData["puntuacion"] = self.ids.score_f.text
                    dictData["modo"] = ch.app.config.get('GamePlay', 'Modo')
                    msg = json.dumps(dictData)
                    s.send(msg)
                    dataServer = s.recv(BUFFER_SIZE)
                    s.close()
                    listaPuntuaciones = json.loads(dataServer)
                    r = Ranking()
                    for item in listaPuntuaciones:
                        l1 = Puntuacion(text=str(item[0]))
                        l2 = Puntuacion(text=str(item[1]), color=(0.5, 0.5, 1, 1))
                        r.ids.punt.add_widget(l1)
                        r.ids.punt.add_widget(l2)
                    self.title = 'Ranking'
                    self.content = r
                except socket.error, msg:
                    print "No se pudo conectar con el servidor: %s" % msg
                    self.dismiss()
                    for ch in self.parent.children:
                        if isinstance(ch, ScreenManager):
                            ch.current = 'Menu'


class Ranking (Widget):

    def cerrar(self, **kwargs):
        self.parent.parent.parent.dismiss()
        for ch in self.parent.parent.parent.parent.children:
            if isinstance(ch, ScreenManager):
                ch.current = 'Menu'


class Puntuacion(Label):
    pass


class Vacio (Widget):
    pass


class InicialesInput(TextInput):

    max_chars = NumericProperty(3)

    def insert_text(self, substring, from_undo=False):
        if not from_undo and (len(self.text) + len(substring) > self.max_chars):
            return
        super(InicialesInput, self).insert_text(substring.upper(), from_undo)


class Score(Widget):
    score = NumericProperty(0)

    def __init__(self):
        super(Score, self).__init__()
        self.score = 0

    def incrementar(self):
        self.score = self.score + 10

    def puntuacion(self):
        return self.score


class JuegoApp(App):

    def build(self):
        root = Principal(transition=RiseInTransition(), app=self)
        root.add_widget(IntroScreen(name='Intro'))
        root.add_widget(MenuScreen(name='Menu'))
        root.add_widget(OpcionesScreen(name='Opciones'))
        root.add_widget(Game1Screen(name='Game1'))
        root.add_widget(Game2Screen(name='Game2'))
        return root

    def build_config(self, config):
        config.adddefaultsection('General')
        config.setdefault('General', 'Sound', '50')
        config.adddefaultsection('GamePlay')
        config.setdefault('GamePlay', 'Modo', '1')
        config.setdefault('GamePlay', 'Dificultad', '2')


if __name__ == '__main__':
    JuegoApp().run()