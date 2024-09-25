from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  model import Base, Comentario


class Jogo(Base):
    __tablename__ = 'jogo'

    id = Column("id", Integer, primary_key=True)
    nome = Column(String(140), unique=True)
    plataforma = Column(String(140))
    loja = Column(String(140))
    preco = Column(Float)
    data_insercao = Column(DateTime, default=datetime.now())

    # Definição do relacionamento entre o jogo e o comentário.
    # Essa relação é implicita, não está salva na tabela 'jogo',
    # mas aqui estou deixando para SQLAlchemy a responsabilidade
    # de reconstruir esse relacionamento.
    comentarios = relationship("Comentario")

    def __init__(self, nome:str, plataforma:str, loja:str, preco:float,
                 data_insercao:Union[DateTime, None] = None):
        """
        Cria um jogo

        Arguments:
            nome: nome do jogo.
            plataforma: plataforma na qual o jogo foi adiquirido
            loja: loja na qual o jogo foi adquirido
            preco : valor esperado para o jogo
            data_insercao: data de quando o jogo foi inserido à base
        """

        self.nome = nome
        self.plataforma = plataforma
        self.loja = loja
        self.preco = preco

        # se não for informada, será o data exata da inserção no banco
        if data_insercao:
            self.data_insercao = data_insercao

    def adiciona_comentario(self, comentario:Comentario):
        """ Adiciona um novo comentário ao jogo
        """
        self.comentarios.append(comentario)

