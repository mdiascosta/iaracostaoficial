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
  var FRETE_GRATIS = 299; // confirmado pela empresa em 16/10/2026 (o dossiê previa R$ 199)

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
    /* Mesma regra da sacola: o frete grátis conta o valor líquido, com o cupom
       já aplicado, para a gaveta não prometer o que o resumo não cumpre. */
    var liquido = subtotal - (cupomAtivo ? subtotal * CUPONS[cupomAtivo] : 0);

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
      if (liquido >= FRETE_GRATIS) {
        textoFrete.textContent = 'Frete grátis liberado para este pedido.';
        barraFrete.style.width = '100%';
      } else {
        textoFrete.textContent = 'Faltam ' + dinheiro(FRETE_GRATIS - liquido) + ' para o frete grátis.';
        barraFrete.style.width = Math.min(100, (liquido / FRETE_GRATIS) * 100).toFixed(1) + '%';
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

  /* ==========================================================================
     CARRINHO: quantidade, remoção, cupom e frete (v0.1.11)

     Vem do loja.js do template do zip, com duas diferenças de propósito:
     1. Nada de valor de frete inventado. A resposta do cálculo é a regra que a
        empresa já definiu (grátis acima de R$ 299) e o resto continua
        [A DEFINIR] até a conta de frete ser contratada.
     2. Cupom só o que o dossiê documenta: BEMVINDO10, 10% na primeira compra.
        Código desconhecido não aplica desconto e diz isso na tela.
     ========================================================================== */
  var CUPONS = { BEMVINDO10: 0.1 };
  var cupomAtivo = null;

  /* Regras confirmadas pela empresa em 16/10/2026 (Mercado Pago):
     - Pix com 5% de desconto, aplicado sobre o valor dos produtos;
     - cartão de crédito em até 6x sem juros, com parcela mínima de R$ 50,00;
     - frete grátis acima de R$ 299 no valor LÍQUIDO, ou seja, depois do cupom;
     - R$ 15,00 no Sudeste vale só para o PAC (SP, RJ, MG e ES). */
  var PIX_DESCONTO = 0.05;
  var PARCELA_MINIMA = 50;
  var MAX_PARCELAS = 6;

  function itensDaSacola() {
    return Array.prototype.slice.call(document.querySelectorAll('[data-item]'));
  }

  function resumoDaSacola() {
    var itens = [];
    var subtotal = 0;

    itensDaSacola().forEach(function (item) {
      if (item.hasAttribute('hidden')) { return; }
      var campo = item.querySelector('.qty__input');
      var preco = item.querySelector('.cart-item__price');
      var unitario = numero(item.getAttribute('data-unitario'));
      var qtd = campo ? (parseInt(campo.value, 10) || 1) : 1;

      if (preco) { preco.textContent = dinheiro(unitario * qtd); }
      subtotal += unitario * qtd;
      if (campo) { itens.push({ item: item, campo: campo, qtd: qtd }); }
    });

    return { itens: itens, subtotal: subtotal };
  }

  function pintarResumo() {
    var subtotalEl = document.querySelector('[data-subtotal]');
    if (!subtotalEl) { return; }

    var resumo = resumoDaSacola();
    var desconto = cupomAtivo ? resumo.subtotal * CUPONS[cupomAtivo] : 0;
    var total = resumo.subtotal - desconto;
    /* O frete grátis olha o valor depois do cupom, como a empresa definiu. */
    var freteGratis = total >= FRETE_GRATIS;

    var descontoEl = document.querySelector('[data-desconto]');
    var descontoRotulo = document.querySelector('[data-desconto-rotulo]');
    var freteEl = document.querySelector('[data-frete]');
    var totalEl = document.querySelector('[data-total]');
    var totalRotulo = document.querySelector('[data-total-rotulo]');

    subtotalEl.textContent = dinheiro(resumo.subtotal);
    if (descontoEl) { descontoEl.textContent = '− ' + dinheiro(desconto); }
    if (descontoRotulo) {
      descontoRotulo.textContent = cupomAtivo ? 'Desconto (' + cupomAtivo + ')' : 'Desconto';
    }
    if (freteEl) { freteEl.textContent = freteGratis ? 'Grátis' : '[A DEFINIR]'; }
    if (totalEl) { totalEl.textContent = dinheiro(total); }
    if (totalRotulo) { totalRotulo.textContent = freteGratis ? 'Total' : 'Total sem frete'; }
  }

  /* Faixa de CEP do Sudeste (SP, RJ, ES e MG), a região do valor fixo de
     R$ 15,00 confirmada pela empresa. Serve só para escolher o texto do recado:
     o valor de verdade vem do cálculo dos Correios. */
  function regiaoDoCep(valor) {
    var faixas = [[1000000, 19999999], [20000000, 28999999],
                  [29000000, 29999999], [30000000, 39999999]];
    var numero = parseInt(String(valor).replace(/\D/g, ''), 10) || 0;

    for (var i = 0; i < faixas.length; i++) {
      if (numero >= faixas[i][0] && numero <= faixas[i][1]) { return 'sudeste'; }
    }
    return 'outra';
  }

  function recadoDoCupom(texto) {
    var alvo = document.querySelector('[data-cupom-msg]');
    if (alvo) { alvo.textContent = texto; }
  }

  function initCarrinho() {
    var formCupom = document.querySelector('[data-cupom-form]');
    var formFrete = document.querySelector('[data-frete-form]');

    /* O cupom que aparece preenchido na página é o do dossiê: começa aplicado. */
    if (formCupom) {
      var campo = formCupom.querySelector('input[name="cupom"]');
      var inicial = campo ? campo.value.trim().toUpperCase() : '';
      cupomAtivo = CUPONS[inicial] ? inicial : null;

      formCupom.addEventListener('submit', function (evento) {
        evento.preventDefault();
        var codigo = campo ? campo.value.trim().toUpperCase() : '';

        if (CUPONS[codigo]) {
          cupomAtivo = codigo;
          recadoDoCupom('Cupom ' + codigo + ' aplicado: ' + Math.round(CUPONS[codigo] * 100) + '% de desconto na primeira compra.');
        } else {
          cupomAtivo = null;
          recadoDoCupom(codigo
            ? 'Cupom não reconhecido. Confira o código e tente de novo.'
            : 'Digite um cupom para aplicar.');
        }

        pintarResumo();
      });
    }

    if (formFrete) {
      var cep = formFrete.querySelector('input[name="cep"]');
      var recado = document.querySelector('[data-frete-msg]');

      if (cep) {
        cep.addEventListener('input', function () {
          var digitos = cep.value.replace(/\D/g, '').slice(0, 8);
          cep.value = digitos.length > 5 ? digitos.slice(0, 5) + '-' + digitos.slice(5) : digitos;
        });
      }

      formFrete.addEventListener('submit', function (evento) {
        evento.preventDefault();
        var digitos = cep ? cep.value.replace(/\D/g, '') : '';

        if (!recado) { return; }

        if (digitos.length !== 8) {
          recado.textContent = 'Digite um CEP com 8 números para ver o frete.';
          return;
        }

        var subtotal = resumoDaSacola().subtotal;
        var regiao = regiaoDoCep(cep.value);

        if (subtotal >= FRETE_GRATIS) {
          recado.textContent = 'Para o CEP ' + cep.value + ': frete grátis nesta compra.';
          return;
        }

        recado.textContent = regiao === 'sudeste'
          ? 'Para o CEP ' + cep.value + ' (Sudeste): PAC por R$ 15,00. O SEDEX sai pelo cálculo dos Correios.'
          : 'Para o CEP ' + cep.value + ': o PAC e o SEDEX são calculados pelos Correios a partir deste CEP.';
      });
    }

    pintarResumo();
  }

  /* ==========================================================================
     CHECKOUT: cartões de opção, totais, máscaras e dados do cartão (v0.1.13)

     O padrão visual veio do template enviado pela cliente (cartões com rádio,
     título, linha de apoio e valor à direita). As decisões são do dossiê:

     1. Nada de valor de frete inventado. A resposta sai das regras confirmadas:
        PAC grátis a partir de R$ 299 no valor líquido; abaixo disso, R$ 15,00 no
        Sudeste e cálculo pelos Correios nas outras regiões; SEDEX sempre
        calculado; retirada no ateliê grátis.
     2. O protótipo NÃO coleta dado de cartão. Os campos do cartão existem para
        mostrar o desenho da tela: não têm atributo name (nada é enviado), não
        são gravados em lugar nenhum e o aviso na tela diz isso. No site
        publicado quem desenha esses campos é o Mercado Pago.
     ========================================================================== */

  function textoDo(seletor) {
    var el = document.querySelector(seletor);
    return el ? el.textContent.trim() : '';
  }

  function numeroDo(seletor) { return numero(textoDo(seletor)); }

  function escolhido(nome) {
    var campo = document.querySelector('input[name="' + nome + '"]:checked');
    return campo ? campo.value : '';
  }

  function marcarCartoesEscolhidos() {
    document.querySelectorAll('.choice').forEach(function (cartao) {
      var campo = cartao.querySelector('.choice__input');
      cartao.classList.toggle('is-selected', !!(campo && campo.checked));
    });
  }

  var TEXTO_ENVIO = {
    PAC: 'PAC: postagem em até 2 dias úteis, com rastreio. O prazo de entrega sai do cálculo dos Correios pelo CEP.',
    SEDEX: 'SEDEX: valor e prazo aparecem depois do cálculo dos Correios pelo CEP.',
    Retirada: 'Retirada no ateliê: dia e horário [A DEFINIR: combinar com o atendimento].'
  };

  var TEXTO_PAGAMENTO = {
    pix: 'No Pix a confirmação é na hora, com 5% de desconto. O QR Code é gerado pelo Mercado Pago depois de confirmar o pedido.',
    cartao: 'Cartão em até 6x sem juros, parcela mínima de R$ 50,00, processado pelo Mercado Pago. No site publicado os campos do cartão são os do gateway.'
  };

  /* Faixa do CEP digitado no checkout; sem CEP completo, não dá para dizer qual. */
  function regiaoDoCheckout() {
    var cep = document.getElementById('cep2');
    if (!cep || cep.value.replace(/\D/g, '').length !== 8) { return 'sem-cep'; }
    return regiaoDoCep(cep.value);
  }

  /* Quanto custa o frete escolhido. null = depende do cálculo dos Correios. */
  function valorDoFrete() {
    var forma = escolhido('envio');
    var liquido = numeroDo('[data-resumo-produtos]') - numeroDo('[data-resumo-cupom]');

    if (forma === 'Retirada') { return 0; }
    if (forma === 'SEDEX') { return null; }
    if (liquido >= FRETE_GRATIS) { return 0; }
    return regiaoDoCheckout() === 'sudeste' ? 15 : null;
  }

  function pintarCheckout() {
    var totalEl = document.querySelector('[data-resumo-total]');
    if (!totalEl) { return; }

    var produtos = numeroDo('[data-resumo-produtos]');
    var desconto = numeroDo('[data-resumo-cupom]');
    var liquido = Math.max(0, produtos - desconto);
    var forma = escolhido('envio');
    var pix = escolhido('pagamento') === 'pix';
    var frete = valorDoFrete();
    var freteSomado = frete === null ? 0 : frete;

    /* Preço das duas formas de pagamento. Quando o frete depende do cálculo, o
       cartão mostra só os produtos e o total do resumo sai sem frete. */
    var precoPix = document.querySelector('[data-preco-pix]');
    var precoCartao = document.querySelector('[data-preco-cartao]');
    if (precoPix) { precoPix.textContent = dinheiro(liquido * (1 - PIX_DESCONTO) + freteSomado); }
    if (precoCartao) { precoCartao.textContent = dinheiro(liquido + freteSomado); }

    /* Preço do PAC no cartão de envio. */
    var pacEl = document.querySelector('[data-frete-pac]');
    if (pacEl) {
      if (liquido >= FRETE_GRATIS) { pacEl.textContent = 'Grátis'; }
      else if (regiaoDoCheckout() === 'sudeste') { pacEl.textContent = dinheiro(15); }
      else { pacEl.textContent = 'Calculado pelo CEP'; }
    }

    /* O SEDEX nunca tem valor fixo: a conta é sempre dos Correios, pelo CEP. */
    var sedexEl = document.querySelector('[data-frete-sedex]');
    if (sedexEl) { sedexEl.textContent = 'Calculado pelo CEP'; }

    /* Linha do frete e total do resumo. */
    var freteEl = document.querySelector('[data-resumo-frete]');
    var freteRotulo = document.querySelector('[data-resumo-frete-rotulo]');
    var totalRotulo = document.querySelector('[data-resumo-total-rotulo]');

    if (freteRotulo) {
      freteRotulo.textContent = forma === 'Retirada'
        ? 'Retirada no ateliê'
        : 'Frete no ' + (forma === 'SEDEX' ? 'SEDEX' : 'PAC');
    }
    if (freteEl) {
      if (frete === null) { freteEl.textContent = 'Calculado pelo CEP'; }
      else { freteEl.textContent = frete === 0 ? 'Grátis' : dinheiro(frete); }
    }

    var base = pix ? liquido * (1 - PIX_DESCONTO) : liquido;
    if (frete === null) {
      totalEl.textContent = dinheiro(base);
      if (totalRotulo) { totalRotulo.textContent = 'Total sem frete'; }
    } else {
      totalEl.textContent = dinheiro(base + frete);
      if (totalRotulo) { totalRotulo.textContent = pix ? 'Total no Pix' : 'Total no cartão'; }
    }

    /* Parcelas, respeitando a parcela mínima de R$ 50,00 confirmada pela empresa. */
    var parcelas = document.querySelector('[data-parcelas]');
    if (parcelas) {
      var totalCartao = liquido + freteSomado;
      var escolhida = parcelas.value;
      var opcoes = [];

      for (var n = 1; n <= MAX_PARCELAS; n++) {
        var valorParcela = totalCartao / n;
        if (n > 1 && valorParcela < PARCELA_MINIMA) { break; }
        opcoes.push('<option value="' + n + '"' +
                    (String(n) === String(escolhida) ? ' selected' : '') + '>' +
                    n + 'x de ' + dinheiro(valorParcela) + ' sem juros</option>');
      }
      parcelas.innerHTML = opcoes.join('');
    }
  }

  function sincronizarCheckout() {
    marcarCartoesEscolhidos();

    /* Campos do cartão só aparecem quando o cartão é a forma escolhida. */
    var camposCartao = document.getElementById('cartao-campos');
    if (camposCartao) {
      if (escolhido('pagamento') === 'cartao') { camposCartao.removeAttribute('hidden'); }
      else { camposCartao.setAttribute('hidden', ''); }
    }

    var recadoEnvio = document.querySelector('[data-envio-msg]');
    if (recadoEnvio) { recadoEnvio.textContent = TEXTO_ENVIO[escolhido('envio')] || ''; }

    var recadoPagamento = document.querySelector('[data-pay-note]');
    if (recadoPagamento) { recadoPagamento.textContent = TEXTO_PAGAMENTO[escolhido('pagamento')] || ''; }

    pintarCheckout();
  }

  function mascararCampo(campo, formatar) {
    if (!campo) { return; }
    campo.addEventListener('input', function () { campo.value = formatar(campo.value); });
  }

  function initCheckout() {
    var cepCheckout = document.getElementById('cep2');
    var telefone = document.getElementById('telefone');

    if (cepCheckout) {
      cepCheckout.addEventListener('input', function () {
        var digitos = cepCheckout.value.replace(/\D/g, '').slice(0, 8);
        cepCheckout.value = digitos.length > 5 ? digitos.slice(0, 5) + '-' + digitos.slice(5) : digitos;
        sincronizarCheckout();
      });
    }

    if (telefone) {
      telefone.addEventListener('input', function () {
        var d = telefone.value.replace(/\D/g, '').slice(0, 11);
        if (d.length > 10) { telefone.value = '(' + d.slice(0, 2) + ') ' + d.slice(2, 7) + '-' + d.slice(7); }
        else if (d.length > 6) { telefone.value = '(' + d.slice(0, 2) + ') ' + d.slice(2, 6) + '-' + d.slice(6); }
        else if (d.length > 2) { telefone.value = '(' + d.slice(0, 2) + ') ' + d.slice(2); }
        else { telefone.value = d; }
      });
    }

    /* Máscaras dos campos de demonstração do cartão. Elas só arrumam o que
       aparece na tela: nada é validado, guardado ou enviado. */
    mascararCampo(document.getElementById('cc-numero'), function (valor) {
      return valor.replace(/\D/g, '').slice(0, 16).replace(/(\d{4})(?=\d)/g, '$1 ');
    });
    mascararCampo(document.getElementById('cc-validade'), function (valor) {
      var d = valor.replace(/\D/g, '').slice(0, 4);
      return d.length > 2 ? d.slice(0, 2) + '/' + d.slice(2) : d;
    });
    mascararCampo(document.getElementById('cc-cvv'), function (valor) {
      return valor.replace(/\D/g, '').slice(0, 4);
    });

    document.querySelectorAll('input[name="envio"], input[name="pagamento"]').forEach(function (opcao) {
      opcao.addEventListener('change', sincronizarCheckout);
    });

    sincronizarCheckout();
  }

  /* Botões +/- e Remover da página da sacola. */
  document.addEventListener('click', function (evento) {
    var passo = evento.target.closest('[data-qty-step]');
    var remover = evento.target.closest('[data-remover]');

    if (passo) {
      var item = passo.closest('[data-item]');
      var campo = item ? item.querySelector('.qty__input') : null;
      if (!campo) { return; }

      var direcao = parseInt(passo.getAttribute('data-qty-step'), 10) || 1;
      var minimo = parseInt(campo.getAttribute('min') || '1', 10);
      var maximo = parseInt(campo.getAttribute('max') || '10', 10);
      var atual = parseInt(campo.value, 10) || minimo;

      campo.value = String(Math.min(maximo, Math.max(minimo, atual + direcao)));
      campo.dispatchEvent(new Event('change', { bubbles: true }));
      pintarResumo();
      return;
    }

    if (remover) {
      var linha = remover.closest('[data-item]');
      if (!linha) { return; }

      linha.setAttribute('hidden', '');
      pintarResumo();
      mostrarAviso('Peça removida da sacola.');
    }
  });

  /* ------------------------------------------------------------ INÍCIO */
  function seguro(nome, fn) {
    try {
      fn();
    } catch (erro) {
      /* Uma melhoria com problema não pode derrubar as outras. Nada essencial
         depende do JS: sem ele a página continua legível e navegável. */
      if (window.console && console.warn) {
        console.warn('[iara-loja] "' + nome + '" não foi inicializada:', erro);
      }
    }
  }

  seguro('contadores', atualizarContadores);
  seguro('desejos', pintarCoracoes);
  seguro('carrinho', function () {
    initCarrinho();

    /* A quantidade digitada à mão também recalcula o resumo. */
    document.addEventListener('change', function (evento) {
      if (evento.target.closest('.qty__input')) { pintarResumo(); }
    });
  });
  /* A gaveta vem depois do carrinho: ela usa o cupom que o carrinho acabou de
     ler da tela, para o frete grátis contar o mesmo valor líquido nas duas. */
  seguro('mini-sacola', pintarSacola);
  seguro('checkout', initCheckout);
})();
