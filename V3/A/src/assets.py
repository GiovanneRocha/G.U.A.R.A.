
# -*- coding: utf-8 -*-
import os
import pygame
import settings as S

SFX = {}

def load_assets():
    try:
        pygame.mixer.pre_init(44100, -16, 2, 256)
        pygame.mixer.init()
    except Exception:
        pass
    try:
        def safe(p):
            return pygame.mixer.Sound(p) if os.path.exists(p) else None
        ok = os.path.join(S.SFX_DIR, 'type_ok.wav')
        clean = os.path.join(S.SFX_DIR, 'word_clean.wav')
        boss = os.path.join(S.SFX_DIR, 'boss_hit.wav')
        SFX['ok'] = safe(ok)
        SFX['clean'] = safe(clean)
        SFX['boss'] = safe(boss)
    except Exception:
        pass

def play(name: str):
    s = SFX.get(name)
    if s:
        try:
            s.play()
        except Exception:
            pass
