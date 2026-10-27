(function(){
  const video = document.getElementById('video');
  const photo = document.getElementById('photo');
  const canvas = document.getElementById('canvas');
  const msg = document.getElementById('msg');
  const startBtn = document.getElementById('start');
  const snapBtn = document.getElementById('snap');
  const flipBtn = document.getElementById('flip');
  const retakeBtn = document.getElementById('retake');
  const downloadLink = document.getElementById('download');

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

      if (video) {
        video.srcObject = stream;
        video.classList.remove('hidden');
      }
      if (photo) photo.classList.add('hidden');
      if (snapBtn) snapBtn.disabled = false;
      if (flipBtn) flipBtn.disabled = false;
      if (startBtn) startBtn.classList.add('hidden');
      if (retakeBtn) retakeBtn.classList.add('hidden');
      if (downloadLink) downloadLink.classList.add('hidden');
      if (msg) msg.textContent = 'Câmera ativa. Clique em “Tirar foto”.';
    } catch (err) {
      if (msg) {
        msg.textContent = err.name === 'NotAllowedError'
          ? 'Acesso negado. Permita o uso da câmera nas configurações do navegador.'
          : 'Não foi possível abrir a câmera: ' + err.message;
      }
    }
  }

  function stopCamera() {
    if (stream) {
      stream.getTracks().forEach(t => t.stop());
      stream = null;
    }
  }

  async function sendImageToBackend(blob) {
    if (msg) msg.textContent = 'Analisando imagem...';
    if (resultContainer) resultContainer.classList.add('hidden');

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
        if (resClass) resClass.textContent = data.prediction.nome_popular || '-';
        if (resCientific) resCientific.textContent = data.prediction.nome_cientifico || '-';
        if (resDangerLevel) resDangerLevel.textContent = data.prediction.nivel_perigo || '-';
        if (resDangerType) resDangerType.textContent = data.prediction.tipo_perigo || '-';
        if (resExtinction) resExtinction.textContent = data.prediction.status_extincao || '-';
        if (resFirstAid) resFirstAid.textContent = data.prediction.primeiros_socorros || '-';
        if (resTypeSalineSolution) resTypeSalineSolution.textContent = data.prediction.tipo_soro || '-';
        if (resLegalProtection) resLegalProtection.textContent = data.prediction.protegido_por_lei || '-';
        if (resLegalInfo) resLegalInfo.textContent = data.prediction.info_legal || '-';
        
        if (resultContainer) resultContainer.classList.remove('hidden');
        if (msg) msg.textContent = 'Análise concluída!';
      } else if (data.low_confidence) {
        if (resultContainer) resultContainer.classList.add('hidden');
        if (msg) msg.textContent = data.error;
      } else {
        if (msg) msg.textContent = 'Erro no processamento: ' + (data.error || 'Resposta sem classificação.');
      }
    } catch (err) {
      console.error('Erro ao enviar imagem:', err);
      if (msg) msg.textContent = 'Falha na análise: ' + err.message;
    }
  }

  function takePhoto() {
    if (!video || !canvas) return;
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height);

    const dataUrl = canvas.toDataURL('image/png');
    if (photo) photo.src = dataUrl;
    if (downloadLink) downloadLink.href = dataUrl;

    video.classList.add('hidden');
    if (photo) photo.classList.remove('hidden');
    if (downloadLink) downloadLink.classList.remove('hidden');
    if (retakeBtn) retakeBtn.classList.remove('hidden');
    if (snapBtn) snapBtn.disabled = true;
    if (flipBtn) flipBtn.disabled = true;
    stopCamera();

    canvas.toBlob((blob) => {
      if (blob) {
        sendImageToBackend(blob);
      } else {
        if (msg) msg.textContent = 'Erro ao gerar imagem para envio.';
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