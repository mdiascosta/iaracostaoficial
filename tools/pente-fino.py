#!/usr/bin/env python3
"""Pente fino: HTML e CSS dos arquivos do protótipo.

Roda com as bibliotecas de parse de verdade:
  html5lib   -> erros de sintaxe do HTML (fecha o que faltou fechar, etc.)
  tinycss2   -> erros de sintaxe do CSS
E, em cima do DOM já parseado, confere o que costuma quebrar na mão:
ids repetidos, links internos que não existem, âncoras vazias,
aria-controls/labelledby/describedby e for/id apontando para o nada,
imagens que não existem, classes sem CSS, CSS sem uso e ganchos (data-*)
que nenhum JS lê.

COMO RODAR (na raiz do repositório):
  python3 -m venv .venv && .venv/bin/pip install html5lib tinycss2
  .venv/bin/python tools/pente-fino.py

Ele só LÊ: não corrige nada. Cada achado sai com arquivo e linha para a
correção ser feita à mão, com conferência.
"""
import html5lib
import tinycss2
from html5lib import HTMLParser
from pathlib import Path
import re
import sys

RAIZ = Path(__file__).resolve().parent.parent
PROJ = RAIZ / 'seu-projeto'
CONTENT = RAIZ / 'tools' / 'content'
PARTS = RAIZ / 'tools' / 'partials'

paginas = sorted(PROJ.glob('*.html'))
parciais = sorted(CONTENT.glob('*.html')) + sorted(PARTS.glob('*.html'))
csss = sorted((PROJ / 'assets' / 'css').glob('*.css'))
jss = sorted((PROJ / 'assets' / 'js').glob('*.js'))

problemas = []
def erro(origem, msg):
    problemas.append((origem, msg))

# ---------------------------------------------------------------- HTML
def erros_html(caminho, fragmento=False):
    texto = caminho.read_text(encoding='utf-8')
    parser = HTMLParser(namespaceHTMLElements=False)
    if fragmento:
        parser.parseFragment(texto)
    else:
        parser.parse(texto)
    saida = []
    for pos, codigo, dados in parser.errors:
        linha, col = pos if isinstance(pos, tuple) else (pos[0], pos[1])
        saida.append((linha, col, codigo, dados))
    return texto, saida

TOLERADOS = {
    # o html5lib reclama de coisas que são escolha nossa e válidas
    'unexpected-end-tag',
    'unknown-start-tag',
}

for grupo, arquivos, fragmento in (('pagina', paginas, False), ('parcial', parciais, True)):
    for arq in arquivos:
        texto, erros = erros_html(arq, fragmento)
        for linha, col, codigo, dados in erros:
            if codigo in TOLERADOS:
                continue
            erro(f'{arq.relative_to(RAIZ)}:{linha}:{col}',
                 f'{codigo} {dados if dados else ""}'.strip())

# ---------------------------------------------------------------- CSS
def erros_css(caminho):
    texto = caminho.read_text(encoding='utf-8')
    regras = tinycss2.parse_stylesheet(texto, skip_comments=True, skip_whitespace=True)
    saida = []
    for regra in regras:
        if regra.type == 'error':
            saida.append((regra.source_line, regra.source_column, regra.message))
        elif regra.type == 'qualified-rule':
            # valida também o conteúdo das declarações
            for decl in tinycss2.parse_declaration_list(regra.content, skip_comments=True, skip_whitespace=True):
                if decl.type == 'error':
                    saida.append((decl.source_line, decl.source_column, decl.message))
    return texto, saida

def limpar_css(texto):
    texto = re.sub(r'/\*[\s\S]*?\*/', ' ', texto)      # comentários
    texto = re.sub(r'"[^"\n]*"', '""', texto)            # strings
    texto = re.sub(r"'[^'\n]*'", "''", texto)
    return texto

todos_css = ''
for arq in csss:
    texto, erros = erros_css(arq)
    todos_css += limpar_css(texto)
    for linha, col, msg in erros:
        erro(f'{arq.relative_to(RAIZ)}:{linha}:{col}', f'CSS: {msg}')

# variáveis usadas que nunca são definidas
definidas = set(re.findall(r'(--iara-[a-z0-9-]+)\s*:', todos_css)) | set(re.findall(r'(--fs-[a-z0-9-]+)\s*:', todos_css))
usadas = set(re.findall(r'var\(\s*(--[a-z0-9-]+)', todos_css))
for v in sorted(usadas - definidas):
    if v.startswith('--e-global'):
        continue
    erro('CSS', f'variável usada e nunca definida: {v}')

