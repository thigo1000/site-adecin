from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = 'ADECIN Nova Jerusalém'
admin.site.site_title = 'ADECIN'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('agenda/', include('agenda.urls')),
    path ('galeria/', include('galeria.urls')),
    path('ebd/', include('ebd.urls')),
    path('curso/', include('cursos.urls')),
    path('conta/', include('usuario.urls')),
    path('conta/', include('django.contrib.auth.urls')),
    path('gabinete/', include('gabinete.urls')),
    path('pgm/', include('pgm.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
