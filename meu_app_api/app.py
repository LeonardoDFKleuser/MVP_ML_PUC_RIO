from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Jogo, Comentario
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
jogo_tag = Tag(name="Jogo", description="Adição, visualização e remoção de jogos à base")
comentario_tag = Tag(name="Comentario", description="Adição de um comentário à um jogo cadastrado na base")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/jogo', tags=[jogo_tag],
          responses={"200": JogoViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_jogo(form: JogoSchema):
    """Adiciona um novo jogo à base de dados

    Publica uma representação dos jogos e comentários associados.
    """
    jogo = Jogo(
        nome=form.nome,
        plataforma=form.plataforma,
        loja=form.loja,
        preco=form.preco)
    logger.debug(f"Adicionando jogo de nome: '{jogo.nome}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando jogo
        session.add(jogo)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        session.refresh(jogo)
        logger.debug(f"Adicionado jogo de nome: '{jogo.nome}'")
        return apresenta_jogo(jogo), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "jogo de mesmo nome já salvo na base :/"
        logger.warning(f"Erro ao adicionar jogo '{jogo.nome}', {error_msg}")
        return {"message": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar jogo '{jogo.nome}', {error_msg}")
        return {"message": error_msg}, 400


@app.get('/jogos', tags=[jogo_tag],
         responses={"200": ListagemJogoSchema, "404": ErrorSchema})
def get_jogos():
    """Faz a busca por todos os jogos cadastrados

    Retorna uma representação da listagem de jogos.
    """
    logger.debug(f"Coletando jogos ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    jogos = session.query(Jogo).all()

    if not jogos:
        # se não há jogos cadastrados
        return {"jogos": []}, 200
    else:
        logger.debug(f"%d rodutos econtrados" % len(jogos))
        # retorna a representação de produto
        print(jogos)
        return apresenta_jogos(jogos), 200


@app.delete('/jogo', tags=[jogo_tag],
            responses={"200": JogoDelSchema, "404": ErrorSchema})
def del_jogo(query: JogoBuscaSchema):
    """Deleta um Produto a partir do id do jogo informado

    Retorna uma mensagem de confirmação da remoção.
    """
    jogo_id = query.id
    jogo_nome = query.nome
    print(jogo_id)
    # criando conexão com a base
    session = Session()
    jogo = session.query(Jogo).filter(Jogo.id == jogo_id)
    logger.debug(f"Deletando dados sobre jogo #{jogo_nome}")
    
    # fazendo a remoção
    count = session.query(Jogo).filter(Jogo.id == jogo_id).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado jogo #{jogo_nome}")
        return {"message": "jogo removido", "id": jogo_id}
    else:
        # se o jogo não foi encontrado
        error_msg = "Jogo não encontrado na base :/"
        logger.warning(f"Erro ao deletar jogo #'{jogo_id}', {jogo.nome}, {error_msg}")
        return {"message": error_msg}, 404



