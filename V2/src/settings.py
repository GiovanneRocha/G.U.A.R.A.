
# -*- coding: utf-8 -*-
import os

# Tela
WIDTH, HEIGHT = 1024, 600
FPS = 60
TITLE = "GuaraByte: Protocolo ODS"

# HUD / Barra
CORRUPTION_MAX = 100.0
CORRUPTION_HIT_WRONG = 1.5   # penalidade ao errar letra
CORRUPTION_LEAK_PER_SEC = 0.30  # corrupção natural por segundo
CLEAN_REWARD_PER_WORD = 3.0  # redução ao depurar um inimigo

# Inimigos / Spawner
BASE_SPAWN_INTERVAL = 1.8  # s
MIN_SPAWN_INTERVAL  = 0.6  # s
ENEMY_BASE_SPEED    = 60.0 # px/s

# Tipografia
FONT_NAME = None  # usa default do pygame
FONT_BIG = 36
FONT_MED = 24
FONT_SMALL = 18

# Caminhos
ASSETS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")
FONTS_DIR  = os.path.join(ASSETS_DIR, "fonts")
SFX_DIR    = os.path.join(ASSETS_DIR, "sfx")
IMAGES_DIR = os.path.join(ASSETS_DIR, "images")
DEMO_DIR   = os.path.join(os.path.dirname(os.path.dirname(__file__)), "demo")
