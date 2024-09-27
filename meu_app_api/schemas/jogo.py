from pydantic import BaseModel
from typing import Optional, List
from model.jogo import Jogo
from schemas import ComentarioSchema

class JogoSchema(BaseModel):
    """ Define como um novo jogo a ser inserido deve ser representado
    """
    nome: Optional[str] = "Dark cats 3"
    plataforma: Optional[str] = "Pc"
    loja: Optional[str] = "Valvula"
    preco: Optional[float] = 12.50  # Isso permite valores nulos para preco
    genres: List[str] = ["Ação", "Aventura"]  # Adicionando o campo de gêneros
    categories: List[str] = ["Single-player", "Multi-player"]  # Adicionando o campo de categorias

class JogoBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome do jogo.
    """
    nome: str = "Dark cats 3"
    id: int = 1

class ListagemJogoSchema(BaseModel):
    """ Define como uma listagem de jogos será retornada.
    """
    jogos: List[JogoSchema]

def apresenta_jogos(jogos: List[Jogo]):
    """ Retorna uma representação dos jogos seguindo o schema definido em JogoViewSchema. """
    result = []
    for jogo in jogos:
        result.append({
            "id": jogo.id,
            "nome": jogo.nome,
            "plataforma": jogo.plataforma,
            "loja": jogo.loja,
            "preco": jogo.preco,
            "generos": jogo.generos.split() if isinstance(jogo.generos, str) else jogo.generos,
            "categorias": jogo.categorias.split() if isinstance(jogo.categorias, str) else jogo.categorias,
            "faixa_predita": jogo.faixa_predita  # Incluindo o campo faixa_predita
        })
    return {"jogos": result}


class JogoViewSchema(BaseModel):
    """ Define como um jogo será retornado: jogo + comentários.
    """
    id: int = 1
    nome: str = "Banana Prata"
    plataforma: str = "Pc"
    loja: str = "Valvula"
    preco: float = 12.50
    total_cometarios: int = 1
    comentarios: List[ComentarioSchema]

class JogoDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    nome: str

def apresenta_jogo(jogo: Jogo):
    """ Retorna uma representação do jogo seguindo o schema definido em JogoViewSchema. """
    return {
        "id": jogo.id,
        "nome": jogo.nome,
        "plataforma": jogo.plataforma,
        "loja": jogo.loja,
        "preco": jogo.preco,
        "generos": jogo.generos.split() if isinstance(jogo.generos, str) else jogo.generos,
        "categorias": jogo.categorias.split() if isinstance(jogo.categorias, str) else jogo.categorias,
        "faixa_predita": jogo.faixa_predita,  # Garantindo que faixa_predita seja retornado
        "total_comentarios": len(jogo.comentarios),
        "comentarios": [{"texto": c.texto} for c in jogo.comentarios]
    }

