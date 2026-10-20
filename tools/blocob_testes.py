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

print('== cabeçalho: ícones de ação ==')
icones = [e for e in percorre(cab['content'])
          if e.get('widgetType') == 'icon']
testa('são 4 ações (busca, conta, desejos, sacola)', len(icones) == 4,
      str(len(icones)))
testa('ícones a 17px declarados no widget',
      all(e['settings']['size'].get('size') == 17 for e in icones))
testa('ícones na cor suave do menu',
      all(e['settings'].get('__globals__', {}).get('primary_color')
          == 'globals/colors?id=iara-menu' for e in icones))
testa('conta e desejos em contorno (fa-regular)',
      all(e['settings']['selected_icon'].get('library') == 'fa-regular'
          for e in icones
          if e['settings'].get('_title') in ('Minha conta',
                                             'Lista de desejos')))
testa('alvo de toque e hover dos ícones no CSS',
      '.iara-acoes .elementor-icon' in css and 'padding: 12px' in css
      and '.iara-acoes .elementor-icon:hover' in css)

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

print()
if FALHAS:
    print(f'resultado: {len(FALHAS)} teste(s) falharam')
    sys.exit(1)
print('resultado: todos os testes passaram')
