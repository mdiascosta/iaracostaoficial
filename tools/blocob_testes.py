#!/usr/bin/env python3
"""Testes locais dos templates JSON, sem WordPress.

Confere nos arquivos de bloco-b/json/ e no CSS do kit exatamente os
pontos que só apareciam depois de importar: fonte e estados do menu do
cabeçalho, tamanho e cor dos ícones de ação, tipografia embutida nos
widgets, faixa e títulos do rodapé. Cada teste imprime ok ou ERRO; o
processo sai com código 1 se algo falhar.

Uso:  python3 tools/blocob_testes.py
"""
import json
import pathlib
import sys

RAIZ = pathlib.Path(__file__).resolve().parent.parent
FALHAS = []


def testa(nome, condicao, detalhe=''):
    marca = 'ok  ' if condicao else 'ERRO'
    print(f'  {marca} {nome}' + (f'  ({detalhe})' if detalhe else ''))
    if not condicao:
        FALHAS.append(nome)


def carrega(nome):
    return json.loads((RAIZ / 'bloco-b' / 'json' / nome)
                      .read_text(encoding='utf-8'))


def percorre(elementos):
    for el in elementos:
        yield el
        yield from percorre(el.get('elements', []))


print('== cabeçalho: menu ==')
cab = carrega('01-cabecalho.json')
menu = next(e for e in percorre(cab['content'])
            if e.get('widgetType') == 'nav-menu')
st = menu['settings']
testa('menu usa o Menu Principal (slug menu-principal)',
      st.get('menu') == 'menu-principal', st.get('menu', ''))
testa('ponteiro do widget desligado (a linha é do nosso CSS)',
      st.get('pointer') == 'none', st.get('pointer', ''))
testa('fonte do menu embutida: Jost 12px caixa alta',
      st.get('menu_typography_font_family') == 'Jost'
      and st['menu_typography_font_size'].get('size') == 12
      and st.get('menu_typography_text_transform') == 'uppercase',
      '%s %spx %s' % (st.get('menu_typography_font_family'),
                      st.get('menu_typography_font_size', {}).get('size'),
                      st.get('menu_typography_text_transform')))
globais = st.get('__globals__', {})
testa('cores do item pelas globais (item, hover e ativo)',
      globais.get('color_menu_item') == 'globals/colors?id=iara-menu'
      and globais.get('color_menu_item_hover') == 'globals/colors?id=accent'
      and globais.get('color_menu_item_active') == 'globals/colors?id=accent')

print('== cabeçalho: CSS dos estados (o que viaja no kit) ==')
css = (RAIZ / 'bloco-b' / 'css' / 'iara-cabecalho.css') \
    .read_text(encoding='utf-8')
testa('hover: Terracota escuro com linha escura',
      '.iara-menu-nav .elementor-nav-menu--main .elementor-item:hover' in css
      and 'box-shadow: inset 0 -1px 0 #78452f' in css)
testa('ativo: Terracota escuro com linha Terracota claro',
      '.elementor-item.elementor-item-active' in css
      and 'box-shadow: inset 0 -1px 0 #e4cbb5' in css)
testa('menu em caixa alta também no CSS',
      '.iara-menu-nav .elementor-nav-menu--main .elementor-item' in css
      and 'text-transform: uppercase;' in css)
testa('cabeçalho fixo (sticky) no CSS',
      '.elementor-location-header' in css and 'position: sticky' in css)

print('== cabeçalho: faixa (topbar) ==')
faixa = next(e for e in percorre(cab['content'])
             if e.get('settings', {}).get('css_classes') == 'iara-faixa-lista')
fg = faixa['settings'].get('__globals__', {})
testa('hover da faixa em Terracota claro, texto e ícone',
      fg.get('text_color_hover') == 'globals/colors?id=iara-terracota-claro'
      and fg.get('icon_color_hover')
      == 'globals/colors?id=iara-terracota-claro',
      'prototipo: accent-soft #e4cbb5 sobre o verde')
testa('sublinhado no hover da faixa no CSS do kit',
      '.iara-faixa-lista .elementor-icon-list-item a:hover' in css
      and 'text-decoration: underline' in css)

print('== cabeçalho: logotipo ==')
logo_w = [e for e in percorre(cab['content'])
          if e.get('widgetType') == 'theme-site-logo']
testa('marca virou o widget Site Logo (lê a mídia do Elementor)',
      len(logo_w) == 1, str(len(logo_w)) + ' widget')
if logo_w:
    lst = logo_w[0]['settings']
    testa('logotipo a 210px, link para a home',
          lst.get('width', {}).get('size') == 210
          and lst.get('link_to') == 'custom'
          and lst.get('link', {}).get('url', '').endswith('/iaracosta/'))
