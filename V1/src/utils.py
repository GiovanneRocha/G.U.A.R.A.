# -*- coding: utf-8 -*-
import pygame
import settings as S

def draw_text(surface, text, x, y, size, color, center=False):
    font = pygame.font.Font(S.FONT_NAME, size)
    surf = font.render(text, True, color)
    rect = surf.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    surface.blit(surf, rect)

def clamp(v, lo, hi):
    return max(lo, min(hi, v))
