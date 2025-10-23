# -*- coding: utf-8 -*-
import sys, os, random
import pygame
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE

# --- Configuração de Janela / FPS ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# --- Cores (HUD e temas por fase) ---
COLOR_TEXT_DEFAULT = (255, 255, 255)
COLOR_TEXT_TYPING  = (0, 255, 255)
COLOR_TEXT_ERROR   = (255, 80, 80)
COLOR_PLAYER_INPUT = (120, 230, 160)

# Temas por fase (bg e grid). Ordem: ODS 4, 9, 10, 11 (Boss)
PHASES = [
    {  # Fase 1 – ODS 4: Educação de Qualidade
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
        "target_score": 100,  # 10 pts por palavra => 10 inimigos
        "boss": False
    },
    {  # Fase 2 – ODS 9: Indústria, Inovação e Infraestrutura
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
        "target_score": 120,  # 12 inimigos
        "boss": False
    },
    {  # Fase 3 – ODS 10: Redução das Desigualdades
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
        "target_score": 140,  # 14 inimigos
        "boss": False
    },
    {  # Fase 4 – ODS 11: Cidades e Comunidades Sustentáveis (BOSS)
        "name": "Core CPS (Boss)",
        "ods":  "ODS 11 - Cidades e Comunidades Sustentaveis",
        "bg":   (20, 14, 18),
        "grid": (40, 24, 34),
        "words": [
            # minions
            "SHUTDOWN","DELETE","CORRUPT","FUTURO","ENERGIA","LIMPA"
        ],
        "spawn_factor": 0.9,   # menos minions
        "speed_factor": 1.0,
        "target_score": 0,     # ignorado em boss
        "boss": True,
        "boss_words": [
            "RECONSTRUIR","SUSTENTABILIDADE","COLABORACAO",
            "COMUNIDADE","GUARABYTE","PROTOCOLOODS"
        ],
        "boss_hp": 6           # 1 palavra = -1 HP
    },
]

# Delay base e velocidade base
BASE_SPAWN_FRAMES = 120  # ~2s a 60fps
MIN_SPAWN_FRAMES  = 30   # ~0.5s
ENEMY_BASE_SPEED  = (0.6, 1.6)  # range px/frame (aprox.)

# Corrupcao (segue sua logica original: começa alto e cai ao errar/escapar)
CORRUPCAO_INICIAL = 100  # começa em 100 e diminui quando inimigo passa
CORRUPCAO_PERDA   = 10   # -10% se um inimigo passa da tela

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

# --- Util: fundo em grid por fase ---
def draw_grid_background(screen, bg_color, grid_color):
    screen.fill(bg_color)
    w, h = screen.get_size()
    for x in range(0, w, 64):
        pygame.draw.line(screen, grid_color, (x, 0), (x, h))
    for y in range(0, h, 64):
        pygame.draw.line(screen, grid_color, (0, y), (w, y))

# --- Classe Enemy (inimigo de palavra) ---
class WordEnemy:
    def __init__(self, words, speed_factor=1.0):
        self.word = random.choice(words)
        self.x = random.randint(50, SCREEN_WIDTH - 150)
        self.y = random.randint(-120, -60)
        base_min, base_max = ENEMY_BASE_SPEED
        spd = random.uniform(base_min, base_max) * speed_factor
        self.speed = spd
        self.typed_len = 0  # quantidade de letras corretas
        self.cleaned = False
        # retangulo visual para “pacote de dados”
        self.rect = pygame.Rect(self.x - 10, self.y - 6, len(self.word) * 16 + 20, 36)

    def update(self):
        self.y += self.speed
        self.rect.y = int(self.y)

    def draw(self, screen, font):
        # fundo do pacote
        pygame.draw.rect(screen, (40, 35, 50), self.rect, border_radius=8)
        # barra de progresso
        total_w = self.rect.width - 20
        prog_w = int(total_w * (self.typed_len / max(1, len(self.word))))
        if prog_w > 0:
            bar_rect = pygame.Rect(self.rect.x + 10, self.rect.y + self.rect.height - 10, prog_w, 6)
            pygame.draw.rect(screen, (80, 220, 140), bar_rect, border_radius=3)
        # texto com highlight
        full = self.word
        done = font.render(full[:self.typed_len], True, (120, 255, 160))
        todo = font.render(full[self.typed_len:], True, COLOR_TEXT_DEFAULT)
        screen.blit(done, (self.x, self.y))
        screen.blit(todo, (self.x + done.get_width(), self.y))

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
        return self.y > SCREEN_HEIGHT

