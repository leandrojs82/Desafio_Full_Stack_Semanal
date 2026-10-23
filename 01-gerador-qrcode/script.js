
const formulario = document.getElementById("form-qrcode");
const campoTexto = document.getElementById("texto");
const areaQrCode = document.getElementById("qrcode");
const tamanhoEscolhido = document.getElementById("tamanho");
const botaoDownload = document.getElementById("baixar-qrcode");

// EVENTO 1 — GERAR QR CODE
formulario.addEventListener("submit", function (event) {
    event.preventDefault();

    // Recupera o texto informado
    const valorDigitado = campoTexto.value.trim();

    // Valida o texto
    if (valorDigitado === "") {
        alert("Digite um texto ou URL válido");
        return;
    }

    // Recupera o tamanho selecionado
    const tamanhoSelecionado = Number(tamanhoEscolhido.value);

    // Desabilita o download durante a geração
    botaoDownload.disabled = true;

    // Remove o QR Code anterior
    areaQrCode.innerHTML = "";

    // Gera o novo QR Code
    new QRCode(areaQrCode, {
        text: valorDigitado,
        width: tamanhoSelecionado,
        height: tamanhoSelecionado,
        colorDark: "#000000",
        colorLight: "#ffffff",
        correctLevel: QRCode.CorrectLevel.H
    });

    // Habilita o botão de download
    botaoDownload.disabled = false;

    console.log("QR Code gerado:", valorDigitado);
    console.log("Botão habilitado:", !botaoDownload.disabled);
});

// EVENTO 2 — BAIXAR QR CODE EM PNG
botaoDownload.addEventListener("click", function () {

    const imagem = areaQrCode.querySelector("img");
    const canvas = areaQrCode.querySelector("canvas");

    let enderecoImagem = "";

    // Prioriza a imagem gerada pela biblioteca
    if (
        imagem &&
        imagem.complete &&
        imagem.naturalWidth > 0 &&
        imagem.src.startsWith("data:image/png")
    ) {
        enderecoImagem = imagem.src;

    // Alternativa: utiliza o canvas
    } else if (canvas && canvas.width > 0 && canvas.height > 0) {
        enderecoImagem = canvas.toDataURL("image/png");
    }

    // Verifica se existe uma imagem válida
    if (!enderecoImagem) {
        alert("Não foi possível preparar o QR Code para download.");
        return;
    }

    // Cria um link temporário
    const link = document.createElement("a");

    link.href = enderecoImagem;
    link.download = "meu-qrcode.png";

    // Executa o download
    document.body.appendChild(link);
    link.click();
    link.remove();

    console.log("Download do QR Code solicitado.");
});
