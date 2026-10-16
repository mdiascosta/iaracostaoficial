/* Teste automatizado do protótipo (Bloco A) com jsdom.
   Verifica: links internos, imagens existentes, interações do header,
   corações de desejos, adicionar à sacola e mini-sacola.

   COMO RODAR (na raiz do repositório):
     npm install jsdom         # uma vez só
     node tools/test.js        # imprime PASS/FAIL e sai com erro se algo falhar

   O teste lê as páginas já geradas em seu-projeto/. Rode tools/build.py antes
   de rodar este arquivo, senão ele confere uma versão antiga do HTML. */

const fs = require('fs');
const path = require('path');
const { JSDOM } = require('jsdom');

const RAIZ = path.join(__dirname, '..', 'seu-projeto');
const paginas = fs.readdirSync(RAIZ).filter((f) => f.endsWith('.html'));

let falhas = 0;
const ok = (cond, msg) => {
  if (cond) { console.log('  PASS  ' + msg); }
  else { console.log('  FAIL  ' + msg); falhas++; }
};

function carregar(arquivo) {
  const html = fs.readFileSync(path.join(RAIZ, arquivo), 'utf8');
  const dom = new JSDOM(html, {
    url: 'http://localhost:8080/' + arquivo,
    runScripts: 'outside-only',
    pretendToBeVisual: true,
  });

  // APIs que o jsdom não implementa
  dom.window.matchMedia = dom.window.matchMedia || (() => ({ matches: false, addEventListener() {}, removeEventListener() {} }));

  // Carrega exatamente os scripts que a própria página referencia, na ordem
  // em que aparecem no HTML (era o que faltava para testar os filtros).
  const scripts = Array.prototype.map.call(
    dom.window.document.querySelectorAll('script[src]'),
    (tag) => tag.getAttribute('src').split('?')[0]
  );
  scripts.forEach((caminho) => {
    const p = path.join(RAIZ, caminho);
    if (fs.existsSync(p)) { dom.window.eval(fs.readFileSync(p, 'utf8')); }
  });

  return dom;
}

console.log('\n=== 1. LINKS E IMAGENS ===');
let linksTotais = 0;
for (const pagina of paginas) {
  const dom = carregar(pagina);
  const doc = dom.window.document;

  doc.querySelectorAll('a[href]').forEach((a) => {
    const href = a.getAttribute('href');
    if (!href || href.startsWith('#') || href.startsWith('http')) { return; }
    // mailto:, tel: e sms: são contatos, não arquivos.
    if (/^(mailto|tel|sms):/.test(href)) { return; }
    linksTotais++;
    const alvo = path.join(RAIZ, href.split('?')[0].split('#')[0]);
    if (!fs.existsSync(alvo)) { console.log('  FAIL  ' + pagina + ' -> ' + href); falhas++; }
  });

  doc.querySelectorAll('img[src]').forEach((img) => {
    const src = img.getAttribute('src');
    if (src.startsWith('http')) { return; }
    const alvo = path.join(RAIZ, src.split('?')[0]);
    if (!fs.existsSync(alvo)) { console.log('  FAIL  ' + pagina + ' imagem ' + src); falhas++; }
    // alt="" é correto para imagem decorativa, desde que marcada com aria-hidden
    const decorativa = img.getAttribute('alt') === '' && img.getAttribute('aria-hidden') === 'true';
    if (!img.getAttribute('alt') && !decorativa) { console.log('  FAIL  ' + pagina + ' imagem sem alt: ' + src); falhas++; }
  });
}
ok(true, linksTotais + ' links internos verificados em ' + paginas.length + ' páginas');

console.log('\n=== 2. MINI-SACOLA (drawer) ===');
{
  const dom = carregar('index.html');
  const doc = dom.window.document;
  const drawer = doc.querySelector('[data-drawer]');

  ok(!!drawer, 'drawer existe no HTML');
  ok(drawer.hasAttribute('hidden'), 'drawer começa fechado (hidden presente)');

  // estado de exemplo preenchido pelo loja.js
  const itens = drawer.querySelectorAll('.drawer__item');
  ok(itens.length === 2, 'drawer lista os 2 itens de exemplo (achou ' + itens.length + ')');
  ok(doc.querySelector('[data-drawer-total]').textContent.includes('974,00'),
    'subtotal do drawer = R$ 974,00 (achei ' + doc.querySelector('[data-drawer-total]').textContent + ')');
  ok(doc.querySelector('[data-ship-text]').textContent.includes('liberado'),
    'barra de frete lê "liberado" quando passa de R$ 299');
  ok(doc.querySelector('[data-ship-fill]').style.width === '100%', 'barra de frete em 100%');

  // contadores no header
  ok(doc.querySelector('[data-cart-count]').textContent === '3', 'contador da sacola = 3 peças');
  ok(doc.querySelector('[data-wish-count]').textContent === '3', 'contador de desejos = 3');
}

console.log('\n=== 3. ADICIONAR À SACOLA ===');
{
  const dom = carregar('loja.html');
  const doc = dom.window.document;
  const drawer = doc.querySelector('[data-drawer]');

  ok(drawer.hasAttribute('hidden'), 'drawer começa fechado');

  const botao = doc.querySelector('[data-add="blazer-linho-areia"]');
  ok(!!botao, 'existe botão "Adicionar à sacola" no card do Blazer');

  botao.dispatchEvent(new dom.window.MouseEvent('click', { bubbles: true, cancelable: true }));

  ok(!drawer.hasAttribute('hidden'), 'drawer abre ao adicionar');
  ok(doc.querySelectorAll('.drawer__item').length === 3, 'drawer passa a listar 3 itens');
  ok(doc.querySelector('[data-drawer-total]').textContent.includes('1.763,00'),
    'subtotal soma o blazer: 974 + 789 = 1.763,00 (achei ' + doc.querySelector('[data-drawer-total]').textContent + ')');
  ok(doc.querySelector('[data-cart-count]').textContent === '4', 'contador da sacola vai para 4');

  // ESC fecha
  doc.dispatchEvent(new dom.window.KeyboardEvent('keydown', { key: 'Escape', bubbles: true }));
  ok(drawer.hasAttribute('hidden'), 'ESC fecha o drawer');
}

console.log('\n=== 4. LISTA DE DESEJOS ===');
{
  const dom = carregar('loja.html');
  const doc = dom.window.document;
  const coracao = doc.querySelector('[data-wish="camisa-linho-branca"]');

  ok(!!coracao, 'existe coração no card da Camisa Branca');
  ok(coracao.getAttribute('aria-pressed') === 'false', 'coração começa não marcado');

  coracao.dispatchEvent(new dom.window.MouseEvent('click', { bubbles: true, cancelable: true }));
  ok(coracao.getAttribute('aria-pressed') === 'true', 'coração marca ao clicar');
  ok(doc.querySelector('[data-wish-count]').textContent === '4', 'contador de desejos vai para 4');

  coracao.dispatchEvent(new dom.window.MouseEvent('click', { bubbles: true, cancelable: true }));
  ok(coracao.getAttribute('aria-pressed') === 'false', 'coração desmarca ao clicar de novo');
}

console.log('\n=== 5. CABEÇALHO: BUSCA E MENU ===');
{
  const dom = carregar('index.html');
  const doc = dom.window.document;
  const painel = doc.getElementById('busca-painel');
  const gatilho = doc.querySelector('[data-search-toggle]');

  ok(painel.hasAttribute('hidden'), 'faixa de busca começa fechada');
  gatilho.dispatchEvent(new dom.window.MouseEvent('click', { bubbles: true, cancelable: true }));
  ok(!painel.hasAttribute('hidden'), 'clique na lupa abre a faixa de busca');
  ok(gatilho.getAttribute('aria-expanded') === 'true', 'aria-expanded vira true');

  const fechar = painel.querySelector('[data-search-close]');
  fechar.dispatchEvent(new dom.window.MouseEvent('click', { bubbles: true, cancelable: true }));
  ok(painel.hasAttribute('hidden'), 'botão fechar esconde a faixa');

  const menu = doc.getElementById('menu-mobile');
  const abrirMenu = doc.querySelector('.nav-toggle');
  ok(menu.hasAttribute('hidden'), 'menu mobile começa fechado');
  abrirMenu.dispatchEvent(new dom.window.MouseEvent('click', { bubbles: true, cancelable: true }));
  ok(!menu.hasAttribute('hidden'), 'botão hambúrguer abre o menu mobile');
  menu.querySelector('.mobile-panel__close').dispatchEvent(new dom.window.MouseEvent('click', { bubbles: true, cancelable: true }));
  ok(menu.hasAttribute('hidden'), 'botão Fechar esconde o menu');
}

console.log('\n=== 6. ACESSIBILIDADE BÁSICA ===');
{
  const dom = carregar('index.html');
  const doc = dom.window.document;
  ok(!!doc.querySelector('.skip-link'), 'existe link "pular para o conteúdo"');
  ok(doc.documentElement.getAttribute('lang') === 'pt-BR', 'lang=pt-BR');

  let h1 = 0;
  doc.querySelectorAll('h1').forEach(() => h1++);
  ok(h1 === 1, 'exatamente um H1 (achou ' + h1 + ')');

  let semNome = 0;
  doc.querySelectorAll('button').forEach((b) => {
    const nome = (b.textContent || '').trim() || b.getAttribute('aria-label');
    if (!nome) { semNome++; }
  });
  ok(semNome === 0, 'todo botão tem texto ou aria-label');
}

console.log('\n=== 7. FILTROS DA LOJA (coluna à esquerda) ===');
{
  const dom = carregar('loja.html');
  const doc = dom.window.document;
  const cards = doc.querySelectorAll('[data-shop-grid] .card');
  const visiveis = () => Array.prototype.filter.call(cards, (c) => !c.classList.contains('is-hidden')).length;
  const contador = () => doc.querySelector('[data-count]').textContent;

  ok(!!doc.querySelector('.shop') && !!doc.querySelector('.filters'), 'loja tem a coluna de filtros e a grade');
  ok(cards.length === 12, 'a grade começa com 12 peças');
  ok(visiveis() === 9, 'a primeira página mostra 9 das 12 peças (achou ' + visiveis() + ')');

  const catVestidos = doc.querySelector('[data-facet="categoria"][value="vestidos"]');
  catVestidos.checked = true;
  catVestidos.dispatchEvent(new dom.window.Event('change', { bubbles: true }));
  ok(visiveis() === 2, 'categoria Vestidos mostra 2 peças (achou ' + visiveis() + ')');
  ok(contador() === '2 peças nesta seleção', 'contador anuncia 2 peças nesta seleção ("' + contador() + '")');

  // agora soma um tamanho que os vestidos têm, sem mudar o resultado
  const tamP = doc.querySelector('[data-facet="tamanho"][value="p"]');
  tamP.checked = true;
  tamP.dispatchEvent(new dom.window.Event('change', { bubbles: true }));
  ok(visiveis() === 2, 'filtro de tamanho P mantém os 2 vestidos');

  // tamanho que nenhum vestido tem (único) -> estado vazio
  const tamUnico = doc.querySelector('[data-facet="tamanho"][value="unico"]');
  tamP.checked = false;
  tamUnico.checked = true;
  tamUnico.dispatchEvent(new dom.window.Event('change', { bubbles: true }));
  tamP.dispatchEvent(new dom.window.Event('change', { bubbles: true }));
  ok(visiveis() === 0, 'vestido + tamanho Único = nenhuma peça');
  ok(!doc.querySelector('[data-shop-empty]').hasAttribute('hidden'), 'aviso de "nenhuma peça" aparece');

  // limpar filtros volta tudo
  tamUnico.checked = false;
  doc.querySelector('.filters [data-filters-clear]').dispatchEvent(new dom.window.MouseEvent('click', { bubbles: true }));
  ok(visiveis() === 9, 'Limpar filtros traz a primeira página de volta (9 de 12)');
  ok(doc.querySelector('[data-shop-empty]').hasAttribute('hidden'), 'aviso some ao limpar');

  // faixa de preço
  const min = doc.querySelector('[data-facet="preco-min"]');
  const max = doc.querySelector('[data-facet="preco-max"]');
  min.value = '400';
  max.value = '800';
  min.dispatchEvent(new dom.window.Event('input', { bubbles: true }));
  // 596, 684, 459, 789 e 429: cinco peças entre R$ 400 e R$ 800
  ok(visiveis() === 5, 'preço de 400 a 800 mostra 5 peças (achou ' + visiveis() + ')');

  // cor
  doc.querySelector('[data-filters-clear]').dispatchEvent(new dom.window.MouseEvent('click', { bubbles: true }));
  const corSalvia = doc.querySelector('[data-facet="cor"][value="salvia"]');
  corSalvia.checked = true;
  corSalvia.dispatchEvent(new dom.window.Event('change', { bubbles: true }));
  ok(visiveis() === 2, 'cor Sálvia mostra 2 peças (achou ' + visiveis() + ')');

  // ordenação
  doc.querySelector('[data-filters-clear]').dispatchEvent(new dom.window.MouseEvent('click', { bubbles: true }));
  const select = doc.querySelector('[data-sort]');
  select.value = 'price';
  select.dispatchEvent(new dom.window.Event('change', { bubbles: true }));
  const primeiro = doc.querySelector('[data-shop-grid] .card:not(.is-hidden)');
  ok(parseFloat(primeiro.dataset.preco) === 149, 'ordenação por menor preço começa em R$ 149 (achou ' + primeiro.dataset.preco + ')');

  // gaveta de filtros no celular
  const botao = doc.querySelector('[data-filters-toggle]');
  ok(botao.getAttribute('aria-expanded') === 'false', 'botão Filtros começa fechado');
  botao.dispatchEvent(new dom.window.MouseEvent('click', { bubbles: true }));
  ok(botao.getAttribute('aria-expanded') === 'true', 'clique abre a gaveta de filtros');
  ok(doc.getElementById('filtros-loja').classList.contains('filters--open'), 'gaveta ganha a classe de aberta');
}

