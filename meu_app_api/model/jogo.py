from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from model import Base, Comentario


class Jogo(Base):
    __tablename__ = 'jogo'

    id = Column("id", Integer, primary_key=True)
    nome = Column(String(140), unique=True)
    plataforma = Column(String(140))
    loja = Column(String(140))
    preco = Column(Float)
    data_insercao = Column(DateTime, default=datetime.now())
    faixa_predita = Column(String(50))  # Nova coluna para armazenar a faixa predita

    # Definição do relacionamento entre o jogo e o comentário
    comentarios = relationship("Comentario")

    def __init__(self, nome: str, plataforma: str, loja: str, preco: float, faixa_predita: str,
                 data_insercao: Union[DateTime, None] = None):
        """
        Cria um jogo

        Arguments:
            nome: nome do jogo
            plataforma: plataforma na qual o jogo foi adiquirido
            loja: loja na qual o jogo foi adquirido
            preco : valor esperado para o jogo
            faixa_predita: faixa predita do preço do jogo (Baixo, Médio, Alto)
            data_insercao: data de quando o jogo foi inserido à base
        """

        self.nome = nome
        self.plataforma = plataforma
        self.loja = loja
        self.preco = preco
        self.faixa_predita = faixa_predita

        # Se não for informada, será a data exata da inserção no banco
        if data_insercao:
            self.data_insercao = data_insercao
