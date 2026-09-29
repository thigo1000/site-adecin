from PIL import Image, ImageOps


def redimensionar(caminho, largura, altura):
    with Image.open(caminho) as original:
        imagem = ImageOps.exif_transpose(original)
        imagem.thumbnail((largura, altura))
        imagem.save(caminho, quality=85)