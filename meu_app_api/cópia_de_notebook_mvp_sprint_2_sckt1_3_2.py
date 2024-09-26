# configuração para não exibir os warnings
import warnings
warnings.filterwarnings("ignore")

# Imports necessários
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.model_selection import train_test_split, KFold, cross_val_score, GridSearchCV
from sklearn.metrics import accuracy_score
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeClassifier
from pickle import dump, load

"""## Carga do Dataset"""

# URL do dataset Steam
url = "https://raw.githubusercontent.com/LeonardoDFKleuser/MVP_ML_PUC_RIO/main/meu_app_api/database/steam.csv"

# Lê o arquivo
df = pd.read_csv(url, delimiter=',')

# Mostra as primeiras linhas do dataset
df.head()

"""## Separação em conjunto de treino e conjunto de teste com holdout"""

# Definir o tamanho do conjunto de teste e a semente aleatória
test_size = 0.20  # Mudança para 20% de dados de teste
seed = 7

# Recarregar o dataset e garantir que as colunas estejam disponíveis
input_columns = ['genres', 'categories']
output_column = 'price'

# Transformar as colunas de entrada (genres, categories) em representações numéricas
X = pd.get_dummies(df[input_columns], drop_first=True)

# Definir a coluna de saída (price)
y = df[output_column]

# Definir as faixas de preço
price_bins = [0, 5, 15, np.inf]  # Faixas de preço: até 5, entre 5 e 15, e acima de 15
price_labels = ['Baixo', 'Médio', 'Alto']  # Nome das categorias

# Criar a coluna de categorias de preços
y_class = pd.cut(y, bins=price_bins, labels=price_labels)

# Verificar e tratar NaNs
print(f"Valores NaN em y_class: {y_class.isna().sum()}")  # Ver quantos valores NaN existem
y_class = y_class.fillna('Baixo')  # Preencher valores NaN com a categoria 'Baixo'

# Dividir em treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y_class, test_size=test_size, shuffle=True, random_state=seed)

# Escalar os dados de entrada
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

"""## Modelagem e Inferência"""

# Criar e treinar o modelo de árvore de decisão
model = DecisionTreeClassifier()
model.fit(X_train_scaled, y_train)

# Avaliar a acurácia no conjunto de treino e teste
train_accuracy = model.score(X_train_scaled, y_train)
test_accuracy = model.score(X_test_scaled, y_test)

print(f"Acurácia no conjunto de treino: {train_accuracy:.3f}")
print(f"Acurácia no conjunto de teste: {test_accuracy:.3f}")

"""## Otimização dos Hiperparâmetros"""

# Definir o KFold com 5 divisões
kfold = KFold(n_splits=5, shuffle=True, random_state=seed)

# Definir o grid de parâmetros para DecisionTreeClassifier
param_grid = {
    'max_depth': [5, 10, 15, 20, None],
    'min_samples_split': [2, 10, 20],
    'min_samples_leaf': [1, 5, 10]
}

# Executar o GridSearchCV
grid = GridSearchCV(estimator=model, param_grid=param_grid, scoring='accuracy', cv=kfold)
grid.fit(X_train_scaled, y_train)

# Imprimir a melhor configuração encontrada
print(f"Melhor configuração: {grid.best_score_:.3f} usando {grid.best_params_}")

# Atualizar o modelo com os melhores parâmetros
model = grid.best_estimator_

"""## Salvamento do Modelo"""

# Padronizar todo o conjunto de dados para treinar o modelo final
scaler_final = StandardScaler().fit(X)  # Ajustar o scaler com TODO o dataset
X_scaled = scaler_final.transform(X)

# Remover valores ausentes (NaNs)
mask = ~y_class.isna()
X_clean = X_scaled[mask]
y_clean = y_class[mask]

# Treinar o modelo final com todos os dados
model.fit(X_clean, y_clean)

# Salvar o modelo e o scaler
model_path = 'ml_model/steam_model.pkl'
scaler_path = 'ml_model/steam_scaler.pkl'

# Salvar o modelo e o scaler em arquivos pickle
with open(model_path, 'wb') as model_file:
    dump(model, model_file)

with open(scaler_path, 'wb') as scaler_file:
    dump(scaler_final, scaler_file)

print(f"Modelo e scaler salvos com sucesso!")

"""## Teste com novos dados"""

# Simular a predição de novos dados
data = {
    'genres': ['Action', 'Adventure'],
    'categories': ['Multi-player', 'Co-op']
}

# Criar um DataFrame com os novos dados
entrada = pd.DataFrame(data)

# Transformar as colunas de entrada em dummies (igual ao que foi feito no treinamento)
entrada_transformada = pd.get_dummies(entrada, drop_first=True)

# Garantir que as colunas de 'entrada_transformada' coincidam com as colunas usadas no treinamento
entrada_transformada = entrada_transformada.reindex(columns=X.columns, fill_value=0)

# Padronizar os novos dados usando o scaler treinado
entrada_scaled = scaler_final.transform(entrada_transformada)

# Fazer a predição
predictions = model.predict(entrada_scaled)

# Mostrar as predições
print(f"Predições para os novos dados: {predictions}")
