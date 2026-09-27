from PIL import Image, ImageOps


def redimensionar(caminho, largura, altura):
    imagem = ImageOps.exif_transpose(Image.open(caminho))
    imagem.thumbnail((largura, altura))
    imagem.save(caminho)