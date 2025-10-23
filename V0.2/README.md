# GuaraByte: Protocolo ODS (single-file, portrait)

**Engine:** Pygame  
**Modo:** Janela vertical (portrait), estilo mobile  
**Estilo:** Digitação (inspirado em zty.pe)

## Como rodar
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/Mac: source .venv/bin/activate
pip install pygame Pillow
python main.py
```

## Gravar GIF demo (autoplay)
```bash
python main.py --record-demo 10  # salva em demo/demo.gif
```

## Dicas de jogo
- Digite as palavras nos pacotes para depurar.
- Com o **Boss** ativo, inicie uma **nova palavra** para alternar o alvo para minions.
- Palavras duplicadas: ao concluir uma, **todas** iguais na tela são limpas.
