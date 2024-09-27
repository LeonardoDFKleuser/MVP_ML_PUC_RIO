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
    generos = Column(String)  # Adicionando campo para gêneros
    categorias = Column(String)  # Adicionando campo para categorias
    faixa_predita = Column(String)  # Adicionando campo para faixa de preço predita
    data_insercao = Column(DateTime, default=datetime.now())

    # Definição do relacionamento entre o jogo e o comentário.
    comentarios = relationship("Comentario")

    def __init__(self, nome: str, plataforma: str, loja: str, preco: float, generos: str, categorias: str,
                 faixa_predita: str, data_insercao: Union[DateTime, None] = None):
        """
        Cria um jogo

        Arguments:
            nome: nome do jogo.
            plataforma: plataforma na qual o jogo foi adquirido.
            loja: loja na qual o jogo foi adquirido.
            preco: valor esperado para o jogo.
            generos: gêneros associados ao jogo.
            categorias: categorias associadas ao jogo.
            faixa_predita: faixa de preço predita para o jogo.
            data_insercao: data de quando o jogo foi inserido à base.
        """
        self.nome = nome
        self.plataforma = plataforma
        self.loja = loja
        self.preco = preco
        self.generos = generos
        self.categorias = categorias
        self.faixa_predita = faixa_predita
        if data_insercao:
            self.data_insercao = data_insercao
