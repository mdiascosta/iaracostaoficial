/* ============================================================================
   IARA COSTA · BLOCO A (Etapa E1) · filtros.js
   Loja: filtro por categoria e ordenação simples, sem recarregar a página.
   ----------------------------------------------------------------------------
   Com 10 produtos não existe paginação (7.7). Este arquivo só esconde e ordena
   os cards já presentes no HTML, para a equipe validar o comportamento visual.
   No Bloco B quem faz isso é o widget de arquivo de produtos do WooCommerce.
   ========================================================================= */

(function () {
  'use strict';

  var grid = document.querySelector('[data-shop-grid]');
  if (!grid) { return; }

  var items = Array.prototype.slice.call(grid.querySelectorAll('[data-categoria]'));
  var chips = Array.prototype.slice.call(document.querySelectorAll('.filter-list [data-filter]'));
  /* Botões de "ver todas" fora da barra de filtros (estado vazio) */
  var resetButtons = Array.prototype.slice.call(document.querySelectorAll('[data-shop-empty] [data-filter]'));
  var sort = document.querySelector('[data-sort]');
  var count = document.querySelector('[data-count]');
  var empty = document.querySelector('[data-shop-empty]');

  var state = { categoria: 'todas', ordem: 'destaque' };

  function matches(item) {
    if (state.categoria === 'todas') { return true; }
    return (item.dataset.categoria || '').split(' ').indexOf(state.categoria) !== -1;
  }

  function price(item) {
    return parseFloat(item.dataset.preco || '0');
  }

  function sortItems(list) {
    var sorted = list.slice();

    if (state.ordem === 'preco-asc') {
      sorted.sort(function (a, b) { return price(a) - price(b); });
    } else if (state.ordem === 'preco-desc') {
      sorted.sort(function (a, b) { return price(b) - price(a); });
    } else if (state.ordem === 'nome') {
      sorted.sort(function (a, b) {
        return (a.dataset.nome || '').localeCompare(b.dataset.nome || '', 'pt-BR');
      });
    } else {
      sorted.sort(function (a, b) {
        return parseInt(a.dataset.ordem || '0', 10) - parseInt(b.dataset.ordem || '0', 10);
      });
    }

    sorted.forEach(function (item) { grid.appendChild(item); });
  }

  function render() {
    var visible = 0;

    items.forEach(function (item) {
      var show = matches(item);
      item.classList.toggle('is-hidden', !show);
      if (show) { visible += 1; }
    });

    sortItems(items.filter(matches));

    if (count) {
      count.textContent = visible === 1
        ? '1 peça encontrada'
        : visible + ' peças encontradas';
    }

    if (empty) {
      if (visible === 0) { empty.removeAttribute('hidden'); } else { empty.setAttribute('hidden', ''); }
    }
  }

  function setCategoria(categoria) {
    state.categoria = categoria;

    chips.forEach(function (chip) {
      chip.setAttribute('aria-pressed', chip.dataset.filter === categoria ? 'true' : 'false');
    });

    render();
  }

  chips.forEach(function (chip) {
    chip.addEventListener('click', function () { setCategoria(chip.dataset.filter); });
  });

  resetButtons.forEach(function (button) {
    button.addEventListener('click', function () {
      setCategoria('todas');
      var first = chips[0];
      if (first) { first.focus(); }
    });
  });

  if (sort) {
    sort.addEventListener('change', function () {
      state.ordem = sort.value;
      render();
    });
  }

  render();
})();
