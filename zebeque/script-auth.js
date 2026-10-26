(function(){
  const tabL = document.getElementById("tab-login");
  const tabC = document.getElementById("tab-cadastro");
  const fL = document.getElementById("form-login");
  const fC = document.getElementById("form-cadastro");
  const titulo = document.getElementById("titulo");
  const sub = document.getElementById("sub");

  function alternarAba(modoLogin) {
    if (!tabL || !tabC) return;
    tabL.setAttribute("aria-selected", modoLogin);
    tabC.setAttribute("aria-selected", !modoLogin);
    if (fL) fL.hidden = !modoLogin;
    if (fC) fC.hidden = modoLogin;
    if (titulo) titulo.textContent = modoLogin ? "Entrar" : "Criar conta";
    if (sub) sub.textContent = modoLogin ? "Acesse sua conta para continuar." : "Preencha seus dados para começar.";
  }

  if (tabL && tabC) {
    tabL.addEventListener("click", () => alternarAba(true));
    tabC.addEventListener("click", () => alternarAba(false));
  }

  document.querySelectorAll(".ver").forEach(btn => {
    btn.addEventListener("click", () => {
      const input = btn.previousElementSibling;
      if (!input) return;
      const mostrar = input.type === "password";
      input.type = mostrar ? "text" : "password";
      btn.textContent = mostrar ? "Ocultar" : "Mostrar";
    });
  });

  function entrarNoSistema(e) {
    e.preventDefault();
    window.location.href = "camera.html";
  }

  if (fL) fL.addEventListener("submit", entrarNoSistema);
  if (fC) fC.addEventListener("submit", entrarNoSistema);
})();