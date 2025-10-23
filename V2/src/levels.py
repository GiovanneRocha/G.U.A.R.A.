
# -*- coding: utf-8 -*-
from dataclasses import dataclass

@dataclass
class LevelConfig:
    name: str
    ods: str
    description: str
    words: list[str]
    spawn_factor: float
    speed_factor: float
    target_score: int
    bg_color: tuple
    grid_color: tuple
    has_boss: bool = False
    boss_words: list[str] | None = None
    boss_health: int = 0

LEVELS: list[LevelConfig] = [
    LevelConfig(
        name="Servidor Academico",
        ods="ODS 4 - Educacao de Qualidade",
        description="Depure dados corrompidos do SIGA e biblioteca digital.",
        words=[
            "spam","fake","erro404","quebrado","link",
            "ensinar","ler","ciencia","verdade","aula","fatec"
        ],
        spawn_factor=1.0,
        speed_factor=1.0,
        target_score=15,
        bg_color=(16,18,28),
        grid_color=(28,34,48)
    ),
    LevelConfig(
        name="Servidor de Infraestrutura",
        ods="ODS 9 - Industria, Inovacao e Infraestrutura",
        description="Conserte circuitos, patches e codigo limpo.",
        words=[
            "bug","glitch","atraso","obsoleto",
            "inovar","criar","fix","deploy","logica","clean"
        ],
        spawn_factor=1.1,
        speed_factor=1.1,
        target_score=18,
        bg_color=(18,16,24),
        grid_color=(32,28,44)
    ),
    LevelConfig(
        name="Servidor de Acesso",
        ods="ODS 10 - Reducao das Desigualdades",
        description="Remova muros digitais e garanta acesso a todos.",
        words=[
            "paywall","bloqueio","muro","negado",
            "incluir","abrir","acesso","todos","unir","igualdade"
        ],
        spawn_factor=1.2,
        speed_factor=1.15,
        target_score=20,
        bg_color=(14,20,20),
        grid_color=(24,36,36)
    ),
    LevelConfig(
        name="Core CPS",
        ods="ODS 11 - Cidades e Comunidades Sustentaveis",
        description="Conter a Anomalia e restaurar a rede do CPS.",
        words=[
            "shutdown","delete","corrupt",
            "sustentavel","comunidade","paulasouza","futuro","energia","limpa"
        ],
        spawn_factor=1.0,
        speed_factor=1.0,
        target_score=0,
        bg_color=(20,14,18),
        grid_color=(40,24,34),
        has_boss=True,
        boss_words=[
            "reconstruir","sustentabilidade","colaboracao","comunidade","guarabyte","protocoloods"
        ],
        boss_health=6
    ),
]
