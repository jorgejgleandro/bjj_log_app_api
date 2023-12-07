from sqlalchemy import Column, String, Integer, DateTime, Date, Float
from sqlalchemy.orm import relationship
from datetime import date, datetime
from typing import Union

from  model import Base, Comentario

class Aluno(Base):
    __tablename__ = 'aluno'

    id = Column("pk_aluno", Integer, primary_key=True)
    nome = Column(String(140), unique=True)    
    data_de_nascimento = Column(DateTime)
    data_de_inicio = Column(DateTime)
    graduacao = Column(String(140))

    # Definição do relacionamento entre o aluno e o comentário.
    # Essa relação é implicita, não está salva na tabela 'aluno',
    # mas aqui estou deixando para SQLAlchemy a responsabilidade
    # de reconstruir esse relacionamento.
    #comentarios = relationship("Comentario")

    def __init__(self, nome:str, graduacao:str, data_de_nascimento:str, data_de_inicio:str):
        """
        Cadastra um Auno

        Arguments:
            nome: nome do aluno.
            data de nascimento: data de nascimento do aluno.
            data de inicio: data da primeira aula do aluno
            graduacao: cor da faixa do aluno
        """
        self.nome = nome
        self.data_de_nascimento = datetime.strptime("%s" % data_de_nascimento, "%d/%m/%Y")
        self.data_de_inicio = datetime.strptime("%s" % data_de_inicio, "%d/%m/%Y")             
        self.graduacao = graduacao

        # se não for informada, será a data exata da inserção no banco
        #if data_de_inicio:
        #    self.data_de_inicio = data_de_inicio

        # if data_de_nascimento:
        #     self.data_de_nascimento = data_de_nascimento





    # def adiciona_comentario(self, comentario:Comentario):
    #     """ Adiciona um novo comentário ao aluno
    #     """
    #     self.comentarios.append(comentario)