# --- Boss do Core ---
class Boss:
    def __init__(self, boss_words: list[str], hp: int):
        words = list(boss_words)
        random.shuffle(words)
        self.queue = words
        self.hp = hp
        self.current = self.queue.pop(0) if self.queue else ""
        self.matched = 0
        self.spawn_timer = 0
        self.spawn_interval_frames = int(2.0 * FPS)  # minion a cada ~2s
        self.defeated = False

    def handle_char(self, ch: str) -> tuple[bool, bool]:
        """Retorna (acerto, palavra_concluida) sobre a palavra atual do boss."""
        if self.defeated or not self.current:
            return (False, False)
        if self.matched < len(self.current) and ch == self.current[self.matched]:
            self.matched += 1
            if self.matched == len(self.current):
                # Tirou 1 de HP
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

# --- Funções novas (pedido) ---
def destroy_all_enemies_with_word(enemies, word):
    """Remove todos os inimigos cujo texto == word. Retorna quantidade removida."""
    removed = 0
    for e in list(enemies):
        if e.word == word:
            enemies.remove(e)
            removed += 1
    return removed

def choose_enemy_by_prefix(enemies, prefix):
    """Escolhe um inimigo que comece com o prefixo (preferindo o mais abaixo)."""
    candidates = [e for e in enemies if e.starts_with(prefix)]
    if not candidates:
        return None
    # prioriza o que está mais baixo (maior y)
    candidates.sort(key=lambda e: e.y, reverse=True)
    return candidates[0]