# chaves desbalanceadas
for arq in csss:
    texto = arq.read_text(encoding='utf-8')
    if texto.count('{') != texto.count('}'):
        erro(arq.relative_to(RAIZ), f'chaves desbalanceadas: {texto.count("{")} abrem, {texto.count("}")} fecham')

# ---------------------------------------------------------------- DOM
def classes_de(html_texto):
    achadas = set()
    for m in re.finditer(r'class="([^"]*)"', html_texto):
        for c in m.group(1).split():
            achadas.add(c)
    return achadas

html_gerado = '\n'.join(p.read_text(encoding='utf-8') for p in paginas)
html_tudo = html_gerado + '\n' + '\n'.join(p.read_text(encoding='utf-8') for p in parciais)
classes_usadas = classes_de(html_tudo)

# classes que o JS cria em tempo de execução contam como usadas
js_tudo = '\n'.join(q.read_text(encoding='utf-8') for q in jss)
classes_do_js = classes_de(js_tudo)
for m in re.finditer(r'classList\.(?:add|toggle|remove)\(\s*[\'"]([a-zA-Z0-9_-]+)', js_tudo):
    classes_do_js.add(m.group(1))
classes_usadas |= classes_do_js

seletores_css = set(re.findall(r'\.([a-zA-Z][a-zA-Z0-9_-]*)', todos_css))
# Conhecidas e conferidas: existem para dar contexto ou são só estrutura,
# sem precisar de nenhuma regra de CSS. Não entram como achado.
CLASSES_OK = {
    'hero__copy', 'product__info', 'shop__main',      # caixas de layout
    'pay', 'seals', 'seal__text',                     # quadro de segurança do rodapé
    'cookie-bar__text', 'drawer__close',              # texto e botão de fechar
    'gallery', 'site-footer__col',                    # agrupamentos do rodapé
}
classes_sem_css = sorted(c for c in (classes_usadas - seletores_css)
                         if c not in CLASSES_OK and not c.startswith('page-'))
classes_sem_css_ok = sorted(c for c in (classes_usadas - seletores_css)
                            if c in CLASSES_OK or c.startswith('page-'))
classes_sem_html = sorted(seletores_css - classes_usadas)

print('=' * 78)
print('PENTE FINO · BLOCO A')
print('=' * 78)
print(f'arquivos: {len(paginas)} páginas geradas, {len(parciais)} parciais, '
      f'{len(csss)} CSS, {len(jss)} JS')

print('\n--- 1. Erros de sintaxe (html5lib / tinycss2)')
if problemas:
    for origem, msg in problemas:
        print(f'  ! {origem}: {msg}')
else:
    print('  nenhum')

print(f'\n--- 2. Classes no HTML sem nenhuma regra no CSS ({len(classes_sem_css)})')
for c in classes_sem_css:
    print(f'  - .{c}')
if not classes_sem_css:
    print('  nenhum')
if classes_sem_css_ok:
    print(f'  (conferidas e sem necessidade de CSS: {len(classes_sem_css_ok)})')
    print('   ' + ', '.join('.' + c for c in classes_sem_css_ok))

print(f'\n--- 3. Regras no CSS que não aparecem no HTML ({len(classes_sem_html)})')
for c in classes_sem_html:
    print(f'  - .{c}')

# ---------------------------------------------------------------- DOM: referências
from html5lib import HTMLParser as _HP

def elementos(doc):
    """Aceita a árvore do html5lib seja ElementTree (lxml) seja minidom."""
    if hasattr(doc, 'documentElement'):
        pilha = [doc.documentElement]
        while pilha:
            no = pilha.pop()
            for filho in no.childNodes:
                if filho.nodeType == filho.ELEMENT_NODE:
                    yield filho
                    pilha.append(filho)
    else:
        for no in doc.iter():
            # o html5lib representa comentários como "elementos" de tag função
            if isinstance(no.tag, str):
                yield no

def dom_de(caminho):
    parser = _HP(namespaceHTMLElements=False)
    return parser.parse(caminho.read_text(encoding='utf-8'))

