# -*- coding: utf-8 -*-

import os

# Tela
WIDTH, HEIGHT = 1024, 600
FPS = 60
TITLE = "GuaráByte: Protocolo ODS"

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY  = (30, 30, 40)
GREEN = (80, 220, 120)
RED   = (240, 80, 90)
YELLOW= (255, 210, 80)
BLUE  = (90, 160, 255)
CYAN  = (80, 240, 240)
MAGENTA = (220, 120, 255)

# HUD / Barra
CORRUPTION_MAX = 100.0
CORRUPTION_HIT_WRONG = 1.5   # penalidade ao errar letra
CORRUPTION_LEAK_PER_SEC = 0.3  # corrupção natural por segundo (pressão do vírus)
CLEAN_REWARD_PER_WORD = 3.0  # reducao ao depurar um inimigo

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
