# -*- coding: utf-8 -*-
import random
import pygame
from dataclasses import dataclass, field
import settings as S
from utils import clamp

@dataclass
class Enemy:
    word: str
    x: float
    y: float
    speed: float
    matched: int = 0
    cleaned: bool = False
    death_timer: float = 0.0
    color: tuple = field(default_factory=lambda: (random.randint(150,255), random.randint(80,200), random.randint(80,200)))

    def rect(self):
        # área aproximada para UI (não colisão física)
        return pygame.Rect(self.x-80, self.y-20, 160, 40)

    def update(self, dt):
        if not self.cleaned:
            self.y += self.speed * dt
        else:
            self.death_timer += dt

    def progress_ratio(self):
        if not self.word:
            return 0.0
        return self.matched / len(self.word)

class TypingManager:
    def __init__(self, level_words, speed_factor=1.0):
        self.enemies: list[Enemy] = []
        self.input_buffer = ""
        self.active_index: int | None = None
        self.level_words = level_words
        self.base_speed = S.ENEMY_BASE_SPEED * speed_factor

    def spawn_enemy(self, width):
        word = random.choice(self.level_words)
        x = random.randint(80, width-80)
        y = -40
        speed = self.base_speed * random.uniform(0.9, 1.2)
        self.enemies.append(Enemy(word=word, x=x, y=y, speed=speed))

    def update(self, dt, height):
        # remove inimigos fora da tela (penalidade leve poderia ser aplicada)
        survived = []
        for e in self.enemies:
            e.update(dt)
            if e.cleaned and e.death_timer > 0.35:
                # animação de limpeza terminou
                continue
            if not e.cleaned and e.y > height + 50:
                # inimigo passou - penalidade poderia ser maior
                continue
            survived.append(e)
        self.enemies = survived

        # ajustar alvo ativo: primeiro o que tiver maior progresso e estiver mais abaixo
        if self.enemies:
            best_idx = None
            best_score = -1
            for i, e in enumerate(self.enemies):
                if e.cleaned:
                    continue
                score = e.progress_ratio()*2.0 + (e.y/height)
                if score > best_score:
                    best_idx = i
                    best_score = score
            self.active_index = best_idx
        else:
            self.active_index = None

    def handle_char(self, ch) -> tuple[bool, bool]:
        """Retorna (acerto, limpou)"""
        if self.active_index is None:
            return (False, False)
        e = self.enemies[self.active_index]
        if e.cleaned:
            return (False, False)
        if e.matched < len(e.word) and ch == e.word[e.matched]:
            e.matched += 1
            if e.matched == len(e.word):
                e.cleaned = True
                return (True, True)
            return (True, False)
        return (False, False)

    def draw(self, screen):
        for idx, e in enumerate(self.enemies):
            # fundo do "pacote"
            bg_col = (30, 20, 35) if idx != self.active_index else (40, 35, 50)
            pygame.draw.rect(screen, bg_col, e.rect(), border_radius=8)

            # barra de progresso (depuração)
            bar_w = int(160 * e.progress_ratio())
            bar_rect = pygame.Rect(e.x-80, e.y+14, bar_w, 6)
            pygame.draw.rect(screen, (80,220,120), bar_rect, border_radius=3)

            # palavra com highlight nas letras corretas
            font = pygame.font.Font(S.FONT_NAME, S.FONT_MED)
            done = font.render(e.word[:e.matched], True, (120, 255, 140))
            todo = font.render(e.word[e.matched:], True, (220, 220, 230))
            surf = pygame.Surface((done.get_width()+todo.get_width(), max(done.get_height(), todo.get_height())), pygame.SRCALPHA)
            surf.blit(done, (0, 0))
            surf.blit(todo, (done.get_width(), 0))

            text_rect = surf.get_rect(center=(e.x, e.y))
            screen.blit(surf, text_rect)

            # efeito de limpeza (halo/cor)
            if e.cleaned:
                aura = pygame.Surface((170, 60), pygame.SRCALPHA)
                pygame.draw.ellipse(aura, (100, 255, 180, 90), aura.get_rect())
                aura_rect = aura.get_rect(center=(e.x, e.y))
                screen.blit(aura, aura_rect)
