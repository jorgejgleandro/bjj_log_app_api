from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from sqlalchemy.types import Enum
from enum import Enum as PyEnum
from datetime import datetime
from typing import Union

from  model import Base, Comentario

class NivelEnum(PyEnum):
    INICIANTE = 'Iniciante'
    INTERMEDIARIO = 'Intermediário'
    AVANCADO = 'Avançado'

NivelTipo = Enum(
    NivelEnum,
    nome="nivel_tipo",
    values_callable=lambda obj: [item.value for item in obj],
)


class Tecnica(Base):
    __tablename__ = 'tecnica'

    id = Column("pk_tecnica", Integer, primary_key=True)
    nome = Column(String(140), unique=True)
    descricao = Column(String(4000))
    nivel = Column(NivelTipo)
    video = Column(String)

    # Definição do relacionamento entre a tecnica e o comentário.
    # Essa relação é implicita, não está salva na tabela 'tecnica',
    # mas aqui estou deixando para SQLAlchemy a responsabilidade
    # de reconstruir esse relacionamento.
    comentarios = relationship("Comentario")

    def __init__(self, nome:str, descricao:str, nivel:NivelTipo,
                 video:str):
        """
        Cria um Tecnica

        Arguments:
            nome: nome da tecnica.
            descricao: breve texto explicativo sobre a tecnica.
            nivel: um de tres niveis possiveis: iniciante, intermediario ou avancado
            video: url para video demonstrativo
        """
        self.nome = nome
        self.descricao = descricao
        self.nivel = nivel
        self.video = video


    def adiciona_comentario(self, comentario:Comentario):
        """ Adiciona um novo comentário à técnica
        """
        self.comentarios.append(comentario)

