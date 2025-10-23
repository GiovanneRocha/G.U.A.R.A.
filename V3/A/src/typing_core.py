
# -*- coding: utf-8 -*-
from dataclasses import dataclass
import random
import pygame
import settings as S
from utils import clamp

@dataclass
class Enemy:
    word: str
    x: float
    y: float
    vx: float
    vy: float
    typed_len: int = 0

    def update(self, dt, screen_w, sc, font):
        # Advance
        self.x += self.vx * dt
        self.y += self.vy * dt

        # Measure current rect width to keep inside
        text_w, text_h = font.size(self.word)
        pad_x = int(12 * sc)
        rect_w = text_w + pad_x*2
        half = rect_w/2
        left = self.x - half
        right = self.x + half
        margin = max(4, int(8*sc))
        # Bounce horizontally at walls
        if left < margin:
            self.x = margin + half
            self.vx = abs(self.vx)
        elif right > (screen_w - margin):
            self.x = screen_w - margin - half
            self.vx = -abs(self.vx)

    def starts_with(self, prefix: str) -> bool:
        return self.word.startswith(prefix)

    def consume_char(self, ch: str) -> bool:
        if self.typed_len < len(self.word) and ch == self.word[self.typed_len]:
            self.typed_len += 1
            return True
        return False

    def is_completed(self) -> bool:
        return self.typed_len >= len(self.word)

class Boss:
    def __init__(self, words: list[str], hp: int):
        ws = list(words)
        random.shuffle(ws)
        self.queue = ws
        self.hp = hp
        self.current = self.queue.pop(0) if self.queue else ''
        self.matched = 0
        self.spawn_timer = 0.0
        self.spawn_interval = 1.8  # seconds
        self.defeated = False

    def handle_char(self, ch: str) -> tuple[bool, bool]:
        if self.defeated or not self.current:
            return (False, False)
        if self.matched < len(self.current) and ch == self.current[self.matched]:
            self.matched += 1
            if self.matched == len(self.current):
                self.hp -= 1
                if self.hp <= 0:
                    self.defeated = True
                else:
                    self.current = self.queue.pop(0) if self.queue else ''
                    self.matched = 0
                return (True, True)
            return (True, False)
        return (False, False)

    def update(self, dt):
        self.spawn_timer += dt

    def should_spawn(self) -> bool:
        return (not self.defeated) and (self.spawn_timer >= self.spawn_interval)

    def reset_spawn(self):
        self.spawn_timer = 0.0
