from PIL import Image


def redimensionar(caminho, largura, altura):
    imagem = Image.open(caminho)
    imagem.thumbnail((largura, altura))
    imagem.save(caminho)