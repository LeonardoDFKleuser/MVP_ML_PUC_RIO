/*
  --------------------------------------------------------------------------------------
  Função para obter uma lista existente no servidor preenchida preeviamente via requisição GET
  --------------------------------------------------------------------------------------
*/
const getList = () => {
  let url = "http://127.0.0.1:5000/jogos";
  fetch(url, {
    method: "get",
  })
    .then((response) => {
      if (response.status != 200) {
        throw response.body.message;
      }
      return response.json();
    })
    .then((data) => {
      data.jogos.forEach((item) =>
        insertList(item.nome, item.plataforma, item.loja, item.preco, item.id)
      );
    })
    .catch((error) => {
      console.error("Error:", error);
    });
};

/*
  --------------------------------------------------------------------------------------
  Chamada da função para carregamento inicial dos dados
  --------------------------------------------------------------------------------------
*/
document.addEventListener("DOMContentLoaded", () => {
  getList();
});

/*
    Definição de Plataformas e Lojas para cadastro
*/
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

/*
  Evento para exibição da lista de opções
  */

document
  .getElementById("newPlatform")
  .addEventListener("change", function (event) {
    let Loja = document.getElementById("newStore");
    while (Loja.options.length > 0) {
      Loja.remove(0);
    }
    if (!event.target.value) {
      let lojaOption = document.createElement("option");
      lojaOption.innerText = "Loja";
      Loja.appendChild(lojaOption);
      return;
    }

    for (const [chave, valor] of Object.entries(Plataforma)) {
      if (chave == event.target.value) {
        for (const loja of valor) {
          let lojaOption = document.createElement("option");
          lojaOption.innerText = loja;
          lojaOption.value = loja;
          Loja.appendChild(lojaOption);
        }
      }
    }
  });

/*
  --------------------------------------------------------------------------------------
  Função para inserir items na lista apresentada
  --------------------------------------------------------------------------------------
*/
const insertList = (gameName, gamePlatform, gameStore, gamePrice, gameId) => {
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

  let gameDeleteCell = document.createElement("td");
  gameDeleteCell.innerHTML = "&times;";
  gameDeleteCell.setAttribute("class", "delete-item");
  gameDeleteCell.addEventListener("click", () => deleteItem(gameId, row));

  row.appendChild(gameNameCell);
  row.appendChild(gamePlatformCell);
  row.appendChild(gameStoreCell);
  row.appendChild(gamePriceCell);
  row.appendChild(gameDeleteCell);

  tableBody.appendChild(row);

  document.getElementById("newGameName").value = "";
  document.getElementById("newPlatform").value = "";
  document.getElementById("newPrice").value = "";
};

/*
  --------------------------------------------------------------------------------------
  Função para colocar um item na lista do servidor via requisição POST
  --------------------------------------------------------------------------------------
*/
const postItem = (gameName, gamePlatform, gameStore, gamePrice) => {
  const formData = new FormData();
  formData.append("nome", gameName);
  formData.append("plataforma", gamePlatform);
  formData.append("loja", gameStore);
  formData.append("preco", gamePrice);

  let url = "http://127.0.0.1:5000/jogo";
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
      insertList(gameName, gamePlatform, gameStore, gamePrice, data.id);
      alert("Item adicionado!");
    })
    .catch(async (data) => {
      let error = await data;
      console.error("Error:", error);
      alert(`Erro no cadastro: ${error.message}`);
    });
};

/*
  --------------------------------------------------------------------------------------
  Função para adicionar um novo item com Nome, Plataforma, Loja e valor 
  --------------------------------------------------------------------------------------
*/
const newGame = () => {
  let gameName = document.getElementById("newGameName").value;
  let gamePlatform = document.getElementById("newPlatform").value;
  let gameStore = document.getElementById("newStore").value;
  let gamePrice = document.getElementById("newPrice").value;

  if (!gameName) {
    alert("Escreva o nome de um item!");
    return;
  } else if (isNaN(parseFloat(gamePrice))) {
    alert("Preço precisa ser um número!");
    return;
  } else {
    postItem(gameName, gamePlatform, gameStore, gamePrice);
  }
};

/*
  --------------------------------------------------------------------------------------
  Função para deletar um item da lista do servidor via requisição DELETE
  --------------------------------------------------------------------------------------
*/
const deleteItem = (item, row) => {
  let url = "http://127.0.0.1:5000/jogo?id=" + item;
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
      removeList(row);
      alert("Jogo foi removido com Sucesso!");
    })
    .catch((error) => {
      console.error("Error:", error);
    });
};

/*
  Função para remoção de lista 
*/

const removeList = (row) => {
  let tableBody = document.getElementById("myGamesBody");
  tableBody.removeChild(row);
};
