from django.shortcuts import render, get_object_or_404
from galeria.models import Album

def album(request, id):
    galeria = get_object_or_404(Album, pk=id)
    foto = galeria.fotos.all()
    video = galeria.videos.all()
    return render(request, 'midia_album.html', {
        'album': galeria,
        'fotos': foto,
        'videos': video,
    })
def galeria(request):
    lista_album = Album.objects.all()
    return render(request, 'midia_lista.html', {'albuns': lista_album})