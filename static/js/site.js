/* Menu mobile ------------------------------------------------------------ */

const toggle = document.querySelector('.nav-toggle');
const links  = document.querySelector('.nav-links');

if (toggle && links) {
  toggle.addEventListener('click', () => {
    const aberto = links.classList.toggle('open');
    toggle.setAttribute('aria-expanded', aberto);
    toggle.setAttribute('aria-label', aberto ? 'Fechar menu' : 'Abrir menu');
  });

  // Fecha ao clicar em um link (navegação dentro da mesma página)
  links.addEventListener('click', (e) => {
    if (e.target.tagName === 'A') {
      links.classList.remove('open');
      toggle.setAttribute('aria-expanded', 'false');
      toggle.setAttribute('aria-label', 'Abrir menu');
    }
  });
}


/* Revelação das seções ao rolar ------------------------------------------ */

const els = document.querySelectorAll('.reveal');

if ('IntersectionObserver' in window) {
  const io = new IntersectionObserver((entries) => {
    entries.forEach(e => { if (e.isIntersecting) e.target.classList.add('in'); });
  }, { threshold: 0.15 });
  els.forEach(el => io.observe(el));
} else {
  els.forEach(el => el.classList.add('in'));
}


/* Mural de anúncios ------------------------------------------------------

   O HTML já vem completo do Django: um slide por anúncio publicado.
   O JS só controla qual está visível. Se o JS não carregar, o primeiro
   slide continua aparecendo — o mural degrada para uma imagem estática
   em vez de sumir.
------------------------------------------------------------------------- */

const mural = document.querySelector('.mural');

if (mural) {
  const trilho = mural.querySelector('.mural__trilho');
  const slides = mural.querySelectorAll('.mural__slide');
  const pontos = mural.querySelectorAll('.mural__ponto');
  const anterior = mural.querySelector('.mural__seta--ant');
  const proximo  = mural.querySelector('.mural__seta--prox');

  // Com um anúncio só não há o que girar: esconde os controles.
  if (slides.length < 2) {
    mural.querySelectorAll('.mural__seta, .mural__pontos')
         .forEach(el => el.hidden = true);
  } else {
    const INTERVALO = 6000;
    let atual = 0;
    let timer = null;

    // Respeita quem pediu menos animação no sistema operacional.
    const semMovimento = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    function mostrar(i) {
      atual = (i + slides.length) % slides.length;
      trilho.style.transform = `translateX(-${atual * 100}%)`;

      slides.forEach((slide, n) => {
        // Slide fora de vista não deve ser lido nem receber foco por Tab.
        slide.setAttribute('aria-hidden', n !== atual);
      });
      pontos.forEach((ponto, n) => {
        ponto.classList.toggle('ativo', n === atual);
        ponto.setAttribute('aria-current', n === atual);
      });
    }

    function iniciar() {
      if (semMovimento) return;
      parar();
      timer = setInterval(() => mostrar(atual + 1), INTERVALO);
    }
    function parar() { clearInterval(timer); }

    // Interação do usuário reinicia a contagem — senão o slide troca
    // no meio da leitura logo depois do clique.
    function irPara(i) { mostrar(i); iniciar(); }

    if (proximo)  proximo.addEventListener('click',  () => irPara(atual + 1));
    if (anterior) anterior.addEventListener('click', () => irPara(atual - 1));
    pontos.forEach((ponto, i) => ponto.addEventListener('click', () => irPara(i)));

    // Pausa no hover e quando algo dentro do mural recebe foco pelo teclado.
    mural.addEventListener('mouseenter', parar);
    mural.addEventListener('mouseleave', iniciar);
    mural.addEventListener('focusin',  parar);
    mural.addEventListener('focusout', iniciar);

    // Pausa com a aba em segundo plano.
    document.addEventListener('visibilitychange', () => {
      document.hidden ? parar() : iniciar();
    });

    // Setas do teclado quando o mural está em foco.
    mural.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowRight') irPara(atual + 1);
      if (e.key === 'ArrowLeft')  irPara(atual - 1);
    });

    mostrar(0);
    iniciar();
  }
}


/* Gabinete — troca de dia ------------------------------------------------

   Sem JavaScript todos os painéis aparecem empilhados, e a página continua
   utilizável: os horários estão lá e o formulário envia igual. O script só
   acrescenta o comportamento de aba.
------------------------------------------------------------------------- */

const dias = document.querySelectorAll('.dia');

if (dias.length) {
  const paineis = document.querySelectorAll('.painel');

  dias.forEach(botao => {
    botao.addEventListener('click', () => {
      const alvo = botao.dataset.dia;

      dias.forEach(b => {
        const ativo = b === botao;
        b.classList.toggle('dia--ativo', ativo);
        b.setAttribute('aria-selected', ativo);
      });

      paineis.forEach(p => {
        p.classList.toggle('painel--oculto', p.dataset.dia !== alvo);
      });
    });
  });
}

/* PGM — filtro por bairro ------------------------------------------------

   Os bairros vêm do banco, então nenhuma lista fica fixa aqui: o script
   compara o data-bairro do botão com o do card. Sem JavaScript todos os
   grupos continuam visíveis e a página segue utilizável.
------------------------------------------------------------------------- */

const filtros = document.querySelectorAll('.filtro__item');

if (filtros.length) {
  const grupos = document.querySelectorAll('.grupo');
  const semNada = document.querySelector('.grupos__vazio');

  filtros.forEach(botao => {
    botao.addEventListener('click', () => {
      const alvo = botao.dataset.bairro;

      filtros.forEach(b => b.classList.toggle('filtro__item--ativo', b === botao));

      let visiveis = 0;

      grupos.forEach(card => {
        const mostra = alvo === 'todos' || card.dataset.bairro === alvo;
        card.classList.toggle('grupo--oculto', !mostra);
        if (mostra) visiveis += 1;
      });

      if (semNada) semNada.hidden = visiveis > 0;
    });
  });
}