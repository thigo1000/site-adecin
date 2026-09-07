# ADECIN Nova Jerusalém

Site institucional de uma igreja, com área de membros, cursos em vídeo com
controle de acesso e agendamento pastoral. Construído em Django, do modelo de
dados ao HTML.

Projeto real, em uso pela igreja.

---

## O que o site faz

| Área | Descrição |
|---|---|
| **Home** | Mural de anúncios em carrossel, alimentado pelas artes que a igreja já projeta no telão |
| **Agenda** | Programação semanal fixa e datas especiais do mês |
| **Galeria** | Álbuns de fotos por culto, com vídeo do YouTube embutido |
| **EBD** | Tema do trimestre, turmas por faixa etária e material em PDF |
| **Cursos** | Aulas em vídeo com três níveis de acesso e material de apoio |
| **Área do membro** | Cadastro validado por CPF, login e recuperação de senha |
| **Gabinete** | Agendamento de atendimento com o pastor |

---

## Decisões técnicas

### Controle de acesso em três níveis

Cada curso escolhe como se comporta: **público**, **membro** ou **restrito**.
A regra vive num método do próprio model, não espalhada pelas views:

```python
def pode_ver_aula(self, user, aula):
    if self.acesso == self.Acesso.PUBLICO:
        return True
    if self.acesso == self.Acesso.MEMBRO:
        return aula.gratis or user.is_authenticated
    return user.is_authenticated and self.liberados.filter(pk=user.pk).exists()
```

A política de acesso pertence ao curso; a aula é apenas um parâmetro da decisão.
Isso mantém view e template ignorantes da regra — eles só perguntam.

O modo **membro** libera as aulas marcadas como amostra para qualquer visitante,
o que serve de prévia sem abrir o curso inteiro.

### Restrição única com condição

Um horário do gabinete não pode ter dois agendamentos. Mas um agendamento
cancelado pelo membro devolve o horário para a fila — e `unique_together`
não sabe disso.

```python
constraints = [
    models.UniqueConstraint(
        fields=['data', 'horario'],
        condition=Q(status__in=['ativo', 'cancelado_pastor']),
        name='um_agendamento_por_horario',
    )
]
```

Vira um índice parcial no banco: a unicidade só vale entre os registros que
de fato ocupam o horário. A garantia é do banco, não da aplicação — dois
cliques simultâneos não furam a regra.

### Arquivos protegidos fora do MEDIA_ROOT

Material de curso e da EBD é restrito a membros. Esconder o botão no template
não protege nada: a URL em `/media/` continua servindo o arquivo, e em
produção quem serve nem é o Django.

Os PDFs gravam num diretório próprio, com `FileSystemStorage`:

```python
protegido = FileSystemStorage(location=settings.ARQUIVOS_PROTEGIDOS)
```

O download passa por uma view que confere autenticação e acesso ao curso antes
de devolver um `FileResponse`. Não existe caminho até o arquivo que escape
dessa checagem.

### Dados derivados não são gravados

O pastor cadastra uma **janela** de atendimento — quarta, das 13h às 16h. Os
horários de uma hora que cabem nela são calculados, não persistidos:

```python
while hora + 1 <= self.fim.hour:
    vagas.append(...)
```

Se ele editar a janela, não há registros órfãos para reconciliar. Mesma lógica
vale para a contagem de fotos de um álbum e de aulas de um curso.

### Invariantes no `clean()`

Regras que o banco não expressa ficam no `clean()` do model, onde valem para
o admin e para qualquer formulário:

- Só um trimestre da EBD pode estar ativo
- Janelas de atendimento não podem se sobrepor no mesmo dia
- Um membro não tem dois agendamentos ativos ao mesmo tempo

### Autenticação: aproveitar o que o Django já resolve

Login, logout e recuperação de senha usam as views do `django.contrib.auth`.
A customização entra por formulário, não por reescrita:

```python
path('login/', LoginView.as_view(authentication_form=LoginForms), name='login')
```

O `LoginForms` só normaliza o username com `.strip().lower()`, para que
`Thiago` e `thiago` sejam a mesma conta. Toda a mecânica de sessão, CSRF e
`?next=` continua sendo do framework.

O cadastro, esse sim, é próprio — porque a regra é de domínio: **só quem já
está na lista de membros da igreja pode criar conta**. O fluxo tem duas etapas,
ligadas por sessão: verificação de CPF e criação de acesso.

### Upload em lote no admin

Cada culto rende cinquenta fotos ou mais. Cadastrar uma a uma é inviável, e
o admin não tem upload múltiplo pronto — o `ClearableFileInput` recusa
`multiple` desde o Django 5.

A solução usa a extensão documentada do widget, com um `FileField` que valida
lista em vez de arquivo único. O ponto crítico está na leitura:

```python
arquivos = request.FILES.getlist('imagens')
```

`request.FILES` é um `MultiValueDict`: acessar por chave devolveria apenas o
último arquivo, em silêncio.

As imagens são redimensionadas no `save()` do model com Pillow. Uma foto de
celular sai de 3 MB para cerca de 70 KB.

---

## Stack

- Django 6.1 · Python 3.14
- SQLite em desenvolvimento, PostgreSQL como alvo de produção
- Pillow para processamento de imagem
- HTML e CSS sem framework, com sistema de tokens em `:root`
- JavaScript apenas onde acrescenta conforto — o site funciona sem ele

---

## Rodando localmente

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

O `settings.py` espera uma `SECRET_KEY` e as pastas `media/` e `protegido/`,
criadas no primeiro upload.

---

## O que ainda falta

Honestamente, o projeto não está terminado:

- **Testes.** Nenhum escrito ainda. É a próxima prioridade, com pytest-django
- **Deploy.** Roda apenas em desenvolvimento; falta PostgreSQL, SMTP e servir estáticos
- **Arquivos órfãos.** Excluir uma foto remove o registro, não o arquivo. Falta um sinal `post_delete`
- **Consultas N+1** na listagem de álbuns, resolvíveis com `annotate`
