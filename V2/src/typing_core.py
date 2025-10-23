
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

class Boss:
    def __init__(self, words: list[str], health: int):
        self.words = list(words)
        random.shuffle(self.words)
        self.health = health
        self.current_word = self.words.pop(0) if self.words else ""
        self.matched = 0
        self.spawn_timer = 0.0
        self.spawn_interval = 2.0
        self.defeated = False

    def handle_char(self, ch) -> tuple[bool, bool]:
        if self.defeated or not self.current_word:
            return (False, False)
        if self.matched < len(self.current_word) and ch == self.current_word[self.matched]:
            self.matched += 1
            if self.matched == len(self.current_word):
                self.health -= 1
                if self.health <= 0:
                    self.defeated = True
                else:
                    self.current_word = self.words.pop(0) if self.words else ""
                    self.matched = 0
                return (True, True)
            return (True, False)
        return (False, False)

class TypingManager:
    def __init__(self, level_words, speed_factor=1.0, boss_words=None, boss_health=0):
        self.enemies: list[Enemy] = []
        self.active_index: int | None = None
        self.level_words = level_words
        self.base_speed = S.ENEMY_BASE_SPEED * speed_factor
        self.boss = Boss(boss_words, boss_health) if boss_words else None

        # Autoplay helpers
        self._auto_cooldown = 0.0
        self._auto_cps = 6.0  # chars per second

    def spawn_enemy(self, width):
        word = random.choice(self.level_words)
        x = random.randint(80, width-80)
        y = -40
        speed = self.base_speed * random.uniform(0.9, 1.2)
        self.enemies.append(Enemy(word=word, x=x, y=y, speed=speed))

    def update(self, dt, height):
        # update enemies
        survived = []
        for e in self.enemies:
            e.update(dt)
            if e.cleaned and e.death_timer > 0.35:
                continue
            if not e.cleaned and e.y > height + 50:
                continue
            survived.append(e)
        self.enemies = survived

        # choose active target: prefer the one with most progress / lower on screen
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

        # boss spawn timer (for minions)
        if self.boss and not self.boss.defeated:
            self.boss.spawn_timer += dt

    def handle_char(self, ch) -> tuple[bool, bool, bool]:
        """Retorna (acerto, limpou_inimigo, acertou_boss)"""
        # Boss tem prioridade
        if self.boss and not self.boss.defeated:
            ok_b, hit = self.boss.handle_char(ch)
            if ok_b:
                return (True, False, True)
        # Senão, inimigo comum
        if self.active_index is None:
            return (False, False, False)
        e = self.enemies[self.active_index]
        if e.cleaned:
            return (False, False, False)
        if e.matched < len(e.word) and ch == e.word[e.matched]:
            e.matched += 1
            if e.matched == len(e.word):
                e.cleaned = True
                return (True, True, False)
            return (True, False, False)
        return (False, False, False)

    def boss_should_spawn_minion(self) -> bool:
        return bool(self.boss and not self.boss.defeated and self.boss.spawn_timer >= self.boss.spawn_interval)

    def reset_boss_minion_timer(self):
        if self.boss:
            self.boss.spawn_timer = 0.0

    def draw(self, screen):
        # draw enemies
        for idx, e in enumerate(self.enemies):
            bg_col = (30, 20, 35) if idx != self.active_index else (40, 35, 50)
            pygame.draw.rect(screen, bg_col, e.rect(), border_radius=8)
            # progress bar
            bar_w = int(160 * e.progress_ratio())
            bar_rect = pygame.Rect(e.x-80, e.y+14, bar_w, 6)
            pygame.draw.rect(screen, (80,220,120), bar_rect, border_radius=3)
            # text
            font = pygame.font.Font(S.FONT_NAME, S.FONT_MED)
            done = font.render(e.word[:e.matched], True, (120, 255, 140))
            todo = font.render(e.word[e.matched:], True, (220, 220, 230))
            surf = pygame.Surface((done.get_width()+todo.get_width(), max(done.get_height(), todo.get_height())), pygame.SRCALPHA)
            surf.blit(done, (0, 0))
            surf.blit(todo, (done.get_width(), 0))
            text_rect = surf.get_rect(center=(e.x, e.y))
            screen.blit(surf, text_rect)
            # clean halo
            if e.cleaned:
                aura = pygame.Surface((170, 60), pygame.SRCALPHA)
                pygame.draw.ellipse(aura, (100, 255, 180, 90), aura.get_rect())
                aura_rect = aura.get_rect(center=(e.x, e.y))
                screen.blit(aura, aura_rect)

        # draw boss
        if self.boss and not self.boss.defeated:
            # boss banner at top
            bw = 640
            bh = 60
            rect = pygame.Rect((screen.get_width()-bw)//2, 20, bw, bh)
            pygame.draw.rect(screen, (50, 24, 40), rect, border_radius=12)
            # boss health bar
            maxw = bw - 20
            health_ratio = max(0.0, min(1.0, self.boss.health / max(1, self.boss.health)))  # always 1 for bar bg
            # Draw segments equal to initial health? Simpler: show remaining as text
            font_h = pygame.font.Font(S.FONT_NAME, 18)
            txt_h = font_h.render(f"Boss HP: {self.boss.health}", True, (255, 190, 210))
            screen.blit(txt_h, (rect.x + 12, rect.y + 10))
            # boss word big
            font = pygame.font.Font(S.FONT_NAME, 28)
            w = self.boss.current_word
            done = font.render(w[:self.boss.matched], True, (255, 140, 170))
            todo = font.render(w[self.boss.matched:], True, (250, 230, 240))
            surf = pygame.Surface((done.get_width()+todo.get_width(), max(done.get_height(), todo.get_height())), pygame.SRCALPHA)
            surf.blit(done, (0, 0))
            surf.blit(todo, (done.get_width(), 0))
            trect = surf.get_rect(center=(rect.centerx, rect.centery+10))
            screen.blit(surf, trect)

    # Autoplay for demo
    def autoplay_step(self, dt) -> str | None:
        self._auto_cooldown -= dt
        if self._auto_cooldown > 0:
            return None
        self._auto_cooldown = 1.0 / self._auto_cps
        # Prefer boss
        target = None
        matched = 0
        if self.boss and not self.boss.defeated and self.boss.current_word:
            target = self.boss.current_word
            matched = self.boss.matched
        elif self.active_index is not None and 0 <= self.active_index < len(self.enemies):
            e = self.enemies[self.active_index]
            target = e.word
            matched = e.matched
        if target and matched < len(target):
            return target[matched]
        return None
