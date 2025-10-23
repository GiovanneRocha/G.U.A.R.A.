# -*- coding: utf-8 -*-
import sys
import pygame
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE
import settings as S
import assets
from levels import LEVELS
from typing_core import TypingManager
from utils import draw_text, clamp

class GameState:
    MENU = "menu"
    PLAY = "play"
    VICTORY = "victory"
    DEFEAT = "defeat"

class Game:
    def __init__(self):
        try:
            pygame.mixer.pre_init(44100, -16, 2, 256)
        except Exception:
            pass
        pygame.init()
        pygame.display.set_caption(S.TITLE)
        self.screen = pygame.display.set_mode((S.WIDTH, S.HEIGHT))
        self.clock = pygame.time.Clock()

        # áudio
        try:
            pygame.mixer.init()
        except Exception:
            pass
        assets.load_assets()

        self.state = GameState.MENU
        self.level_index = 0
        self.reset_level()

    def reset_level(self):
        cfg = LEVELS[self.level_index]
        self.manager = TypingManager(cfg.words, speed_factor=cfg.speed_factor)
        self.score = 0
        self.hits = 0
        self.misses = 0
        self.words_cleared = 0
        self.wpm_timer = 0.0
        self.wpm_words = 0
        self.corruption = 25.0  # começa com pressão inicial
        self.spawn_t = 0.0
        self.spawn_interval = max(S.MIN_SPAWN_INTERVAL, S.BASE_SPAWN_INTERVAL / cfg.spawn_factor)
        self.running = True

    def handle_events(self):
        for ev in pygame.event.get():
            if ev.type == QUIT:
                pygame.quit()
                sys.exit(0)
            if ev.type == KEYDOWN:
                if ev.key == K_ESCAPE:
                    if self.state == GameState.PLAY:
                        # pausa simples: volta pro menu
                        self.state = GameState.MENU
                    else:
                        pygame.quit()
                        sys.exit(0)
                elif self.state == GameState.MENU:
                    # qualquer tecla inicia a fase 1
                    self.level_index = 0
                    self.reset_level()
                    self.state = GameState.PLAY
                elif self.state in (GameState.VICTORY, GameState.DEFEAT):
                    self.state = GameState.MENU
                elif self.state == GameState.PLAY:
                    ch = ev.unicode.lower()
                    if ch and ch.isprintable() and len(ch) == 1 and ch.isalnum():
                        ok, cleared = self.manager.handle_char(ch)
                        if ok:
                            self.hits += 1
                            assets.play("ok")
                            if cleared:
                                self.words_cleared += 1
                                self.score += 10
                                self.wpm_words += 1
                                self.corruption = clamp(self.corruption - S.CLEAN_REWARD_PER_WORD, 0, S.CORRUPTION_MAX)
                                assets.play("clean")
                        else:
                            self.misses += 1
                            self.corruption = clamp(self.corruption + S.CORRUPTION_HIT_WRONG, 0, S.CORRUPTION_MAX)

    def update(self, dt):
        if self.state != GameState.PLAY:
            return
        # corrupção natural
        self.corruption = clamp(self.corruption + S.CORRUPTION_LEAK_PER_SEC * dt, 0, S.CORRUPTION_MAX)

        # spawn
        self.spawn_t += dt
        if self.spawn_t >= self.spawn_interval:
            self.spawn_t = 0.0
            self.manager.spawn_enemy(S.WIDTH)

        # update inimigos
        self.manager.update(dt, S.HEIGHT)

        # vit/derrota
        target = LEVELS[self.level_index].target_score
        if self.score >= target:
            # próxima fase ou vitória final
            if self.level_index < len(LEVELS) - 1:
                self.level_index += 1
                self.reset_level()
            else:
                self.state = GameState.VICTORY
        if self.corruption >= S.CORRUPTION_MAX:
            self.state = GameState.DEFEAT

        # WPM
        self.wpm_timer += dt

    def draw_hud(self):
        # topo
        cfg = LEVELS[self.level_index]
        draw_text(self.screen, f"{cfg.name} | {cfg.ods}", 16, 12, S.FONT_MED, (220, 230, 255))
        draw_text(self.screen, f"Objetivo: {cfg.target_score} pts", 16, 40, S.FONT_SMALL, (190, 200, 230))
        draw_text(self.screen, f"Score: {self.score}", S.WIDTH-200, 12, S.FONT_MED, (255,255,255))
        acc = 0.0 if (self.hits + self.misses) == 0 else (self.hits/(self.hits+self.misses)*100.0)
        draw_text(self.screen, f"Precisao: {acc:0.0f}%", S.WIDTH-200, 40, S.FONT_SMALL, (210,210,220))

        # WPM simples (palavras completadas por minuto)
        wpm = 0.0 if self.wpm_timer < 1e-6 else (self.wpm_words / (self.wpm_timer/60.0))
        draw_text(self.screen, f"WPM: {wpm:0.1f}", S.WIDTH-200, 60, S.FONT_SMALL, (210,210,220))

        # barra corrupção
        pygame.draw.rect(self.screen, (50, 40, 55), (16, 70, 300, 16), border_radius=8)
        w = int(300 * (self.corruption/S.CORRUPTION_MAX))
        col = (240, 110, 110) if self.corruption > 65 else (255, 210, 80) if self.corruption > 35 else (120, 230, 160)
        pygame.draw.rect(self.screen, col, (16, 70, w, 16), border_radius=8)
        draw_text(self.screen, "Corrupção da Rede", 16, 90, S.FONT_SMALL, (200,200,220))

    def draw_menu(self):
        self.screen.fill((18, 16, 24))
        draw_text(self.screen, "G.U.A.R.A. - Guardião Unificado de Ambientes de Rede e Aprendizagem", S.WIDTH//2, 140, 22, (180,220,255), center=True)
        draw_text(self.screen, "GuaráByte: Protocolo ODS", S.WIDTH//2, 190, 42, (120, 230, 180), center=True)
        draw_text(self.screen, "Pressione qualquer tecla para iniciar", S.WIDTH//2, 260, 24, (210,210,230), center=True)
        draw_text(self.screen, "Mecânica: digite as palavras nos 'pacotes corrompidos' para depurar a rede.", S.WIDTH//2, 320, 20, (200,200,220), center=True)
        draw_text(self.screen, "ESC: sair (ou voltar ao menu durante o jogo).", S.WIDTH//2, 360, 18, (160,160,180), center=True)

    def draw_victory(self):
        self.screen.fill((8, 30, 20))
        draw_text(self.screen, "Rede CPS Restaurada!", S.WIDTH//2, 200, 42, (140, 255, 190), center=True)
        draw_text(self.screen, "Parabéns, G.U.A.R.Á.! Missão Cumprida.", S.WIDTH//2, 260, 24, (220, 240, 230), center=True)
        draw_text(self.screen, "Pressione qualquer tecla para voltar ao menu.", S.WIDTH//2, 320, 20, (200,200,220), center=True)

    def draw_defeat(self):
        self.screen.fill((30, 10, 16))
        draw_text(self.screen, "A Anomalia corrompeu a rede...", S.WIDTH//2, 200, 36, (255, 130, 130), center=True)
        draw_text(self.screen, "Tente novamente e proteja o Core do CPS!", S.WIDTH//2, 260, 24, (240, 220, 230), center=True)
        draw_text(self.screen, "Pressione qualquer tecla para voltar ao menu.", S.WIDTH//2, 320, 20, (200,200,220), center=True)

    def run(self):
        while True:
            dt = self.clock.tick(S.FPS) / 1000.0
            self.handle_events()
            if self.state == GameState.PLAY:
                self.update(dt)

            # draw
            if self.state == GameState.MENU:
                self.draw_menu()
            elif self.state == GameState.PLAY:
                self.screen.fill((18, 16, 24))
                # grid/circuitos de fundo simples
                for x in range(0, S.WIDTH, 64):
                    pygame.draw.line(self.screen, (25,25,35), (x,0), (x, S.HEIGHT))
                for y in range(0, S.HEIGHT, 64):
                    pygame.draw.line(self.screen, (25,25,35), (0,y), (S.WIDTH, y))

                self.manager.draw(self.screen)
                self.draw_hud()
            elif self.state == GameState.VICTORY:
                self.draw_victory()
            elif self.state == GameState.DEFEAT:
                self.draw_defeat()

            pygame.display.flip()

if __name__ == "__main__":
    Game().run()
