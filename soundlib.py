# -*- coding: utf-8 -*-
from kivy.core.audio import SoundLoader
from kivy.loader import Loader
s = {}
s['env'] = SoundLoader.load('sounds/environment.ogg')
s['env'].loop = True
s['shot'] = SoundLoader.load('sounds/shot.ogg')
s['click'] = SoundLoader.load('sounds/click.ogg')
s['click2'] = SoundLoader.load('sounds/click2.ogg')
s['menu'] = SoundLoader.load('sounds/menu.ogg')
s['menu2'] = SoundLoader.load('sounds/menu2.ogg')
s['explosion'] = SoundLoader.load('sounds/explosion.ogg')
s['music'] = SoundLoader.load('sounds/music.ogg')
s['music'].loop = True

i = {}
i['explosion'] = Loader.image("images/explosion.png")