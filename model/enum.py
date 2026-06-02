from enum import Enum


class StatusEnum(str, Enum):
    PENDENTE = "PENDENTE"  # IA
    ABERTO = "ABERTO"  # HUMANO
    FECHADO = "FECHADO"  # FINALISOU A CONVERSA
