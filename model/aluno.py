from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import 
relationship
from datetime import date, datetime
from typing import Union

from  model import Base, Comentario

class Aluno(Base):
    __tablename__ = 'aluno'

    id = Column("pk_aluno", Integer, primary_key=True)
    nome = Column(String(140), unique=True)
    data_de_nascimento = Column(Date)
    data_de_inicio = Column(DateTime, default=datetime.now())
    descricao = Column(String(4000))
    nivel = Column(String)
    video = Column(String)

    # Definição do relacionamento entre o aluno e o comentário.
    # Essa relação é implicita, não está salva na tabela 'aluno',
    # mas aqui estou deixando para SQLAlchemy a responsabilidade
    # de reconstruir esse relacionamento.
    comentarios = relationship("Comentario")

    def __init__(self, nome:str, data_de_nascimento:Union[Date, None] = None), data_de_inicio:Union[DateTime, None] = None), graduacao:str):
        """
        Cadastra um Auno

        Arguments:
            nome: nome do aluno.
            data de nascimento: data de nascimento do aluno.
            data de inicio: data da primeira aula do aluno
            graduacao: cor da faixa do aluno
        """
        self.nome = nome
        self.data_de_nascimento = data_de_nascimento
        self.data_de_inicio = data_de_inicio
        self.graduacao = graduacao


    def adiciona_comentario(self, comentario:Comentario):
        """ Adiciona um novo comentário à técnica
        """
        self.comentarios.append(comentario)

