/* ============================================================================
   IARA COSTA · BLOCO A (Etapa E1) · filtros.js
   Loja: filtros laterais (categoria, preço, cor, tamanho) e ordenação,
   tudo sem recarregar a página.
   ----------------------------------------------------------------------------
   Como funciona: os cards já estão no HTML e trazem as informações em
   atributos (data-categoria, data-cores, data-tamanhos, data-preco). Este
   arquivo só esconde o que não combina com os filtros escolhidos e reordena
   o que sobra.

   No Bloco B este arquivo NÃO é usado: quem faz este trabalho é o widget de
   filtragem do WooCommerce, com os mesmos campos na mesma coluna.
   ========================================================================= */

(function () {
  'use strict';

  /* A loja inteira depende deste arquivo: filtro, ordenação e contagem.
     Esta melhoria inicia isolada: se ela falhar, as outras continuam
     de pé (mesma ideia do safeInit do template do zip). */
  try {
    var grid = document.querySelector('[data-shop-grid]');
    if (!grid) { return; }

    var cards = Array.prototype.slice.call(grid.querySelectorAll('[data-categoria]'));
    var categorias = Array.prototype.slice.call(document.querySelectorAll('[data-facet="categoria"]'));
    var cores = Array.prototype.slice.call(document.querySelectorAll('[data-facet="cor"]'));
    var tamanhos = Array.prototype.slice.call(document.querySelectorAll('[data-facet="tamanho"]'));
    var precoMin = document.querySelector('[data-facet="preco-min"]');
    var precoMax = document.querySelector('[data-facet="preco-max"]');
    var limparBotoes = Array.prototype.slice.call(document.querySelectorAll('[data-filters-clear]'));
    var alternarFiltros = document.querySelector('[data-filters-toggle]');
    var insignia = document.querySelector('[data-filters-badge]');
    var painel = document.getElementById('filtros-loja');
    var sort = document.querySelector('[data-sort]');
    var count = document.querySelector('[data-count]');
    var vazio = document.querySelector('[data-shop-empty]');

    /* ------------------------------------------------------------- LEITURA */

    function marcados(lista) {
      return lista.filter(function (campo) { return campo.checked; })
                  .map(function (campo) { return campo.value; });
    }

    function numero(campo, padrao) {
      if (!campo) { return padrao; }
      var valor = parseFloat(String(campo.value).replace(',', '.'));
      return isNaN(valor) ? padrao : valor;
    }

    function precoDo(card) {
      return parseFloat(card.dataset.preco || '0');
    }

    function listaDe(card, atributo) {
      return (card.dataset[atributo] || '').split(' ').filter(Boolean);
    }

    /* Tem interseção? Usado quando o cliente marca mais de uma opção: vale
       qualquer uma delas (OU dentro do grupo, E entre os grupos). */
    function cruza(escolhidos, doCard) {
      if (!escolhidos.length) { return true; }
      return escolhidos.some(function (item) { return doCard.indexOf(item) !== -1; });
    }

    /* -------------------------------------------------------------- FILTRO */

    function combina(card) {
      var preco = precoDo(card);

      if (!cruza(marcados(categorias), listaDe(card, 'categoria'))) { return false; }
      if (!cruza(marcados(cores), listaDe(card, 'cores'))) { return false; }
      if (!cruza(marcados(tamanhos), listaDe(card, 'tamanhos'))) { return false; }

      if (precoMin && preco < numero(precoMin, 0)) { return false; }
      if (precoMax && preco > numero(precoMax, Infinity)) { return false; }

      return true;
    }

    /* ------------------------------------------------------------ ORDENAR */

    function ordenar(lista) {
      var ordem = sort ? sort.value : 'destaque';
      var copia = lista.slice();

      if (ordem === 'preco-asc') {
        copia.sort(function (a, b) { return precoDo(a) - precoDo(b); });
      } else if (ordem === 'preco-desc') {
        copia.sort(function (a, b) { return precoDo(b) - precoDo(a); });
      } else if (ordem === 'nome') {
        copia.sort(function (a, b) {
          return (a.dataset.nome || '').localeCompare(b.dataset.nome || '', 'pt-BR');
        });
      } else {
        copia.sort(function (a, b) {
          return parseInt(a.dataset.ordem || '0', 10) - parseInt(b.dataset.ordem || '0', 10);
        });
      }

      copia.forEach(function (card) { grid.appendChild(card); });
    }

    /* ------------------------------------------------------- CONTADOR/AVISO */

    function contarAtivos() {
      return categorias.concat(cores, tamanhos).filter(function (campo) {
        return campo.checked;
      }).length;
    }

    function render() {
      var visiveis = cards.filter(combina);

      cards.forEach(function (card) {
        card.classList.toggle('is-hidden', visiveis.indexOf(card) === -1);
      });

      ordenar(visiveis);

      if (count) {
        count.textContent = visiveis.length === 1
          ? '1 peça encontrada'
          : visiveis.length + ' peças encontradas';
      }

      if (vazio) {
        if (visiveis.length === 0) { vazio.removeAttribute('hidden'); }
        else { vazio.setAttribute('hidden', ''); }
      }

      var ativos = contarAtivos();

      if (insignia) {
        if (ativos > 0) {
          insignia.textContent = '(' + ativos + ')';
          insignia.removeAttribute('hidden');
        } else {
          insignia.setAttribute('hidden', '');
        }
      }
    }

    /* --------------------------------------------------------------- EVENTOS */

    categorias.concat(cores, tamanhos).forEach(function (campo) {
      campo.addEventListener('change', render);
    });

    [precoMin, precoMax].forEach(function (campo) {
      if (!campo) { return; }
      campo.addEventListener('input', render);
      /* Ao sair do campo, valores fora da faixa do catálogo voltam ao limite */
      campo.addEventListener('blur', function () {
        var valor = numero(campo, null);
        if (valor === null) { return; }
        if (valor < 0) { campo.value = '0'; }
        render();
      });
    });

    if (sort) { sort.addEventListener('change', render); }

    limparBotoes.forEach(function (botao) {
      botao.addEventListener('click', function () {
        categorias.concat(cores, tamanhos).forEach(function (campo) { campo.checked = false; });
        if (precoMin) { precoMin.value = '149'; }
        if (precoMax) { precoMax.value = '789'; }
        render();

        var primeiro = categorias[0] || cores[0] || tamanhos[0];
        if (primeiro && botao.closest('.state')) { primeiro.focus(); }
      });
    });

    /* No celular e no tablet a coluna de filtros vira gaveta */
    if (alternarFiltros && painel) {
      alternarFiltros.addEventListener('click', function () {
        var aberto = painel.classList.toggle('filters--open');
        alternarFiltros.setAttribute('aria-expanded', aberto ? 'true' : 'false');
      });
    }

    render();
  } catch (erro) {
    if (window.console && console.warn) {
      console.warn('[iara-filtros] melhoria não inicializada:', erro);
    }
  }
})();