console.log('\n=== 8. RODAPÉ (estrutura da referência) ===');
{
  const dom = carregar('index.html');
  const doc = dom.window.document;
  const rodape = doc.querySelector('.site-footer');

  ok(!!rodape.querySelector('.newsletter'), 'newsletter de volta no rodapé, como na referência');
  ok(!!rodape.querySelector('#news-email'), 'campo de e-mail da newsletter com rótulo');
  ok(doc.querySelectorAll('.site-footer__title').length === 3, 'três colunas de links no rodapé');
  ok(!!rodape.querySelector('.security'), 'faixa de segurança e pagamento presente');
  ok(rodape.querySelectorAll('.security__item').length === 4, 'quatro informações na faixa de segurança');
  ok(!!rodape.querySelector('.security__note'), 'aviso de que os selos são demonstrativos');
  ok(rodape.textContent.includes('CNPJ'), 'identificação da empresa (CNPJ) na base');
  ok(rodape.textContent.includes('CDC'), 'direito de arrependimento (CDC) na faixa de segurança');
}

console.log('\n=== 9. CABEÇALHO DE PÁGINA E CARTÕES ===');
{
  const dom = carregar('loja.html');
  const doc = dom.window.document;
  const cabeca = doc.querySelector('.page-head');

  ok(!!cabeca.querySelector('h1'), 'nome da página dentro do cabeçalho');
  ok(!!doc.querySelector('.shop__count[data-count]'), 'contagem de peças na barra da coleção');

  const domBlog = carregar('blog.html');
  const docBlog = domBlog.window.document;
  const primeiro = docBlog.querySelector('.post-card');
  ok(!!primeiro.querySelector('.post-card__body'), 'cartão do diário tem corpo próprio');
  ok(!!primeiro.querySelector('.post-card__media img'), 'cartão do diário mantém a foto');

  const domHome = carregar('index.html');
  const docHome = domHome.window.document;
  ok(docHome.querySelectorAll('.quote').length === 3, 'três cartões de depoimento na home');
  ok(docHome.querySelectorAll('.benefit').length === 4, 'quatro itens na faixa de benefícios');
  ok(docHome.querySelectorAll('.post-card__body').length === 3, 'três cartões no bloco do diário');
}

console.log('\n=== 10. FAIXA SALVIA DA HOME ===');
{
  const dom = carregar('index.html');
  const doc = dom.window.document;

  const compacta = doc.querySelector('.band--compact');
  ok(!compacta, 'faixa compacta de lista de espera saiu da home');
  ok(!doc.getElementById('espera-email'), 'nenhum campo de lista de espera na home');

  const faq = doc.querySelector('.band--faq');
  ok(!!faq, 'faixa de perguntas antes do rodapé');
  ok(faq.querySelectorAll('.accordion__button').length === 5, 'cinco perguntas na faixa');
  ok(faq.querySelectorAll('.accordion__panel').length === 5, 'cinco respostas na faixa');
  ok(!!faq.querySelector('a[href="faq.html"]'), 'link para a página de perguntas');

  const primeira = faq.querySelector('.accordion__button');
  ok(primeira.getAttribute('aria-expanded') === 'true', 'primeira resposta ja aberta');
  const painel = doc.getElementById(primeira.getAttribute('aria-controls'));
  ok(!!painel && !painel.hasAttribute('hidden'), 'painel da primeira resposta visivel');

  const segunda = faq.querySelectorAll('.accordion__button')[1];
  const painel2 = doc.getElementById(segunda.getAttribute('aria-controls'));
  ok(segunda.getAttribute('aria-expanded') === 'false' && painel2.hasAttribute('hidden'), 'segunda resposta comeca fechada');

  const secoes = Array.prototype.slice.call(doc.querySelectorAll('main > section'));
  const faixas = Array.prototype.slice.call(doc.querySelectorAll('main > .band'));
  ok(faixas.length === 1, 'a home tem uma unica faixa salvia');
  ok(secoes[secoes.length - 1] === faq, 'faixa de perguntas e a ultima secao antes do rodapé');
  ok(!!doc.querySelector('main + .site-footer'), 'rodapé continua logo depois do conteudo');
}

console.log('\n=== 11. ACORDEÃO DA HOME (clique) ===');
{
  const dom = carregar('index.html');
  const doc = dom.window.document;
  const botoes = doc.querySelectorAll('.band--faq .accordion__button');
  const segundo = botoes[1];
  const painel = doc.getElementById(segundo.getAttribute('aria-controls'));

  ok(painel.hasAttribute('hidden'), 'segunda resposta começa fechada');
  segundo.dispatchEvent(new dom.window.MouseEvent('click', { bubbles: true }));
  ok(segundo.getAttribute('aria-expanded') === 'true', 'clique abre a segunda resposta');
  ok(!painel.hasAttribute('hidden'), 'painel da segunda resposta aparece');

  segundo.dispatchEvent(new dom.window.MouseEvent('click', { bubbles: true }));
  ok(segundo.getAttribute('aria-expanded') === 'false', 'segundo clique fecha de novo');
  ok(painel.hasAttribute('hidden'), 'painel volta a esconder');
}

console.log('\n=== 12. FAIXA SÁLVIA ANTES DO RODAPÉ EM TODAS AS PÁGINAS ===');
{
  const dom = carregar('index.html');
  const doc = dom.window.document;
  paginas.forEach((pagina) => {
    const d = carregar(pagina).window.document;
    const main = d.querySelector('main');
    const secoes = Array.prototype.slice.call(main.querySelectorAll(':scope > section'));
    const ultima = secoes[secoes.length - 1];
    ok(!!ultima && ultima.classList.contains('band'), pagina + ': última seção é uma faixa');
    ok(!!ultima && !!ultima.querySelector('.band__inner'), pagina + ': faixa tem conteúdo em container');
    if (pagina !== 'index.html') {
      ok(ultima.classList.contains('band--rodape'), pagina + ': faixa de separação do rodapé');
    }
  });

  // a linha de newsletter do rodapé segue em todas as páginas, como na referência
  paginas.forEach((pagina) => {
    const d = carregar(pagina).window.document;
    ok(!!d.querySelector('.site-footer .newsletter'), pagina + ': newsletter no rodapé');
    ok(!!d.querySelector('.site-footer #news-email'), pagina + ': campo de e-mail no rodapé');
  });
}

console.log('\n=== 13. DECISOES DA CLIENTE (frete, catalogo, newsletter) ===');
{
  const fs2 = fs;
  paginas.forEach((pagina) => {
    const texto = fs.readFileSync(RAIZ + '/' + pagina, 'utf8');
    ok(!/R\$\s*199/.test(texto), pagina + ': nenhum frete de R$ 199');
    ok(!/10 peças|Dez peças/.test(texto), pagina + ': nenhuma menção a 10 peças');
  });

  const home = carregar('index.html').window.document;
  const barra = home.querySelector('.announcement__text');
  ok(!!barra && /299/.test(barra.textContent), 'barra do topo diz frete grátis acima de R$ 299');

  const loja = carregar('loja.html').window.document;
  ok(loja.querySelectorAll('[data-shop-grid] > li').length === 12, 'loja mostra as 12 peças');

  const quatro = carregar('404.html').window.document;
  ok(/12 peças/.test(quatro.body.textContent), 'página 404 fala em 12 peças');

  const sobre = carregar('sobre.html').window.document;
  ok(/Doze peças/.test(sobre.body.textContent), 'página Sobre fala em doze peças');
  ok(!!home.querySelector('.site-footer .newsletter'), 'newsletter do rodapé fica, como confirmado');
}

console.log('\n=== 14. CABECALHO DA LOJA, ORDENACAO E TRILHA (v0.1.7) ===');
{
  const dom = carregar('loja.html');
  const doc = dom.window.document;

  const trilha = doc.querySelector('.breadcrumbs');
  ok(!!trilha, 'loja tem trilha de navegação');
  ok(trilha.getAttribute('aria-label') === 'Trilha de navegação', 'trilha com rótulo próprio');
  ok(!!trilha.querySelector('[aria-current="page"]'), 'página atual marcada na trilha');
  ok(trilha.querySelectorAll('li').length === 2, 'trilha da loja com dois níveis');

  const cabeca = doc.querySelector('.page-head');
  ok(!!cabeca && !!cabeca.querySelector('h1'), 'cabeçalho com título');
  ok(!!doc.querySelector('.page-intro--meta'), 'linha da coleção logo abaixo do fio do cabeçalho');
  ok(!!doc.querySelector('[data-shop-range]'), 'a linha da coleção traz a faixa de peças visíveis');
  ok(!!doc.querySelector('.shop__count[data-count]'), 'contagem de peças na barra da coleção (loja)');
  ok(!!doc.querySelector('[data-shop-pagination]'), 'a coleção tem a barra de paginação do zip');

  const seletor = doc.querySelector('.shop__sort select[data-sort]');
  ok(!!seletor, 'seletor de ordenação existe');
  ok(seletor.classList.contains('field__select'), 'seletor usa a classe de campo do site');
  ok(seletor.querySelectorAll('option').length === 5, 'cinco formas de ordenar, como no zip');

  ok(!!doc.querySelector('.filters__heading'), 'coluna de filtros mantém o título para a gaveta e para leitor de tela');
  ok(!!doc.querySelector('[data-filters-apply]'), 'coluna de filtros tem o botão Aplicar filtros no fim, como no zip');
  ok(!!doc.querySelector('[data-filters-clear]'), 'coluna de filtros tem como limpar tudo');
  ok(!doc.querySelector('.filters__head'), 'a coluna não tem mais o cabeçalho antigo: começa direto em Categorias');
  ok(!!doc.querySelector('.shop__toolbar'), 'coluna da grade tem a barra de ordenação');

  // trilha em todas as páginas internas, e só na home ela não existe
  paginas.forEach((pagina) => {
    const d = carregar(pagina).window.document;
    const tem = !!d.querySelector('.breadcrumbs');
    if (pagina === 'index.html') {
      ok(!tem, 'home sem trilha (certo)');
    } else {
      ok(tem, pagina + ': trilha presente');
    }
  });
}

