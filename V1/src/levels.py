# -*- coding: utf-8 -*-

from dataclasses import dataclass

@dataclass
class LevelConfig:
    name: str
    ods: str
    description: str
    words: list[str]
    spawn_factor: float  # multiplicador de spawn
    speed_factor: float  # multiplicador de velocidade
    target_score: int    # objetivo para vencer a fase

LEVELS: list[LevelConfig] = [
    LevelConfig(
        name="Servidor Acadêmico",
        ods="ODS 4 - Educação de Qualidade",
        description="Depure dados corrompidos do SIGA e biblioteca digital.",
        words=[
            # inimigos (conceitos negativos) e comandos (positivos) misturados
            "spam","fake","erro404","quebrado","link",
            "ensinar","ler","ciencia","verdade","aula","fatec"
        ],
        spawn_factor=1.0,
        speed_factor=1.0,
        target_score=15
    ),
    LevelConfig(
        name="Servidor de Infraestrutura",
        ods="ODS 9 - Indústria, Inovação e Infraestrutura",
        description="Conserte circuitos, patches e código limpo.",
        words=[
            "bug","glitch","atraso","obsoleto",
            "inovar","criar","fix","deploy","logica","clean"
        ],
        spawn_factor=1.1,
        speed_factor=1.1,
        target_score=18
    ),
    LevelConfig(
        name="Servidor de Acesso",
        ods="ODS 10 - Redução das Desigualdades",
        description="Remova muros digitais e garanta acesso a todos.",
        words=[
            "paywall","bloqueio","muro","negado",
            "incluir","abrir","acesso","todos","unir","igualdade"
        ],
        spawn_factor=1.2,
        speed_factor=1.15,
        target_score=20
    ),
    LevelConfig(
        name="Core CPS",
        ods="ODS 11 - Cidades e Comunidades Sustentáveis",
        description="Conter a Anomalia e restaurar a rede do CPS.",
        words=[
            "shutdown","delete","corrupt",
            "sustentavel","comunidade","paulasouza","futuro","energia","limpa"
        ],
        spawn_factor=1.3,
        speed_factor=1.25,
        target_score=24
    ),
]
