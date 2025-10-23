
# -*- coding: utf-8 -*-
import os

# Base portrait reference (mobile-like)
BASE_W, BASE_H = 540, 960  # 9:16
INIT_W, INIT_H = 540, 960  # initial window size
FPS = 60
TITLE = "GuaraByte: Protocolo ODS"

# Colors
COLOR_TEXT_DEFAULT = (255, 255, 255)
COLOR_TEXT_ERROR   = (255, 80, 80)
COLOR_PLAYER_INPUT = (120, 230, 160)
COLOR_PANEL_BG     = (22, 22, 30)

# Gameplay tuning
CORRUPCAO_INICIAL = 100
CORRUPCAO_PERDA   = 10

BASE_SPAWN_FRAMES = 90
MIN_SPAWN_FRAMES  = 24
ENEMY_BASE_VY     = (90.0, 160.0)  # px/s (vertical)
ENEMY_BASE_VX     = (-40.0, 40.0)  # px/s (horizontal) ricochete

# Assets
ASSETS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets')
SFX_DIR    = os.path.join(ASSETS_DIR, 'sfx')
FONTS_DIR  = os.path.join(ASSETS_DIR, 'fonts')
IMAGES_DIR = os.path.join(ASSETS_DIR, 'images')
DEMO_DIR   = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'demo')
