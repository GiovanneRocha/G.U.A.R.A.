# -*- coding: utf-8 -*-
import sys, os, random
import pygame
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE

# ------------------------------
# Dimensoes e escala (portrait)
# ------------------------------
BASE_W, BASE_H = 540, 960  # base para proporcao mobile 9:16
SCREEN_WIDTH  = 540
SCREEN_HEIGHT = 960
FPS = 60

# ------------------------------
# Cores / UI
# ------------------------------
COLOR_TEXT_DEFAULT = (255, 255, 255)
COLOR_TEXT_TYPING  = (0, 255, 255)
COLOR_TEXT_ERROR   = (255, 80, 80)
COLOR_PLAYER_INPUT = (120, 230, 160)
COLOR_PANEL_BG     = (22, 22, 30)
COLOR_PANEL_ACCENT = (60, 60, 90)

# Temas por fase (bg e grid). Ordem: ODS 4, 9, 10, 11 (Boss)
PHASES = [
    {
        "name": "Servidor Academico",
        "ods":  "ODS 4 - Educacao de Qualidade",
        "bg":   (16, 18, 28),
        "grid": (28, 34, 48),
        "words": [
            "SPAM","FAKE","ERRO404","QUEBRADO","LINK",
            "ENSINAR","LER","CIENCIA","VERDADE","AULA","FATEC"
        ],
        "spawn_factor": 1.0,
        "speed_factor": 1.0,
        "target_score": 120,  # mais inimigos (portrait tem mais altura)
        "boss": False
    },
    {
        "name": "Servidor de Infraestrutura",
        "ods":  "ODS 9 - Industria, Inovacao e Infraestrutura",
        "bg":   (18, 16, 24),
        "grid": (32, 28, 44),
        "words": [
            "BUG","GLITCH","ATRASO","OBSOLETO",
            "INOVAR","CRIAR","FIX","DEPLOY","LOGICA","CLEAN"
        ],
        "spawn_factor": 1.1,
        "speed_factor": 1.15,
        "target_score": 150,
        "boss": False
    },
    {
        "name": "Servidor de Acesso",
        "ods":  "ODS 10 - Reducao das Desigualdades",
        "bg":   (14, 20, 20),
        "grid": (24, 36, 36),
        "words": [
            "PAYWALL","BLOQUEIO","MURO","NEGADO",
            "INCLUIR","ABRIR","ACESSO","TODOS","UNIR","IGUALDADE"
        ],
        "spawn_factor": 1.2,
        "speed_factor": 1.2,
        "target_score": 180,
        "boss": False
    },
    {
        "name": "Core CPS (Boss)",
        "ods":  "ODS 11 - Cidades e Comunidades Sustentaveis",
        "bg":   (20, 14, 18),
        "grid": (40, 24, 34),
        "words": [
            "SHUTDOWN","DELETE","CORRUPT","FUTURO","ENERGIA","LIMPA"
        ],
        "spawn_factor": 0.9,
        "speed_factor": 1.0,
        "target_score": 0,
        "boss": True,
        "boss_words": [
            "RECONSTRUIR","SUSTENTABILIDADE","COLABORACAO",
            "COMUNIDADE","GUARABYTE","PROTOCOLOODS"
        ],
        "boss_hp": 6
    },
]

# Spawn e velocidade
BASE_SPAWN_FRAMES = 90   # portrait mais alto, spawna um pouco mais rapido
MIN_SPAWN_FRAMES  = 24
ENEMY_BASE_SPEED  = (0.7, 1.7)  # px/frame base ~ ajustado para portrait

# Corrupcao
CORRUPCAO_INICIAL = 100
CORRUPCAO_PERDA   = 10

# Sons (via assets/sfx/*)
SFX = {}

def load_sfx():
    try:
        pygame.mixer.init()
    except Exception:
        pass
    try:
        base = os.path.join("assets", "sfx")
        def safe(path):
            return pygame.mixer.Sound(path) if os.path.exists(path) else None
        SFX["ok"]    = safe(os.path.join(base, "type_ok.wav"))
        SFX["clean"] = safe(os.path.join(base, "word_clean.wav"))
        SFX["boss"]  = safe(os.path.join(base, "boss_hit.wav"))
    except Exception:
        pass

