
# -*- coding: utf-8 -*-
import sys, os, random
import pygame
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE, VIDEORESIZE
import settings as S
from utils import scale_for, draw_grid_background, make_font, render_fit, clamp
from levels import LEVELS
from typing_core import Enemy, Boss
import assets

# Helpers

def destroy_all_enemies_with_word(enemies, word):
    removed = 0
    for e in list(enemies):
        if e.word == word:
            enemies.remove(e)
            removed += 1
    return removed

def choose_enemy_by_prefix(enemies, prefix):
    cand = [e for e in enemies if e.starts_with(prefix)]
    if not cand:
        return None
    cand.sort(key=lambda e: e.y, reverse=True)
    return cand[0]

class GameState:
    MENU = 'menu'
    PLAY = 'play'
    VICTORY = 'victory'
    DEFEAT = 'defeat'

class Game:
    def __init__(self):
        pygame.init()
        flags = pygame.RESIZABLE
        self.screen = pygame.display.set_mode((S.INIT_W, S.INIT_H), flags)
        pygame.display.set_caption(S.TITLE)
        self.clock = pygame.time.Clock()
        assets.load_assets()
        self.state = GameState.MENU
        self.level_index = 0
        self.reset_level()

    def reset_level(self):
        self.enemies: list[Enemy] = []
        self.target_enemy: Enemy | None = None
        self.current_input = ''
        self.score = 0
        self.corrupcao = S.CORRUPCAO_INICIAL
        self.spawn_timer = 0.0
        self.spawn_delay = max(S.MIN_SPAWN_FRAMES, S.BASE_SPAWN_FRAMES / LEVELS[self.level_index].spawn_factor)
        cfg = LEVELS[self.level_index]
        self.boss = Boss(cfg.boss_words, cfg.boss_health) if cfg.has_boss else None

    def spawn_enemy(self, sc):
        cfg = LEVELS[self.level_index]
        screen_w, screen_h = self.screen.get_size()
        wlist = cfg.words
        # velocities scaled
        vy = random.uniform(*S.ENEMY_BASE_VY) * cfg.speed_factor * sc
        vx = random.uniform(*S.ENEMY_BASE_VX) * cfg.speed_factor * sc
        margin = max(24, int(24*sc))
        x = random.randint(margin, screen_w - margin)
        y = random.randint(int(-160*sc), int(-80*sc))
        word = random.choice(wlist)
        self.enemies.append(Enemy(word=word, x=x, y=y, vx=vx, vy=vy))

    def handle_typing(self, ch, sc):
        cfg = LEVELS[self.level_index]
        # start-of-word decision when boss active
        if (self.boss and not self.boss.defeated) and (not self.current_input) and (self.target_enemy is None):
            # try enemy by prefix
            cand = choose_enemy_by_prefix(self.enemies, ch)
            if cand:
                self.target_enemy = cand
                self.current_input = ch
                return
            # else type to boss
            ok_b, done = self.boss.handle_char(ch)
            if ok_b:
                assets.play('ok')
            self.current_input += ch
            return

        # Continue boss typing if no enemy targeted
        if self.boss and not self.boss.defeated and self.target_enemy is None and self.current_input:
            ok_b, done = self.boss.handle_char(ch)
            if ok_b:
                assets.play('ok')
            self.current_input += ch
            return

        # Default: prefix typing for enemies
        self.current_input += ch

    def update(self, dt):
        if self.state != GameState.PLAY:
            return
        sc = scale_for(self.screen)
        cfg = LEVELS[self.level_index]

        # corruption leak is not used; gameplay uses hits/misses
        
        # spawn
        self.spawn_timer += dt * S.FPS  # convert to frames
        if self.boss and not self.boss.defeated:
            self.boss.update(dt)
            if self.boss.should_spawn():
                self.spawn_enemy(sc)
                self.boss.reset_spawn()
        else:
            if self.spawn_timer >= self.spawn_delay:
                self.spawn_timer = 0.0
                self.spawn_enemy(sc)
                if self.spawn_delay > S.MIN_SPAWN_FRAMES:
                    self.spawn_delay = max(S.MIN_SPAWN_FRAMES, self.spawn_delay * 0.99)

        # choose target by prefix when not boss-focused
        if (not (self.boss and not self.boss.defeated)) or (self.target_enemy is not None):
            if not self.target_enemy and self.current_input:
                self.target_enemy = choose_enemy_by_prefix(self.enemies, self.current_input)
            if self.target_enemy and self.current_input:
                if not self.target_enemy.starts_with(self.current_input):
                    self.current_input = ''
                    self.target_enemy.typed_len = 0
                    self.target_enemy = None
                else:
                    if self.current_input == self.target_enemy.word:
                        word = self.target_enemy.word
                        removed = destroy_all_enemies_with_word(self.enemies, word)
                        self.target_enemy = None
                        self.current_input = ''
                        if removed > 0:
                            self.score += 10 * removed
                            assets.play('clean')

        # update enemies + keep inside walls + fall off bottom
        w, h = self.screen.get_size()
        # dynamic fonts for measurement
        font_word = make_font(26, sc, True)
        for e in list(self.enemies):
            e.update(dt, w, sc, font_word)
            if e.y - int(20*sc) > h:
                self.enemies.remove(e)
                self.corrupcao -= S.CORRUPCAO_PERDA
                if e == self.target_enemy:
                    self.target_enemy = None
                    self.current_input = ''

        # check defeat
        if self.corrupcao <= 0:
            self.state = GameState.DEFEAT

        # check progress
        if not cfg.has_boss:
            if self.score >= cfg.target_score:
                if self.level_index < len(LEVELS) - 1:
                    self.level_index += 1
                    self.reset_level()
                else:
                    self.state = GameState.VICTORY
        else:
            if self.boss and self.boss.defeated:
                self.state = GameState.VICTORY

    def draw_hud(self, sc):
        cfg = LEVELS[self.level_index]
        w, h = self.screen.get_size()
        pad = int(10*sc)
        hud_h = int(96*sc)
        pygame.draw.rect(self.screen, S.COLOR_PANEL_BG, (0, 0, w, hud_h))
        # Fit title/subtitle
        title_surf, _ = render_fit(cfg.name, w - pad*2, 28, sc, (220,230,255), True)
        subtitle_surf, _ = render_fit(cfg.ods, w - pad*2, 18, sc, (190,200,230), False)
        self.screen.blit(title_surf, (pad, pad))
        self.screen.blit(subtitle_surf, (pad, pad + title_surf.get_height() + int(4*sc)))
        # Score on right
        score_surf, _ = render_fit(f"Score: {self.score}", w//3, 24, sc, (255,255,255), False)
        self.screen.blit(score_surf, (w - score_surf.get_width() - pad, pad))
        # Corrupcao bar
        bar_w = w - pad*2
        bar_y = hud_h - int(20*sc)
        pygame.draw.rect(self.screen, (50, 40, 55), (pad, bar_y, bar_w, int(12*sc)), border_radius=int(6*sc))
        ratio = clamp(self.corrupcao/100.0, 0, 1)
        fill = int(bar_w * ratio)
        col = (240,110,110) if self.corrupcao < 35 else (255,210,80) if self.corrupcao < 65 else (120,230,160)
        pygame.draw.rect(self.screen, col, (pad, bar_y, fill, int(12*sc)), border_radius=int(6*sc))

        # Boss banner
        if self.boss and not self.boss.defeated:
            bw = int(w*0.92)
            bh = int(80*sc)
            bx = (w - bw)//2
            by = hud_h + int(10*sc)
            pygame.draw.rect(self.screen, (50,24,40), (bx, by, bw, bh), border_radius=int(12*sc))
            hp_surf, _ = render_fit(f"Boss HP: {self.boss.hp}", bw - int(24*sc), 18, sc, (255,190,210), False)
            self.screen.blit(hp_surf, (bx + int(12*sc), by + int(8*sc)))
            # boss word
            done = self.boss.current[:self.boss.matched]
            todo = self.boss.current[self.boss.matched:]
            done_s, done_f = render_fit(done if done else ' ', bw- int(24*sc), 30, sc, (255,140,170), True)
            todo_s, todo_f = render_fit(todo if todo else ' ', bw- int(24*sc), 30, sc, (250,230,240), False)
            # compose side by side
            total_w = done_s.get_width() + todo_s.get_width()
            tx = bx + (bw - total_w)//2
            ty = by + bh//2 - max(done_s.get_height(), todo_s.get_height())//2 + int(8*sc)
            self.screen.blit(done_s, (tx, ty))
            self.screen.blit(todo_s, (tx + done_s.get_width(), ty))

        return hud_h

    def draw_footer(self, sc):
        w, h = self.screen.get_size()
        panel_h = int(64*sc)
        y = h - panel_h
        pygame.draw.rect(self.screen, S.COLOR_PANEL_BG, (0, y, w, panel_h))
        instr = "Digite para depurar • BACKSPACE apaga • ESC sai • Dica: com Boss ativo, inicie nova palavra para mudar o alvo"
        surf, _ = render_fit(instr, w - int(16*sc), 16, sc, (210,210,230), False)
        self.screen.blit(surf, ((w - surf.get_width())//2, y + (panel_h - surf.get_height())//2))
        return y

    def run(self):
        while True:
            dt = self.clock.tick(S.FPS)/1000.0
            for ev in pygame.event.get():
                if ev.type == QUIT:
                    pygame.quit(); sys.exit(0)
                if ev.type == VIDEORESIZE:
                    # Pygame RESIZABLE preserves surface automatically
                    pass
                if ev.type == KEYDOWN:
                    if ev.key == K_ESCAPE:
                        pygame.quit(); sys.exit(0)
                    if self.state == GameState.MENU:
                        self.state = GameState.PLAY
                        self.level_index = 0
                        self.reset_level()
                    elif self.state in (GameState.VICTORY, GameState.DEFEAT):
                        self.state = GameState.MENU
                    elif self.state == GameState.PLAY:
                        ch = ev.unicode.upper()
                        if ch and ch.isalnum() and len(ch)==1:
                            self.handle_typing(ch, scale_for(self.screen))

            if self.state == GameState.PLAY:
                self.update(dt)

            # Draw
            sc = scale_for(self.screen)
            cfg = LEVELS[self.level_index]
            draw_grid_background(self.screen, cfg.bg_color, cfg.grid_color, sc)

            # Enemies
            font_word = make_font(26, sc, True)
            for e in self.enemies:
                # draw word box centered and bar
                full = e.word
                text_w, text_h = font_word.size(full)
                pad_x = int(12*sc); pad_y = int(8*sc)
                rect_w = text_w + pad_x*2
                rect_h = text_h + pad_y*2
                rect_x = int(e.x - rect_w/2)
                rect_y = int(e.y - rect_h/2)
                rect = pygame.Rect(rect_x, rect_y, rect_w, rect_h)
                pygame.draw.rect(self.screen, (40,35,50), rect, border_radius=int(10*sc))
                total_w = rect_w - pad_x*2
                prog_w = int(total_w * (e.typed_len / max(1, len(e.word))))
                if prog_w>0:
                    bar_rect = pygame.Rect(rect_x + pad_x, rect_y + rect_h - int(8*sc), prog_w, int(6*sc))
                    pygame.draw.rect(self.screen, (80,220,140), bar_rect, border_radius=int(4*sc))
                # text
                done_s = font_word.render(full[:e.typed_len], True, (120,255,160))
                todo_s = font_word.render(full[e.typed_len:], True, S.COLOR_TEXT_DEFAULT)
                tx = rect_x + pad_x + (total_w - (done_s.get_width()+todo_s.get_width()))//2
                ty = rect_y + pad_y
                self.screen.blit(done_s, (tx, ty))
                self.screen.blit(todo_s, (tx + done_s.get_width(), ty))

            hud_h = self.draw_hud(sc)
            footer_y = self.draw_footer(sc)

            # Input current text just above footer
            inp_font = make_font(30, sc, True)
            inp = inp_font.render(self.current_input, True, S.COLOR_PLAYER_INPUT)
            self.screen.blit(inp, ( (self.screen.get_width()-inp.get_width())//2, footer_y - int(28*sc)))

            if self.state == GameState.MENU:
                title_s, _ = render_fit("GuaraByte: Protocolo ODS", self.screen.get_width()-40, 34, sc, (120,230,180), True)
                press_s, _ = render_fit("Pressione qualquer tecla para iniciar", self.screen.get_width()-40, 22, sc, (210,210,230), False)
                self.screen.blit(title_s, ((self.screen.get_width()-title_s.get_width())//2, self.screen.get_height()//2 - 40))
                self.screen.blit(press_s, ((self.screen.get_width()-press_s.get_width())//2, self.screen.get_height()//2 + 10))

            if self.state == GameState.DEFEAT:
                over_s, _ = render_fit(f"REDE CORROMPIDA! (Depurados: {self.score})", self.screen.get_width()-40, 28, sc, S.COLOR_TEXT_ERROR, True)
                self.screen.blit(over_s, ((self.screen.get_width()-over_s.get_width())//2, self.screen.get_height()//2))
            if self.state == GameState.VICTORY:
                vic_s, _ = render_fit("MISSAO CUMPRIDA! REDE RESTAURADA.", self.screen.get_width()-40, 28, sc, (140,255,190), True)
                self.screen.blit(vic_s, ((self.screen.get_width()-vic_s.get_width())//2, self.screen.get_height()//2))

            pygame.display.flip()

if __name__ == '__main__':
    Game().run()