ids_por_pagina = {}
for arq in paginas:
    doc = dom_de(arq)
    ids = {}
    repetidos = []
    for el in elementos(doc):
        if el.get('id') is not None:
            i = el.get('id')
            if i in ids:
                repetidos.append(i)
            ids[i] = el
    ids_por_pagina[arq.name] = ids

print('\n--- 4. Ids repetidos na mesma página')
achou = False
for arq, ids in ids_por_pagina.items():
    doc = dom_de(PROJ / arq)
    contagem = {}
    for el in elementos(doc):
        i = el.get('id')
        if i is not None:
            contagem[i] = contagem.get(i, 0) + 1
    for i, n in contagem.items():
        if n > 1:
            achou = True
            print(f'  ! {arq}: id "{i}" aparece {n} vezes')
if not achou:
    print('  nenhum')

print('\n--- 5. Links internos e âncoras quebradas')
quebrados = 0
for arq in paginas:
    doc = dom_de(arq)
    for el in elementos(doc):
        if el.tag.lower() != 'a' or not el.get('href') is not None:
            continue
        href = el.get('href')
        if href.startswith(('http', 'mailto:', 'tel:', '#')) or href == '':
            if href.startswith('#') and len(href) > 1:
                alvo = href[1:]
                if alvo not in ids_por_pagina[arq.name]:
                    print(f'  ! {arq.name}: href="{href}" sem alvo')
                    quebrados += 1
            continue
        destino, _, frag = href.partition('#')
        if not (PROJ / destino).exists():
            print(f'  ! {arq.name}: href="{href}" aponta para arquivo que não existe')
            quebrados += 1
        elif frag:
            if frag not in ids_por_pagina.get(destino, {}):
                print(f'  ! {arq.name}: href="{href}" sem alvo em {destino}')
                quebrados += 1
if not quebrados:
    print('  nenhum')

print('\n--- 6. aria-controls / aria-labelledby / aria-describedby / for')
sem_alvo = 0
for arq in paginas:
    doc = dom_de(arq)
    ids = ids_por_pagina[arq.name]
    for el in elementos(doc):
        for atributo in ('aria-controls', 'aria-labelledby', 'aria-describedby', 'for'):
            if el.get(atributo) is not None:
                valor = el.get(atributo)
                if atributo == 'for' and el.tag.lower() != 'label':
                    continue
                for alvo in valor.split():
                    if alvo and alvo not in ids:
                        print(f'  ! {arq.name}: {el.tag.lower()} {atributo}="{valor}" sem alvo')
                        sem_alvo += 1
if not sem_alvo:
    print('  nenhum')

print('\n--- 7. Imagens e arquivos locais')
falta = 0
for arq in paginas:
    doc = dom_de(arq)
    for el in elementos(doc):
        tag = el.tag.lower()
        atributos = ([('src', el.get('src'))] if tag == 'img' and el.get('src') is not None else [])
        if tag == 'script' and el.get('src') is not None:
            atributos = [('src', el.get('src'))]
        if tag == 'link' and el.get('href') is not None:
            atributos = [('href', el.get('href'))]
        for nome, valor in atributos:
            if valor.startswith(('http', 'data:')):
                continue
            caminho = (PROJ / valor.split('?')[0]).resolve()
            if not caminho.exists():
                print(f'  ! {arq.name}: {tag}[{nome}]="{valor}" não existe')
                falta += 1
        if tag == 'img':
            if not el.get('alt') is not None:
                print(f'  ! {arq.name}: <img> sem alt ({el.get("src")})')
                falta += 1
            if el.get('alt') == '' and el.get('aria-hidden') != 'true':
                print(f'  ! {arq.name}: <img alt=""> sem aria-hidden')
                falta += 1
            for medida in ('width', 'height'):
                if not el.get(medida) is not None:
                    print(f'  ! {arq.name}: <img {el.get("src")}> sem {medida}')
                    falta += 1
if not falta:
    print('  nenhum')

