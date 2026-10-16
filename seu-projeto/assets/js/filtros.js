/* ============================================================================
   IARA COSTA · BLOCO A (Etapa E1) · filtros.js
   Loja: filtros laterais (categoria, preço, cor, tamanho), ordenação e
   paginação, tudo sem recarregar a página.
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
    var aplicarBotao = document.querySelector('[data-filters-apply]');
    var alternarFiltros = document.querySelector('[data-filters-toggle]');
    var insignia = document.querySelector('[data-filters-badge]');
    var painel = document.getElementById('filtros-loja');
    var sort = document.querySelector('[data-sort]');
    var count = document.querySelector('[data-count]');
    var vazio = document.querySelector('[data-shop-empty]');
    var paginacao = document.querySelector('[data-shop-pagination]');
    var faixa = document.querySelector('[data-shop-range]');

    /* Nove peças por página: é o número do zip (52 peças em 6 páginas). O Bloco B
       leva o mesmo valor para o "produtos por página" do WooCommerce. */
    var POR_PAGINA = 9;
    var pagina = 1;

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

    function notaDo(card) {
      return parseFloat(card.dataset.nota || '0');
    }

    function avaliacoesDo(card) {
      return parseInt(card.dataset.avaliacoes || '0', 10);
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

    /* As cinco formas de ordenar são as do zip, com os mesmos valores que o
       WooCommerce usa em "orderby": assim o Bloco B não precisa traduzir nada. */
    function ordenar(lista) {
      var ordem = sort ? sort.value : 'date';
      var copia = lista.slice();

      if (ordem === 'price') {
        copia.sort(function (a, b) { return precoDo(a) - precoDo(b); });
      } else if (ordem === 'price-desc') {
        copia.sort(function (a, b) { return precoDo(b) - precoDo(a); });
      } else if (ordem === 'rating') {
        copia.sort(function (a, b) {
          return notaDo(b) - notaDo(a) || avaliacoesDo(b) - avaliacoesDo(a);
        });
      } else if (ordem === 'popularity') {
        copia.sort(function (a, b) {
          return avaliacoesDo(b) - avaliacoesDo(a) || notaDo(b) - notaDo(a);
        });
      } else {
        copia.sort(function (a, b) {
          return parseInt(a.dataset.ordem || '0', 10) - parseInt(b.dataset.ordem || '0', 10);
        });
      }

      copia.forEach(function (card) { grid.appendChild(card); });

      return copia;
    }

    /* ---------------------------------------------------------- PAGINAÇÃO */

    function textoDaFaixa(total, inicio, naPagina) {
      if (total === 0) { return 'Nenhuma peça nesta seleção'; }
      if (total === 1) { return 'Mostrando 1 de 1 peça'; }
      return 'Mostrando ' + (inicio + 1) + '–' + (inicio + naPagina) + ' de ' + total + ' peças';
    }

    /* Devolve o controle de uma página: a atual é um texto marcado (não se
       clica no que já está aberto), as outras são botões, e as setas ficam
       desligadas nas pontas. Mesmo desenho do zip. */
    function criarPagina(rotulo, nome, destino, estado) {
      var elemento = document.createElement(estado === 'atual' ? 'span' : 'button');
      elemento.classList.add('shop__page');
      elemento.textContent = rotulo;
      elemento.setAttribute('aria-label', nome);
      if (destino) { elemento.setAttribute('data-pagina', String(destino)); }

      if (estado === 'atual') {
        elemento.setAttribute('aria-current', 'page');
        elemento.setAttribute('tabindex', '-1');
      } else if (estado === 'desligada') {
        elemento.disabled = true;
      } else {
        elemento.type = 'button';
        elemento.addEventListener('click', function () { irPara(destino); });
      }

      return elemento;
    }

    function irPara(destino) {
      pagina = destino;
      render();

      var atual = paginacao && paginacao.querySelector('[data-pagina="' + destino + '"]');
      if (atual) { atual.focus(); }

      irParaGrade();
    }

    /* Ao trocar de página a grade volta ao topo, descontando o cabeçalho fixo.
       Se a página não rola (tela alta, pouca coisa), não há o que fazer. */
    function irParaGrade() {
      var rolavel = (document.documentElement.scrollHeight || 0) > (window.innerHeight || 0);
      if (!rolavel) { return; }

      var topo = grid.getBoundingClientRect().top + (window.pageYOffset || 0);
      var recuo = parseInt(getComputedStyle(document.documentElement)
        .getPropertyValue('--iara-scroll-padding'), 10);
      if (isNaN(recuo)) { recuo = 96; }

      var reduzido = window.matchMedia
        && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

      try {
        window.scrollTo({
          top: Math.max(0, topo - recuo),
          behavior: reduzido ? 'auto' : 'smooth',
        });
      } catch (erro) { /* navegador antigo: segue sem rolar */ }
    }

    function desenharPaginacao(totalPaginas) {
      if (!paginacao) { return; }

      while (paginacao.firstChild) { paginacao.removeChild(paginacao.firstChild); }

      if (totalPaginas < 2) {
        paginacao.setAttribute('hidden', '');
        return;
      }

      paginacao.removeAttribute('hidden');

      paginacao.appendChild(criarPagina('←', 'Página anterior', pagina - 1,
        pagina === 1 ? 'desligada' : 'ativa'));

      for (var i = 1; i <= totalPaginas; i++) {
        paginacao.appendChild(criarPagina(String(i), 'Página ' + i, i,
          i === pagina ? 'atual' : 'ativa'));
      }

      paginacao.appendChild(criarPagina('→', 'Próxima página', pagina + 1,
        pagina === totalPaginas ? 'desligada' : 'ativa'));
    }

    /* ------------------------------------------------------- CONTADOR/AVISO */

    function contarAtivos() {
      return categorias.concat(cores, tamanhos).filter(function (campo) {
        return campo.checked;
      }).length;
    }

    function render() {
      var visiveis = cards.filter(combina);
      var totalPaginas = Math.max(1, Math.ceil(visiveis.length / POR_PAGINA));

      if (pagina > totalPaginas) { pagina = totalPaginas; }
      if (pagina < 1) { pagina = 1; }

      /* A página é montada sobre a lista JÁ ordenada: sem isso a grade mostraria
         a ordem antiga do HTML enquanto a ordenação só mudava as posições. */
      var ordenados = ordenar(visiveis);

      var inicio = (pagina - 1) * POR_PAGINA;
      var daPagina = ordenados.slice(inicio, inicio + POR_PAGINA);

      cards.forEach(function (card) {
        card.classList.toggle('is-hidden', daPagina.indexOf(card) === -1);
      });

      if (count) {
        count.textContent = visiveis.length === 1
          ? '1 peça nesta seleção'
          : visiveis.length + ' peças nesta seleção';
      }

      if (faixa) {
        faixa.textContent = textoDaFaixa(visiveis.length, inicio, daPagina.length);
      }

      desenharPaginacao(totalPaginas);

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

    /* Filtro novo recomeça da primeira página: sem isso, quem está na página 2
       e escolhe um filtro pode cair numa página que não existe mais. */
    function aoFiltrar() {
      pagina = 1;
      render();
    }

    categorias.concat(cores, tamanhos).forEach(function (campo) {
      campo.addEventListener('change', aoFiltrar);
    });

    [precoMin, precoMax].forEach(function (campo) {
      if (!campo) { return; }
      campo.addEventListener('input', aoFiltrar);
      /* Ao sair do campo, valores fora da faixa do catálogo voltam ao limite */
      campo.addEventListener('blur', function () {
        var valor = numero(campo, null);
        if (valor === null) { return; }
        if (valor < 0) { campo.value = '0'; }
        aoFiltrar();
      });
    });

    if (sort) { sort.addEventListener('change', aoFiltrar); }

    /* O botão do fim da coluna aplica o que já está marcado e devolve o foco
       para a contagem, que é anunciada por leitor de tela. No protótipo o filtro
       responde na hora; o botão existe porque faz parte do layout do zip. */
    if (aplicarBotao) {
      aplicarBotao.addEventListener('click', function () {
        render();
        if (count) { count.focus(); }
      });
    }

    limparBotoes.forEach(function (botao) {
      botao.addEventListener('click', function () {
        categorias.concat(cores, tamanhos).forEach(function (campo) { campo.checked = false; });
        if (precoMin) { precoMin.value = '149'; }
        if (precoMax) { precoMax.value = '789'; }
        pagina = 1;
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