def play_sfx(name):
    snd = SFX.get(name)
    if snd:
        try:
            snd.play()
        except Exception:
            pass

# ------ Util ------

def scale():
    return min(SCREEN_WIDTH/BASE_W, SCREEN_HEIGHT/BASE_H)

def draw_grid_background(screen, bg_color, grid_color):
    screen.fill(bg_color)
    w, h = screen.get_size()
    step = int(48 * scale())
    step = max(32, step)
    for x in range(0, w, step):
        pygame.draw.line(screen, grid_color, (x, 0), (x, h))
    for y in range(0, h, step):
        pygame.draw.line(screen, grid_color, (0, y), (w, y))

# ------ Inimigos ------
class WordEnemy:
    def __init__(self, words, speed_factor=1.0):
        self.word = random.choice(words)
        margin = int(24 * scale())
        self.x = random.randint(margin, SCREEN_WIDTH - margin)
        self.y = random.randint(int(-160*scale()), int(-80*scale()))
        base_min, base_max = ENEMY_BASE_SPEED
        spd = random.uniform(base_min, base_max) * speed_factor * scale()
        self.speed = spd
        self.typed_len = 0
        self.cleaned = False

    def update(self):
        self.y += self.speed

    def draw(self, screen, font):
        full = self.word
        # largura do texto com fonte atual
        text_w, text_h = font.size(full)
        pad_x = int(12 * scale())
        pad_y = int(8 * scale())
        rect_w = text_w + pad_x*2
        rect_h = text_h + pad_y*2
        rect_x = int(self.x - rect_w/2)
        rect_y = int(self.y - rect_h/2)
        rect = pygame.Rect(rect_x, rect_y, rect_w, rect_h)

        # pacote
        pygame.draw.rect(screen, (40, 35, 50), rect, border_radius=int(10*scale()))
        # barra de progresso
        total_w = rect_w - pad_x*2
        prog_w = int(total_w * (self.typed_len / max(1, len(self.word))))
        if prog_w > 0:
            bar_rect = pygame.Rect(rect_x + pad_x, rect_y + rect_h - int(8*scale()), prog_w, int(6*scale()))
            pygame.draw.rect(screen, (80, 220, 140), bar_rect, border_radius=int(4*scale()))
        # texto centralizado
        done = font.render(full[:self.typed_len], True, (120, 255, 160))
        todo = font.render(full[self.typed_len:], True, COLOR_TEXT_DEFAULT)
        tx = rect_x + pad_x + (total_w - (done.get_width()+todo.get_width()))//2
        ty = rect_y + pad_y
        screen.blit(done, (tx, ty))
        screen.blit(todo, (tx + done.get_width(), ty))

    def starts_with(self, prefix: str) -> bool:
        return self.word.startswith(prefix)

    def consume_char(self, ch: str) -> bool:
        if self.typed_len < len(self.word) and ch == self.word[self.typed_len]:
            self.typed_len += 1
            return True
        return False

    def is_completed(self) -> bool:
        return self.typed_len >= len(self.word)

    def is_off_screen(self) -> bool:
        return self.y - int(20*scale()) > SCREEN_HEIGHT

# ------ Boss ------
class Boss:
    def __init__(self, boss_words: list[str], hp: int):
        words = list(boss_words)
        random.shuffle(words)
        self.queue = words
        self.hp = hp
        self.current = self.queue.pop(0) if self.queue else ""
        self.matched = 0
        self.spawn_timer = 0
        self.spawn_interval_frames = int(1.8 * FPS)  # minion ~1.8s
        self.defeated = False

    def handle_char(self, ch: str) -> tuple[bool, bool]:
        if self.defeated or not self.current:
            return (False, False)
        if self.matched < len(self.current) and ch == self.current[self.matched]:
            self.matched += 1
            if self.matched == len(self.current):
                self.hp -= 1
                play_sfx("boss")
                if self.hp <= 0:
                    self.defeated = True
                else:
                    self.current = self.queue.pop(0) if self.queue else ""
                    self.matched = 0
                return (True, True)
            return (True, False)
        return (False, False)

    def tick_spawn(self):
        self.spawn_timer += 1

    def should_spawn_minion(self) -> bool:
        return (not self.defeated) and (self.spawn_timer >= self.spawn_interval_frames)

    def reset_spawn(self):
        self.spawn_timer = 0