# campos de formulário sem rótulo
print('\n--- 8. Campos de formulário sem rótulo acessível')
sem_rotulo = 0
for arq in paginas:
    doc = dom_de(arq)
    ids = ids_por_pagina[arq.name]
    rotulados = set()
    for el in elementos(doc):
        if el.tag.lower() == 'label' and el.get('for') is not None:
            rotulados.add(el.get('for'))
    for el in elementos(doc):
        tag = el.tag.lower()
        if tag not in ('input', 'select', 'textarea'):
            continue
        tipo = (el.get('type') or '').lower()
        if tipo in ('hidden', 'submit', 'button', 'reset', 'image'):
            continue
        if el.get('aria-label') is not None or el.get('aria-labelledby') is not None:
            continue
        i = el.get('id')
        if not i or i not in rotulados:
            print(f'  ! {arq.name}: <{tag} type="{tipo}" name="{el.get("name")}"> sem rótulo')
            sem_rotulo += 1
if not sem_rotulo:
    print('  nenhum')

# ---------------------------------------------------------------- JS
print('\n--- 9. Ganchos data-* do HTML que nenhum JS lê')
js_texto = '\n'.join(p.read_text(encoding='utf-8') for p in jss)
ganchos_html = set(re.findall(r'\s(data-[a-z0-9-]+)(?=[\s=/>])', html_tudo))
lidos = set(re.findall(r'data-[a-z0-9-]+', js_texto))
for m in re.finditer(r'dataset\.([a-zA-Z0-9]+)', js_texto):
    camel = m.group(1)
    kebab = re.sub(r'([A-Z])', lambda x: '-' + x.group(1).lower(), camel)
    lidos.add('data-' + kebab)
for m in re.finditer(r'getAttribute\(\s*["\'](data-[a-z0-9-]+)', js_texto):
    lidos.add(m.group(1))
# data-nav não é para o JS do navegador: é a marca que o tools/build.py lê para
# escrever aria-current="page" no item de menu da página atual.
GANCHOS_OK = {'data-nav'}
orfaos = sorted(g for g in (ganchos_html - lidos) if g not in GANCHOS_OK)
for g in orfaos:
    print(f'  - {g}')
if not orfaos:
    print('  nenhum')

print('\n--- 10. Ganchos lidos pelo JS que não existem no HTML')
# data-drawer-open é a porta de entrada da mini-sacola: existe no loja.js para
# qualquer botão que queira abrir a gaveta. No protótipo o ícone do cabeçalho
# continua levando para a página da sacola, então nenhuma tela usa o gancho.
# data-pagina é escrito e lido pelo próprio filtros.js: os botões da paginação
# nascem no JavaScript, então não existem no HTML entregue.
GANCHOS_LIDOS_OK = {'data-drawer-open', 'data-pagina'}
fantasmas = sorted(g for g in (lidos - ganchos_html)
                   if g.startswith('data-') and g not in GANCHOS_LIDOS_OK)
for g in fantasmas:
    print(f'  - {g}')
if not fantasmas:
    print('  nenhum')


# ---------------------------------------------------------------- inline e ids
print('\n--- 11. Estilos escritos direto no HTML (style="...")')
total_inline = 0
for arq in sorted(list(paginas) + list(parciais)):
    texto = arq.read_text(encoding='utf-8')
    achados = re.findall(r'style="([^"]*)"', texto)
    if achados:
        total_inline += len(achados)
        print(f'  - {arq.relative_to(RAIZ)}: {len(achados)}')
        for a in achados[:6]:
            print(f'      {a[:90]}')
print(f'  total: {total_inline}')

print('\n--- 12. Ids usados no CSS/JS que não existem no HTML')
tds_ids = set(re.findall(r'id="([^"]+)"', html_tudo))
js_ids = set(re.findall(r'getElementById\(\s*["\']([^"\']+)["\']', js_tudo))
js_ids |= set(re.findall(r'querySelector\(\s*["\']#([a-zA-Z0-9_-]+)', js_tudo))
# ids de verdade do CSS: só os que aparecem na posição de seletor (#id), lidos
# pelo parser (token hash), o que deixa as cores HEX de fora
for arq in csss:
    for regra in tinycss2.parse_stylesheet(limpar_css(arq.read_text(encoding='utf-8')),
                                           skip_comments=True, skip_whitespace=True):
        if regra.type == 'qualified-rule':
            for token in regra.prelude:
                if token.type == 'hash':
                    js_ids.add(token.value)
js_ids |= set(re.findall(r'querySelector\(\s*["\']#([a-zA-Z0-9_-]+)', js_texto))
js_ids = {i.lstrip('#') for i in js_ids}
faltando = sorted(i for i in js_ids if i not in tds_ids)
for i in faltando:
    print(f'  - #{i}')
if not faltando:
    print('  nenhum')