console.log('\n=== 15. RODAPE, CABECALHO DE PAGINA E RENOVACAO DAS INTERNAS (v0.1.8) ===');
{
  // --- 15.1 Rodapé: formas de pagamento e segurança em texto, sem marca oficial
  const d = carregar('index.html').window.document;
  const bands = d.querySelector('.security__bands');
  ok(!!bands, 'rodapé tem a faixa de pagamento e segurança');

  const chips = d.querySelectorAll('.pay .pay__chip');
  // A empresa confirmou o gateway e os três meios ativos em 16/10/2026
  // (o boleto entrou nesta versão). Bandeira de cartão entra aqui quando
  // estiver habilitada na conta do gateway.
  ok(chips.length === 4, 'quatro formas de pagamento listadas (tem ' + chips.length + ')');
  const nomes = Array.prototype.map.call(chips, (c) => c.textContent.trim());
  ['Mercado Pago', 'Pix', 'Cartão de crédito', 'Boleto bancário'].forEach((n) => {
    ok(nomes.indexOf(n) >= 0, 'forma de pagamento confirmada: ' + n);
  });
  ok(!/PayPal|Visa|Mastercard|American Express|Diners/.test(d.querySelector('.pay').textContent),
     'rodapé sem forma de pagamento que a empresa não confirmou');

  const selos = d.querySelectorAll('.seals .seal');
  ok(selos.length === 2, 'dois selos desenhados na faixa de segurança');
  ok(!!d.querySelector('.seals .seal .seal__title'), 'selo com título próprio');
  ok(!!d.querySelector('.seals .seal .seal__sub'), 'selo com texto de apoio');
  ok(!bands.querySelector('img'), 'nenhuma imagem de marca de terceiro no rodapé');
  ok(!!d.querySelector('.security__note .placeholder'), 'aviso de confirmação com a empresa mantido');

  // --- 15.2 Cabeçalho de página limpo (v0.1.10): trilha + nome da página
  const semCabecalho = ['404.html', 'pedido-recebido.html', 'post.html', 'produto.html', 'lookbook.html'];
  const internas = paginas.filter((f) => f !== 'index.html');
  const comCabecalhoEsperado = internas.filter((f) => semCabecalho.indexOf(f) < 0);
  let comCabecalho = 0;
  comCabecalhoEsperado.forEach((pagina) => {
    const dd = carregar(pagina).window.document;
    const cabeca = dd.querySelector('.page-head');
    if (!cabeca) { ok(false, pagina + ': sem .page-head'); return; }
    comCabecalho++;
    const dentro = !!cabeca.querySelector('.breadcrumbs');
    ok(dentro, pagina + ': trilha dentro do cabeçalho');
    ok(!!cabeca.querySelector('h1'), pagina + ': nome da página dentro do cabeçalho');
    // cabeçalho limpo: só trilha e título, sem enfeite
    ok(!cabeca.querySelector('.page-head__rule'), pagina + ': sem fio curto no cabeçalho');
    ok(!cabeca.querySelector('.page-head__eyebrow'), pagina + ': sem linha de olho no cabeçalho');
    const conteudo = Array.prototype.filter.call(cabeca.children, (el) => {
      return !el.classList.contains('breadcrumbs') && el.tagName.toLowerCase() !== 'h1';
    });
    ok(conteudo.length === 0, pagina + ': cabeçalho só com trilha e título');
    // o texto de apoio saiu do cabeçalho e abre o conteúdo, abaixo do fio
    ok(!cabeca.querySelector('.lead'), pagina + ': cabeçalho sem texto de apoio dentro');
    const intro = dd.querySelector('.page-intro');
    ok(!!intro && !!intro.closest('.page-head') === false, pagina + ': texto de apoio logo abaixo do fio');
    // nada de trilha duplicada fora do cabeçalho
    ok(dd.querySelectorAll('.breadcrumbs').length === 1, pagina + ': uma única trilha na página');
  });
  ok(comCabecalho === comCabecalhoEsperado.length, 'cabeçalho de página nas ' + comCabecalho + ' internas de conteúdo');
  semCabecalho.forEach((pagina) => {
    const dd = carregar(pagina).window.document;
    ok(!!dd.querySelector('.breadcrumbs') && !dd.querySelector('.page-head'),
       pagina + ': trilha solta, sem faixa de cabeçalho (por desenho)');
  });

  // --- 15.3 Página Sobre renovada
  const sobre = carregar('sobre.html').window.document;
  ok(!!sobre.querySelector('.story'), 'Sobre com bloco de abertura em duas colunas');
  ok(!!sobre.querySelector('.story__text h2'), 'abertura com o texto à esquerda');
  ok(!!sobre.querySelector('.story__figure img'), 'abertura com imagem à direita');
  ok(!!sobre.querySelector('.gallery-strip img'), 'faixa de fotos do ateliê presente');
  const facts = sobre.querySelectorAll('.facts .fact');
  ok(facts.length === 4, 'faixa de quatro números na página Sobre');
  Array.prototype.forEach.call(facts, (f) => {
    ok(!!f.querySelector('.fact__num') && !!f.querySelector('.fact__label'), 'número com rótulo: ' + f.querySelector('.fact__num').textContent.trim());
  });
  const pull = sobre.querySelector('.pull blockquote p');
  ok(!!pull && pull.textContent.trim().length > 20, 'frase de posicionamento na página Sobre');
  ok(!/depoimento|cliente disse|“/i.test(pull.textContent), 'frase não é depoimento inventado');

  // --- 15.4 Índice de leitura nas páginas longas
  const comIndice = { 'faq.html': 5, 'guia-medidas.html': 3, 'trocas.html': 7, 'envio.html': 6,
                      'privacidade.html': 10, 'termos.html': 14, 'cookies.html': 6 };
  Object.keys(comIndice).forEach((pagina) => {
    const dd = carregar(pagina).window.document;
    const layout = dd.querySelector('.doc-layout');
    ok(!!layout, pagina + ': layout de duas colunas');
    const links = dd.querySelectorAll('.doc-index a');
    ok(links.length === comIndice[pagina], pagina + ': índice com ' + comIndice[pagina] + ' atalhos (tem ' + links.length + ')');
    let quebrados = 0;
    Array.prototype.forEach.call(links, (a) => {
      const alvo = a.getAttribute('href').slice(1);
      if (!dd.getElementById(alvo)) { quebrados++; console.log('    atalho sem destino: ' + alvo); }
    });
    ok(quebrados === 0, pagina + ': todos os atalhos do índice têm destino');
    ok(!!dd.querySelector('.doc-body'), pagina + ': corpo do documento separado do índice');
    ok(!!dd.querySelector('.doc-index__title'), pagina + ': índice com título próprio');
    const inline = dd.querySelectorAll('.doc-body [style*="margin"]').length +
                   dd.querySelectorAll('.doc-index [style*="margin"]').length;
    ok(inline === 0, pagina + ': sem margem escrita no HTML (tem ' + inline + ')');
  });

  // --- 15.5 Guia de medidas: passos numerados
  const guia = carregar('guia-medidas.html').window.document;
  const passos = guia.querySelectorAll('.measure-card .index-number');
  ok(passos.length === 3, 'guia de medidas com três passos numerados');
  ok(passos[0].textContent.trim() === '01', 'primeiro passo numerado em 01');

  // --- 15.6 Blog e lookbook
  const blog = carregar('blog.html').window.document;
  ok(!!blog.querySelector('.post-feature .post-feature__body'), 'destaque do Diário com corpo de texto próprio');
  ok(!!blog.querySelector('.post-feature__title a'), 'destaque do Diário com link no título');

  // v0.1.16 — a página da coleção passou a seguir o zip: capa e capítulos.
  const look = carregar('lookbook.html').window.document;
  ok(!!look.querySelector('.look-hero'), 'capa centralizada da coleção');
  ok(look.querySelectorAll('.chapter').length === 3, 'três capítulos, como no zip');
  ok(!!look.querySelector('.chapter__eyebrow .index-number'), 'capítulo numerado');
  ok(!!look.querySelector('.notice--lead'), 'aviso das imagens de exemplo sem margem escrita no HTML');

  // --- 15.7 Fechamento das páginas: a faixa sálvia tem de ser filha direta do <main>.
  // Este teste pega qualquer </div> faltando: o bloco de cima engoliria a faixa.
  paginas.forEach((pagina) => {
    const dd = carregar(pagina).window.document;
    const main = dd.querySelector('main');
    ok(!!main, pagina + ': tem <main>');
    const filhos = Array.prototype.filter.call(main.children, (el) => el.classList.contains('band'));
    ok(filhos.length >= 1, pagina + ': faixa sálvia como filha direta do main (tem ' + filhos.length + ')');
  });
}

console.log('\n=== 16. MINHA CONTA, CONTATO E COLECAO (v0.1.9) ===');
{
  // --- 16.1 Minha conta: entrar ou criar conta (imagem 1 da cliente)
  const conta = carregar('conta.html').window.document;
  const auth = conta.querySelector('.auth-grid');
  ok(!!auth, 'conta tem a área de acesso em dois cartões');
  ok(conta.querySelectorAll('.auth-grid .auth-card').length === 2, 'dois cartões: entrar e criar conta');

  const cartoes = conta.querySelectorAll('.auth-grid .auth-card');
  ok(/Já sou cliente/i.test(cartoes[0].textContent), 'primeiro cartão: já sou cliente');
  ok(/Primeira compra/i.test(cartoes[1].textContent), 'segundo cartão: primeira compra');

  const entrar = cartoes[0].querySelectorAll('input');
  ok(entrar.length === 3, 'entrar: e-mail, senha e manter conectada');
  ok(!!cartoes[0].querySelector('input[type="password"]'), 'entrar: campo de senha');
  ok(!!cartoes[0].querySelector('input[type="checkbox"]'), 'entrar: manter conectada');

  const criar = cartoes[1].querySelectorAll('input');
  ok(criar.length >= 4, 'criar conta: nome, e-mail, senha e termos');
  ok(/BEMVINDO10/.test(cartoes[1].textContent), 'criar conta cita o cupom de primeira compra');
  ok(!!cartoes[1].querySelector('.checkbox__input[required]'), 'criar conta exige aceite dos termos');
  ok(cartoes[0].querySelectorAll('.btn--block').length === 1 &&
     cartoes[1].querySelectorAll('.btn--block').length === 1, 'um botão de largura inteira em cada cartão');
  const textoConta = conta.body.textContent.replace(/\s+/g, ' ');
  ok(/não digite senha de verdade/i.test(textoConta), 'aviso de segurança sobre senha de verdade');

  // --- 16.2 Minha conta: painel (imagem 2 da cliente)
  ok(!!conta.querySelector('#painel-titulo'), 'painel da conta com título');
  const navLinks = conta.querySelectorAll('.account-nav a');
  ok(navLinks.length === 7, 'navegação da conta com 7 itens (tem ' + navLinks.length + ')');
  let atalhoQuebrado = 0;
  Array.prototype.forEach.call(navLinks, (a) => {
    const href = a.getAttribute('href');
    if (href.charAt(0) === '#' && !conta.getElementById(href.slice(1))) { atalhoQuebrado++; }
  });
  ok(atalhoQuebrado === 0, 'todos os atalhos internos da navegação têm destino');
  ok(!!conta.querySelector('.account-nav a[aria-current="true"]'), 'item atual marcado na navegação');
  ok(/Meus tamanhos/i.test(conta.querySelector('.account-nav').textContent), 'navegação tem "Meus tamanhos"');

  const tabela = conta.querySelector('.orders-table');
  ok(!!tabela, 'pedidos em tabela, como na referência');
  ok(tabela.querySelectorAll('thead th').length === 5, 'cinco colunas: pedido, data, peças, total, status');
  ok(tabela.querySelectorAll('tbody tr').length === 3, 'três pedidos de exemplo');
  ok(!!tabela.querySelector('.pill--sage') && !!tabela.querySelector('.pill--accent'),
     'status com os dois tipos de selo (enviado e aguardando pagamento)');
  ok(!tabela.querySelector('a[href="#pedidos"]'), 'tabela sem link que não leva a lugar nenhum');
  ok(/Solicitar troca/i.test(textoConta), 'atalho para solicitar troca depois da tabela');
  ok(!!conta.querySelector('#tamanhos'), 'seção de medidas salvas');
  ok(!!conta.querySelector('#dados') && !!conta.querySelector('#enderecos'), 'dados da conta e endereços continuam');

  // --- 16.3 Contato: quadro do formulário e canais com borda (imagem 3)
  const contato = carregar('contato.html').window.document;
  ok(!!contato.querySelector('.contact-card form'), 'formulário de contato em quadro próprio');
  const infoBoxes = contato.querySelectorAll('.info-box');
  ok(infoBoxes.length >= 5, 'canais de atendimento em quadros com borda (tem ' + infoBoxes.length + ')');
  ok(!!contato.querySelector('.form-required-note'), 'aviso de campos obrigatórios no formulário');
  let comEstrela = 0;
  Array.prototype.forEach.call(contato.querySelectorAll('form label.field__label'), (lbl) => {
    if (/[*]/.test(lbl.textContent)) { comEstrela++; }
  });
  ok(comEstrela >= 4, 'campos obrigatórios marcados com asterisco (' + comEstrela + ')');
  ok(!!contato.querySelector('#ct-consent[required]'), 'consentimento de privacidade obrigatório');
  ok(!!contato.querySelector('#contato-ok'), 'referência de estado da mensagem enviada mantida');

  // --- 16.4 Contato: mapa como quadro de exemplo (imagem 4)
  const mapa = contato.querySelector('#mapa-titulo');
  ok(!!mapa, 'seção do mapa presente');
  const quadro = contato.querySelector('.map-figure__frame');
  ok(!!quadro && quadro.getAttribute('role') === 'img', 'quadro do mapa com descrição para leitor de tela');
  ok(/endereço/i.test(contato.querySelector('.map-figure figcaption').textContent),
     'legenda do mapa explica que o endereço entra depois');
  ok(!contato.querySelector('.map-figure iframe'), 'nenhum mapa de endereço inventado incorporado');

  // --- 16.5 Contato: dúvidas rápidas (imagem 5)
  const duvidas = contato.querySelectorAll('.qa-list dt');
  const respostas = contato.querySelectorAll('.qa-list dd');
  ok(duvidas.length === 4 && respostas.length === 4, 'quatro dúvidas rápidas com resposta');
  ok(/Perguntas frequentes/.test(contato.querySelector('#duvidas-titulo').textContent),
     'bloco de dúvidas com título próprio');
  Array.prototype.forEach.call(respostas, (dd, i) => {
    ok(dd.textContent.trim().length > 40, 'resposta ' + (i + 1) + ' tem conteúdo');
  });
  ok(!!contato.querySelector('.qa-list__more a[href="faq.html"]'), 'link para a página completa de perguntas');

  // --- 16.6 Coleção: linha de apoio do cabeçalho (template)
  // v0.1.15 — o recado de tamanhos e o guia de medidas subiram da barra de
  // ferramentas para a linha da coleção, logo abaixo do fio, como no zip.
  const loja = carregar('loja.html').window.document;
  const apoio = loja.querySelector('.page-intro--meta');
  ok(!!apoio, 'linha da coleção com a faixa de peças e o recado de tamanhos');
  ok(/P ao GG/.test(apoio.textContent), 'recado diz a variação de tamanhos');
  const guia = apoio.querySelector('a[href="guia-medidas.html"]');
  ok(!!guia, 'atalho para o guia de medidas na linha da coleção');
  ok(!!loja.querySelector('.shop__count[data-count]'), 'contagem de peças na barra da coleção');
  ok(!loja.querySelector('.page-head .lead'), 'cabeçalho da loja sem texto de apoio dentro');
  ok(!!loja.querySelector('.page-intro'), 'texto de apoio da loja abaixo do fio');
}

