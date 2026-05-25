from enum import Enum


class StatusEnum(str, Enum):
    ABERTO = "ABERTO"
    EM_PROCESSO = "EM PROCESSO"
    FECHADO = "FECHADO"
