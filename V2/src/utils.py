
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

def draw_grid_background(screen, bg_color, grid_color):
    screen.fill(bg_color)
    w, h = screen.get_size()
    for x in range(0, w, 64):
        pygame.draw.line(screen, grid_color, (x, 0), (x, h))
    for y in range(0, h, 64):
        pygame.draw.line(screen, grid_color, (0, y), (w, y))
