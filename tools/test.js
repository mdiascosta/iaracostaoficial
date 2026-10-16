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
  ok(visiveis() === 12, '12 peças visíveis sem filtro');

  const catVestidos = doc.querySelector('[data-facet="categoria"][value="vestidos"]');
  catVestidos.checked = true;
  catVestidos.dispatchEvent(new dom.window.Event('change', { bubbles: true }));
  ok(visiveis() === 2, 'categoria Vestidos mostra 2 peças (achou ' + visiveis() + ')');
  ok(contador() === '2 peças encontradas', 'contador anuncia 2 peças ("' + contador() + '")');

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
  ok(visiveis() === 12, 'Limpar filtros traz as 12 peças de volta');
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
  select.value = 'preco-asc';
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
  ok(!!doc.querySelector('.page-intro'), 'texto de apoio abaixo do fio do cabeçalho');
  ok(!!doc.querySelector('.shop__count[data-count]'), 'contagem de peças na barra da coleção (loja)');

  const seletor = doc.querySelector('.shop__sort select[data-sort]');
  ok(!!seletor, 'seletor de ordenação existe');
  ok(seletor.classList.contains('field__select'), 'seletor usa a classe de campo do site');
  ok(seletor.querySelectorAll('option').length === 4, 'quatro formas de ordenar');

  ok(!!doc.querySelector('.filters__head'), 'coluna de filtros tem o cabeçalho próprio');
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
  // A empresa confirmou o gateway e os dois meios ativos em 16/10/2026.
  // Bandeira de cartão entra aqui quando estiver habilitada na conta do gateway.
  ok(chips.length === 3, 'três formas de pagamento listadas (tem ' + chips.length + ')');
  const nomes = Array.prototype.map.call(chips, (c) => c.textContent.trim());
  ['Mercado Pago', 'Pix', 'Cartão de crédito'].forEach((n) => {
    ok(nomes.indexOf(n) >= 0, 'forma de pagamento confirmada: ' + n);
  });
  ok(!/Boleto|PayPal|Visa|Mastercard|American Express|Diners/.test(d.querySelector('.pay').textContent),
     'rodapé sem forma de pagamento que a empresa não confirmou');

  const selos = d.querySelectorAll('.seals .seal');
  ok(selos.length === 2, 'dois selos desenhados na faixa de segurança');
  ok(!!d.querySelector('.seals .seal .seal__title'), 'selo com título próprio');
  ok(!!d.querySelector('.seals .seal .seal__sub'), 'selo com texto de apoio');
  ok(!bands.querySelector('img'), 'nenhuma imagem de marca de terceiro no rodapé');
  ok(!!d.querySelector('.security__note .placeholder'), 'aviso de confirmação com a empresa mantido');

  // --- 15.2 Cabeçalho de página limpo (v0.1.10): trilha + nome da página
  const semCabecalho = ['404.html', 'pedido-recebido.html', 'post.html', 'produto.html'];
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

  const look = carregar('lookbook.html').window.document;
  ok(look.querySelectorAll('.lookbook-grid .look-item').length === 4, 'lookbook com quatro looks');
  ok(!!look.querySelector('.look-item .index-number'), 'look numerado');
  ok(!!look.querySelector('.notice--lead'), 'aviso do lookbook sem margem escrita no HTML');

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
  const loja = carregar('loja.html').window.document;
  const apoio = loja.querySelector('.shop__toolbar .shop__meta');
  ok(!!apoio, 'barra da coleção com a contagem e o recado de tamanhos');
  ok(/P ao GG/.test(apoio.textContent), 'recado diz a variação de tamanhos');
  const guia = apoio.querySelector('a[href="guia-medidas.html"]');
  ok(!!guia, 'atalho para o guia de medidas na barra');
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
  ok(!!lojaDoc.querySelector('.shop__sizes a[href="guia-medidas.html"]'),
     'loja: recado de tamanhos com o guia de medidas, agora na barra da coleção');
  ok(/P ao GG/.test(lojaDoc.querySelector('.shop__sizes').textContent.replace(/\s+/g, ' ')),
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
  ok(!/data-cartao|cc-number/i.test(cdoc.documentElement.outerHTML),
     'protótipo não pede número de cartão em nenhum campo');

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
  let comBoleto = [];
  paginasComTexto.forEach((pagina) => {
    const t = textoDe(pagina);
    if (/boleto/i.test(t) || /PayPal/.test(t) || /transfer[eê]ncia banc[aá]ria/i.test(t)) {
      comBoleto.push(pagina);
    }
  });
  ok(comBoleto.length === 0,
     'nenhuma página oferece boleto, PayPal ou transferência bancária (achados: ' + (comBoleto.join(', ') || 'nenhum') + ')');

  const checkoutTexto = textoDe('checkout.html');
  ok(/5% de desconto/.test(checkoutTexto), 'checkout: Pix com 5% de desconto');
  ok(/6x sem juros/.test(checkoutTexto), 'checkout: cartão em até 6x sem juros');
  ok(/Mercado Pago/.test(checkoutTexto), 'checkout: gateway Mercado Pago nomeado');
  ok(!/pg-boleto|pg-transferencia/.test(carregar('checkout.html').window.document.documentElement.outerHTML),
     'checkout sem os campos de boleto e transferência');

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
  ok(/nao se acumula com outras promocoes/i.test(semAcento(termos)),
     'termos: cupom não se acumula com outras promoções');

  // 19.8 — privacidade: controlador e canal de titular preenchidos
  const privacidade = textoDe('privacidade.html');
  ok(privacidade.indexOf(RAZAO) >= 0 && privacidade.indexOf(CNPJ) >= 0,
     'privacidade: controlador identificado');
  ok(privacidade.indexOf(EMAIL) >= 0, 'privacidade: canal de atendimento ao titular');
  ok(!/Razão social: \[PREENCHER\]/.test(privacidade), 'privacidade: sem razão social por preencher');
  ok(/\[A DEFINIR: pessoa responsável/.test(privacidade),
     'privacidade: encarregado de dados segue como decisão da empresa');

  // 19.9 — frete: regras confirmadas e nenhum valor inventado
  const envio = textoDe('envio.html');
  ok(/Correios/.test(envio), 'envio: modalidades pelos Correios');
  ok(/R\$ 15,00 no Sudeste/.test(envio), 'envio: valor fixo do Sudeste');
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
  ok(!/boleto|transferência bancária/i.test(js), 'loja.js: sem forma de pagamento que a empresa não confirmou');
  ok(/5% de desconto/.test(js), 'loja.js: recado do Pix com 5% de desconto');

  // 19.11 — nenhuma página promete troca em 30 dias como se fosse regra fechada
  const home = textoDe('index.html');
  ok(/30 dias/.test(home) && /\[A DEFINIR\]/.test(home),
     'home: prazo de troca de 30 dias marcado como pendente de confirmação');

  // 19.12 — o endereço de exemplo da conta é o do ateliê
  ok(textoDe('conta.html').indexOf(ENDERECO) >= 0, 'conta: endereço de exemplo é o do ateliê');
}

console.log('\n========================================');
console.log(falhas === 0 ? 'RESULTADO: TUDO CERTO' : 'RESULTADO: ' + falhas + ' FALHA(S)');
console.log('========================================\n');
process.exit(falhas === 0 ? 0 : 1);
