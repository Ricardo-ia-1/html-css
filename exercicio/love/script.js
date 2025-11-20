function abrirCarta() {
  document.querySelector(".envelope").style.display = "none";
  document.getElementById("mensagem").style.display = "flex";
}

function revelarMensagem() {
  const senha = document.getElementById("senha").value.toLowerCase();
  const segredo = "thays"; // Palavra mágica correta

  if (senha === segredo) {
    const msg = document.getElementById("thays");
    msg.style.opacity = 1;
    msg.innerText = "🌹 Vou caçar mais um milhão de vagalumes por ai pra ti ver sorrir, eu posso colorir o céu de outra cor, eu só quero amar você e quando amanhecer eu quero acorda do seu lado...🌹";
  } else {
    alert("Essa não é a palavra mágica... tente de novo 💔");
    alert("Dica: tem cinco letras, e é tudo minusculo. 💖");
  }
}
function fecharMensagem() {
  document.getElementById("mensagem").style.display = "none";
  document.querySelector(".envelope").style.display = "flex";
  document.getElementById("senha").value = "";
  const msg = document.getElementById("thays");
  msg.style.opacity = 0;
  msg.innerText = "";
}
