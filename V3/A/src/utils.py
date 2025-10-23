
# -*- coding: utf-8 -*-
import pygame
import settings as S

def scale_for(screen):
    w, h = screen.get_size()
    return min(w / S.BASE_W, h / S.BASE_H)

def clamp(v, lo, hi):
    return max(lo, min(hi, v))

def draw_grid_background(screen, bg_color, grid_color, sc):
    screen.fill(bg_color)
    w, h = screen.get_size()
    step = int(48 * sc)
    step = max(32, step)
    for x in range(0, w, step):
        pygame.draw.line(screen, grid_color, (x, 0), (x, h))
    for y in range(0, h, step):
        pygame.draw.line(screen, grid_color, (0, y), (w, y))

def make_font(px, sc, bold=False):
    size = max(12, int(px * sc))
    try:
        return pygame.font.SysFont('Consolas', size, bold=bold)
    except Exception:
        return pygame.font.Font(None, size)

def render_fit(text, max_width, base_px, sc, color=(255,255,255), bold=False):
    # Reduce size until fits width
    px = base_px
    while px >= 10:
        font = make_font(px, sc, bold)
        surf = font.render(text, True, color)
        if surf.get_width() <= max_width:
            return surf, font
        px -= 1
    # Fallback tiny
    font = make_font(10, sc, bold)
    return font.render(text, True, color), font
