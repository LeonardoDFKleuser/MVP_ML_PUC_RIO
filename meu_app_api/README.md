# Minha API

Este pequeno projeto faz parte do MVP realizado por Leonardo Kleuser para a pós graduação em Engenharia de Software na PUC Rio

O objetivo aqui é apresentar um site com uma unica tela no qual serve como um lista para controle de biblioteca de jogos, tendo o jogo, o local comprado e o valor comprado para controle do usuário.

## Como executar

Antes de começar é importante que o usuario possua Python instalado no computador (https://www.python.org/downloads/).
Será necessário ter todas as libs python listadas no `requirements.txt` instaladas.
Após clonar o repositório, é necessário ir ao diretório raiz, pelo terminal, para poder executar os comandos descritos abaixo.
obs: vale observer o endereço representado no terminal pois deve terminar com "meu_app_api".

> É fortemente indicado o uso de ambientes virtuais do tipo [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).

```
antes da instalação dos requirements é necessario rodar 2 comando para ativar a pasta env na qual os requirements serão instalados. (Os comando que serão indicados foram rodados no windows, caso esteja rodando pelo linux pode possuir alguma mudança na nomeclatura)
Comando para criar a pasta env no diretorio:
    python3 -m venv env

Comando para a ativar a pasta env:
    env/Scripts/activate

Comando para instalar os requirements:
    (env)$ pip install -r requirements.txt
```

Este comando instala as dependências/bibliotecas, descritas no arquivo `requirements.txt`.

Para executar a API basta executar:

```
(env)$ flask run --host 0.0.0.0 --port 5000
```

Em modo de desenvolvimento é recomendado executar utilizando o parâmetro reload, que reiniciará o servidor
automaticamente após uma mudança no código fonte.

```
(env)$ flask run --host 0.0.0.0 --port 5000 --reload
```

Abra o [http://localhost:5000/#/](http://localhost:5000/#/) no navegador para verificar o status da API em execução.
