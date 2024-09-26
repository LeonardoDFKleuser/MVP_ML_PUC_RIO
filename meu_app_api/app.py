from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect, request
from urllib.parse import unquote
from sqlalchemy.exc import IntegrityError
from model import Session, Jogo, Model  # Agora importa a classe Model para machine learning
from schemas import *
from flask_cors import CORS
import pandas as pd

# Instanciando o objeto OpenAPI
info = Info(title="API Steam Machine Learning", version="1.0.0")

app = OpenAPI(__name__, info=info)
CORS(app)

# Definindo tags para agrupamento das rotas
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
jogo_tag = Tag(name="Jogo", description="Adição, visualização, remoção e predição de faixas de preço para jogos")

# Rota home
@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação."""
    return redirect('/openapi')


# Rota de listagem de jogos
@app.get('/jogos', tags=[jogo_tag],
         responses={"200": ListagemJogoSchema, "404": ErrorSchema})
def get_jogos():
    """Lista todos os jogos cadastrados na base
    Retorna uma lista de jogos cadastrados na base.
    
    Returns:
        list: lista de jogos cadastrados na base
    """
    session = Session()

    # Buscando todos os jogos
    jogos = session.query(Jogo).all()
    
    if not jogos:
        return {"message": "Não há jogos cadastrados na base."}, 404
    else:
        return apresenta_jogos(jogos), 200


# Rota de adição e predição de jogo
@app.post('/jogo', tags=[jogo_tag],
          responses={"200": JogoViewSchema, "400": ErrorSchema, "409": ErrorSchema})
def predict_jogo(form: JogoSchema):
    """Adiciona um novo jogo à base de dados e faz a predição da faixa de preço
    Retorna a classificação do jogo em uma faixa de preço com base nos gêneros e categorias.
    
    Args:
        nome (str): nome do jogo
        plataforma (str): plataforma do jogo
        loja (str): loja onde o jogo está sendo vendido
        preco (float): preço do jogo
        genres (list): gêneros do jogo
        categories (list): categorias do jogo
        
    Returns:
        dict: representação do jogo e faixa de preço prevista
    """
    
    # Carregando o modelo de machine learning
    try:
        ml_path = 'ml_model/steam_model.pkl'  # Alterar o caminho conforme necessário
        modelo = Model.carrega_modelo(ml_path)
    except FileNotFoundError:
        return {"message": "Erro ao carregar o modelo de machine learning"}, 400

    # Montando os dados de entrada para predição
    dados_jogo = {
        'genres': ' '.join(form.genres),  # Convertendo a lista de gêneros para uma string
        'categories': ' '.join(form.categories)  # Convertendo a lista de categorias para uma string
    }

    try:
        # Criar um DataFrame com os novos dados para predição
        entrada = pd.DataFrame([dados_jogo])

        # Transformar as colunas de entrada em variáveis dummificadas
        entrada_transformada = pd.get_dummies(entrada, drop_first=True)

        # Garantir que as colunas de 'entrada_transformada' coincidam com o modelo treinado
        entrada_transformada = entrada_transformada.reindex(columns=modelo.feature_names_in_, fill_value=0)

        # Realiza a predição da faixa de preço
        faixa_de_preco = modelo.predict(entrada_transformada)

    except Exception as e:
        return {"message": f"Erro na predição: {str(e)}"}, 400

    # Criando o novo jogo e armazenando no banco de dados
    jogo = Jogo(
        nome=form.nome,
        plataforma=form.plataforma,
        loja=form.loja,
        preco=form.preco,
        faixa_predita=faixa_de_preco[0]  # Usando o primeiro valor previsto
    )
    
    try:
        # Criando conexão com a base
        session = Session()
        
        # Adicionando o novo jogo à base
        session.add(jogo)
        session.commit()
        
        return apresenta_jogo(jogo), 200

    except IntegrityError:
        error_msg = "Jogo de mesmo nome já cadastrado na base."
        return {"message": error_msg}, 409

    except Exception as e:
        error_msg = f"Erro ao adicionar jogo à base: {str(e)}"
        return {"message": error_msg}, 400


# Rota para remoção de um jogo pelo ID
@app.delete('/jogo', tags=[jogo_tag],
            responses={"200": JogoDelSchema, "404": ErrorSchema, "400": ErrorSchema})
def delete_jogo(query: JogoBuscaSchema):
    """Remove um jogo cadastrado na base a partir do ID
    
    Args:
        id (int): ID do jogo
        
    Returns:
        msg: Mensagem de sucesso ou erro
    """
    try:
        jogo_id = query.id  # O ID já vem como inteiro no esquema `JogoBuscaSchema`

        # Criando conexão com a base
        session = Session()

        # Buscando o jogo pelo ID
        jogo = session.query(Jogo).filter(Jogo.id == jogo_id).first()

        if not jogo:
            error_msg = "O jogo não está cadastrado na base."
            return {"message": error_msg}, 404
        else:
            session.delete(jogo)
            session.commit()
            return {"message": f"Jogo {jogo.nome} removido com sucesso."}, 200

    except ValueError:
        return {"message": "ID inválido."}, 400

    except Exception as e:
        return {"message": f"Erro ao remover o jogo: {str(e)}"}, 500


if __name__ == '__main__':
    app.run(debug=True)  # Ativar o modo de depuração