# --- Autoplay para demo (mantido) ---
class AutoPlayer:
    def __init__(self, cps=6):
        self.cooldown = 0.0
        self.cps = cps

    def step(self, dt, boss, enemies, target_enemy):
        self.cooldown -= dt
        if self.cooldown > 0:
            return None
        self.cooldown = 1.0 / max(1.0, self.cps)

        # Preferir inimigo mais perigoso (mais baixo); se não houver, boss
        if enemies:
            # Se já há alvo, continuar nele
            if target_enemy:
                idx = target_enemy.typed_len
                if idx < len(target_enemy.word):
                    return target_enemy.word[idx]
            # Senão pegar o mais baixo e iniciar
            e = max(enemies, key=lambda x: x.y)
            return e.word[0]
        # Sem inimigos: digitar boss
        if boss and not boss.defeated and boss.current:
            return boss.current[boss.matched] if boss.matched < len(boss.current) else None
        return None

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("GuaraByte: Protocolo ODS (MVP+)")
    clock = pygame.time.Clock()

    # Fontes
    try:
        font = pygame.font.SysFont("Consolas", 28, bold=True)
        player_font = pygame.font.SysFont("Consolas", 32, bold=True)
        small_font = pygame.font.SysFont("Consolas", 18, bold=False)
    except Exception:
        font = pygame.font.Font(None, 34)
        player_font = pygame.font.Font(None, 38)
        small_font = pygame.font.Font(None, 22)

    # SFX
    load_sfx()

    # CLI: --record-demo N (segundos)
    record_seconds = None
    autoplay = None
    frames_for_gif = []
    Image = None
    if len(sys.argv) >= 3 and sys.argv[1] == "--record-demo":
        try:
            record_seconds = int(sys.argv[2])
        except Exception:
            record_seconds = 10
        autoplay = AutoPlayer(cps=6)
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

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0

        # --- Eventos ---
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
                            # >>> NOVO: Se é o início de uma nova palavra, decidir alvo (minion vs boss)
                            if (boss and not boss.defeated) and (not current_input) and (target_enemy is None):
                                # Tentar escolher inimigo por prefixo do 1º caractere
                                candidate = choose_enemy_by_prefix(enemies, ch)
                                if candidate:
                                    # Decide pelo inimigo: inicia input por prefixo
                                    target_enemy = candidate
                                    current_input = ch
                                else:
                                    # Sem inimigo compatível -> envia ao boss
                                    ok_b, _ = boss.handle_char(ch)
                                    if ok_b:
                                        play_sfx("ok")
                                    # Visual: mostra input mesmo no boss
                                    current_input += ch
                            else:
                                # Fluxo normal anterior
                                if boss and not boss.defeated and target_enemy is None:
                                    # Continuar no boss
                                    ok_b, _ = boss.handle_char(ch)
                                    if ok_b:
                                        play_sfx("ok")
                                    current_input += ch
                                else:
                                    # Sem boss ou mirando minion por prefixo
                                    current_input += ch

        # --- Lógica de alvo por prefixo (quando sem boss OU quando decidimos minion) ---
        if not game_over and not victory:
            cfg = PHASES[phase_idx]

            # Só processa prefixo se NÃO estiver focado em boss neste momento
            if (not (boss and not boss.defeated)) or (target_enemy is not None):
                if not target_enemy and current_input:
                    target_enemy = choose_enemy_by_prefix(enemies, current_input)

                if target_enemy and current_input:
                    # Se o prefixo nao bate mais, reseta
                    if not target_enemy.starts_with(current_input):
                        current_input = ""
                        target_enemy.typed_len = 0
                        target_enemy = None
                    else:
                        # Se completou a palavra por prefixo inteiro
                        if current_input == target_enemy.word:
                            # >>> NOVO: remover TODOS com a mesma palavra e pontuar por cada
                            word = target_enemy.word
                            removed = destroy_all_enemies_with_word(enemies, word)
                            target_enemy = None
                            current_input = ""
                            if removed > 0:
                                score += 10 * removed
                                play_sfx("clean")

        # --- Atualizações por frame ---
        if not (game_over or victory):
            # Spawn (boss pode gerar minions)
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

            # Autoplay (demo)
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
                        # se já tem alvo minion por prefixo:
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
                                # erro -> reset
                                current_input = ""
                                target_enemy.typed_len = 0
                                target_enemy = None
                        else:
                            # sem alvo, tentar escolher pelo prefixo
                            candidate = choose_enemy_by_prefix(enemies, ch)
                            if candidate:
                                target_enemy = candidate
                                current_input = ch
                            elif boss and not boss.defeated:
                                ok_b, _ = boss.handle_char(ch)
                                if ok_b: play_sfx("ok")
                                current_input += ch

            # Atualiza inimigos e checa quedas
            for e in list(enemies):
                e.update()
                if e.is_off_screen():
                    enemies.remove(e)
                    corrupcao -= CORRUPCAO_PERDA
                    if e == target_enemy:
                        target_enemy = None
                        current_input = ""

            # Checa game over
            if corrupcao <= 0:
                game_over = True

            # Checa progresso de fase
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

        # --- Desenho ---
        cfg = PHASES[min(phase_idx, len(PHASES)-1)]
        draw_grid_background(screen, cfg["bg"], cfg["grid"])

        # Inimigos
        for e in enemies:
            e.draw(screen, font)

        # HUD superior
        hud_left  = f"{cfg['name']} | {cfg['ods']}"
        hud_right = f"Score: {score}"
        txt_l = font.render(hud_left, True, (220, 230, 255))
        txt_r = font.render(hud_right, True, (255, 255, 255))
        screen.blit(txt_l, (10, 10))
        screen.blit(txt_r, (SCREEN_WIDTH - txt_r.get_width() - 10, 10))

        # Barra Corrupcao
        pygame.draw.rect(screen, (50, 40, 55), (10, 46, 280, 16), border_radius=8)
        bar_w = int(280 * max(0, min(1, corrupcao/100.0)))
        col = (240, 110, 110) if corrupcao < 35 else (255, 210, 80) if corrupcao < 65 else (120, 230, 160)
        pygame.draw.rect(screen, col, (10, 46, bar_w, 16), border_radius=8)
        lab = font.render("Corrupcao da Rede", True, (200,200,220))
        screen.blit(lab, (10, 66))

        # Boss UI (se ativo)
        if boss and not boss.defeated:
            bw, bh = 560, 60
            rect = pygame.Rect((SCREEN_WIDTH-bw)//2, 80, bw, bh)
            pygame.draw.rect(screen, (50, 24, 40), rect, border_radius=12)
            small = small_font.render(f"Boss HP: {boss.hp}", True, (255, 190, 210))
            screen.blit(small, (rect.x + 12, rect.y + 8))
            w = boss.current
            big_font = pygame.font.Font(None, 36)
            done = big_font.render(w[:boss.matched], True, (255, 140, 170))
            todo = big_font.render(w[boss.matched:], True, (250, 230, 240))
            cx = rect.centerx - (done.get_width() + todo.get_width())//2
            cy = rect.y + 28
            screen.blit(done, (cx, cy))
            screen.blit(todo, (cx + done.get_width(), cy))

        # Input do jogador (feedback visual)
        input_surface = player_font.render(current_input, True, COLOR_PLAYER_INPUT)
        input_rect = input_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 40))
        screen.blit(input_surface, input_rect)

        # Telas finais
        if game_over:
            over = font.render(f"REDE CORROMPIDA! (Dados Depurados: {score})", True, COLOR_TEXT_ERROR)
            rect = over.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            screen.blit(over, rect)

        if victory:
            vic = font.render("MISSAO CUMPRIDA! REDE CPS RESTAURADA.", True, (140, 255, 190))
            rect = vic.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            screen.blit(vic, rect)

        pygame.display.flip()

        # Gravação de GIF (se ativada via CLI)
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