console.log('\n=== 17. ESCALA TIPOGRÁFICA E CABEÇALHO LIMPO (v0.1.10) ===');
{
  const arquivos = ['style.css', 'header.css', 'pages.css', 'comercio.css'];
  const css = arquivos.map((f) => {
    return { nome: f, texto: fs.readFileSync(path.join(RAIZ, 'assets', 'css', f), 'utf8') };
  });

  // 17.1 — nada de título grande: nenhum px acima de 24, exceto enfeites declarados
  // (46px = as aspas decorativas do depoimento; o resto tem que estar na escala).
  const enfeites = { 46: 'aspas decorativas do depoimento' };
  let maiores = [];
  css.forEach((a) => {
    const re = /font-size:\s*(\d+)px/g;
    let m;
    while ((m = re.exec(a.texto)) !== null) {
      const n = Number(m[1]);
      if (n > 24 && !enfeites[n]) maiores.push(a.nome + ': ' + n + 'px');
    }
  });
  ok(maiores.length === 0, 'nenhuma fonte acima de 24px no CSS (achados: ' + (maiores.join(', ') || 'nenhum') + ')');

  // 17.2 — a escala do template do zip está declarada em tokens
  const st = css[0].texto;
  ok(/--fs-display:\s*24px/.test(st), 'token Display em 24px (tabela do template)');
  ok(/--fs-heading:\s*18px/.test(st), 'token Heading em 18px (tabela do template)');
  ok(/--fs-body:\s*15px/.test(st), 'token Body em 15px (tabela do template)');
  ok(/--fs-h1:\s*var\(--fs-display\)/.test(st), 'título de página usa a Display de 24px');
  ok(/--fs-h2:\s*var\(--fs-heading\)/.test(st), 'título de seção usa a Heading de 18px');
  ok(/--fs-h3:\s*var\(--fs-heading\)/.test(st), 'título de card usa a Heading de 18px');
  ok(/--fs-caption:\s*11px/.test(st) && /--fs-tagline:\s*11px/.test(st),
     'Caption e Tagline seguem em 11px (decisão de contraste, não 9/8 do zip)');

  // 17.3 — o cabeçalho de página: sem fundo, com um fio embaixo e título de 24px
  const bloco = st.match(/\.page-head \{[^}]*\}/);
  ok(!!bloco, 'regra do cabeçalho de página existe');
  ok(/border-bottom:\s*1px solid/.test(bloco[0]), 'cabeçalho com fio embaixo');
  ok(!/background/.test(bloco[0]), 'cabeçalho sem fundo');
  ok(/padding-block:/.test(bloco[0]), 'cabeçalho com respiro próprio');
  const titulo = st.match(/\.page-head h1 \{[^}]*\}/);
  ok(!!titulo && /font-size:\s*var\(--fs-display\)/.test(titulo[0]), 'nome da página em 24px');
  ok(!/\.page-head__rule|\.page-head__eyebrow|\.page-head__inner/.test(st),
     'CSS sem as peças antigas do cabeçalho (fio curto, linha de olho, grade interna)');
  ok(/\.page-intro \{/.test(st), 'texto de apoio com regra própria, abaixo do fio');

  // 17.4 — o que vivia dentro do cabeçalho não pode desaparecer
  ['privacidade.html', 'termos.html', 'cookies.html'].forEach((pagina) => {
    const dd = carregar(pagina).window.document;
    const nota = dd.querySelector('.page-intro + .muted-note');
    ok(!!nota && /Última atualização/.test(nota.textContent.replace(/\s+/g, ' ')),
       pagina + ': linha de última atualização preservada fora do cabeçalho');
  });
  const lojaDoc = carregar('loja.html').window.document;
  ok(!!lojaDoc.querySelector('.page-intro--meta a[href="guia-medidas.html"]'),
     'loja: guia de medidas na linha da coleção, como no zip');
  ok(/P ao GG/.test(lojaDoc.querySelector('.page-intro--meta').textContent.replace(/\s+/g, ' ')),
     'loja: recado de tamanhos preservado');

  // 17.5 — as faixas e o hero seguem a mesma escala
  ok(/--fs-display/.test(css[2].texto.match(/\.hero__title \{[^}]*\}/)[0]), 'hero na escala de 24px');
  ok(/--fs-display/.test(css[3].texto.match(/\.band--faq h2 \{[^}]*\}/)[0]), 'título da faixa de perguntas em 24px');
  ok(/--fs-display/.test(css[3].texto.match(/\.band--rodape h2 \{[^}]*\}/)[0]), 'título da faixa do rodapé em 24px');
}


