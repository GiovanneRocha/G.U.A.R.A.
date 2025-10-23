import pygame
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60


COLOR_BACKGROUND = (10, 10, 25)
COLOR_TEXT_DEFAULT = (255, 255, 255) 
COLOR_TEXT_TYPING = (0, 255, 255) 
COLOR_TEXT_ERROR = (255, 0, 0) 
COLOR_PLAYER_INPUT = (0, 255, 0) 

WORD_LIST = [
    "ENSINAR", "LER", "CIENCIA", "VERDADE", "AULA", "FATEC",
    "SPAM", "FAKENEWS", "ERRO404", "BUG", "GLITCH"
]

class WordEnemy:
    def __init__(self):
        self.word = random.choice(WORD_LIST)
        self.x = random.randint(50, SCREEN_WIDTH - 150)
        self.y = random.randint(-100, -50)
        self.speed = random.uniform(0.5, 1.5)
        self.typed_part = "" 

    def update(self):
        self.y += self.speed

    def draw(self, screen, font):
        base_text_surface = font.render(self.word, True, COLOR_TEXT_DEFAULT)
        screen.blit(base_text_surface, (self.x, self.y))
        if self.typed_part:
            typed_text_surface = font.render(self.typed_part, True, COLOR_TEXT_TYPING)
            screen.blit(typed_text_surface, (self.x, self.y))
            
    def is_off_screen(self):
        return self.y > SCREEN_HEIGHT

def main():
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("GuaráByte: Protocolo ODS (MVP)")
    clock = pygame.time.Clock()
    

    try:

        font = pygame.font.SysFont("Consolas", 28, bold=True)
        player_font = pygame.font.SysFont("Consolas", 32, bold=True)
    except:
 
        font = pygame.font.Font(None, 34)
        player_font = pygame.font.Font(None, 38)

    enemies = [] 
    current_input = ""
    target_enemy = None
    
    score = 0 # "Dados Depurados"
    corrupcao = 100 # "Corrupção da Rede CPS" (começa em 100 e diminui)
    
    spawn_timer = 0
    spawn_delay = 120 # A cada 2 segundos (120 frames / 60 FPS)

    running = True
    game_over = False

    while running:
        # Limita o FPS
        clock.tick(FPS)

        # --- 1. Tratamento de Eventos (Input) ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if game_over: # Se o jogo acabou, só permite sair
                continue

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:

                    current_input = current_input[:-1]
  
                    if not current_input and target_enemy:
                        target_enemy = None

                elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:

                    pass 
                
                else:

                    char = event.unicode.upper()
                    if char.isalnum(): # Aceita apenas letras e números
                        current_input += char

        if game_over:
            # --- Tela de Game Over ---
            screen.fill(COLOR_BACKGROUND)
            game_over_text = font.render(f"REDE CORROMPIDA! (Dados Depurados: {score})", True, COLOR_TEXT_ERROR)
            rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(game_over_text, rect)
            pygame.display.flip()
            continue 
        
        spawn_timer += 1
        if spawn_timer >= spawn_delay:
            enemies.append(WordEnemy())
            spawn_timer = 0
            # Aumenta a dificuldade (opcional)
            if spawn_delay > 30: # Limite de 0.5s
                spawn_delay *= 0.99 

        # 2.2. Lógica de "Mira" (Targeting)
        if not target_enemy and current_input:

            for enemy in enemies:
                if enemy.word.startswith(current_input):
                    target_enemy = enemy
                    break # Mira no primeiro que encontrar

        if target_enemy:
            # Atualiza o feedback visual do inimigo
            target_enemy.typed_part = current_input

            if not target_enemy.word.startswith(current_input):
                # O jogador errou a digitação
                # AÇÃO: Limpa o input e a mira
                current_input = ""
                target_enemy.typed_part = ""
                target_enemy = None
                # (Aqui você pode adicionar um som de "erro")
            
            elif current_input == target_enemy.word:
                # O jogador ACERTOU!
                # AÇÃO: "Depura" o inimigo
                enemies.remove(target_enemy)
                current_input = ""
                target_enemy = None
                score += 10 # Aumenta a pontuação

        for enemy in list(enemies):
            enemy.update()

            # 2.5. Verificar Falha (Inimigo chegou ao fim)
            if enemy.is_off_screen():
                enemies.remove(enemy)
                corrupcao -= 10 # Perde "vida"
                
                # Se o inimigo que sumiu era o alvo, limpa a mira
                if enemy == target_enemy:
                    target_enemy = None
                    current_input = ""

        # 2.6. Verificar Game Over
        if corrupcao <= 0:
            game_over = True
            # (Aqui você pode tocar um som de "game over")

        # --- 3. Desenho (Renderização) ---
        
        # 3.1. Limpa a tela
        screen.fill(COLOR_BACKGROUND)

        # 3.2. Desenha todos os inimigos
        for enemy in enemies:
            enemy.draw(screen, font)

        # 3.3. Desenha o HUD (Score e Corrupção)
        score_surface = font.render(f"Dados Depurados: {score}", True, COLOR_TEXT_TYPING)
        screen.blit(score_surface, (10, 10))

        corrupcao_surface = font.render(f"Corrupção da Rede: {corrupcao}%", True, COLOR_TEXT_ERROR)
        screen.blit(corrupcao_surface, (SCREEN_WIDTH - corrupcao_surface.get_width() - 10, 10))

        # 3.4. Desenha o Input do Jogador (O que ele está digitando)
        input_surface = player_font.render(current_input, True, COLOR_PLAYER_INPUT)
        input_rect = input_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 40))
        screen.blit(input_surface, input_rect)

        # 3.5. Atualiza a tela
        pygame.display.flip()

    # --- Fim do Jogo ---
    pygame.quit()

# --- Ponto de Entrada do Script ---
if __name__ == "__main__":
    main()