# ------ Helpers pedidas ------

def destroy_all_enemies_with_word(enemies, word):
    removed = 0
    for e in list(enemies):
        if e.word == word:
            enemies.remove(e)
            removed += 1
    return removed


def choose_enemy_by_prefix(enemies, prefix):
    candidates = [e for e in enemies if e.starts_with(prefix)]
    if not candidates:
        return None
    candidates.sort(key=lambda e: e.y, reverse=True)  # prioriza mais baixo
    return candidates[0]

# ------ Autoplay para demo ------
class AutoPlayer:
    def __init__(self, cps=7):
        self.cooldown = 0.0
        self.cps = cps

    def step(self, dt, boss, enemies, target_enemy):
        self.cooldown -= dt
        if self.cooldown > 0:
            return None
        self.cooldown = 1.0 / max(1.0, self.cps)
        # Prioriza inimigo mais baixo; senao boss
        if enemies:
            if target_enemy:
                idx = target_enemy.typed_len
                if idx < len(target_enemy.word):
                    return target_enemy.word[idx]
            e = max(enemies, key=lambda x: x.y)
            return e.word[0]
        if boss and not boss.defeated and boss.current:
            return boss.current[boss.matched] if boss.matched < len(boss.current) else None
        return None

# ------------------------------
# Jogo principal
# ------------------------------

