/*
  Função para obter uma lista existente no servidor preenchida previamente via requisição GET
*/
const getList = () => {
  let url = "http://127.0.0.1:5000/jogos";  // Certifique-se de que o endpoint está correto
  fetch(url, {
    method: "get",
  })
    .then((response) => {
      if (response.status != 200) {
        throw response.json();  // Atualiza para verificar o status da resposta
      }
      return response.json();
    })
    .then((data) => {
      // Garante que a lista de jogos está no formato esperado
      if (data.jogos && Array.isArray(data.jogos)) {
        data.jogos.forEach((item) =>
          insertList(item.nome, item.plataforma, item.loja, item.preco, item.faixa_predita, item.id)  // Adiciona faixa_predita e id corretamente
        );
      } else {
        console.error("Formato de resposta inesperado:", data);
        alert("Erro ao carregar a lista de jogos");
      }
    })
    .catch((error) => {
      console.error("Erro ao carregar lista de jogos:", error);
      alert("Erro ao carregar lista de jogos");
    });
};

/*
  Chamada da função para carregamento inicial dos dados
*/
document.addEventListener("DOMContentLoaded", () => {
  getList();  // Carregar a lista de jogos ao carregar a página
});

/*
  Evento para exibição da lista de opções de loja com base na plataforma selecionada
*/
document.getElementById("newPlatform").addEventListener("change", function (event) {
  let Loja = document.getElementById("newStore");

  // Limpar as opções de loja anteriores
  while (Loja.options.length > 0) {
    Loja.remove(0);
  }

  if (!event.target.value) {
    let lojaOption = document.createElement("option");
    lojaOption.innerText = "Loja";
    Loja.appendChild(lojaOption);
    return;
  }

  // Adiciona as lojas com base na plataforma selecionada
  for (const [plataforma, lojas] of Object.entries(Plataforma)) {
    if (plataforma == event.target.value) {
      for (const loja of lojas) {
        let lojaOption = document.createElement("option");
        lojaOption.innerText = loja;
        lojaOption.value = loja;
        Loja.appendChild(lojaOption);
      }
    }
  }
});

/*
  Função para inserir itens na lista apresentada
*/
const insertList = (gameName, gamePlatform, gameStore, gamePrice, gamePriceRange, gameId) => {
  let tableBody = document.getElementById("myGamesBody");
  let row = document.createElement("tr");

  let gameNameCell = document.createElement("td");
  gameNameCell.innerText = gameName;

  let gamePlatformCell = document.createElement("td");
  gamePlatformCell.innerText = gamePlatform;

  let gameStoreCell = document.createElement("td");
  gameStoreCell.innerText = gameStore;

  let gamePriceCell = document.createElement("td");
  gamePriceCell.innerText = gamePrice;

  let gamePriceRangeCell = document.createElement("td");
  gamePriceRangeCell.innerText = gamePriceRange;

  let gameDeleteCell = document.createElement("td");
  gameDeleteCell.innerHTML = "&times;";
  gameDeleteCell.setAttribute("class", "delete-item");
  gameDeleteCell.addEventListener("click", () => deleteItem(gameId, row));

  row.appendChild(gameNameCell);
  row.appendChild(gamePlatformCell);
  row.appendChild(gameStoreCell);
  row.appendChild(gamePriceCell);
  row.appendChild(gamePriceRangeCell);
  row.appendChild(gameDeleteCell);

  tableBody.appendChild(row);
};

/*
  Função para colocar um item na lista do servidor via requisição POST
*/
const postItem = (gameName, gamePlatform, gameStore, gamePrice) => {
  const formData = new FormData();
  formData.append("nome", gameName);
  formData.append("plataforma", gamePlatform);
  formData.append("loja", gameStore);
  formData.append("preco", gamePrice);

  let url = "http://127.0.0.1:5000/jogo";  // Certifique-se de que o endpoint está correto
  fetch(url, {
    method: "post",
    body: formData,
  })
    .then((response) => {
      if (response.status != 200) {
        if (response.body) {
          throw response.json();
        }
        throw response;
      }
      return response.json();
    })
    .then((data) => {
      // Inserir o jogo na tabela, incluindo a faixa de preço prevista
      insertList(gameName, gamePlatform, gameStore, gamePrice, data.faixa_predita, data.id);
      alert("Jogo adicionado!");
    })
    .catch(async (data) => {
      let error = await data;
      console.error("Error:", error);
      alert(`Erro no cadastro: ${error.message}`);
    });
};

// Função que é chamada quando o botão de adicionar é clicado
const newGame = () => {
  let gameName = document.getElementById("newGameName").value;
  let gamePlatform = document.getElementById("newPlatform").value;
  let gameStore = document.getElementById("newStore").value;
  let gamePrice = document.getElementById("newPrice").value;

  if (!gameName) {
    alert("Escreva o nome de um jogo!");
    return;
  } else if (isNaN(parseFloat(gamePrice))) {
    alert("Preço precisa ser um número!");
    return;
  } else {
    postItem(gameName, gamePlatform, gameStore, gamePrice);  // Chama a função para enviar o POST
  }
};

/*
  Função para deletar um item da lista do servidor via requisição DELETE
*/
const deleteItem = (item, row) => {
  let url = "http://127.0.0.1:5000/jogo?id=" + item;  // Certifique-se de que o ID está correto
  fetch(url, {
    method: "delete",
  })
    .then((response) => {
      if (response.status != 200) {
        throw response.body.message;
      }
      return response.json();
    })
    .then(() => {
      removeList(row);  // Remove a linha da tabela após exclusão
      alert("Jogo removido com sucesso!");
    })
    .catch((error) => {
      console.error("Error:", error);
    });
};

// Função auxiliar para remover o jogo da tabela após exclusão
const removeList = (row) => {
  let tableBody = document.getElementById("myGamesBody");
  tableBody.removeChild(row);
};

// Definição de Plataformas e Lojas para cadastro
let Plataforma = {
  Pc: [
    "Steam",
    "Epic",
    "Ea Play",
    "Ubisoft Connect",
    "Battle.net",
    "GOG",
    "Xbox",
    "Rockstar Laucher",
  ],
  Playstation: ["PlayStation Store"],
  Xbox: ["Microsoft Store"],
  Nintendo: ["Nintendo eShop"],
  Mobile: ["Play Store", "Apple Store"],
};
