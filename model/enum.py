from enum import Enum


class StatusEnum(str, Enum):
    PENDENTE = "PENDENTE"  # IA
    ABERTO = "ABERTO"  # HUMANO
    FECHADO = "FECHADO"  # FINALISOU A CONVERSA


class Categoria(str, Enum):
    BAIXA = "BAIXA"
    MEDIA = "MEDIA"
    ALTA = "ALTA"
