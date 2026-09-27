from django.conf import settings
from django.core.files.storage import FileSystemStorage


def protegido():
    return FileSystemStorage(location=settings.ARQUIVOS_PROTEGIDOS)