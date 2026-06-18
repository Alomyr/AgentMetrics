from enum import Enum


class StatusEnum(str, Enum):
    """
    Enumeração dos estados possíveis do ciclo de vida de um atendimento.

    Define se a conversação está na esteira automatizada da IA, em atendimento 
    humano ativo ou se já foi concluída.
    """
    PENDENTE = "PENDENTE"  # Operado por: Inteligência Artificial (IA)
    ABERTO = "ABERTO"      # Operado por: Operador/Atendente Humano
    FECHADO = "FECHADO"    # Estado: Conversa finalizada e arquivada


class Categoria(str, Enum):
    """
    Enumeração dos níveis de classificação e prioridade aplicados aos leads.
    """
    BAIXA = "BAIXA"
    MEDIA = "MEDIA"
    ALTA = "ALTA"