
# -*- coding: utf-8 -*-
import os
import pygame
import settings as S

SFX = {}

def load_assets():
    # Sons opcionais: se não encontrar, segue sem erro
    try:
        beep_ok = os.path.join(S.SFX_DIR, "type_ok.wav")
        beep_clean = os.path.join(S.SFX_DIR, "word_clean.wav")
        beep_boss = os.path.join(S.SFX_DIR, "boss_hit.wav")
        if os.path.exists(beep_ok):
            SFX["ok"] = pygame.mixer.Sound(beep_ok)
        if os.path.exists(beep_clean):
            SFX["clean"] = pygame.mixer.Sound(beep_clean)
        if os.path.exists(beep_boss):
            SFX["boss"] = pygame.mixer.Sound(beep_boss)
    except Exception:
        pass

def play(name):
    snd = SFX.get(name)
    if snd:
        try:
            snd.play()
        except Exception:
            pass
