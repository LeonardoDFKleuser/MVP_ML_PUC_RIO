function newGame() {
  const gameName = document.getElementById("newGameName").value;
  const platform = document.getElementById("newPlatform").value;
  const store = document.getElementById("newStore").value;
  const price = document.getElementById("newPrice").value;

  // Capturando valores dos novos campos
  const genresSelect = document.getElementById("newGenres");
  const categoriesSelect = document.getElementById("newCategories");

  // Captura as opções selecionadas para genres e categories
  const genres = Array.from(genresSelect.selectedOptions).map(
    (option) => option.value
  );
  const categories = Array.from(categoriesSelect.selectedOptions).map(
    (option) => option.value
  );

  // Criação do objeto jogo
  const newGame = {
    nome: gameName,
    plataforma: platform,
    loja: store,
    preco: parseFloat(price),
    genres: genres, // Gêneros capturados
    categories: categories, // Categorias capturadas
  };

  // Enviando dados para a API
  fetch("http://localhost:5000/jogo", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(newGame),
  })
    .then((response) => response.json())
    .then((data) => {
      // Atualiza a tabela com o novo jogo
      if (data.message) {
        console.error(data.message);
      } else {
        addGameToTable(data);
      }
    })
    .catch((error) => {
      console.error("Erro:", error);
    });
}

function addGameToTable(game) {
  const table = document.getElementById("myGamesBody");
  const row = table.insertRow();
  row.insertCell(0).textContent = game.nome;
  row.insertCell(1).textContent = game.plataforma;
  row.insertCell(2).textContent = game.loja;
  row.insertCell(3).textContent = game.preco;
  row.insertCell(4).textContent = game.faixa_predita; // Mostrando a faixa de preço
  row.insertCell(5).innerHTML =
    '<img src=".imgicons8-lixo.svg" width="15px" height="15px" alt="Delete" onclick="deleteGame(' +
    game.id +
    ')">';
}

function deleteGame(gameId) {
  fetch(`http://localhost:5000/jogo?id=${gameId}`, {
    method: "DELETE",
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.message) {
        console.log(data.message);
      } else {
        document.getElementById(`game-row-${gameId}`).remove();
      }
    })
    .catch((error) => {
      console.error("Erro ao remover jogo:", error);
    });
}
