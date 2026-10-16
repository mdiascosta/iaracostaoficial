/* ============================================================================
   IARA COSTA · BLOCO A (Etapa E1) · artigo.js
   Página do artigo do diário (post.html): o que dá vida ao layout novo.

   1. Barra de progresso da leitura, no alto do artigo.
   2. Índice "Neste texto": marca em qual seção o leitor está.
   3. Botão "Copiar link", que copia o endereço do artigo.

   Nada aqui é obrigatório para ler a página: se o JavaScript não carregar, o
   texto continua inteiro, o índice continua sendo uma lista de atalhos e a
   barra fica escondida. No Bloco B o artigo é um template do Elementor, e este
   arquivo não vai para o WordPress.
   ========================================================================= */

(function () {
  'use strict';

  try {
    var artigo = document.querySelector('[data-post-artigo]');
    if (!artigo) { return; }

    var reduzirMovimento = window.matchMedia
      ? window.matchMedia('(prefers-reduced-motion: reduce)').matches
      : false;

    /* ------------------------------------------------ 1. BARRA DE PROGRESSO */

    var barra = document.querySelector('[data-post-progress]');
    var preenchimento = document.querySelector('[data-post-progress-fill]');

    function atualizarProgresso() {
      if (!barra || !preenchimento) { return; }

      var alturaJanela = window.innerHeight || document.documentElement.clientHeight;
      var inicio = artigo.offsetTop;
      var altura = artigo.offsetHeight;

      /* Sem layout medido (ou artigo curto), a barra não tem o que mostrar. */
      if (!altura || altura <= alturaJanela) {
        barra.setAttribute('hidden', '');
        return;
      }

      var andado = (window.pageYOffset || document.documentElement.scrollTop || 0) - inicio;
      var total = altura - alturaJanela;
      var razao = total > 0 ? andado / total : 0;

      razao = Math.max(0, Math.min(1, razao));
      barra.removeAttribute('hidden');
      preenchimento.style.width = (razao * 100).toFixed(2) + '%';
      barra.setAttribute('aria-hidden', 'true');
    }

    var agendado = false;
    function agendar() {
      if (agendado) { return; }
      agendado = true;
      window.requestAnimationFrame(function () {
        agendado = false;
        atualizarProgresso();
      });
    }

    if (barra && preenchimento) {
      window.addEventListener('scroll', agendar, { passive: true });
      window.addEventListener('resize', agendar);
      atualizarProgresso();
    }

    /* ------------------------------------------- 2. ÍNDICE QUE ACOMPANHA */

    var indice = document.querySelector('[data-post-indice]');
    var secoes = Array.prototype.slice.call(artigo.querySelectorAll('.prose > h2[id]'));

    function marcarAtual(id) {
      if (!indice) { return; }
      Array.prototype.forEach.call(indice.querySelectorAll('a'), function (link) {
        if (link.getAttribute('href') === '#' + id) { link.setAttribute('aria-current', 'true'); }
        else { link.removeAttribute('aria-current'); }
      });
    }

    if (indice && secoes.length && 'IntersectionObserver' in window) {
      var visiveis = {};

      var observador = new IntersectionObserver(function (entradas) {
        entradas.forEach(function (entrada) {
          if (entrada.isIntersecting) { visiveis[entrada.target.id] = true; }
          else { delete visiveis[entrada.target.id]; }
        });

        /* Vale a seção visível mais próxima do topo da janela; se nenhuma
           estiver visível (entre duas seções), o índice fica como estava. */
        var atual = null;
        secoes.forEach(function (secao) {
          if (!visiveis[secao.id] || atual) { return; }
          atual = secao.id;
        });

        if (atual) { marcarAtual(atual); }
      }, { rootMargin: '-25% 0px -55% 0px' });

      secoes.forEach(function (secao) { observador.observe(secao); });
      marcarAtual(secoes[0].id);
    }

    /* ------------------------------------------------- 3. COPIAR O LINK */

    var botaoCopiar = artigo.querySelector('[data-copy-link]');
    if (botaoCopiar && navigator.clipboard && navigator.clipboard.writeText) {
      botaoCopiar.addEventListener('click', function () {
        navigator.clipboard.writeText(window.location.href).then(function () {
          botaoCopiar.textContent = reduzirMovimento ? 'Link copiado' : 'Link copiado ✓';
        }, function () {
          botaoCopiar.textContent = 'Não foi possível copiar';
        });
      });
    } else if (botaoCopiar) {
      /* Navegador sem área de transferência: o botão sai do caminho em vez de
         prometer algo que não acontece. */
      botaoCopiar.setAttribute('hidden', '');
    }
  } catch (erro) {
    if (window.console && console.warn) {
      console.warn('[iara-artigo] melhoria não inicializada:', erro);
    }
  }
})();