testa('largura do logotipo reforçada no CSS do kit',
      '.iara-marca-logo img' in css and 'width: 210px' in css)

print('== cabeçalho: ícones de ação ==')
icones = [e for e in percorre(cab['content'])
          if e.get('widgetType') == 'icon']
testa('busca e conta seguem ícones simples', len(icones) == 2,
      str(len(icones)))
testa('ícones a 17px declarados no widget',
      all(e['settings']['size'].get('size') == 17 for e in icones))
sacola = [e for e in percorre(cab['content'])
          if e.get('widgetType') == 'woocommerce-menu-cart']
testa('sacola é o Carrinho do Menu, com bolha e traço fino (bag-light)',
      len(sacola) == 1
      and sacola[0]['settings'].get('icon') == 'bag-light'
      and sacola[0]['settings'].get('items_indicator') == 'bubble')
desejos = [e for e in percorre(cab['content'])
           if e.get('widgetType') == 'wp-widget-widget_top_wishlist']
testa('desejos é o contador do plugin TI (ícone, sem texto)',
      len(desejos) == 1
      and desejos[0]['settings'].get('wp', {}).get('show_icon') == 1
      and desejos[0]['settings'].get('wp', {}).get('show_text') == 0)
acoes_st = next(e for e in percorre(cab['content'])
                if e.get('settings', {}).get('css_classes') == 'iara-acoes')
testa('distância entre os ícones igual à do protótipo (4px)',
      (acoes_st['settings'].get('flex_gap') or {}).get('size') == 4,
      'botões de 43px encostados, como no .header-actions')
testa('selo Terracota dos contadores no CSS do kit',
      '.elementor-button-icon-qty[data-counter]' in css
      and '.wishlist_products_counter_number' in css
      and 'background: #a45f43' in css)
testa('ícones na cor suave do menu',
      all(e['settings'].get('__globals__', {}).get('primary_color')
          == 'globals/colors?id=iara-menu' for e in icones))
testa('conta e desejos em contorno (fa-regular)',
      all(e['settings']['selected_icon'].get('library') == 'fa-regular'
          for e in icones
          if e['settings'].get('_title') in ('Minha conta',
                                             'Lista de desejos')))
testa('alvo de toque e hover dos ícones no CSS',
      '.iara-acoes .elementor-icon' in css and 'padding: 13px' in css
      and '.iara-acoes .elementor-icon:hover' in css
      and '#78452f' in css.split('.iara-acoes .elementor-icon:hover')[1]
      .split('}')[0])

print('== tipografia embutida nos widgets (todos os templates) ==')
sem_fonte = []
for arquivo in sorted((RAIZ / 'bloco-b' / 'json').glob('*.json')):
    dados = json.loads(arquivo.read_text(encoding='utf-8'))
    for el in percorre(dados['content']):
        if el.get('elType') != 'widget':
            continue
        wst = el.get('settings', {})
        for chave, referencia in wst.get('__globals__', {}).items():
            if 'typography' in chave and referencia.startswith(
                    'globals/typography'):
                sem_fonte.append(f'{arquivo.name}:{wst.get("_title", "?")}')
testa('nenhum widget depende de fonte global (tudo embutido)',
      not sem_fonte, '; '.join(sem_fonte[:4]))

print('== rodapé: títulos e listas miúdos ==')
rod = carrega('02-rodape.json')
titulos = [e for e in percorre(rod['content'])
           if e.get('widgetType') == 'heading']
DE_COLUNA = ('Institucional', 'Categorias', 'Atendimento')
testa('títulos de coluna em Jost 11px caixa alta',
      all(e['settings'].get('typography_font_family') == 'Jost'
          and e['settings']['typography_font_size'].get('size') == 11
          and e['settings'].get('typography_text_transform') == 'uppercase'
          for e in titulos
          if e['settings'].get('_title') in DE_COLUNA)
      and sum(1 for e in titulos
              if e['settings'].get('_title') in DE_COLUNA) == 3,
      'Institucional, Categorias, Atendimento')
listas = [e for e in percorre(rod['content'])
          if e.get('widgetType') == 'icon-list']
com_texto = [e for e in listas
             if any(i.get('text') for i in e['settings'].get('icon_list', []))]
testa('listas do rodapé com texto em Jost embutido (icon_typography)',
      all(e['settings'].get('icon_typography_font_family')
          for e in com_texto),
      str(len(com_texto)) + ' listas com texto')

print('== rodapé: faixa de segurança e selos (imagem do protótipo) ==')
seg_titulos = [e for e in percorre(rod['content'])
               if e.get('widgetType') == 'heading'
               and e['settings'].get('_title')
               in ('Pix, cartão e boleto', 'Ambiente protegido',
                   'Pedido rastreado', '7 dias para desistir')]
