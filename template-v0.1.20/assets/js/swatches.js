/* ============================================================================
   IARA COSTA · BLOCO A (Etapa E1) · swatches.js
   Página de produto: galeria, seleção de tamanho e cor, quantidade e abas.
   Também é o arquivo do acordeão (perguntas frequentes e ficha do produto).

   Regras do dossiê atendidas:
   - Nada só por cor: a opção escolhida aparece escrita (7.6).
   - Toda opção é um botão de verdade, com aria-pressed e área de toque 44px.
   - O anúncio da troca de opção vai para uma região aria-live (leitor de tela).

   v0.1.11 — duas coisas vieram do swatches/header.js do template do zip:
   1. Cada melhoria inicia isolada (seguro), então uma falha não derruba as
      outras. Antes, um erro na galeria deixava o acordeão sem funcionar.
   2. O seletor de quantidade confere o mínimo e o máximo e avisa a página com
      um evento "change", que é o que o WooCommerce escuta no carrinho.

   No Bloco B (Elementor) este arquivo NÃO é usado: quem faz isso é o plugin de
   variações aprovado + widgets do WooCommerce.
   ========================================================================= */

(function () {
  'use strict';

  /* Cada melhoria roda isolada: uma falha não leva as outras junto. */
  function seguro(nome, fn) {
    try {
      fn();
    } catch (erro) {
      if (window.console && console.warn) {
        console.warn('[iara-produto] "' + nome + '" não foi inicializada:', erro);
      }
    }
  }

  /* ------------------------------------------------------------ 1. Galeria */
  function initGaleria() {
    var mainImage = document.querySelector('[data-gallery-main]');
    var thumbs = document.querySelectorAll('[data-gallery-thumb]');

    if (!mainImage || !thumbs.length) { return; }

    Array.prototype.forEach.call(thumbs, function (thumb) {
      thumb.addEventListener('click', function () {
        var img = thumb.querySelector('img');
        if (!img) { return; }

        mainImage.src = img.dataset.full || img.src;
        mainImage.alt = img.alt;

        Array.prototype.forEach.call(thumbs, function (other) {
          other.setAttribute('aria-current', other === thumb ? 'true' : 'false');
        });
      });
    });
  }

  /* ---------------------------------------------------------- 2. Opções */
  function initOpcoes() {
    var groups = document.querySelectorAll('[data-option-group]');

    Array.prototype.forEach.call(groups, function (group) {
      var label = group.dataset.optionLabel || 'Opção';
      var output = group.querySelector('[data-option-output]');
      var hidden = group.querySelector('input[type="hidden"]');
      var buttons = group.querySelectorAll('.swatch');

      Array.prototype.forEach.call(buttons, function (button) {
        button.addEventListener('click', function () {
          if (button.disabled) { return; }

          Array.prototype.forEach.call(buttons, function (other) {
            other.setAttribute('aria-pressed', other === button ? 'true' : 'false');
          });

          var value = button.dataset.value || button.textContent.trim();

          if (output) {
            output.textContent = label + ' selecionado: ' + value;
          }
          if (hidden) {
            hidden.value = value;
          }
          /* Anúncio para leitores de tela */
          if (output && output.hasAttribute('data-live')) {
            output.setAttribute('aria-live', 'polite');
          }
        });
      });
    });
  }

  /* -------------------------------------------------------- 3. Quantidade */
  function initQuantidade() {
    var qtyInput = document.querySelector('[data-qty-input]');
    if (!qtyInput) { return; }

    var minimo = parseInt(qtyInput.getAttribute('min') || '1', 10);
    var maximo = parseInt(qtyInput.getAttribute('max') || '10', 10);

    function ajustar(valor) {
      if (isNaN(valor)) { valor = minimo; }
      var dentro = Math.min(maximo, Math.max(minimo, valor));
      qtyInput.value = String(dentro);
      /* O WooCommerce reage ao evento change, não ao clique no botão. */
      qtyInput.dispatchEvent(new Event('change', { bubbles: true }));
    }

    function step(delta) {
      ajustar((parseInt(qtyInput.value, 10) || minimo) + delta);
    }

    var minus = document.querySelector('[data-qty-minus]');
    var plus = document.querySelector('[data-qty-plus]');

    if (minus) { minus.addEventListener('click', function () { step(-1); }); }
    if (plus) { plus.addEventListener('click', function () { step(1); }); }

    /* Digitação à mão: mesma conferência que o carrinho do WooCommerce faz. */
    qtyInput.addEventListener('change', function () {
      ajustar(parseInt(qtyInput.value, 10));
    });
  }

  /* -------------------------------------------------------------- 4. Abas */
  function initAbas() {
    var tablist = document.querySelector('[data-tabs]');
    if (!tablist) { return; }

    var tabs = Array.prototype.slice.call(tablist.querySelectorAll('[role="tab"]'));

    function selectTab(tab, setFocus) {
      tabs.forEach(function (item) {
        var selected = item === tab;
        item.setAttribute('aria-selected', selected ? 'true' : 'false');
        item.setAttribute('tabindex', selected ? '0' : '-1');

        var panel = document.getElementById(item.getAttribute('aria-controls'));
        if (panel) { panel.hidden = !selected; }
      });

      if (setFocus) { tab.focus(); }
    }

    tabs.forEach(function (tab, index) {
      tab.addEventListener('click', function () { selectTab(tab, false); });

      tab.addEventListener('keydown', function (event) {
        var target = null;

        if (event.key === 'ArrowRight') { target = tabs[(index + 1) % tabs.length]; }
        if (event.key === 'ArrowLeft') { target = tabs[(index - 1 + tabs.length) % tabs.length]; }
        if (event.key === 'Home') { target = tabs[0]; }
        if (event.key === 'End') { target = tabs[tabs.length - 1]; }

        if (target) {
          event.preventDefault();
          selectTab(target, true);
        }
      });
    });
  }

  /* ------------------------------------------- 5. Acordeão (FAQ e produto) */
  function initAcordeao() {
    var accordions = document.querySelectorAll('[data-accordion]');

    Array.prototype.forEach.call(accordions, function (accordion) {
      var buttons = accordion.querySelectorAll('.accordion__button');

      Array.prototype.forEach.call(buttons, function (button) {
        button.addEventListener('click', function () {
          var expanded = button.getAttribute('aria-expanded') === 'true';
          var panel = document.getElementById(button.getAttribute('aria-controls'));

          button.setAttribute('aria-expanded', expanded ? 'false' : 'true');
          if (panel) {
            if (expanded) { panel.setAttribute('hidden', ''); } else { panel.removeAttribute('hidden'); }
          }
        });
      });
    });
  }

  /* ------------------------------------------------------------ INÍCIO */
  seguro('galeria', initGaleria);
  seguro('opcoes', initOpcoes);
  seguro('quantidade', initQuantidade);
  seguro('abas', initAbas);
  seguro('acordeao', initAcordeao);
})();