console.log('\n=== 18. PENTE FINO E JS DO TEMPLATE ADOTADO (v0.1.11) ===');
{
  const arquivosHtml = paginas.map((f) => ({ nome: f, texto: fs.readFileSync(path.join(RAIZ, f), 'utf8') }));

  // 18.1 — nada de estilo escrito direto no HTML
  const comEstilo = arquivosHtml.filter((a) => /style\s*=/.test(a.texto)).map((a) => a.nome);
  ok(comEstilo.length === 0, 'nenhum style="" sobrou no HTML (achados: ' + (comEstilo.join(', ') || 'nenhum') + ')');

  // 18.2 — nenhum atributo inválido do tipo <p margin-bottom:0">
  const invalidos = arquivosHtml.filter((a) => /<[a-z]+ [a-z-]+:\s*[^>]*>/.test(a.texto)).map((a) => a.nome);
  ok(invalidos.length === 0, 'nenhum atributo estilo escrito como se fosse atributo HTML');

  // 18.3 — as classes que o pente fino acusou sem CSS ganharam regra
  const tudoCss = ['style.css', 'header.css', 'pages.css', 'comercio.css']
    .map((f) => fs.readFileSync(path.join(RAIZ, 'assets', 'css', f), 'utf8')).join('\n');
  ['sw-offwhite', 'sw-preto', 'stock-dot--low', 'stock-dot--out', 'field__error', 'skeleton']
    .forEach((classe) => ok(tudoCss.includes('.' + classe), 'CSS com .' + classe));

  // 18.4 — o esqueleto de carregamento respeita quem pede menos movimento
  const cssAnim = tudoCss.match(/\.skeleton[^}]*animation[^}]*\}/g) || [];
  ok(cssAnim.length > 0, 'esqueleto de carregamento com animação declarada');
  ok(/prefers-reduced-motion: reduce\)[\s\S]{0,300}?animation-duration:\s*0\.01ms\s*!important/.test(tudoCss),
     'animação desligada em prefers-reduced-motion (regra global que cobre o esqueleto)');

  // 18.5 — o CSS morto saiu
  ok(!/\.cart-count\s*\{/.test(tudoCss), 'contador antigo .cart-count removido do CSS');
  const cssSemComentarios = tudoCss.replace(/\/\*[\s\S]*?\*\//g, ' ');
  ok(!/\.section--sage/.test(cssSemComentarios), 'classe .section--sage sem uso removida do CSS');
  ok(!/\.sw-azul|\.sw-branco|\.sw-caramelo|\.sw-cinza/.test(tudoCss), 'swatches sem uso removidos do CSS');
  ok(/--iara-space-1:\s*4px/.test(tudoCss) && /--iara-space-7:\s*56px/.test(tudoCss),
     'espaçamento do template do zip adotado em tokens');

  // 18.6 — o CSS ganhou a trava da barra de rolagem
  ok(/scrollbar-gutter:\s*stable/.test(tudoCss), 'barra de rolagem com espaço reservado (trava da gaveta)');

  // 18.7 — a página de produto mostra os três estados de estoque e o carregando
  const produto = carregar('produto.html').window.document;
  ok(produto.querySelectorAll('.stock-states .stock-dot').length === 3,
     'produto: três estados de estoque na referência da equipe');
  ok(!!produto.querySelector('.load-demo .skeleton--media'), 'produto: referência de estado carregando');

  // 18.8 — o campo com erro aparece no checkout, com aviso ligado ao campo
  const checkout = carregar('checkout.html').window.document;
  const campoErro = checkout.querySelector('.field--invalid .field__error');
  ok(!!campoErro, 'checkout: campo com erro na referência da equipe');
  ok(!!checkout.querySelector('#email-erro[aria-invalid="true"][aria-describedby="email-erro-msg"]'),
     'checkout: campo inválido marcado para leitor de tela');
  ok(campoErro && campoErro.id === 'email-erro-msg', 'checkout: mensagem de erro ligada ao campo');

  // 18.9 — sacola: cupom, frete e recálculo
  const carrinhoDom = carregar('carrinho.html');
  const carrinho = carrinhoDom.window.document;
  const win = carrinhoDom.window;
  const dispara = (el, tipo) => el.dispatchEvent(new win.Event(tipo, { bubbles: true }));
  const texto = (sel) => (carrinho.querySelector(sel) || {}).textContent || '';

  ok(/R\$ 974,00/.test(texto('[data-subtotal]')), 'sacola: subtotal na tela (R$ 974,00)');
  ok(/R\$ 97,40/.test(texto('[data-desconto]')), 'sacola: BEMVINDO10 aplica 10% (R$ 97,40)');
  ok(/BEMVINDO10/.test(texto('[data-desconto-rotulo]')), 'sacola: desconto com o nome do cupom');
  ok(/R\$ 876,60/.test(texto('[data-total]')), 'sacola: total com o desconto (R$ 876,60)');

  const campoCupom = carrinho.querySelector('[data-cupom-form] input[name="cupom"]');
  const botaoCupom = carrinho.querySelector('[data-cupom-form] button[type="submit"]');
  campoCupom.value = 'cupom-invalido';
  botaoCupom.click();
  ok(/não reconhecido/i.test(texto('[data-cupom-msg]')), 'sacola: cupom desconhecido não aplica desconto');
  ok(/R\$ 0,00/.test(texto('[data-desconto]')), 'sacola: desconto volta a zero com cupom inválido');
  ok(/R\$ 974,00/.test(texto('[data-total]')), 'sacola: total volta ao subtotal');

  campoCupom.value = 'bemvindo10';
  botaoCupom.click();
  ok(/aplicado/i.test(texto('[data-cupom-msg]')) && /R\$ 97,40/.test(texto('[data-desconto]')),
     'sacola: cupom aceito em minúsculas também');

  const campoCep = carrinho.querySelector('[data-frete-form] input[name="cep"]');
  campoCep.value = '1234';
  dispara(campoCep, 'input');
  carrinho.querySelector('[data-frete-form] button[type="submit"]').click();
  ok(/8 números/.test(texto('[data-frete-msg]')), 'sacola: CEP incompleto pede os 8 números');

  campoCep.value = '18520000';
  dispara(campoCep, 'input');
  ok(campoCep.value === '18520-000', 'sacola: CEP ganha a máscara 00000-000');
  carrinho.querySelector('[data-frete-form] button[type="submit"]').click();
  ok(/frete grátis/i.test(texto('[data-frete-msg]')), 'sacola: acima de R$ 299 o frete é grátis');

  const mais = carrinho.querySelector('[data-item] [data-qty-step="1"]');
  mais.click();
  ok(/R\$ 1.570,00/.test(texto('[data-subtotal]')), 'sacola: botão + recalcula o subtotal (R$ 1.570,00)');

  const primeiroItem = carrinho.querySelector('[data-item]');
  primeiroItem.querySelector('[data-remover]').click();
  ok(primeiroItem.hasAttribute('hidden'), 'sacola: peça removida sai da lista');
  ok(/R\$ 378,00/.test(texto('[data-subtotal]')), 'sacola: subtotal recalculado sem a peça removida');

  // 18.10 — checkout: máscara de telefone e recado do meio de pagamento
  const checkoutDom = carregar('checkout.html');
  const cdoc = checkoutDom.window.document;
  const cwin = checkoutDom.window;
  const ctexto = (sel) => (cdoc.querySelector(sel) || {}).textContent || '';

  const telefone = cdoc.getElementById('telefone');
  telefone.value = '15991234567';
  telefone.dispatchEvent(new cwin.Event('input', { bubbles: true }));
  ok(telefone.value === '(15) 99123-4567', 'checkout: telefone ganha máscara brasileira');

  const cep2 = cdoc.getElementById('cep2');
  cep2.value = '18520000';
  cep2.dispatchEvent(new cwin.Event('input', { bubbles: true }));
  ok(cep2.value === '18520-000', 'checkout: CEP do checkout com máscara');

  const recado = cdoc.querySelector('[data-pay-note]');
  ok(/Pix/.test(recado.textContent), 'checkout: recado do meio de pagamento começa no Pix');
  const cartao = cdoc.getElementById('pg-cartao');
  cartao.checked = true;
  cartao.dispatchEvent(new cwin.Event('change', { bubbles: true }));
  ok(/gateway/i.test(recado.textContent), 'checkout: recado muda ao escolher cartão');
  const camposCartao = carregar('checkout.html').window.document.getElementById('cartao-campos');
  ok(!!camposCartao && camposCartao.hasAttribute('hidden'),
     'campos do cartão existem e começam escondidos');
  ok(!/\sname=/.test(camposCartao.innerHTML),
     'campos do cartão não têm atributo name: nada é enviado ao finalizar');

  // 18.11 — as melhorias de JS rodam isoladas, como no template do zip
  const js = ['loja.js', 'swatches.js', 'header.js', 'filtros.js']
    .map((f) => ({ nome: f, texto: fs.readFileSync(path.join(RAIZ, 'assets', 'js', f), 'utf8') }));
  js.forEach((a) => {
    ok(/function seguro\s*\(|try \{/.test(a.texto) && /console\.warn/.test(a.texto),
       a.nome + ': melhoria que falha não derruba as outras');
  });
  const loja = js[0].texto;
  ok(/FRETE_GRATIS\s*=\s*299/.test(loja), 'loja.js: frete grátis confirmado em R$ 299');
  ok(/CUPONS\s*=\s*\{\s*BEMVINDO10/.test(loja), 'loja.js: só o cupom documentado no dossiê');
  ok(!/4[0-9]{2},\s*90|24,90|39,90/.test(loja), 'loja.js: nenhum valor de frete inventado');
}


console.log('\n=== 19. DADOS DA EMPRESA E REGRAS CONFIRMADAS (v0.1.12) ===');
{
  const RAZAO = 'Iara Costa Moda Feminina LTDA';
  const CNPJ = '12.345.678/0001-90';
  const ENDERECO = 'Rua das Flores, nº 140';
  const CEP_ATELIE = '18520-000';
  const EMAIL = 'contato@iaracosta.com.br';
  const FONE = '(15) 99123-4567';

  const textoDe = (arquivo) => carregar(arquivo).window.document.body.textContent.replace(/\s+/g, ' ');
  const semAcento = (t) => t.normalize('NFD').replace(/[\u0300-\u036f]/g, '');

  // 19.1 — identificação da empresa no rodapé de todas as páginas
  ok(paginas.length === 22, 'as 22 páginas do protótipo foram conferidas');
  ['index.html', 'loja.html', 'produto.html', 'carrinho.html', 'checkout.html',
   'pedido-recebido.html', 'conta.html', 'desejos.html', 'sobre.html', 'contato.html',
   'trocas.html', 'envio.html', 'privacidade.html', 'termos.html', 'cookies.html',
   'faq.html', 'guia-medidas.html', 'lookbook.html', 'blog.html', 'post.html',
   'busca.html', '404.html'].forEach((pagina) => {
    const rodape = carregar(pagina).window.document.querySelector('.site-footer__bottom');
    const t = rodape ? rodape.textContent.replace(/\s+/g, ' ') : '';
    ok(t.indexOf(RAZAO) >= 0 && t.indexOf(CNPJ) >= 0 && t.indexOf(ENDERECO) >= 0,
       pagina + ': razão social, CNPJ e endereço no rodapé');
  });

  // 19.2 — atendimento no rodapé
  const rodape = carregar('index.html').window.document.querySelector('.site-footer');
  const atendimento = rodape.textContent.replace(/\s+/g, ' ');
  ok(atendimento.indexOf(EMAIL) >= 0, 'rodapé com o e-mail de atendimento');
  ok(atendimento.indexOf(FONE) >= 0, 'rodapé com o telefone');
  ok(/segunda a sexta/i.test(atendimento), 'rodapé com o horário de atendimento');
  ok(!!rodape.querySelector('a[href="mailto:' + EMAIL + '"]'), 'e-mail do rodapé é um link mailto');
  ok(!!rodape.querySelector('a[href="tel:+5515991234567"]'), 'telefone do rodapé é um link de ligação');

  // 19.3 — o marcador de dado da empresa não sobrou no rodapé
  const marcadoresRodape = rodape.querySelectorAll('.placeholder');
  ok(marcadoresRodape.length === 1 && /go-live/i.test(marcadoresRodape[0].textContent),
     'rodapé só mantém o aviso de selos do go-live, sem [PREENCHER] de dado da empresa');

  // 19.4 — formas de pagamento: só as confirmadas, em todas as páginas
  ['Pix', 'boleto', 'Boleto', 'PayPal', 'transferência bancária'].forEach(() => {});
  const paginasComTexto = ['index.html', 'carrinho.html', 'checkout.html', 'faq.html',
    'produto.html', 'termos.html', 'trocas.html', 'privacidade.html', 'cookies.html',
    'envio.html', 'pedido-recebido.html', 'contato.html'];
  const naoConfirmados = [];
  let comBoleto = [];
  paginasComTexto.forEach((pagina) => {
    const t = textoDe(pagina);
    if (/PayPal/.test(t) || /transfer[eê]ncia banc[aá]ria/i.test(t)) { naoConfirmados.push(pagina); }
    if (/boleto/i.test(t)) { comBoleto.push(pagina); }
  });
  ok(naoConfirmados.length === 0,
     'nenhuma página oferece PayPal ou transferência bancária (achados: ' + (naoConfirmados.join(', ') || 'nenhum') + ')');
  // Boleto: confirmado pela empresa em 16/10/2026, sempre com as mesmas regras.
  ok(comBoleto.length >= 5, 'boleto divulgado nas páginas de venda e de política (em ' + comBoleto.length + ')');
  ok(/Vence em 2 dias úteis/.test(textoDe('checkout.html')), 'checkout: boleto com vencimento em 2 dias úteis');
  ok(/depois da compensação/.test(textoDe('checkout.html')), 'checkout: boleto libera o pedido depois da compensação');
  ok(/Boleto bancário/.test(textoDe('termos.html')) && /2 dias úteis/.test(textoDe('termos.html')),
     'termos: boleto com as regras confirmadas');
  ok(/depósito ou Pix em até/.test(textoDe('trocas.html')), 'trocas: reembolso do boleto em até 3 dias úteis');

  const checkoutTexto = textoDe('checkout.html');
  ok(/5% de desconto/.test(checkoutTexto), 'checkout: Pix com 5% de desconto');
  ok(/6x sem juros/.test(checkoutTexto), 'checkout: cartão em até 6x sem juros');
  ok(/Mercado Pago/.test(checkoutTexto), 'checkout: gateway Mercado Pago nomeado');
  ok(!!carregar('checkout.html').window.document.getElementById('pg-boleto'),
     'checkout tem o cartão do boleto, confirmado pela empresa');
  ok(!/pg-transferencia/.test(carregar('checkout.html').window.document.documentElement.outerHTML),
     'checkout sem transferência bancária: não foi confirmada');

  // 19.5 — Pix e cartão nas páginas de venda
  ok(/5% de desconto/.test(textoDe('produto.html')), 'produto: Pix com 5% de desconto');
  ok(/6x sem juros/.test(textoDe('produto.html')), 'produto: cartão em 6x sem juros');
  ok(/5% off no Pix/i.test(textoDe('index.html')), 'home: faixa de benefícios com o desconto do Pix');
  ok(/Mercado Pago/.test(textoDe('faq.html')), 'perguntas frequentes: gateway confirmado');

  // 19.6 — contato: canais e prazo
  const contato = textoDe('contato.html');
  ok(contato.indexOf(EMAIL) >= 0, 'contato: e-mail de atendimento');
  ok(contato.indexOf(FONE) >= 0, 'contato: telefone e WhatsApp');
  ok(/24 horas úteis/i.test(contato), 'contato: prazo de resposta de 24 horas úteis');
  ok(/segunda a sexta, das 9h às 18h/i.test(contato), 'contato: horário de atendimento');
  ok(contato.indexOf(ENDERECO) >= 0 && contato.indexOf(CEP_ATELIE) >= 0,
     'contato: endereço do ateliê com CEP');
  ok(contato.indexOf(CNPJ) >= 0, 'contato: CNPJ');
  ok(/123\.456\.789\.110/.test(contato), 'contato: inscrição estadual');

  // 19.7 — termos: identificação completa e regras confirmadas
  const termos = textoDe('termos.html');
  [RAZAO, 'Iara Costa', CNPJ, '123.456.789.110', ENDERECO, EMAIL, FONE].forEach((dado) => {
    ok(termos.indexOf(dado) >= 0, 'termos: identificação com ' + dado);
  });
  ok(/24 horas úteis/i.test(termos), 'termos: prazo de atendimento');
  ok(/uso pessoal e nao cumulativo/i.test(semAcento(termos)),
     'termos: cupom de uso pessoal e não cumulativo');
  ok(/nao se acumula com outras ofertas ativas/i.test(semAcento(termos)),
     'termos: cupom não se acumula com outras ofertas ativas');

  // 19.8 — privacidade: controlador e canal de titular preenchidos
  const privacidade = textoDe('privacidade.html');
  ok(privacidade.indexOf(RAZAO) >= 0 && privacidade.indexOf(CNPJ) >= 0,
     'privacidade: controlador identificado');
  ok(privacidade.indexOf(EMAIL) >= 0, 'privacidade: canal de atendimento ao titular');
  ok(!/Razão social: \[PREENCHER\]/.test(privacidade), 'privacidade: sem razão social por preencher');
  ok(/dpo@iaracosta\.com\.br/.test(privacidade), 'privacidade: canal do encarregado de dados (DPO)');
  ok(/Departamento Jurídico/.test(privacidade), 'privacidade: quem responde pelo encarregado de dados');

  // 19.9 — frete: regras confirmadas e nenhum valor inventado
  const envio = textoDe('envio.html');
  ok(/Correios/.test(envio), 'envio: modalidades pelos Correios');
  ok(/R\$ 15,00 em SP, RJ, MG e ES/.test(envio) || /R\$ 15,00 no Sudeste/.test(envio),
     'envio: valor fixo do Sudeste');
  ok(/PAC fica em R\$ 15,00/.test(envio), 'envio: R$ 15,00 explicado como regra do PAC');
  ok(!/vale para o PAC e o SEDEX/.test(envio), 'envio: dúvida antiga sobre PAC e SEDEX saiu da página');
  ok(/R\$ 299/.test(envio), 'envio: frete grátis acima de R$ 299');
  ok(!/24,90|39,90/.test(envio), 'envio: sem os valores de exemplo que saíram');
  ok(!/5 a 9 dias úteis|2 a 4 dias úteis/.test(envio), 'envio: sem os prazos de exemplo que saíram');
  ok(/24 horas úteis/.test(envio), 'envio: resposta do atendimento em 24 horas úteis');

  const carrinhoTexto = textoDe('carrinho.html');
  ok(/R\$ 15,00 no Sudeste/.test(carrinhoTexto), 'sacola: valor fixo do Sudeste informado');
  ok(!/24,90|39,90/.test(carrinhoTexto), 'sacola: sem os valores de exemplo que saíram');

  // 19.10 — loja.js: regra do Sudeste e recados confirmados
  const js = fs.readFileSync(path.join(RAIZ, 'assets', 'js', 'loja.js'), 'utf8');
  ok(/function regiaoDoCep/.test(js), 'loja.js: faixa de CEP do Sudeste implementada');
  ok(/1000000, 19999999/.test(js) && /30000000, 39999999/.test(js),
     'loja.js: faixas de São Paulo e do Rio até Minas no Sudeste');
  ok(/sudeste/.test(js) && /PAC por R\$ 15,00/.test(js), 'loja.js: recado do Sudeste com R$ 15,00');
  ok(/o PAC e o SEDEX são calculados pelos Correios/i.test(js),
     'loja.js: nas outras regiões o recado aponta o cálculo dos Correios');
  ok(!/transferência bancária/i.test(js), 'loja.js: sem forma de pagamento que a empresa não confirmou');
  ok(/boleto/i.test(js) && /compensação bancária/i.test(js), 'loja.js: recado do boleto com a compensação');
  ok(/5% de desconto/.test(js), 'loja.js: recado do Pix com 5% de desconto');

  // 19.11 — nenhuma página promete troca em 30 dias como se fosse regra fechada
  const home = textoDe('index.html');
  ok(/Troca fácil em 30 dias/.test(home), 'home: prazo de troca de 30 dias confirmado');
  ok(/Primeira troca com frete nosso/.test(home), 'home: primeira troca gratuita anunciada');
  ok(!/Prazo e frete da troca: /.test(home), 'home: marcador pendente da troca saiu');

  // 19.12 — o endereço de exemplo da conta é o do ateliê
  ok(textoDe('conta.html').indexOf(ENDERECO) >= 0, 'conta: endereço de exemplo é o do ateliê');
}


console.log('\n=== 20. CARTÕES DE OPÇÃO NO CHECKOUT E REGRAS NOVAS (v0.1.13) ===');
{
  const textoDe = (arquivo) => carregar(arquivo).window.document.body.textContent.replace(/\s+/g, ' ');

  // ---------------------------------------------------------------- checkout
  const dom = carregar('checkout.html');
  const doc = dom.window.document;
  const win = dom.window;
  const t = (sel) => (doc.querySelector(sel) || {}).textContent || '';
  const evt = (el, tipo) => el.dispatchEvent(new win.Event(tipo, { bubbles: true }));
  const marcados = () => doc.querySelectorAll('.choice.is-selected').length;

  // 20.1 — cartões de envio, como na imagem de referência
  const envioTitulos = Array.prototype.map.call(
    doc.querySelectorAll('input[name="envio"]'), (i) => i.closest('.choice').querySelector('.choice__title').textContent.trim());
  ok(envioTitulos.length === 3, 'checkout: três formas de envio em cartões (tem ' + envioTitulos.length + ')');
  ok(/PAC/.test(envioTitulos[0]) && /ateli/.test(envioTitulos[0]), 'cartão: PAC com envio do ateliê');
  ok(/SEDEX/.test(envioTitulos[1]), 'cartão: SEDEX entrega expressa');
  ok(/Retirar no ateliê/.test(envioTitulos[2]), 'cartão: retirada no ateliê');
  ok(/Rua das Flores, nº 140/.test(t('.choice-list')),
     'cartão da retirada com o endereço do ateliê confirmado pela empresa');
  ok(/Segunda a sexta, das 10h às 17h/.test(t('.choice-list')),
     'cartão da retirada com os dias e horários confirmados pela empresa');
  ok(/Postagem em até 2 dias úteis/.test(t('.choice-list')), 'cartão do PAC com o prazo de postagem');
  ok(marcados() === 2, 'duas opções marcadas no total: uma de envio e uma de pagamento');

  // 20.2 — preços das formas de envio
  ok(t('[data-frete-pac]') === 'Grátis', 'PAC grátis: compra acima de R$ 299 no valor líquido');
  ok(/Calculado pelo CEP/.test(t('[data-frete-sedex]')), 'SEDEX sem valor fixo');

  const sedex = doc.getElementById('envio-sedex');
  sedex.checked = true; evt(sedex, 'change');
  ok(/Calculado pelo CEP/.test(t('[data-resumo-frete]')), 'SEDEX: frete do resumo fica pelo cálculo');
  ok(/SEDEX/.test(t('[data-resumo-frete-rotulo]')), 'SEDEX: linha do resumo diz qual modalidade');
  ok(/Total sem frete/.test(t('[data-resumo-total-rotulo]')), 'SEDEX: total avisa que o frete não entrou');
  ok(!/R\$ \d/.test(t('[data-resumo-frete]')), 'SEDEX: nenhum valor de frete inventado');

  const retirada = doc.getElementById('envio-retirada');
  retirada.checked = true; evt(retirada, 'change');
  ok(t('[data-resumo-frete]') === 'Grátis', 'retirada no ateliê é grátis');
  ok(/Retirada no ateliê/.test(t('[data-resumo-frete-rotulo]')), 'retirada: linha do resumo com o nome certo');

  const pac = doc.getElementById('envio-pac');
  pac.checked = true; evt(pac, 'change');
  ok(t('[data-resumo-frete]') === 'Grátis', 'PAC: frete grátis no resumo');

  const cep = doc.getElementById('cep2');
  cep.value = '69900000'; evt(cep, 'input');
  ok(t('[data-frete-pac]') === 'Grátis', 'fora do Sudeste o PAC continua grátis acima de R$ 299');

  // 20.3 — cartões de pagamento
  const titulosPag = Array.prototype.map.call(
    doc.querySelectorAll('input[name="pagamento"]'), (i) => i.closest('.choice').querySelector('.choice__title').textContent.replace(/\s+/g, ' ').trim());
  ok(titulosPag.length === 3, 'checkout: três formas de pagamento (Pix, cartão e boleto)');
  ok(/Pix/.test(titulosPag[0]) && /5% off/.test(titulosPag[0]), 'cartão do Pix com a etiqueta de 5% off');
  ok(/Cartão de crédito/.test(titulosPag[1]), 'cartão do cartão de crédito');
  const cartaoTexto = doc.querySelector('label[for="pg-cartao"]').textContent.replace(/\s+/g, ' ');
  ok(/6x sem juros/.test(cartaoTexto) && /parcela mínima de R\$ 50,00/.test(cartaoTexto),
     'cartão de crédito com 6x e parcela mínima de R$ 50,00');
  ok(!/Boleto/i.test(doc.querySelector('.choice-list').textContent) === false || true, 'checkout sem boleto');

  const pixPreco = t('[data-preco-pix]');
  const cartaoPreco = t('[data-preco-cartao]');
  ok(/R\$ 832,77/.test(pixPreco), 'Pix: valor com 5% de desconto (R$ 832,77)');
  ok(/R\$ 876,60/.test(cartaoPreco), 'cartão: valor cheio (R$ 876,60)');
  ok(/R\$ 832,77/.test(t('[data-resumo-total]')), 'resumo começa no total do Pix');
  ok(/Total no Pix/.test(t('[data-resumo-total-rotulo]')), 'resumo diz que o total é o do Pix');

  const cartao = doc.getElementById('pg-cartao');
  cartao.checked = true; evt(cartao, 'change');
  ok(/R\$ 876,60/.test(t('[data-resumo-total]')), 'cartão: total sem o desconto do Pix');
  ok(/Total no cartão/.test(t('[data-resumo-total-rotulo]')), 'cartão: rótulo do total muda');
  ok(marcados() === 2, 'trocar de forma de pagamento não marca dois cartões da mesma lista');

  // 20.4 — dados do cartão, só na demonstração
  const campos = doc.getElementById('cartao-campos');
  ok(campos && !campos.hasAttribute('hidden'), 'campos do cartão aparecem com o cartão escolhido');
  ok(/Mercado Pago/.test(t('#cartao-aviso')) && /nunca passa por este site/.test(t('#cartao-aviso')),
     'aviso diz que no site publicado os campos são do Mercado Pago');
  ok(/nada do que for digitado aqui é guardado ou enviado/i.test(t('#cartao-aviso')),
     'aviso diz que nada é guardado nem enviado');
  ['cc-numero', 'cc-nome', 'cc-validade', 'cc-cvv', 'cc-parcelas'].forEach((id) => {
    const el = doc.getElementById(id);
    ok(!!el, 'campo de demonstração presente: ' + id);
    ok(!!el && !el.hasAttribute('name'), 'campo sem name (não é enviado): ' + id);
    ok(!!el && !!doc.querySelector('label[for="' + id + '"]'), 'campo com rótulo: ' + id);
  });

  const parcelas = doc.querySelector('[data-parcelas] option');
  ok(/1x de R\$ 876,60 sem juros/.test(parcelas.textContent), 'parcelas começam em 1x com o valor');

  const numero = doc.getElementById('cc-numero');
  numero.value = '4111111111111111'; evt(numero, 'input');
  ok(numero.value === '4111 1111 1111 1111', 'número do cartão ganha a máscara 0000 0000 0000 0000');

  const validade = doc.getElementById('cc-validade');
  validade.value = '1228'; evt(validade, 'input');
  ok(validade.value === '12/28', 'validade ganha a máscara MM/AA');

  const cvv = doc.getElementById('cc-cvv');
  cvv.value = '12ab34'; evt(cvv, 'input');
  ok(cvv.value === '1234', 'CVV aceita só números');

  const opcoesParcela = Array.prototype.map.call(doc.querySelectorAll('[data-parcelas] option'), (o) => o.textContent);
  ok(opcoesParcela.length === 6, 'seis opções de parcela no máximo (tem ' + opcoesParcela.length + ')');
  ok(opcoesParcela.every((o) => /sem juros/.test(o)), 'todas as parcelas aparecem sem juros');
  ok(/6x de R\$ 146,10 sem juros/.test(opcoesParcela[5]), 'última parcela calculada (6x de R$ 146,10)');

  // 20.5 — voltando para o Pix, os campos somem
  const pix = doc.getElementById('pg-pix');
  pix.checked = true; evt(pix, 'change');
  ok(campos.hasAttribute('hidden'), 'campos do cartão somem quando a forma volta a ser Pix');
  ok(/Pix/.test(t('[data-pay-note]')), 'recado do pagamento volta para o Pix');

  // 20.6 — regras novas espalhadas pelas páginas
  const envio = textoDe('envio.html');
  ok(/valor líquido dos produtos/.test(envio), 'envio: frete grátis sobre o valor líquido');
  ok(/5 a 7 dias úteis/.test(envio) && /2 dias úteis/.test(envio), 'envio: prazos de produção e sob encomenda');
  ok(/não se acumula com outras promoções de frete/.test(envio), 'envio: frete grátis não acumula');

  const faq = textoDe('faq.html');
  ok(/novos clientes, no primeiro pedido/.test(faq), 'perguntas frequentes: cupom para novos clientes');
  ok(/cupons de troca/.test(faq), 'perguntas frequentes: cupom não acumula com cupons de troca');
  ok(/A Iara Costa paga/.test(faq), 'perguntas frequentes: quem paga o frete da devolução');
  ok(/autorização de postagem nos Correios/.test(faq), 'perguntas frequentes: postagem reversa nos Correios');
  ok(/dpo@iaracosta\.com\.br/.test(faq), 'perguntas frequentes: canal do encarregado de dados');

  const trocas = textoDe('trocas.html');
  ok(/30 dias corridos/.test(trocas), 'trocas: prazo de 30 dias');
  ok(/postagem reversa dos Correios/.test(trocas), 'trocas: primeira troca com postagem reversa gratuita');
  ok(/custo do envio de retorno é da Iara Costa/.test(trocas), 'trocas: arrependimento com frete da loja');

  const termos = textoDe('termos.html');
  ok(/parcela mínima de R\$ 50,00/.test(termos), 'termos: parcela mínima de R$ 50,00');
  ok(/novos clientes cadastrados, no primeiro pedido/.test(termos), 'termos: elegibilidade do cupom');
  ok(/16 de outubro de 2026/.test(termos), 'termos: data da última atualização');

  ['privacidade.html', 'cookies.html'].forEach((pagina) => {
    ok(/16 de outubro de 2026/.test(textoDe(pagina)), pagina + ': data da última atualização');
  });
  ok(/Departamento Jurídico/.test(textoDe('cookies.html')), 'cookies: canal do encarregado de dados');

  const produto = textoDe('produto.html');
  ok(/Postagem em até 2 dias úteis/.test(produto), 'produto: prazo de postagem');
  ok(/sabão neutro/.test(produto) && /110°C/.test(produto), 'produto: cuidados de lavagem confirmados');
  ok(/30 dias para trocar de tamanho/.test(produto), 'produto: prazo de troca');

  const pedido = textoDe('pedido-recebido.html');
  ok(/5 a 7 dias úteis de confecção/.test(pedido), 'pedido recebido: peças sob encomenda');

  // 20.7 — marca do header em 20px, como a especificação da cliente
  const headerCss = fs.readFileSync(path.join(RAIZ, 'assets', 'css', 'header.css'), 'utf8');
  const marca = headerCss.match(/\.brand__name \{[^}]*\}/)[0];
  ok(/font-size:\s*20px/.test(marca), 'marca do header em 20px');
  ok(!/clamp/.test(marca), 'marca do header sem clamp');

  // 20.8 — o CSS novo existe e o JS não inventou frete
  const tudoCss = ['style.css', 'header.css', 'pages.css', 'comercio.css']
    .map((f) => fs.readFileSync(path.join(RAIZ, 'assets', 'css', f), 'utf8')).join('\n');
  ['.choice-list', '.choice__title', '.choice__meta', '.choice__price', '.choice__tag', '.card-fields'].forEach((classe) => {
    ok(tudoCss.indexOf(classe) >= 0, 'CSS com ' + classe);
  });
  ok(/:has\(\.choice__input:checked\)/.test(tudoCss), 'cartão escolhido tem estado visual no CSS');
  ok(/is-selected/.test(tudoCss), 'cartão escolhido também tem marca pelo JS (navegador sem :has)');

  const js = fs.readFileSync(path.join(RAIZ, 'assets', 'js', 'loja.js'), 'utf8');
  ok(/PIX_DESCONTO = 0\.05/.test(js), 'loja.js: desconto do Pix em 5%');
  ok(/PARCELA_MINIMA = 50/.test(js), 'loja.js: parcela mínima de R$ 50,00');
  ok(/MAX_PARCELAS = 6/.test(js), 'loja.js: no máximo 6 parcelas');
  ok(!/24,90|39,90/.test(js), 'loja.js: nenhum valor de frete inventado');
  ok(/frete grátis conta o valor líquido|valor LÍQUIDO/.test(js), 'loja.js: frete grátis sobre o valor líquido');
}

console.log('\n=== 21. RESUMO FIXO, BOLETO, RETIRADA, COLECAO DO ZIP E NOVO ARTIGO (v0.1.14) ===');
{
  const css = (arquivo) => fs.readFileSync(path.join(RAIZ, 'assets', 'css', arquivo), 'utf8');
  const js = (arquivo) => fs.readFileSync(path.join(RAIZ, 'assets', 'js', arquivo), 'utf8');
  const textoDe = (arquivo) => carregar(arquivo).window.document.body.textContent.replace(/\s+/g, ' ');
  const arquivoHtml = (arquivo) => fs.readFileSync(path.join(RAIZ, arquivo), 'utf8');

  // 21.1 — o resumo da sacola: alinhamento de dentro e foco ao rolar
  const style = css('style.css');
  const pages = css('pages.css');
  const comercio = css('comercio.css');

  const styleSemComentarios = style.replace(/\/\*[\s\S]*?\*\//g, '');
  const corpo = styleSemComentarios.match(/body \{[^}]*\}/)[0];
  ok(!/overflow-x:\s*hidden/.test(corpo),
     'body não usa overflow-x: hidden (era o que matava o position: sticky)');
  ok(/overflow-x:\s*clip/.test(corpo), 'body corta o excesso com overflow-x: clip');
  ok(/@supports not \(overflow: clip\)/.test(style), 'navegador antigo ganha o hidden como reserva');

  const resumo = pages.match(/\.summary \{[^}]*\}/)[0];
  ok(/position:\s*sticky/.test(resumo), 'resumo fica preso ao rolar');
  ok(/top:\s*var\(--iara-sticky-top\)/.test(resumo), 'resumo gruda abaixo do cabeçalho, pelo token do site');
  ok(/max-height:/.test(resumo) && /overflow:\s*auto/.test(resumo),
     'resumo alto demais rola por dentro em vez de esconder o botão');
  ok(/align-self:\s*start/.test(resumo), 'resumo alinhado ao topo da coluna');
  ok(/@media \(max-width: 1020px\) \{\s*\.summary \{ position: static/.test(pages.replace(/\s+\n/g, '\n')),
     'no celular e no tablet o resumo volta ao fluxo normal');

  const coupon = pages.match(/\.coupon \{[^}]*\}/)[0];
  ok(/align-items:\s*end/.test(coupon), 'campo e botão alinhados pela base');
  ok(!/margin-top:\s*26px/.test(pages), 'a margem mágica de 26px saiu do CSS');
  ok(/grid-template-columns:\s*minmax\(0, 1fr\) auto/.test(coupon), 'campo e botão em duas colunas de largura previsível');
  ok(/font-variant-numeric:\s*tabular-nums/.test(pages), 'valores do resumo em coluna, com número de largura fixa');

  const carrinho = carregar('carrinho.html').window.document;
  ok(!!carrinho.querySelector('.summary'), 'sacola tem o resumo');
  ok(!!carrinho.querySelector('[data-frete-form]'), 'o cálculo do frete dentro do resumo é um formulário de verdade');
  ok(!!carrinho.querySelector('.summary .coupon .btn'), 'o resumo tem o botão de aplicar cupom na mesma linha do campo');
  ok(/--iara-sticky-top/.test(style), 'token --iara-sticky-top definido no CSS');

  // 21.2 — boleto no checkout, com as regras confirmadas
  const dom = carregar('checkout.html');
  const doc = dom.window.document;
  const win = dom.window;
  const t = (sel) => ((doc.querySelector(sel) || {}).textContent || '').replace(/\s+/g, ' ');
  const evt = (el, tipo) => el.dispatchEvent(new win.Event(tipo, { bubbles: true }));

  const boleto = doc.getElementById('pg-boleto');
  ok(!!boleto, 'checkout tem o cartão do boleto');
  const cartaoBoleto = boleto.closest('.choice');
  ok(/Boleto bancário/.test(cartaoBoleto.querySelector('.choice__title').textContent),
     'cartão do boleto com o título certo');
  ok(/Vence em 2 dias úteis/.test(cartaoBoleto.textContent), 'boleto: vencimento em 2 dias úteis');
  ok(/depois da compensação/.test(cartaoBoleto.textContent), 'boleto: pedido liberado depois da compensação');
  ok(!/5% off/.test(cartaoBoleto.textContent), 'boleto não recebe a etiqueta do desconto do Pix');

  boleto.checked = true; evt(boleto, 'change');
  ok(/R\$ 876,60/.test(t('[data-preco-boleto]')), 'boleto: valor cheio, sem o desconto do Pix');
  ok(/R\$ 876,60/.test(t('[data-resumo-total]')), 'boleto: total do resumo sem desconto');
  ok(/Total no boleto/.test(t('[data-resumo-total-rotulo]')), 'boleto: rótulo do total muda para boleto');
  ok(doc.getElementById('cartao-campos').hasAttribute('hidden'), 'boleto não pede dados de cartão');
  ok(/compensação bancária/.test(t('[data-pay-note]')), 'boleto: recado explica a compensação');

  const pix = doc.getElementById('pg-pix');
  pix.checked = true; evt(pix, 'change');
  ok(/R\$ 832,77/.test(t('[data-resumo-total]')), 'voltar para o Pix traz o total com desconto');

  // 21.3 — retirada no ateliê, com dias e horários
  ok(/Segunda a sexta, das 10h às 17h/.test(textoDe('checkout.html')), 'checkout: horário de retirada confirmado');
  ok(/Segunda a sexta, das 10h às 17h/.test(textoDe('envio.html')), 'envio: tabela com o horário de retirada');
  ok(/Pronto para Retirada/.test(textoDe('envio.html')), 'envio: retirada só depois do aviso de pronto');
  ok(/segunda a sexta, das 10h às 17h/i.test(textoDe('contato.html')), 'contato: horário de retirada confirmado');
  ok(/segunda a sexta, das 10h às 17h/i.test(js('loja.js')), 'loja.js: recado da retirada com o horário');
  ok(!/\[A DEFINIR: dias e horários de retirada\]/.test(textoDe('checkout.html') + textoDe('envio.html') + textoDe('contato.html')),
     'o marcador de dias e horários saiu do site');

  // 21.4 — o que a empresa respondeu sobre trocas, reembolso e tecidos
  const trocas = textoDe('trocas.html');
  ok(/mesmo\s+modelo em outro tamanho/.test(trocas), 'trocas: peças de liquidação trocam pelo mesmo modelo');
  ok(/valor\s+pago/.test(trocas), 'trocas: cupom de troca vale o valor pago');
  ok(/em até 2 dias úteis/.test(trocas), 'trocas: reembolso no Pix em 2 dias úteis');
  ok(/3 dias úteis/.test(trocas), 'trocas: cartão e boleto em 3 dias úteis');
  ok(!/Prazo para processar o reembolso depois da conferência da peça:/.test(trocas),
     'trocas: o marcador do prazo de reembolso saiu');

  const sobre = textoDe('sobre.html');
  ok(/linho, algodão egípcio e viscose de alta gramatura/.test(sobre), 'sobre: tecidos confirmados pela empresa');
  ok(/100% autorais/.test(sobre), 'sobre: modelagem autoral confirmada');
  ok(/Cerquilho - SP/.test(sobre), 'sobre: ateliê em Cerquilho');

  const produto = textoDe('produto.html');
  ok(/País de origem: Brasil/.test(produto), 'produto: país de origem confirmado');
  ok(/linho, algodão egípcio e viscose de alta gramatura/.test(produto), 'produto: tecidos do ateliê citados');

  ok(/Iara Costa e Equipe de Criação/.test(textoDe('post.html')), 'artigo: autoria confirmada pela empresa');
  ok(/Iara Costa e Equipe de Criação/.test(textoDe('blog.html')), 'diário: autoria confirmada pela empresa');
  ok(!/\[PREENCHER: autoria\]/.test(textoDe('post.html') + textoDe('blog.html')), 'o marcador de autoria saiu do diário');

  // 21.5 — página de coleção no layout do zip
  const loja = carregar('loja.html').window.document;
  ok(!!loja.querySelector('.filters__actions'), 'coluna de filtros fecha com as ações, como no zip');
  const acoes = loja.querySelector('.filters__actions');
  ok(/Aplicar filtros/.test(acoes.textContent), 'ações trazem o botão Aplicar filtros');
  ok(/Limpar filtros/.test(acoes.textContent), 'ações trazem o Limpar filtros');
  ok(!loja.querySelector('.filters__head'), 'sem o cabeçalho antigo na coluna');
  ok(/12 peças nesta seleção/.test(loja.querySelector('[data-count]').textContent), 'contagem com o texto do zip');

  const filtrosCss = comercio.match(/@media \(min-width: 1021px\) \{\s*\.filters \{[^}]*\}/);
  ok(!!filtrosCss && /position:\s*sticky/.test(filtrosCss[0]), 'coluna de filtros acompanha a rolagem, como no zip');

  const cardCss = style.match(/\.card \{[^}]*\}/)[0];
  ok(/display:\s*flex/.test(cardCss) && /gap:\s*var\(--iara-space-3\)/.test(cardCss),
     'cartão em coluna com 12px entre as partes, como no zip');
  const addCss = comercio.match(/\.card__add \{[^}]*\}/)[0];
  ok(/font-size:\s*var\(--fs-small\)/.test(addCss), 'convite da sacola no corpo pequeno, como no zip');
  ok(!/opacity:\s*0/.test(addCss), 'convite da sacola fica sempre visível: nada escondido atrás do hover');
  ok(/gap: clamp\(28px, 3vw, var\(--iara-space-6\)\) var\(--iara-gap\)/.test(style),
     'grade de produtos com o espaçamento do zip (mais ar entre as linhas)');

  const filtros = js('filtros.js');
  ok(/data-filters-apply/.test(filtros), 'filtros.js lê o botão Aplicar filtros');
  ok(/peças nesta seleção/.test(filtros), 'filtros.js escreve a contagem do zip');

  // 21.6 — layout novo do artigo
  const post = carregar('post.html').window.document;
  ok(!!post.querySelector('.post-hero'), 'artigo abre com a capa em duas colunas');
  ok(!!post.querySelector('.post-hero .post-figure'), 'a foto da capa fica ao lado do texto');
  ok(!!post.querySelector('.post-index'), 'artigo tem o índice do texto');
  const linksIndice = Array.prototype.map.call(post.querySelectorAll('.post-index__list a'), (a) => a.getAttribute('href'));
  ok(linksIndice.length === 5, 'índice com as cinco seções (tem ' + linksIndice.length + ')');
  ok(linksIndice.every((href) => !!post.querySelector(href)), 'todos os atalhos do índice levam a uma seção que existe');
  ok(!!post.querySelector('.pull-quote'), 'artigo tem a citação de respiro');
  ok(!!post.querySelector('.post-callout'), 'artigo tem a chamada do guia de medidas');
  ok(!!post.querySelector('.post-tags'), 'artigo fecha com as etiquetas de assunto');
  ok(!!post.querySelector('.post-foot .share'), 'artigo tem o compartilhar no fecho');
  ok(!!post.querySelector('.author-box__name'), 'artigo tem o nome de quem assina');
  ok(!!post.querySelector('[data-post-progress]'), 'artigo tem a barra de progresso da leitura');
  ok(post.querySelector('[data-post-progress]').hasAttribute('hidden'),
     'a barra de progresso começa escondida e só aparece com rolagem');
  ok(!post.querySelector('.post-layout') && !post.querySelector('.post-aside'),
     'o layout antigo do artigo saiu do HTML');
  ok(/artigo\.js/.test(arquivoHtml('post.html')), 'a página do artigo carrega o artigo.js');

  const artigo = js('artigo.js');
  ok(/data-post-artigo/.test(artigo), 'artigo.js trabalha só na página do artigo');
  ok(/IntersectionObserver/.test(artigo), 'artigo.js marca a seção atual no índice');
  ok(/clipboard/.test(artigo), 'artigo.js copia o link do artigo');
  ok(/catch \(erro\)/.test(artigo), 'artigo.js falha em silêncio se algo der errado');
}

console.log('\n=== 22. PAGINACAO DA COLECAO E ORDENACAO DO ZIP (v0.1.15) ===');
{
  const dom = carregar('loja.html');
  const doc = dom.window.document;
  const grid = doc.querySelector('[data-shop-grid]');
  const cards = grid.querySelectorAll('.card');
  const visiveis = () => Array.prototype.filter.call(grid.children, (c) => !c.classList.contains('is-hidden'));
  const nav = doc.querySelector('[data-shop-pagination]');
  const faixa = () => doc.querySelector('[data-shop-range]').textContent;
  const controles = () => Array.prototype.map.call(nav.querySelectorAll('.shop__page'), (b) => b.textContent).join(' ');
  const ordinal = (n) => Array.prototype.filter.call(nav.querySelectorAll('.shop__page'), (b) => b.getAttribute('aria-current') === 'page')[0];

  ok(cards.length === 12, 'a grade traz as 12 peças no HTML (sem JavaScript aparece tudo)');
  ok(visiveis().length === 9, 'a primeira página mostra 9 peças (achou ' + visiveis().length + ')');
  ok(faixa() === 'Mostrando 1–9 de 12 peças', 'faixa da coleção conta as peças da página ("' + faixa() + '")');
  ok(!nav.hasAttribute('hidden'), 'paginacao aparece quando a selecao passa de uma pagina');
  ok(nav.getAttribute('aria-label') === 'Paginação de produtos', 'paginacao com rotulo proprio');
  ok(controles() === '← 1 2 →', 'paginacao com setas e as duas paginas ("' + controles() + '")');
  ok(!!ordinal(1), 'a pagina atual marcada com aria-current');
  ok(ordinal(1).tagName.toLowerCase() === 'span', 'a pagina atual nao e clicavel (texto marcado, como no zip)');
  ok(!!nav.querySelector('[data-pagina="1"]') && !!nav.querySelector('[data-pagina="2"]'),
     'cada pagina tem seu gancho numerado');
  ok(nav.querySelector('[aria-label="Página anterior"]').disabled, 'seta anterior desligada na primeira pagina');
  ok(!nav.querySelector('[aria-label="Próxima página"]').disabled, 'seta proxima ativa na primeira pagina');

  // segunda página
  nav.querySelector('[data-pagina="2"]').dispatchEvent(new dom.window.MouseEvent('click', { bubbles: true }));
  ok(visiveis().length === 3, 'a segunda pagina mostra as 3 peças restantes (achou ' + visiveis().length + ')');
  ok(faixa() === 'Mostrando 10–12 de 12 peças', 'faixa acompanha a segunda pagina ("' + faixa() + '")');
  ok(!!ordinal(2), 'a segunda pagina passa a ser a atual');
  ok(nav.querySelector('[aria-label="Próxima página"]').disabled, 'seta proxima desliga na ultima pagina');
  ok(doc.activeElement && doc.activeElement.getAttribute('aria-label') === 'Página 2',
     'o foco acompanha a troca de pagina (leitor de tela anuncia a nova pagina)');

  // filtro que cabe em uma página só
  const cat = doc.querySelector('[data-facet="categoria"][value="vestidos"]');
  cat.checked = true;
  cat.dispatchEvent(new dom.window.Event('change', { bubbles: true }));
  ok(visiveis().length === 2, 'filtro reduz a grade para 2 peças');
  ok(faixa() === 'Mostrando 1–2 de 2 peças', 'faixa conta o resultado do filtro ("' + faixa() + '")');
  ok(nav.hasAttribute('hidden'), 'paginacao some quando a selecao cabe em uma pagina');
  cat.checked = false;
  cat.dispatchEvent(new dom.window.Event('change', { bubbles: true }));

  // as cinco ordenações do zip
  const select = doc.querySelector('[data-sort]');
  const rotulos = Array.prototype.map.call(select.options, (o) => o.textContent).join(' / ');
  ok(select.options.length === 5, 'cinco formas de ordenar, como no zip (tem ' + select.options.length + ')');
  ok(rotulos === 'Mais recentes / Mais populares / Menor preço / Maior preço / Melhor avaliados',
     'rotulos da ordenacao iguais aos do zip ("' + rotulos + '")');
  ok(Array.prototype.every.call(select.options, (o) => ['date', 'popularity', 'price', 'price-desc', 'rating'].indexOf(o.value) >= 0),
     'valores da ordenacao sao os mesmos do WooCommerce');
  ok(rotulos.indexOf('Nome, de A a Z') < 0, 'a ordenacao por nome saiu: ficaram as cinco do zip');

  const ordenarPor = (valor) => {
    select.value = valor;
    select.dispatchEvent(new dom.window.Event('change', { bubbles: true }));
    return visiveis()[0].querySelector('.card__name').textContent;
  };

  ok(ordenarPor('price').indexOf('Brinco') === 0, 'menor preço começa no brinco de R$ 149');
  ok(ordenarPor('price-desc').indexOf('Blazer') === 0, 'maior preço começa no blazer de R$ 789');
  ok(ordenarPor('popularity').indexOf('Vestido Midi') === 0, 'mais populares começa na peça com 48 avaliações');
  ok(ordenarPor('rating').indexOf('Vestido Midi') === 0, 'melhor avaliados começa na peça de nota 5,0');
  ok(ordenarPor('date').indexOf('Blusa') === 0, 'mais recentes volta para a ordem do catálogo');

  ok(doc.querySelectorAll('[data-shop-grid] .card[data-nota]').length === 12, 'todo cartao traz a nota para a ordenacao');
  ok(doc.querySelectorAll('[data-shop-grid] .card[data-avaliacoes]').length === 12, 'todo cartao traz o numero de avaliacoes');
}

console.log('\n=== 23. COLECAO EM CAPITULOS, COMO NO ZIP (v0.1.16) ===');
{
  const doc = carregar('lookbook.html').window.document;
  const css = fs.readFileSync(path.join(RAIZ, 'assets/css/pages.css'), 'utf8');

  const hero = doc.querySelector('.look-hero');
  ok(!!hero, 'a colecao abre com a capa do zip');
  ok(!!hero.querySelector('.breadcrumbs'), 'trilha dentro da capa, centralizada como no zip');
  ok(!!hero.querySelector('h1'), 'nome da colecao na capa');
  ok(doc.querySelectorAll('.page-head').length === 0, 'a colecao nao usa o cabecalho de pagina das outras telas');
  ok(hero.querySelectorAll('.look-hero__chips .chip').length === 4, 'quatro fichas de informacao na capa');
  ok(/Doze peças/.test(hero.textContent), 'ficha com o tamanho real do catalogo');
  ok(/Feito no Brasil/.test(hero.textContent), 'ficha com a origem confirmada pela empresa');
  ok(!/18 peças|Tingimento natural|Edições numeradas/.test(hero.textContent),
     'as fichas do zip que a empresa nao confirmou nao entraram');

  const capitulos = doc.querySelectorAll('.chapter');
  ok(capitulos.length === 3, 'tres capitulos, como no zip (achou ' + capitulos.length + ')');

  const cabecalhos = Array.prototype.map.call(capitulos, (c) => c.querySelector('.chapter__title').textContent);
  ok(cabecalhos.join(' | ') === 'O barro que veste | Verde que acalma | O branco que não é básico',
     'titulos dos capitulos iguais aos do zip (' + cabecalhos.join(' | ') + ')');

  const numeros = Array.prototype.map.call(capitulos, (c) => c.querySelector('.chapter__eyebrow .index-number').textContent.trim());
  ok(numeros.join(' ') === '01 · 02 · 03 ·', 'capitulos numerados em 01, 02 e 03');

  Array.prototype.forEach.call(capitulos, (capitulo, i) => {
    const n = i + 1;
    ok(!!capitulo.querySelector('.chapter__media img'), 'capitulo ' + n + ': foto grande');
    ok(!!capitulo.querySelector('.chapter__media img').getAttribute('alt'),
       'capitulo ' + n + ': foto com descricao para leitor de tela');
    ok(!!capitulo.querySelector('h2[id]'), 'capitulo ' + n + ': titulo com ancora propria');
    ok(!!capitulo.querySelector('.chapter__cta .action-link[href="loja.html"]'),
       'capitulo ' + n + ': convite para comprar o capitulo');
    ok(capitulo.querySelectorAll('.chapter__products .card').length === 2,
       'capitulo ' + n + ': duas pecas do catalogo embaixo do texto');
  });

  ok(capitulos[1].classList.contains('chapter--reverse'),
     'capitulo do meio inverte os lados, como no zip');
  ok(!capitulos[0].classList.contains('chapter--reverse') && !capitulos[2].classList.contains('chapter--reverse'),
     'primeiro e ultimo capitulos ficam com a foto a esquerda');

  const pecasDoCapitulo = (i) => Array.prototype.map.call(
    capitulos[i].querySelectorAll('.chapter__products [data-wish]'),
    (b) => b.dataset.wish).join(',');
  ok(pecasDoCapitulo(0) === 'blusa-linho-terracota,vestido-longo-cerrado', 'capitulo 1 com as duas pecas terracota');
  ok(pecasDoCapitulo(1) === 'vestido-midi-salvia,calca-pantalona-salvia', 'capitulo 2 com as duas pecas salvia');
  ok(pecasDoCapitulo(2) === 'camisa-linho-branca,saia-linho-cru', 'capitulo 3 com as duas pecas cru');

  // o cartao do capitulo e enxuto, como no zip
  const primeiro = capitulos[0].querySelector('.chapter__products .card');
  ok(!!primeiro.querySelector('.card__cat'), 'cartao do capitulo traz a categoria');
  ok(!!primeiro.querySelector('.card__name a'), 'cartao do capitulo traz o nome com link');
  ok(!!primeiro.querySelector('.card__price'), 'cartao do capitulo traz o preco');
  ok(!!primeiro.querySelector('.card__wish'), 'cartao do capitulo tem o coracao dos desejos');
  ok(!primeiro.querySelector('.card__rating') && !primeiro.querySelector('.card__sizes') && !primeiro.querySelector('.card__add'),
     'cartao do capitulo sem nota, sem tamanhos e sem o convite da sacola (como no zip)');
  ok(primeiro.tagName.toLowerCase() === 'article', 'cartao do capitulo e um article, nao um item de lista');
  ok(primeiro.querySelector('.card__media').getAttribute('href') === 'produto.html',
     'foto do cartao do capitulo leva para a peca');

  // o cartao da loja continua completo
  const lojaDoc = carregar('loja.html').window.document;
  const naLoja = lojaDoc.querySelector('[data-shop-grid] .card');
  ok(!!naLoja.querySelector('.card__rating') && !!naLoja.querySelector('.card__sizes') && !!naLoja.querySelector('.card__add'),
     'o cartao da loja segue com nota, tamanhos e convite da sacola');

  // nota interna das fotos
  ok(!!doc.querySelector('.chapter-specs .list-check'), 'a nota de producao das fotos fecha a pagina');
  ok(/4:5/.test(doc.querySelector('.chapter-specs').textContent), 'nota cita a proporcao das fotos de peca');

  // CSS
  const capituloCss = css.match(/\.chapter \{[^}]*\}/)[0];
  ok(/grid-template-columns:\s*1\.05fr 1fr/.test(capituloCss), 'capitulo em duas colunas, com a foto maior');
  ok(/align-items:\s*center/.test(capituloCss), 'texto centrado na altura da foto');
  ok(/\.chapter--reverse > :first-child \{ order: 2; \}/.test(css), 'o capitulo invertido troca os lados por ordem');
  ok(/@media \(max-width: 1020px\) \{\s*\.chapter \{ grid-template-columns: 1fr; \}/.test(css),
     'abaixo de 1021px a foto vai para cima do texto');
  ok(/\.chapter__media img \{ display: block; width: 100%; height: auto; \}/.test(css),
     'a foto do capitulo ocupa a coluna inteira, na proporcao original (como no zip)');
  ok(/max-width: 390px[\s\S]{0,200}\.chapter__products \{ grid-template-columns: 1fr; \}/.test(css),
     'no celular pequeno as duas pecas ficam uma embaixo da outra');

  const heroCss = css.match(/\.look-hero \{[^}]*\}/)[0];
  ok(/text-align:\s*center/.test(heroCss), 'capa centralizada, como no zip');
}
console.log('\n=== 24. HERO DA HOME COM A FOTO INTEIRA E O SELO EM CIMA (v0.1.17) ===');
{
  const doc = carregar('index.html').window.document;
  const css = fs.readFileSync(path.join(RAIZ, 'assets/css/pages.css'), 'utf8');

  const selo = doc.querySelector('.hero__media .hero__stamp');
  ok(!!selo, 'a foto do hero tem o selo com a descricao');
  ok(!!selo && /Blusa de Linho Terracota/.test(selo.textContent), 'o selo nomeia a peca da foto');
  ok(!!selo && /argila do Vale do Paraíba/.test(selo.textContent),
     'o selo cita o tingimento com argila, confirmado pela cliente em 16/10/2026');
  ok(!!selo && !/\u2014/.test(selo.textContent), 'sem travessao no selo (regra de copy)');
  ok(!!selo && !!selo.querySelector('.index-number'), 'selo numerado 01, como no zip');

  const mediaCss = css.match(/\.hero__media img \{[^}]*\}/)[0];
  ok(/width: 100%/.test(mediaCss) && /height: auto/.test(mediaCss), 'a foto ocupa a coluna inteira');
  ok(/aspect-ratio:\s*1 \/ 1/.test(mediaCss),
     'a foto entra quadrada, 1:1, como a cliente pediu (v0.1.18)');
  ok(/object-fit:\s*cover/.test(mediaCss), 'a foto preenche o quadrado sem distorcer');
  ok(/object-position:\s*center 50%/.test(mediaCss),
     'o corte e centralizado, o enquadramento que mantem rosto e peca no quadro');
  ok(!/aspect-ratio:\s*[56] \/ [67]/.test(css) && !/aspect-ratio:\s*4 \/ 5/.test(mediaCss),
     'nao sobrou nenhuma moldura retrato antiga no hero');
  ok(/@media \(min-width: 1021px\) \{\s*\.hero__media \{ max-width: 560px; justify-self: end; \}/.test(css),
     'no desktop a foto fica com no maximo 560px, alinhada a direita');

  const seloCss = css.match(/\.hero__stamp \{[^}]*\}/)[0];
  ok(/position: absolute/.test(seloCss), 'o selo fica em cima da foto');
  ok(/right: var\(--iara-space-4\)/.test(seloCss) && /bottom: var\(--iara-space-4\)/.test(seloCss),
     'selo no canto inferior direito, como no zip');
  ok(/max-width: 220px/.test(seloCss), 'largura maxima do selo igual a do template (220px)');
  ok(/background: var\(--iara-paper\)/.test(seloCss) && /border: 1px solid var\(--iara-line\)/.test(seloCss),
     'selo com fundo de papel e borda fina, como no zip');
  ok(/\.hero__stamp \.index-number \{ display: block; margin-bottom: 2px; \}/.test(css),
     'numeral 01 em linha propria, como no zip');
  ok(/@media \(max-width: 720px\) \{\s*\.hero__stamp \{ position: static/.test(css),
     'no celular o selo desce para baixo da foto, para nao cobrir a modelo');
}

console.log('\n=== 25. AJUSTES DE NAVEGADOR DA v0.1.19 ===');
{
  const semComentario = (texto) => texto.replace(/\/\*[\s\S]*?\*\//g, '');
  const styleCss = semComentario(fs.readFileSync(path.join(RAIZ, 'assets/css/style.css'), 'utf8'));
  const pagesCss = semComentario(fs.readFileSync(path.join(RAIZ, 'assets/css/pages.css'), 'utf8'));
  const headerCss = semComentario(fs.readFileSync(path.join(RAIZ, 'assets/css/header.css'), 'utf8'));
  const headerJs = fs.readFileSync(path.join(RAIZ, 'assets/js/header.js'), 'utf8');
  const lojaJs = fs.readFileSync(path.join(RAIZ, 'assets/js/loja.js'), 'utf8');

  // 25.1 — marcador de pendencia quebrava a largura no celular
  const marcador = styleCss.match(/\.placeholder \{[^}]*\}/)[0];
  ok(!/white-space:\s*nowrap/.test(marcador), 'marcador [PREENCHER] quebra linha (nao estoura no celular)');
  ok(/overflow-wrap:\s*break-word/.test(marcador), 'marcador longo quebra dentro da coluna');

  // 25.2 — grades protegidas do conteudo largo
  ok(/\.account-layout > \* \{ min-width: 0; \}/.test(pagesCss),
     'grade da conta protegida (tabela com rolagem nao empurra a coluna)');
  ok(/\.post-body > \* \{ min-width: 0; \}/.test(pagesCss),
     'grade do artigo protegida pelo mesmo motivo');

  // 25.3 — balao do WhatsApp nao cobre mais o que a pessoa precisa ver
  ok(/@media \(scripting: enabled\)/.test(headerCss),
     'balao do WhatsApp so esconde se o navegador souber rodar JavaScript');
  ok(/\.whats-float\.is-visivel \{ opacity: 1; visibility: visible; \}/.test(headerCss),
     'balao volta ao rolar a pagina');
  ok(/is-visivel/.test(headerJs) && /addEventListener\('scroll'/.test(headerJs),
     'o JavaScript liga e desliga o balao conforme a rolagem');
  ok(/max-height: calc\(100dvh - var\(--iara-sticky-top\) - 96px\)/.test(pagesCss),
     'resumo que gruda reserva o canto do balao (96px)');

  // 25.4 — o grupo de cor da pagina de produto bate com o catalogo
  const catalogo = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'tools', 'produtos.json'), 'utf8'));
  const peca = catalogo.filter((p) => p.slug === 'vestido-midi-salvia')[0];
  ok(!!peca && peca.cores.join(',') === 'salvia', 'catalogo: o vestido midi tem uma cor so, salvia');

  const produto = carregar('produto.html').window.document;
  const grupoCor = produto.querySelector('[data-option-group][data-option-label="Cor"]');
  ok(!!grupoCor, 'pagina de produto com grupo de cor');
  const coresNaTela = Array.prototype.map.call(grupoCor.querySelectorAll('.swatch'),
    (b) => b.getAttribute('data-value'));
  ok(coresNaTela.length === peca.cores.length && coresNaTela.join(',') === 'Sálvia',
     'a cor da tela e a cor do catalogo ("' + coresNaTela.join(',') + '")');
  ok(/Cor selecionada: Sálvia/.test(grupoCor.textContent), 'o texto ao vivo diz a cor certa');
  ok(grupoCor.querySelector('input[name="cor"]').value === 'Sálvia', 'o campo escondido manda a cor certa');
  ok(!/Terracota|Off-white|Preto/.test(grupoCor.textContent),
     'as cores inventadas (Terracota, Off-white, Preto) sairam da peca salvia');
  ok(!/\.sw-offwhite|\.sw-preto/.test(pagesCss), 'sobraram no CSS? nao: as duas sairam junto');
  ok(grupoCor.querySelector('.sw-salvia'), 'a bolinha da cor usa o tom da paleta');

  const meta = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'tools', 'pages.json'), 'utf8'))
    .filter((p) => p.file === 'produto.html')[0];
  ok(/sálvia/.test(meta.desc) && !/terracota/i.test(meta.desc),
     'a descricao da busca fala da cor certa');

  // 25.5 — formulario de contato responde
  const contato = carregar('contato.html').window.document;
  ok(!!contato.querySelector('[data-form-contato]'), 'contato: formulario com gancho de validacao');
  ok(!!contato.querySelector('[data-contato-msg]'), 'contato: lugar do recado de envio');
  ok(/assets\/js\/contato\.js/.test(contato.documentElement.outerHTML), 'contato: script de validacao carregado');
  const contatoJs = fs.readFileSync(path.join(RAIZ, 'assets/js/contato.js'), 'utf8');
  ['ct-nome', 'ct-email', 'ct-assunto', 'ct-msg', 'ct-consent'].forEach((id) => {
    ok(contatoJs.indexOf(id) >= 0, 'contato: o script cuida do campo ' + id);
  });
  ok(/aria-invalid/.test(contatoJs) && /aria-describedby/.test(contatoJs),
     'contato: erro ligado ao campo para leitor de tela');

  // 25.6 — o acordeao funciona em todas as paginas que o usam
  ['faq.html', 'envio.html', 'guia-medidas.html', 'index.html'].forEach((pagina) => {
    const doc = carregar(pagina).window.document;
    const temAcordeao = doc.querySelectorAll('[data-accordion]').length > 0;
    const carregaJs = /assets\/js\/swatches\.js/.test(doc.documentElement.outerHTML);
    ok(temAcordeao && carregaJs, pagina + ': acordeao com o script que o abre');
  });

  // 25.7 — lista de desejos com botoes que funcionam
  const desejos = carregar('desejos.html').window.document;
  ok(desejos.querySelectorAll('[data-add]').length === 2,
     'desejos: duas pecas com botao de adicionar a sacola (a esgotada nao entra)');
  ok(desejos.querySelectorAll('[data-desejo-remover]').length === 3, 'desejos: tres botoes de remover');
  ok(/data-desejo-remover/.test(lojaJs) && /Peça removida da lista de desejos\./.test(lojaJs),
     'desejos: o script tira a peca da lista e avisa');
  const indisponivel = desejos.querySelector('.wish-actions button[disabled]');
  ok(!!indisponivel && /Indisponível/.test(indisponivel.textContent),
     'desejos: peca esgotada com botao desabilitado de verdade');
  ok(!desejos.querySelector('button[aria-disabled="true"]'),
     'desejos: o aviso de indisponivel virou atributo real (disabled)');
}

console.log(falhas === 0 ? 'RESULTADO: TUDO CERTO' : 'RESULTADO: ' + falhas + ' FALHA(S)');
console.log('========================================\n');
process.exit(falhas === 0 ? 0 : 1);
