import qrcode

# Dados que você quer inserir no QR code
data = "https://www.seusite.com"

# Criar o objeto QR code
qr = qrcode.QRCode(
    version=2,  # Tamanho do QR Code (quanto maior o número, mais complexo)
    error_correction=qrcode.constants.ERROR_CORRECT_L,  # Correção de erro (L: 7% de recuperação)
    box_size=10,  # Tamanho de cada caixa do QR code
    border=4,  # Tamanho da borda ao redor do QR code
)

# Adicionar os dados ao QR code
qr.add_data(data)
qr.make(fit=True)

# Criar a imagem do QR code
img = qr.make_image(fill='black', back_color='white')

# Salvar a imagem em um arquivo
img.save("qrcode.png")
