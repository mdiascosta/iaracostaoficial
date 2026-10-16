/* ============================================================================
   IARA COSTA · BLOCO A (Etapa E1) · header.js
   Header: menu mobile e faixa de busca.
   ----------------------------------------------------------------------------
   O que faz:
   - Menu mobile: abre e fecha, fecha com ESC, prende o foco dentro do painel
     e devolve o foco para o botão que abriu.
   - Faixa de busca: a lupa abre a faixa abaixo do header, o foco vai para o
     campo, ESC e clique fora fecham, e a lupa recebe o foco de volta.
   Requisitos atendidos: 7.2 e 10.2 do dossiê (focus-visible, ESC, trap, teclado).
   Não usa bibliotecas. Carregado com defer.
   ========================================================================= */

(function () {
  'use strict';

  /* Cada melhoria do cabeçalho inicia isolada.
     Esta melhoria inicia isolada: se ela falhar, as outras continuam
     de pé (mesma ideia do safeInit do template do zip). */
  try {
    var toggle = document.querySelector('.nav-toggle');
    var panel = document.getElementById('menu-mobile');
    var closeBtn = panel ? panel.querySelector('.mobile-panel__close') : null;

    if (!toggle || !panel) { return; }

    var FOCUSABLE = 'a[href], button:not([disabled]), input:not([disabled]), select, textarea, [tabindex]:not([tabindex="-1"])';
    var lastFocused = null;

    function focusableItems() {
      return Array.prototype.filter.call(
        panel.querySelectorAll(FOCUSABLE),
        function (el) { return el.offsetParent !== null || el === document.activeElement; }
      );
    }

    function isOpen() {
      return !panel.hasAttribute('hidden');
    }

    function open() {
      lastFocused = document.activeElement;
      panel.removeAttribute('hidden');
      toggle.setAttribute('aria-expanded', 'true');
      toggle.setAttribute('aria-label', 'Fechar menu de navegação');
      document.body.classList.add('is-locked');
      var items = focusableItems();
      if (items.length) { items[0].focus(); }
    }

    function close(returnFocus) {
      if (!isOpen()) { return; }
      panel.setAttribute('hidden', '');
      toggle.setAttribute('aria-expanded', 'false');
      toggle.setAttribute('aria-label', 'Abrir menu de navegação');
      document.body.classList.remove('is-locked');
      if (returnFocus !== false) {
        var target = lastFocused && document.contains(lastFocused) ? lastFocused : toggle;
        target.focus();
      }
    }

    toggle.addEventListener('click', function () {
      if (isOpen()) { close(); } else { open(); }
    });

    if (closeBtn) {
      closeBtn.addEventListener('click', function () { close(); });
    }

    panel.addEventListener('click', function (event) {
      var link = event.target.closest('a[href]');
      if (link) {
        close(false);
      }
    });

    document.addEventListener('keydown', function (event) {
      if (!isOpen()) { return; }

      if (event.key === 'Escape') {
        event.preventDefault();
        close();
        return;
      }

      if (event.key === 'Tab') {
        var items = focusableItems();
        if (!items.length) { return; }
        var first = items[0];
        var last = items[items.length - 1];

        if (event.shiftKey && document.activeElement === first) {
          event.preventDefault();
          last.focus();
        } else if (!event.shiftKey && document.activeElement === last) {
          event.preventDefault();
          first.focus();
        }
      }
    });

    /* Botão flutuante ilustrativo: não deve capturar clique nem foco */
    document.addEventListener('click', function (event) {
      var floating = event.target.closest('.whats-float');
      if (floating) { event.preventDefault(); }
    });

    /* Ao passar para o layout de desktop (>=1021px), o painel mobile sai de cena.
       A verificação de suporte evita quebrar o arquivo inteiro em navegadores
       antigos ou ambientes de teste. */
    if (typeof window.matchMedia === 'function') {
      var desktop = window.matchMedia('(min-width: 1021px)');
      var onChange = function (event) { if (event.matches) { close(false); } };

      if (typeof desktop.addEventListener === 'function') {
        desktop.addEventListener('change', onChange);
      } else if (typeof desktop.addListener === 'function') {
        desktop.addListener(onChange);
      }
    }
  } catch (erro) {
    if (window.console && console.warn) {
      console.warn('[iara-header] melhoria não inicializada:', erro);
    }
  }
})();

/* ============================================================================
   FAIXA DE BUSCA
   A lupa é a única coisa visível na barra. Ao clicar nela, a faixa abre logo
   abaixo do header (sobre o conteúdo, sem empurrar a página) e o foco vai
   direto para o campo. Fecha com ESC, com o botão de fechar e ao clicar fora.
   ========================================================================= */
(function () {
  'use strict';

  /* Cada melhoria do cabeçalho inicia isolada.
     Esta melhoria inicia isolada: se ela falhar, as outras continuam
     de pé (mesma ideia do safeInit do template do zip). */
  try {
    var toggleSearch = document.querySelector('[data-search-toggle]');
    var panel = document.getElementById('busca-painel');

    if (!toggleSearch || !panel) { return; }

    var closeBtn = panel.querySelector('[data-search-close]');
    var input = panel.querySelector('[data-search-input]');

    function isOpen() { return !panel.hasAttribute('hidden'); }

    function openSearch() {
      panel.removeAttribute('hidden');
      toggleSearch.setAttribute('aria-expanded', 'true');

      /* Espera o próximo quadro para o foco cair com a faixa já visível */
      window.requestAnimationFrame(function () {
        if (input) { input.focus(); }
      });
    }

    function closeSearch(returnFocus) {
      if (!isOpen()) { return; }

      panel.setAttribute('hidden', '');
      toggleSearch.setAttribute('aria-expanded', 'false');

      if (returnFocus !== false) { toggleSearch.focus(); }
    }

    toggleSearch.addEventListener('click', function () {
      if (isOpen()) { closeSearch(); } else { openSearch(); }
    });

    if (closeBtn) {
      closeBtn.addEventListener('click', function () { closeSearch(); });
    }

    document.addEventListener('keydown', function (event) {
      if (event.key === 'Escape' && isOpen()) {
        event.preventDefault();
        closeSearch();
      }
    });

    document.addEventListener('click', function (event) {
      if (!isOpen()) { return; }

      var insidePanel = panel.contains(event.target);
      var onToggle = toggleSearch.contains(event.target);

      if (!insidePanel && !onToggle) { closeSearch(false); }
    });
  } catch (erro) {
    if (window.console && console.warn) {
      console.warn('[iara-header] melhoria não inicializada:', erro);
    }
  }
})();
