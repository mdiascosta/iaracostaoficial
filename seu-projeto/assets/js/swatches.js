/* ============================================================================
   IARA COSTA · BLOCO A (Etapa E1) · swatches.js
   Página de produto: galeria, seleção de tamanho e cor, quantidade e abas.
   ----------------------------------------------------------------------------
   Regras do dossiê atendidas:
   - Nada só por cor: a opção escolhida aparece escrita (7.6).
   - Toda opção é um botão de verdade, com aria-pressed e área de toque 44px.
   - O anúncio da troca de opção vai para uma região aria-live (leitor de tela).
   No Bloco B (Elementor) este arquivo NÃO é usado: quem faz isso é o plugin de
   variações aprovado + widgets do WooCommerce.
   ========================================================================= */

(function () {
  'use strict';

  /* ------------------------------------------------------------ 1. Galeria */
  var mainImage = document.querySelector('[data-gallery-main]');
  var thumbs = document.querySelectorAll('[data-gallery-thumb]');

  Array.prototype.forEach.call(thumbs, function (thumb) {
    thumb.addEventListener('click', function () {
      var img = thumb.querySelector('img');
      if (!mainImage || !img) { return; }

      mainImage.src = img.dataset.full || img.src;
      mainImage.alt = img.alt;

      Array.prototype.forEach.call(thumbs, function (other) {
        other.setAttribute('aria-current', other === thumb ? 'true' : 'false');
      });
    });
  });

  /* ---------------------------------------------------------- 2. Opções */
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

  /* -------------------------------------------------------- 3. Quantidade */
  var qtyInput = document.querySelector('[data-qty-input]');

  if (qtyInput) {
    var step = function (delta) {
      var current = parseInt(qtyInput.value, 10);
      if (isNaN(current)) { current = 1; }
      var next = Math.min(10, Math.max(1, current + delta));
      qtyInput.value = String(next);
    };

    var minus = document.querySelector('[data-qty-minus]');
    var plus = document.querySelector('[data-qty-plus]');

    if (minus) { minus.addEventListener('click', function () { step(-1); }); }
    if (plus) { plus.addEventListener('click', function () { step(1); }); }
  }

  /* -------------------------------------------------------------- 4. Abas */
  var tablist = document.querySelector('[data-tabs]');

  if (tablist) {
    var tabs = Array.prototype.slice.call(tablist.querySelectorAll('[role="tab"]'));

    function selectTab(tab, setFocus) {
      tabs.forEach(function (item) {
        var selected = item === tab;
        item.setAttribute('aria-selected', selected ? 'true' : 'false');
        item.setAttribute('tabindex', selected ? '0' : '-1');

        var panel = document.getElementById(item.getAttribute('aria-controls'));
        if (panel) {
          if (selected) { panel.removeAttribute('hidden'); } else { panel.setAttribute('hidden', ''); }
        }
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
})();
