(function(){
  // Elementos das telas
  const authScreen = document.getElementById("auth-screen");
  const appScreen = document.getElementById("app-screen");
  const tabL = document.getElementById("tab-login");
  const tabC = document.getElementById("tab-cadastro");
  const fL = document.getElementById("form-login");
  const fC = document.getElementById("form-cadastro");
  const titulo = document.getElementById("titulo");
  const sub = document.getElementById("sub");
  const logoutBtn = document.getElementById("logout-btn");

  // Alternar entre abas "Entrar" e "Criar conta"
  function alternarAba(modoLogin) {
    tabL.setAttribute("aria-selected", modoLogin);
    tabC.setAttribute("aria-selected", !modoLogin);
    fL.hidden = !modoLogin;
    fC.hidden = modoLogin;
    titulo.textContent = modoLogin ? "Entrar" : "Criar conta";
    sub.textContent = modoLogin ? "Acesse sua conta para continuar." : "Preencha seus dados para começar.";
  }

  if (tabL && tabC) {
    tabL.addEventListener("click", () => alternarAba(true));
    tabC.addEventListener("click", () => alternarAba(false));
  }

  // Mostrar/Ocultar Senha
  document.querySelectorAll(".ver").forEach(btn => {
    btn.addEventListener("click", () => {
      const input = btn.previousElementSibling;
      const mostrar = input.type === "password";
      input.type = mostrar ? "text" : "password";
      btn.textContent = mostrar ? "Ocultar" : "Mostrar";
    });
  });

  // Ação ao Entrar/Cadastrar -> Exibe a Tela da Câmera
  function entrarNoSistema(e) {
    e.preventDefault();
    authScreen.classList.add("hidden");
    appScreen.classList.remove("hidden");
  }

  if (fL) fL.addEventListener("submit", entrarNoSistema);
  if (fC) fC.addEventListener("submit", entrarNoSistema);

  if (logoutBtn) {
    logoutBtn.addEventListener("click", () => {
      stopCamera();
      appScreen.classList.add("hidden");
      authScreen.classList.remove("hidden");
    });
  }

  // Elementos da Câmera
  const video = document.getElementById('video');
  const photo = document.getElementById('photo');
  const canvas = document.getElementById('canvas');
  const msg = document.getElementById('msg');
  const startBtn = document.getElementById('start');
  const snapBtn = document.getElementById('snap');
  const flipBtn = document.getElementById('flip');
  const retakeBtn = document.getElementById('retake');
  const downloadLink = document.getElementById('download');

  // Elementos do Resultado
  const resultContainer = document.getElementById('result-container');
  const resClass = document.getElementById('res-class');
  const resCientific = document.getElementById('res-cientific');
  const resDangerLevel = document.getElementById('res-danger-level');
  const resDangerType = document.getElementById('res-danger-type');
  const resExtinction = document.getElementById('res-extinction');
  const resFirstAid = document.getElementById('res-first-aid');
  const resTypeSalineSolution = document.getElementById('res-type-saline-solution');
  const resLegalProtection = document.getElementById('res-legal-protection');
  const resLegalInfo = document.getElementById('res-legal-info');

  let stream = null;
  let facingMode = 'user';

  async function startCamera() {
    stopCamera();
    if (resultContainer) resultContainer.classList.add('hidden');

    try {
      stream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode, width: { ideal: 1280 }, height: { ideal: 960 } },
        audio: false
      });

      video.srcObject = stream;
      video.classList.remove('hidden');
      photo.classList.add('hidden');
      snapBtn.disabled = false;
      flipBtn.disabled = false;
      startBtn.classList.add('hidden');
      retakeBtn.classList.add('hidden');
      downloadLink.classList.add('hidden');
      msg.textContent = 'Câmera ativa. Clique em “Tirar foto”.';
    } catch (err) {
      msg.textContent = err.name === 'NotAllowedError'
        ? 'Acesso negado. Permita o uso da câmera nas configurações do navegador.'
        : 'Não foi possível abrir a câmera: ' + err.message;
    }
  }

  function stopCamera() {
    if (stream) {
      stream.getTracks().forEach(t => t.stop());
      stream = null;
    }
  }

  async function sendImageToBackend(blob) {
    msg.textContent = 'Analisando imagem...';
    resultContainer.classList.add('hidden');

    const formData = new FormData();
    formData.append('file', blob, 'captura.png');

    try {
      const response = await fetch('/model', {
        method: 'POST',
        body: formData
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || data.error || `Erro HTTP ${response.status}`);
      }

      if (data.success && data.prediction) {
        resClass.textContent = data.prediction.nome_popular;
        resCientific.textContent = data.prediction.nome_cientifico;
        resDangerLevel.textContent = data.prediction.nivel_perigo;
        resDangerType.textContent = data.prediction.tipo_perigo;
        resExtinction.textContent = data.prediction.status_extincao;
        resFirstAid.textContent = data.prediction.primeiros_socorros;
        resTypeSalineSolution.textContent = data.prediction.tipo_soro;
        resLegalProtection.textContent = data.prediction.protegido_por_lei;
        resLegalInfo.textContent = data.prediction.info_legal;
        resultContainer.classList.remove('hidden');

        msg.textContent = 'Análise concluída!';
      } else {
        msg.textContent = 'Erro no processamento: ' + (data.error || 'Resposta sem classificação.');
      }
    } catch (err) {
      console.error('Erro ao enviar imagem:', err);
      msg.textContent = 'Falha na análise: ' + err.message;
    }
  }

  function takePhoto() {
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height);

    const dataUrl = canvas.toDataURL('image/png');
    photo.src = dataUrl;
    downloadLink.href = dataUrl;

    video.classList.add('hidden');
    photo.classList.remove('hidden');
    downloadLink.classList.remove('hidden');
    retakeBtn.classList.remove('hidden');
    snapBtn.disabled = true;
    flipBtn.disabled = true;
    stopCamera();

    canvas.toBlob((blob) => {
      if (blob) {
        sendImageToBackend(blob);
      } else {
        msg.textContent = 'Erro ao gerar imagem para envio.';
      }
    }, 'image/png');
  }

  if (startBtn) startBtn.addEventListener('click', startCamera);
  if (retakeBtn) retakeBtn.addEventListener('click', startCamera);
  if (snapBtn) snapBtn.addEventListener('click', takePhoto);
  if (flipBtn) {
    flipBtn.addEventListener('click', () => {
      facingMode = facingMode === 'user' ? 'environment' : 'user';
      startCamera();
    });
  }
})();