
# GuaraByte: Protocolo ODS (Pygame, Portrait, Responsivo)

**Engine:** Pygame  
**Modo:** Janela vertical (portrait), **responsivo** (adapta fonts/elementos ao tamanho da janela).  
**Estilo:** Digitação (inspirado em zty.pe) com 4 fases + Boss.

## Novidades desta versão
- **Layout responsivo**: tudo escala conforme o tamanho da janela (HUD, palavras, barras, instruções).  
- **Sem corte** de palavras/infos: tamanho de fonte reduz automaticamente para caber na largura disponível.  
- **Inimigos ricocheteiam** nas **paredes laterais** (não saem da tela).  
- **Troca de alvo com Boss**: ao iniciar uma **nova palavra**, você direciona o foco para minions ou Boss.  
- **Palavras duplicadas**: ao concluir uma, **todas iguais** em tela são depuradas (pontua +10 por inimigo).  
- **Metas por fase**: Fases 1–3 exigem **300 pontos** para avançar. A Fase 4 termina ao **derrotar o Boss**.

## Rodando
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/Mac: source .venv/bin/activate
pip install -r requirements.txt
python src/main.py
```

## Controles
- Digite as letras para depurar os pacotes.  
- **BACKSPACE** apaga o input atual.  
- **ESC** sai do jogo.

## Estrutura
```
src/
  assets.py       # SFX e carregamento
  levels.py       # Definição das fases (metas de 300 pts)
  main.py         # Loop principal e UI responsiva
  settings.py     # Constantes e parâmetros
  typing_core.py  # Lógica de inimigos (vx/vy + bounce) e Boss
  utils.py        # Escala, texto com ajuste, grid, clamp
assets/
  sfx/
    type_ok.wav
    word_clean.wav
    boss_hit.wav
```

## Build (Windows)
```bash
pip install pyinstaller
pyinstaller --noconfirm --onefile --name GuaraByte src/main.py --paths src --add-data "assets:assets"
```
