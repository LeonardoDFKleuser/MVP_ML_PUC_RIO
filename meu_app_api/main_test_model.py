# Imports necessários
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score
from sklearn.tree import DecisionTreeClassifier  # Caso o modelo não seja importado de um arquivo
from pickle import load

np.random.seed(7)  # Definindo uma semente global

# Referência ao Dataset Steam
dataset_url = "meu_app_api\database\steam.csv"  # Altere para o caminho correto do seu dataset Steam

# Lê o arquivo
dataset = pd.read_csv(dataset_url, delimiter=',')

# Transforma o dataset em um array
array = dataset.values

# Definir as colunas de entrada (variáveis preditoras) e a coluna alvo (price ou categorizada)
input_columns = ['genres', 'categories']  # As colunas que serão usadas como preditores
output_column = 'price'  # A coluna alvo (faixas de preço)

# Transformar as colunas de entrada em variáveis dummificadas (necessário para o modelo)
X = pd.get_dummies(dataset[input_columns], drop_first=True).values  # As variáveis preditoras
Y = pd.cut(dataset[output_column], bins=[0, 5, 15, np.inf], labels=['Baixo', 'Médio', 'Alto']).values  # Faixas de preço como alvo

# Carregar o modelo salvo
ml_path = 'ml_model/steam_model.pkl'  # Caminho do modelo salvo (alterar conforme necessário)
modelo = load(open(ml_path, 'rb'))  # Carrega o modelo treinado

# Realiza predição dos resultados com base no modelo
prediction = modelo.predict(X)

# Definição da classe para manipular o dataset
class Dataset:

    @staticmethod
    def getNoe() -> int:
        """Verifica o número total de elementos (noe) registrados no dataset."""
        get_noe = len(X)
        return get_noe

    @staticmethod
    def getPop() -> float:
        """Verifica o percentual de resultados positivos (quando Y == 'Alto') registrados no dataset."""
        positive_outcomes = sum(Y == 'Alto')
        get_pop = positive_outcomes / len(Y)
        return get_pop


# Definição da classe para testar o modelo
class TestModel:

    @staticmethod
    def get_acc() -> float:
        """Verifica o valor da acurácia do modelo."""
        accuracy = accuracy_score(Y, prediction)
        return accuracy
    
    @staticmethod
    def get_recall() -> float:
        """Verifica o valor de 'recall' do modelo."""
        recall = recall_score(Y, prediction, average='macro')
        return recall
    
    @staticmethod
    def get_precision() -> float:
        """Verifica o valor de precisão do modelo."""
        precision = precision_score(Y, prediction, average='macro')
        return precision

    @staticmethod
    def f1_score() -> float:
        """Verifica o valor de "f1_score" do modelo."""
        f1 = f1_score(Y, prediction, average='macro')
        return f1


# Exemplo de uso
print(f"Total de elementos no dataset: {Dataset.getNoe()}")
print(f"Percentual de jogos na faixa 'Alto': {Dataset.getPop() * 100:.2f}%")

print(f"Acurácia do modelo: {TestModel.get_acc():.3f}")
print(f"Recall do modelo: {TestModel.get_recall():.3f}")
print(f"Precisão do modelo: {TestModel.get_precision():.3f}")
print(f"F1 Score do modelo: {TestModel.f1_score():.3f}")
