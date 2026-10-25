(function(){
  var tabL = document.getElementById("tab-login"),
      tabC = document.getElementById("tab-cadastro"),
      fL = document.getElementById("form-login"),
      fC = document.getElementById("form-cadastro"),
      titulo = document.getElementById("titulo"),
      sub = document.getElementById("sub");

  function alternarAba(modoLogin) {
    tabL.setAttribute("aria-selected", modoLogin);
    tabC.setAttribute("aria-selected", !modoLogin);
    
    fL.hidden = !modoLogin;
    fC.hidden = modoLogin;

    if (modoLogin) {
      titulo.textContent = "Entrar";
      sub.textContent = "Acesse sua conta para continuar.";
    } else {
      titulo.textContent = "Criar conta";
      sub.textContent = "Preencha seus dados para começar.";
    }
  }

  tabL.addEventListener("click", function() { alternarAba(true); });
  tabC.addEventListener("click", function() { alternarAba(false); });

  var botoesVer = document.querySelectorAll(".ver");
  botoesVer.forEach(function(btn) {
    btn.addEventListener("click", function() {
      var input = btn.previousElementSibling;
      var mostrar = input.type === "password";
      
      input.type = mostrar ? "text" : "password";
      btn.textContent = mostrar ? "Ocultar" : "Mostrar";
      btn.setAttribute("aria-pressed", mostrar);
    });
  });
})();