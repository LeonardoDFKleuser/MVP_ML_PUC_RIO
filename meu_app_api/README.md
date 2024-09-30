# Minha API

Este pequeno projeto faz parte do MVP realizado por Leonardo Kleuser para a pós-graduação em Engenharia de Software na PUC Rio.

O objetivo aqui é apresentar um site com uma única tela, que serve como uma lista para controle da biblioteca de jogos, incluindo o nome do jogo, a loja onde foi comprado e o valor, permitindo controle fácil para o usuário.

## Como executar

Antes de começar, é importante que o usuário possua Python instalado no computador (https://www.python.org/downloads/).  
Será necessário ter todas as bibliotecas Python listadas no `requirements.txt` instaladas.

Após clonar o repositório, é necessário ir ao diretório raiz pelo terminal para poder executar os comandos descritos abaixo.  
**Observação:** O endereço representado no terminal deve terminar com "meu_app_api".

> **Dica:** É altamente recomendado o uso de ambientes virtuais, como o [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).

### 1. Configuração do ambiente virtual

Execute os seguintes comandos para configurar o ambiente virtual:

**Para criar o ambiente virtual no diretório:**
```bash
python3 -m venv env
Para ativar o ambiente virtual:

bash
Copiar código
env/Scripts/activate  # No Windows
source env/bin/activate  # No Linux/MacOS
Para instalar as dependências do projeto:

bash
Copiar código
(env)$ pip install -r requirements.txt
Este comando instalará todas as bibliotecas necessárias descritas no arquivo requirements.txt.

2. Executar a API
Após instalar as dependências, você pode rodar a API com o seguinte comando:

bash
Copiar código
(env)$ flask run --host 0.0.0.0 --port 5000
Para facilitar o desenvolvimento, pode-se adicionar a flag --reload, para reiniciar automaticamente a API após modificações no código:

bash
Copiar código
(env)$ flask run --host 0.0.0.0 --port 5000 --reload
Agora, abra http://localhost:5000/#/ no navegador para acessar a interface da aplicação.

Machine Learning
Este projeto também inclui um modelo de machine learning para classificar os jogos em diferentes faixas de preço com base em gêneros e categorias.

O modelo foi treinado com os seguintes algoritmos:

KNN
Decision Tree (Árvore de Decisão)
Naive Bayes
SVM
O modelo final treinado, chamado steam_model.pkl, está localizado na pasta ml_model/.

Executar o modelo de machine learning
O modelo de machine learning é carregado na API e usado para fazer predições com base nos dados inseridos pelo usuário no front-end.

Como rodar os testes unitários
O projeto inclui testes automatizados para garantir que o modelo de machine learning atenda aos requisitos de desempenho. Esses testes verificam métricas como acurácia, recall, precisão e F1-Score.

Para rodar os testes unitários, execute o seguinte comando no terminal a partir da raiz do projeto:

bash
Copiar código
(env)$ pytest test_steam_model.py
Este comando executa os testes automatizados definidos no arquivo test_steam_model.py, validando se o modelo atende aos thresholds (valores mínimos) de desempenho.
