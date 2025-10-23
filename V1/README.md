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
4. **Core CPS** — ODS 11

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

## 📜 Licenças e Créditos
- Código: MIT (ou defina a licença preferida da equipe).
- Assets de áudio/visual: apenas materiais **livres** (CC0/CC-BY) com créditos neste README.
- **Uso de IA** (se houver): declarar no `relatorioFinal_nomeEquipe.md`.

## 👥 Equipe
- Nome da equipe: _preencher_  
- Integrantes: _preencher (curso, período, semestre)_
