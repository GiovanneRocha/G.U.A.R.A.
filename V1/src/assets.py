# -*- coding: utf-8 -*-
import os
import pygame
import settings as S

SFX = {}

def load_assets():
    # Sons opcionais: se não encontrar, segue sem erro
    try:
        beep1_path = os.path.join(S.SFX_DIR, "type_ok.wav")
        beep2_path = os.path.join(S.SFX_DIR, "word_clean.wav")
        if os.path.exists(beep1_path):
            SFX["ok"] = pygame.mixer.Sound(beep1_path)
        if os.path.exists(beep2_path):
            SFX["clean"] = pygame.mixer.Sound(beep2_path)
    except Exception:
        pass

def play(name):
    snd = SFX.get(name)
    if snd:
        try:
            snd.play()
        except Exception:
            pass