testa('títulos da faixa em Jost 600 caixa alta',
      len(seg_titulos) == 4 and all(
          e['settings'].get('typography_font_weight') == '600'
          and e['settings'].get('typography_text_transform') == 'uppercase'
          for e in seg_titulos), str(len(seg_titulos)) + ' títulos')
sociais = [e for e in percorre(rod['content'])
           if e.get('settings', {}).get('css_classes') == 'iara-sociais']
testa('sociais em círculos com borda (classe + CSS)',
      len(sociais) == 1
      and '.iara-sociais .elementor-icon-list-item a' in css
      and 'border-radius: 50%' in css)
testa('divisórias da faixa e linha dos selos no CSS',
      '.iara-seg-faixa > * + *' in css and '.iara-seg-linha' in css)
testa('selo com quadradinho escuro no CSS',
      '.iara-selo-icone' in css and 'background: #2d2925' in css)
testa('selo dos contadores colado no ícone (topo -4px)',
      'top: -4px; right: -6px' in css)

pag = next(e for e in percorre(rod['content'])
           if e.get('settings', {}).get('_title') == 'Formas de pagamento')
sel = next(e for e in percorre(rod['content'])
           if e.get('settings', {}).get('_title') == 'Selos de segurança')
soma = (pag['settings']['_flex_basis']['size']
        + sel['settings']['_flex_basis']['size'])
testa('pagamento e selos na mesma linha (54% + 40% + respiro)',
      soma <= 96 and pag['settings']['_flex_basis']['size'] == 54,
      f'soma {soma}% (antes 96% + gap estourava e a Segurança caía)')
sem_cor = []
for arquivo in sorted((RAIZ / 'bloco-b' / 'json').glob('*.json')):
    dados = json.loads(arquivo.read_text(encoding='utf-8'))
    for el in percorre(dados['content']):
        st = el.get('settings', {})
        if st.get('border_border') == 'solid':
            tem = ('border_color' in st.get('__globals__', {})
                   or str(st.get('border_color', '')).startswith('#'))
            if not tem:
                sem_cor.append(arquivo.name + ':'
                               + st.get('_title', '?'))
testa('todo container com borda tem a cor da borda declarada',
      not sem_cor, '; '.join(sem_cor[:4]))
linha = [e for e in percorre(rod['content'])
         if e.get('settings', {}).get('css_classes') == 'iara-conta-links']
testa('Minha conta, Desejos e Sacola em uma linha com ponto (CSS)',
      len(linha) == 1 and len(linha[0]['settings']['icon_list']) == 3
      and '.iara-conta-links' in css)
logo_rod = [e for e in percorre(rod['content'])
            if e.get('widgetType') == 'theme-site-logo']
testa('rodapé com o logotipo em imagem a 190px (sem marca em texto)',
      len(logo_rod) == 1
      and logo_rod[0]['settings'].get('width', {}).get('size') == 190)
sobre = next(e for e in percorre(rod['content'])
             if e.get('widgetType') == 'text-editor'
             and 'Vestuário feminino autoral' in str(
                 e['settings'].get('editor', '')))
testa('parágrafo da marca a 13px (era 15px)',
      sobre['settings'].get('typography_font_size', {}).get('size') == 13)
nota = next(e for e in percorre(rod['content'])
            if e.get('settings', {}).get('css_classes') == 'iara-news-nota')
news_box = next(e for e in percorre(rod['content'])
                if e.get('settings', {}).get('_title') == 'Newsletter')
testa('nota da newsletter fora da caixa, com largura de leitura',
      nota not in list(percorre(news_box.get('elements', [])))
      and '.iara-news-nota' in css and 'max-width: 76ch' in css)
seg_textos = [e for e in percorre(rod['content'])
              if e.get('widgetType') == 'text-editor'
              and e['settings'].get('typography_font_size', {})
              .get('size') == 12]
testa('textos da faixa de segurança a 12px', len(seg_textos) >= 4,
      str(len(seg_textos)))
form = next(e for e in percorre(rod['content'])
            if e.get('widgetType') == 'form')
testa('formulário da newsletter com 460px (coluna do protótipo)',
      form['settings'].get('_flex_basis', {}).get('size') == 460)
whats = [e for e in percorre(rod['content'])
         if e.get('settings', {}).get('css_classes') == 'iara-whats-float']
testa('botão flutuante de WhatsApp presente, fixo pelo CSS',
      len(whats) == 1 and '.iara-whats-float' in css
      and 'position: fixed' in css)

print()
if FALHAS:
    print(f'resultado: {len(FALHAS)} teste(s) falharam')
    sys.exit(1)
print('resultado: todos os testes passaram')
