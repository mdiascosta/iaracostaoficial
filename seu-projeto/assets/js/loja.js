/* ============================================================================
   IARA COSTA · BLOCO A (Etapa E1) · loja.js
   Comportamento de loja: salvar nos desejos, adicionar à sacola, mini-sacola
   e barra de progresso do frete grátis.
   ----------------------------------------------------------------------------
   Importante para quem for usar este protótipo:
   - Nada aqui é salvo em servidor. O estado vive na memória da página e, quando
     o navegador permite, no armazenamento local (para o coração continuar
     marcado ao navegar entre as páginas).
   - No Bloco B (Elementor) este arquivo NÃO é usado: quem faz isso é o
     mini-carrinho do Elementor Pro e o plugin de lista de desejos aprovado.
   - O valor do frete grátis está em uma constante só (FRETE_GRATIS), para
     trocar em um lugar caso a regra mude.
   ========================================================================= */

(function () {
  'use strict';

  /* ------------------------------------------------------------------ DADOS */
  var FRETE_GRATIS = 299; // [CONFIRMAR COM A EMPRESA] dossiê previa R$ 199

  var CHAVE_CARRINHO = 'iara-carrinho-demo';
  var CHAVE_DESEJOS = 'iara-desejos-demo';

  /* Acesso seguro ao armazenamento: em alguns navegadores, abrir o arquivo
     direto (file://) bloqueia o localStorage e isso não pode quebrar a página. */
  var cofre = {
    ler: function (chave) {
      try {
        return JSON.parse(window.localStorage.getItem(chave)) || [];
      } catch (erro) {
        return [];
      }
    },
    gravar: function (chave, valor) {
      try {
        window.localStorage.setItem(chave, JSON.stringify(valor));
      } catch (erro) {
        /* sem armazenamento: segue só na memória da página */
      }
    }
  };

  /* Estado inicial de demonstração.
     O protótipo é estático: as páginas mostram uma sacola e uma lista de desejos
     já preenchidas para que os estados sejam visíveis sem clicar em nada. Estes
     dois blocos deixam o painel lateral coerente com o que aparece nas páginas
     de Sacola e de Desejos. Tudo some quando o navegador não guarda dados. */
  var SACOLA_EXEMPLO = [
    {
      slug: 'vestido-midi-salvia',
      nome: 'Vestido Midi Sálvia',
      categoria: 'Vestidos',
      preco: 596,
      img: 'assets/img/vestido-salvia.jpg',
      alt: 'Vestido midi sálvia de linho, frente',
      qtd: 1
    },
    {
      slug: 'colar-ceramica',
      nome: 'Colar de Cerâmica',
      categoria: 'Acessórios',
      preco: 189,
      img: 'assets/img/colar-ceramica.jpg',
      alt: 'Colar de contas de cerâmica torneada, frente',
      qtd: 2
    }
  ];

  var DESEJOS_EXEMPLO = ['vestido-longo-cerrado', 'calca-pantalona-salvia', 'saia-linho-cru'];

  var carrinho = cofre.ler(CHAVE_CARRINHO);
  var desejos = cofre.ler(CHAVE_DESEJOS);

  if (!carrinho.length) { carrinho = SACOLA_EXEMPLO.slice(); }
  if (!desejos.length) { desejos = DESEJOS_EXEMPLO.slice(); }

  function dinheiro(valor) {
    return 'R$ ' + valor.toFixed(2).replace('.', ',').replace(/\B(?=(\d{3})+(?!\d))/g, '.');
  }

  function numero(texto) {
    return parseFloat(String(texto).replace(/[^0-9,]/g, '').replace(/\./g, '').replace(',', '.')) || 0;
  }

  /* ----------------------------------------------------------- CONTADORES */
  function atualizarContadores() {
    var itens = carrinho.reduce(function (soma, item) { return soma + item.qtd; }, 0);

    document.querySelectorAll('[data-cart-count]').forEach(function (el) {
      el.textContent = String(itens);
    });
    document.querySelectorAll('[data-wish-count]').forEach(function (el) {
      el.textContent = String(desejos.length);
    });

    var linkSacola = document.querySelector('[data-cart-link]');
    if (linkSacola) {
      var rotulo = itens === 0 ? 'nenhum item' : (itens === 1 ? '1 item' : itens + ' itens');
      linkSacola.setAttribute('aria-label', 'Sacola de compras, ' + rotulo);
    }
  }

  /* --------------------------------------------------------- AVISO RÁPIDO */
  var aviso = document.querySelector('[data-toast]');
  var avisoTempo = null;

  function mostrarAviso(mensagem) {
    if (!aviso) { return; }
    aviso.textContent = mensagem;
    aviso.classList.add('is-visible');

    window.clearTimeout(avisoTempo);
    avisoTempo = window.setTimeout(function () {
      aviso.classList.remove('is-visible');
    }, 2600);
  }

  /* ------------------------------------------------------------- DESEJOS */
  function salvarDesejos() { cofre.gravar(CHAVE_DESEJOS, desejos); }

  function pintarCoracoes() {
    document.querySelectorAll('[data-wish]').forEach(function (botao) {
      var salvo = desejos.indexOf(botao.dataset.wish) !== -1;
      botao.setAttribute('aria-pressed', salvo ? 'true' : 'false');

      var nome = botao.closest('.card') && botao.closest('.card').querySelector('.card__name');
      var rotulo = nome ? nome.textContent.trim() : 'esta peça';
      botao.setAttribute('aria-label', (salvo ? 'Remover ' : 'Salvar ') + rotulo + (salvo ? ' dos desejos' : ' nos desejos'));
    });
  }

  document.addEventListener('click', function (evento) {
    var botao = evento.target.closest('[data-wish]');
    if (!botao) { return; }

    var slug = botao.dataset.wish;
    var posicao = desejos.indexOf(slug);
    var nome = botao.closest('.card').querySelector('.card__name').textContent.trim();

    if (posicao === -1) {
      desejos.push(slug);
      mostrarAviso(nome + ' salvo nos desejos.');
    } else {
      desejos.splice(posicao, 1);
      mostrarAviso(nome + ' removido dos desejos.');
    }

    salvarDesejos();
    pintarCoracoes();
    atualizarContadores();
  });

  /* ------------------------------------------------------------- SACOLA */
  function dadosDoCard(link) {
    var card = link.closest('.card');
    if (!card) { return null; }

    var img = card.querySelector('.card__img');
    var nome = card.querySelector('.card__name');
    var preco = card.querySelector('.card__price');
    var cat = card.querySelector('.card__cat');

    if (!img || !nome || !preco) { return null; }

    return {
      slug: link.dataset.add,
      nome: nome.textContent.trim(),
      categoria: cat ? cat.textContent.trim() : '',
      preco: numero(preco.textContent),
      img: img.getAttribute('src'),
      alt: img.getAttribute('alt'),
      qtd: 1
    };
  }

  function adicionar(produto) {
    var existente = carrinho.filter(function (item) { return item.slug === produto.slug; })[0];

    if (existente) {
      existente.qtd += 1;
    } else {
      carrinho.push(produto);
    }

    cofre.gravar(CHAVE_CARRINHO, carrinho);
    atualizarContadores();
    pintarSacola();
    mostrarAviso(produto.nome + ' entrou na sacola.');
  }

  /* -------------------------------------------------------- MINI-SACOLA */
  var drawer = document.querySelector('[data-drawer]');
  var backdrop = document.querySelector('[data-drawer-backdrop]');
  var ultimoFoco = null;

  function sacolaAberta() { return drawer && !drawer.hasAttribute('hidden'); }

  function abrirSacola() {
    if (!drawer) { return; }
    ultimoFoco = document.activeElement;
    drawer.removeAttribute('hidden');
    if (backdrop) { backdrop.removeAttribute('hidden'); }
    document.body.classList.add('is-locked');

    var foco = drawer.querySelector('[data-drawer-close]');
    if (foco) { foco.focus(); }
  }

  function fecharSacola(devolverFoco) {
    if (!drawer || !sacolaAberta()) { return; }
    drawer.setAttribute('hidden', '');
    if (backdrop) { backdrop.setAttribute('hidden', ''); }
    document.body.classList.remove('is-locked');

    if (devolverFoco !== false && ultimoFoco && document.contains(ultimoFoco)) {
      ultimoFoco.focus();
    }
  }

  function pintarSacola() {
    var corpo = document.querySelector('[data-drawer-body]');
    var totalEl = document.querySelector('[data-drawer-total]');
    var textoFrete = document.querySelector('[data-ship-text]');
    var barraFrete = document.querySelector('[data-ship-fill]');

    var subtotal = carrinho.reduce(function (soma, item) { return soma + item.preco * item.qtd; }, 0);

    if (corpo) {
      if (!carrinho.length) {
        corpo.innerHTML = '<p class="drawer__empty">Sua sacola está vazia. Escolha uma peça para começar.</p>';
      } else {
        corpo.innerHTML = carrinho.map(function (item) {
          return '' +
            '<article class="drawer__item">' +
              '<img src="' + item.img + '" alt="' + (item.alt || item.nome) + '" width="72" height="90">' +
              '<div>' +
                '<p class="drawer__item-name">' + item.nome + '</p>' +
                '<p class="drawer__item-meta">' + (item.categoria ? item.categoria + ' · ' : '') + item.qtd + ' un.</p>' +
                '<p class="drawer__item-price">' + dinheiro(item.preco * item.qtd) + '</p>' +
              '</div>' +
            '</article>';
        }).join('');
      }
    }

    if (totalEl) { totalEl.textContent = dinheiro(subtotal); }

    if (textoFrete && barraFrete) {
      if (subtotal >= FRETE_GRATIS) {
        textoFrete.textContent = 'Frete grátis liberado para este pedido.';
        barraFrete.style.width = '100%';
      } else {
        textoFrete.textContent = 'Faltam ' + dinheiro(FRETE_GRATIS - subtotal) + ' para o frete grátis.';
        barraFrete.style.width = Math.min(100, (subtotal / FRETE_GRATIS) * 100).toFixed(1) + '%';
      }
    }
  }

  document.addEventListener('click', function (evento) {
    var link = evento.target.closest('[data-add]');

    if (link) {
      /* No protótipo o link aponta para o carrinho. Aqui ele só demonstra o
         fluxo: guarda o item, atualiza a sacola e abre o painel lateral. */
      evento.preventDefault();
      var produto = dadosDoCard(link);
      if (produto) {
        adicionar(produto);
        abrirSacola();
      }
      return;
    }

    if (evento.target.closest('[data-drawer-close]') || evento.target.closest('[data-drawer-backdrop]')) {
      fecharSacola();
      return;
    }

    var abrir = evento.target.closest('[data-drawer-open]');
    if (abrir) {
      evento.preventDefault();
      abrirSacola();
    }
  });

  document.addEventListener('keydown', function (evento) {
    if (evento.key !== 'Escape' || !sacolaAberta()) { return; }
    evento.preventDefault();
    fecharSacola();
  });

  /* Trap de foco: com o painel aberto, Tab circula só dentro dele */
  document.addEventListener('keydown', function (evento) {
    if (evento.key !== 'Tab' || !sacolaAberta()) { return; }

    var focaveis = drawer.querySelectorAll('a[href], button:not([disabled]), input, [tabindex]:not([tabindex="-1"])');
    if (!focaveis.length) { return; }

    var primeiro = focaveis[0];
    var ultimo = focaveis[focaveis.length - 1];

    if (evento.shiftKey && document.activeElement === primeiro) {
      evento.preventDefault();
      ultimo.focus();
    } else if (!evento.shiftKey && document.activeElement === ultimo) {
      evento.preventDefault();
      primeiro.focus();
    }
  });

  /* ------------------------------------------------------------ INÍCIO */
  atualizarContadores();
  pintarCoracoes();
  pintarSacola();
})();
