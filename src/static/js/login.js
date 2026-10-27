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

const formLogin = document.getElementById('form-login');
const loginMsg = formLogin.querySelector('.msg');
const loginBtn = formLogin.querySelector('.go');

function mostrarErro(texto) {
  loginMsg.textContent = texto;
  loginMsg.hidden = false;

  // Reinicia a animação para o erro chamar atenção a cada tentativa
  loginMsg.style.animation = 'none';
  loginMsg.offsetHeight; // força o reflow
  loginMsg.style.animation = '';
}

function limparErro() {
  loginMsg.textContent = '';
  loginMsg.hidden = true;
}

async function enviarLogin(event) {
  event.preventDefault(); // impede o envio padrão do formulário
  limparErro();

  const email = formLogin.querySelector('[name="email"]').value.trim();
  const senha = formLogin.querySelector('[name="password"]').value;

  if (!email || !senha) {
    mostrarErro('Preencha o e-mail e a senha.');
    return;
  }

  loginBtn.disabled = true;
  loginBtn.textContent = 'Entrando...';

  try {
    const resposta = await fetch('/login', {
      method: 'POST',
      body: new FormData(formLogin),
    });

    const dados = await resposta.json();

    if (dados.success) {
      // Troque pela rota que você quiser após o login
      window.location.href = dados.redirect || '/';
      return;
    }

    mostrarErro(dados.message || 'E-mail ou senha incorretos. Tente novamente.');
  } catch (erro) {
    console.error('Erro no login:', erro);
    mostrarErro('Não foi possível conectar ao servidor. Tente novamente.');
  } finally {
    loginBtn.disabled = false;
    loginBtn.textContent = 'Entrar';
  }
}

formLogin.addEventListener('submit', enviarLogin);

// Some o erro assim que o usuário voltar a digitar
formLogin.addEventListener('input', limparErro);