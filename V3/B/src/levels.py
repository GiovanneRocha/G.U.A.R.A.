
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
        words=["SPAM","FAKE","ERRO404","QUEBRADO","LINK","ENSINAR","LER","CIENCIA","VERDADE","AULA","FATEC"],
        spawn_factor=1.0,
        speed_factor=1.0,
        target_score=300,
        bg_color=(16,18,28),
        grid_color=(28,34,48)
    ),
    LevelConfig(
        name="Servidor de Infraestrutura",
        ods="ODS 9 - Industria, Inovacao e Infraestrutura",
        description="Conserte circuitos, patches e codigo limpo.",
        words=["BUG","GLITCH","ATRASO","OBSOLETO","INOVAR","CRIAR","FIX","DEPLOY","LOGICA","CLEAN"],
        spawn_factor=1.15,
        speed_factor=1.1,
        target_score=300,
        bg_color=(18,16,24),
        grid_color=(32,28,44)
    ),
    LevelConfig(
        name="Servidor de Acesso",
        ods="ODS 10 - Reducao das Desigualdades",
        description="Remova muros digitais e garanta acesso a todos.",
        words=["PAYWALL","BLOQUEIO","MURO","NEGADO","INCLUIR","ABRIR","ACESSO","TODOS","UNIR","IGUALDADE"],
        spawn_factor=1.25,
        speed_factor=1.2,
        target_score=300,
        bg_color=(14,20,20),
        grid_color=(24,36,36)
    ),
    LevelConfig(
        name="Core CPS (Boss)",
        ods="ODS 11 - Cidades e Comunidades Sustentaveis",
        description="Conter a Anomalia e restaurar a rede do CPS.",
        words=["SHUTDOWN","DELETE","CORRUPT","FUTURO","ENERGIA","LIMPA"],
        spawn_factor=0.9,
        speed_factor=1.0,
        target_score=300,  # precisa bater 300 e derrotar o boss
        bg_color=(20,14,18),
        grid_color=(40,24,34),
        has_boss=True,
        boss_words=["RECONSTRUIR","SUSTENTABILIDADE","COLABORACAO","COMUNIDADE","GUARABYTE","PROTOCOLOODS"],
        boss_health=6
    ),
]
