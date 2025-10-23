
# -*- coding: utf-8 -*-
import os
import pygame
import settings as S

SFX = {}

def load_assets():
    try:
        pygame.mixer.init()
    except Exception:
        pass
    try:
        base = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'sfx')
        def safe(name):
            p = os.path.join(base, name)
            return pygame.mixer.Sound(p) if os.path.exists(p) else None
        SFX['ok']    = safe('type_ok.wav')
        SFX['clean'] = safe('word_clean.wav')
        SFX['boss']  = safe('boss_hit.wav')
    except Exception:
        pass

def play(name):
    snd = SFX.get(name)
    if snd:
        try:
            snd.play()
        except Exception:
            pass
