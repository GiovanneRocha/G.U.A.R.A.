
# GuaráByte: Protocolo ODS

**Engine:** Pygame  
**Estilo:** Digitação (inspirado em zty.pe)  
**Tema:** Segurança/Depuração de rede + ODS (ONU) no contexto FATEC Campinas

## 🤖 Premissa
O sistema ativa o G.U.A.R.Á. (Guardião Unificado de Ambientes de Rede e Aprendizagem) para **depurar pacotes corrompidos** digitando as palavras que aparecem nos inimigos. Ao completar a palavra, o pacote é **restaurado** e a **Corrupção da Rede** diminui.

## 🎮 Como jogar
- Digite as letras das palavras que aparecem nos pacotes.
- Palavras completas **restauram** pacotes e reduzem a barra de **Corrupção**.
- **ESC**: sair/voltar ao menu.

## 🚀 Rodando localmente
```bash
python -m venv .venv
# Ative a venv (Windows) .venv\Scriptsctivate | (Linux/Mac) source .venv/bin/activate
pip install -r requirements.txt
python src/main.py
```

## 🧩 Fases (ODS)
1. **Servidor Acadêmico** — ODS 4  
2. **Servidor de Infraestrutura** — ODS 9  
3. **Servidor de Acesso** — ODS 10  
4. **Core CPS (Boss)** — ODS 11

## 🎨 Tema visual por fase
Cada fase possui **cores e grid** próprias (background sutil), reforçando o tema da ODS.

## 🧱 Estrutura
```
src/ -> código-fonte
assets/ -> fontes, imagens e sons (licenciados)
```

## 📦 Executável
Gerar executável Windows:
```bash
pip install pyinstaller
pyinstaller --noconfirm --onefile --name GuaraByte src/main.py --paths src --add-data "assets:assets"
# O binário ficará em dist/GuaraByte(.exe)
```

## 🎥 Gravar GIF demo automaticamente
Você pode gerar um GIF curto de gameplay automaticamente (modo *autoplay*) e salvar em `demo/demo.gif`:
```bash
python src/main.py --record-demo 10  # grava ~10 segundos
```
> Requer `Pillow` (já está no requirements). Se preferir vídeo, grave com OBS/ShareX e anexe ao PR.

## 📜 Licenças e Créditos
- Código: MIT (ou defina a licença preferida da equipe).
- SFX (CC0) gerados proceduralmente.
- **Uso de IA** (se houver): declarar no `relatorioFinal_nomeEquipe.md`.

## 👥 Equipe
- Nome da equipe: _preencher_  
- Integrantes: _preencher (curso, período, semestre)_