def main():
    pygame.init()
    # Janela vertical fixa (mobile-like)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("GuaraByte: Protocolo ODS — Portrait")
    clock = pygame.time.Clock()

    # Fontes escaladas
    sc = scale()
    def mk_font(px, bold=False):
        try:
            return pygame.font.SysFont("Consolas", max(12, int(px*sc)), bold=bold)
        except Exception:
            f = pygame.font.Font(None, max(12, int(px*sc)))
            return f

    font       = mk_font(26, True)
    player_font= mk_font(30, True)
    small_font = mk_font(16, False)
    boss_font  = mk_font(30, True)

    # SFX
    load_sfx()

    # CLI demo
    record_seconds = None
    autoplay = None
    frames_for_gif = []
    Image = None
    if len(sys.argv) >= 3 and sys.argv[1] == "--record-demo":
        try:
            record_seconds = int(sys.argv[2])
        except Exception:
            record_seconds = 10
        autoplay = AutoPlayer(cps=7)
        try:
            from PIL import Image as PILImage
            Image = PILImage
        except Exception:
            print("Pillow nao encontrado. O GIF nao sera salvo.")
            Image = None

    # Estado
    phase_idx = 0
    enemies = []
    target_enemy = None
    current_input = ""

    score = 0
    corrupcao = CORRUPCAO_INICIAL

    spawn_timer = 0
    spawn_delay = BASE_SPAWN_FRAMES
    game_over = False
    victory = False

    boss = None
    elapsed_demo = 0.0

    def begin_phase(i: int):
        nonlocal enemies, target_enemy, current_input, spawn_timer, spawn_delay, boss
        enemies = []
        target_enemy = None
        current_input = ""
        spawn_timer = 0
        cfg = PHASES[i]
        spawn_delay = max(MIN_SPAWN_FRAMES, int(BASE_SPAWN_FRAMES / max(0.1, cfg["spawn_factor"])))
        if cfg.get("boss", False):
            boss = Boss(cfg["boss_words"], cfg["boss_hp"])
        else:
            boss = None

    begin_phase(phase_idx)

    # UI helpers
    input_y = SCREEN_HEIGHT - int(60*sc)

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                    continue
                if game_over or victory:
                    continue

                if autoplay is None:
                    if event.key == pygame.K_BACKSPACE:
                        current_input = current_input[:-1]
                        if not current_input and target_enemy:
                            target_enemy = None
                    elif event.key in (pygame.K_SPACE, pygame.K_RETURN):
                        pass
                    else:
                        ch = event.unicode.upper()
                        if len(ch) == 1 and ch.isalnum():
                            cfg = PHASES[phase_idx]
                            # nova escolha de alvo ao iniciar palavra com boss ativo
                            if (boss and not boss.defeated) and (not current_input) and (target_enemy is None):
                                candidate = choose_enemy_by_prefix(enemies, ch)
                                if candidate:
                                    target_enemy = candidate
                                    current_input = ch
                                else:
                                    ok_b, _ = boss.handle_char(ch)
                                    if ok_b: play_sfx("ok")
                                    current_input += ch
                            else:
                                # fluxo normal
                                if boss and not boss.defeated and target_enemy is None:
                                    ok_b, _ = boss.handle_char(ch)
                                    if ok_b: play_sfx("ok")
                                    current_input += ch
                                else:
                                    current_input += ch

        # targeting por prefixo (quando estamos caçando minions)
        if not game_over and not victory:
            cfg = PHASES[phase_idx]
            if (not (boss and not boss.defeated)) or (target_enemy is not None):
                if not target_enemy and current_input:
                    target_enemy = choose_enemy_by_prefix(enemies, current_input)
                if target_enemy and current_input:
                    if not target_enemy.starts_with(current_input):
                        current_input = ""
                        target_enemy.typed_len = 0
                        target_enemy = None
                    else:
                        if current_input == target_enemy.word:
                            word = target_enemy.word
                            removed = destroy_all_enemies_with_word(enemies, word)
                            target_enemy = None
                            current_input = ""
                            if removed > 0:
                                score += 10 * removed
                                play_sfx("clean")

        # Atualizacoes
        if not (game_over or victory):
            cfg = PHASES[phase_idx]
            spawn_timer += 1
            if boss and not boss.defeated:
                boss.tick_spawn()
                if boss.should_spawn_minion():
                    enemies.append(WordEnemy(cfg["words"], speed_factor=cfg["speed_factor"]))
                    boss.reset_spawn()
            else:
                if spawn_timer >= spawn_delay:
                    enemies.append(WordEnemy(cfg["words"], speed_factor=cfg["speed_factor"]))
                    spawn_timer = 0
                    if spawn_delay > MIN_SPAWN_FRAMES:
                        spawn_delay = max(MIN_SPAWN_FRAMES, int(spawn_delay * 0.99))

            if autoplay is not None:
                ch = autoplay.step(dt, boss, enemies, target_enemy)
                if ch:
                    if (boss and not boss.defeated) and (not current_input) and (target_enemy is None):
                        candidate = choose_enemy_by_prefix(enemies, ch)
                        if candidate:
                            target_enemy = candidate
                            current_input = ch
                        else:
                            ok_b, _ = boss.handle_char(ch)
                            if ok_b: play_sfx("ok")
                            current_input += ch
                    else:
                        if target_enemy:
                            if target_enemy.consume_char(ch):
                                play_sfx("ok")
                                if target_enemy.is_completed():
                                    word = target_enemy.word
                                    removed = destroy_all_enemies_with_word(enemies, word)
                                    target_enemy = None
                                    score += 10 * removed
                                    play_sfx("clean")
                            else:
                                current_input = ""
                                target_enemy.typed_len = 0
                                target_enemy = None
                        else:
                            candidate = choose_enemy_by_prefix(enemies, ch)
                            if candidate:
                                target_enemy = candidate
                                current_input = ch
                            elif boss and not boss.defeated:
                                ok_b, _ = boss.handle_char(ch)
                                if ok_b: play_sfx("ok")
                                current_input += ch

            # mover inimigos e checar saida
            for e in list(enemies):
                e.update()
                if e.is_off_screen():
                    enemies.remove(e)
                    corrupcao -= CORRUPCAO_PERDA
                    if e == target_enemy:
                        target_enemy = None
                        current_input = ""

            if corrupcao <= 0:
                game_over = True

            if not cfg.get("boss", False):
                if score >= cfg["target_score"]:
                    phase_idx += 1
                    if phase_idx >= len(PHASES):
                        victory = True
                    else:
                        begin_phase(phase_idx)
            else:
                if boss and boss.defeated:
                    phase_idx += 1
                    victory = phase_idx >= len(PHASES)

        # --------- Desenho ---------
        cfg = PHASES[min(phase_idx, len(PHASES)-1)]
        draw_grid_background(screen, cfg["bg"], cfg["grid"])

        # Inimigos
        for e in enemies:
            e.draw(screen, font)

        # Painel topo (HUD) em portrait
        pad = int(10*sc)
        hud_h = int(88*sc)
        pygame.draw.rect(screen, COLOR_PANEL_BG, (0, 0, SCREEN_WIDTH, hud_h))
        title = f"{cfg['name']}"
        subtitle = f"{cfg['ods']}"
        t1 = font.render(title, True, (220, 230, 255))
        t2 = small_font.render(subtitle, True, (190, 200, 230))
        screen.blit(t1, (pad, pad))
        screen.blit(t2, (pad, pad + t1.get_height()+int(4*sc)))

        scr = font.render(f"Score: {score}", True, (255,255,255))
        screen.blit(scr, (SCREEN_WIDTH - scr.get_width() - pad, pad))

        # Barra Corrupcao abaixo do HUD
        bar_w = SCREEN_WIDTH - pad*2
        bar_x = pad
        bar_y = hud_h - int(20*sc)
        pygame.draw.rect(screen, (50, 40, 55), (bar_x, bar_y, bar_w, int(12*sc)), border_radius=int(6*sc))
        wfill = int(bar_w * max(0, min(1, corrupcao/100.0)))
        col = (240, 110, 110) if corrupcao < 35 else (255, 210, 80) if corrupcao < 65 else (120, 230, 160)
        pygame.draw.rect(screen, col, (bar_x, bar_y, wfill, int(12*sc)), border_radius=int(6*sc))

        # Boss UI (banner no topo, abaixo do HUD)
        if boss and not boss.defeated:
            bw = int(SCREEN_WIDTH*0.92)
            bh = int(74*sc)
            bx = (SCREEN_WIDTH - bw)//2
            by = hud_h + int(10*sc)
            pygame.draw.rect(screen, (50, 24, 40), (bx, by, bw, bh), border_radius=int(12*sc))
            hp_txt = small_font.render(f"Boss HP: {boss.hp}", True, (255, 190, 210))
            screen.blit(hp_txt, (bx + int(12*sc), by + int(8*sc)))
            w = boss.current
            done = boss_font.render(w[:boss.matched], True, (255, 140, 170))
            todo = boss_font.render(w[boss.matched:], True, (250, 230, 240))
            tx = bx + (bw - (done.get_width()+todo.get_width()))//2
            ty = by + bh//2 - done.get_height()//2 + int(6*sc)
            screen.blit(done, (tx, ty))
            screen.blit(todo, (tx + done.get_width(), ty))

        # Instrucoes (fixas em portrait no rodape)
        instr_panel_h = int(56*sc)
        iy = SCREEN_HEIGHT - instr_panel_h
        pygame.draw.rect(screen, COLOR_PANEL_BG, (0, iy, SCREEN_WIDTH, instr_panel_h))
        instr = small_font.render(
            "Digite para depurar • BACKSPACE apaga • ESC sai • Dica: com Boss ativo, inicie nova palavra para mudar o alvo",
            True, (210,210,230)
        )
        ix = (SCREEN_WIDTH - instr.get_width())//2
        screen.blit(instr, (max(8, ix), iy + (instr_panel_h - instr.get_height())//2))

        # Input do jogador (logo acima das instrucoes)
        inp = player_font.render(current_input, True, COLOR_PLAYER_INPUT)
        ir = inp.get_rect(center=(SCREEN_WIDTH//2, input_y))
        screen.blit(inp, ir)

        # Game over / victory
        if game_over:
            over = player_font.render(f"REDE CORROMPIDA! (Depurados: {score})", True, COLOR_TEXT_ERROR)
            rect = over.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            screen.blit(over, rect)
        if victory:
            vic = player_font.render("MISSAO CUMPRIDA! REDE RESTAURADA.", True, (140, 255, 190))
            rect = vic.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            screen.blit(vic, rect)

        pygame.display.flip()

        # GIF demo
        if record_seconds is not None and Image is not None:
            raw = pygame.image.tostring(screen, 'RGB')
            frames_for_gif.append(Image.frombytes('RGB', (SCREEN_WIDTH, SCREEN_HEIGHT), raw))
            elapsed_demo += dt
            if elapsed_demo >= record_seconds:
                os.makedirs("demo", exist_ok=True)
                out = os.path.join("demo", "demo.gif")
                frames = frames_for_gif[::2] if len(frames_for_gif) > 1 else frames_for_gif
                if frames:
                    frames[0].save(out, save_all=True, append_images=frames[1:], duration=int(1000/30), loop=0)
                    print(f"GIF salvo em {out}")
                running = False

    pygame.quit()

if __name__ == "__main__":
    main()
