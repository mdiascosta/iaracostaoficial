#!/usr/bin/env python3
"""
Confere os arquivos JSON do Bloco B (templates do Elementor).

O que este script garante
-------------------------
1. Todo arquivo abre como JSON valido, em UTF-8.
2. O formato do envelope e o do export do Elementor:
   content, page_settings, version ("0.4"), title, type.
3. Arvore de elementos so com "container" e "widget": nenhum section/column.
4. Nenhum widget proibido pelo super prompt: html, shortcode, sidebar e os
   widgets novos "Atomics" (nomes que comecam com "e-").
5. Cor e tipografia sempre por referencia a uma Global Color / Global Font, e a
   referencia precisa existir no arquivo de globais.
6. Id de elemento com 7 caracteres e unico dentro do arquivo (inclusive os _id
   de campos repetidores, como a lista de links do rodape).
7. Todo container tem nome (_title), para o navegador de estrutura ficar legivel.
8. Nenhum resto do prototipo: link terminando em .html.
9. Nenhum CSS livre: chave custom_css e afins.

Uso:
    python3 tools/blocob_confere.py
"""

import json
import pathlib
import re
import sys

RAIZ = pathlib.Path(__file__).resolve().parents[1]
PASTA_BLOCO_B = RAIZ / 'bloco-b'
PASTA_JSON = PASTA_BLOCO_B / 'json'
ARQ_GLOBAIS = PASTA_BLOCO_B / 'globais' / 'cores-e-fontes.json'

VERSAO_FORMATO = '0.4'
CHAVES_TOPO = {'content', 'page_settings', 'version', 'title', 'type'}

# Tipos de documento do Elementor usados no projeto.
TIPOS = {
    'page', 'header', 'footer', 'archive', 'single', 'search-results',
    'error-404', 'container', 'section', 'loop-item',
}

# Widgets que podem aparecer nos arquivos do projeto. Lista fechada de proposito:
# se um arquivo trouxer widget fora dela, a checagem avisa.
# wp-widget-widget_top_wishlist: contador de desejos do plugin TI
# WooCommerce Wishlist (widget do WordPress dentro do Elementor).
WIDGETS_PERMITIDOS = {
    'wp-widget-widget_top_wishlist',
    # Elementor gratuito
    'heading', 'text-editor', 'image', 'button', 'icon', 'icon-list', 'icon-box',
    'image-box', 'divider', 'spacer', 'accordion', 'toggle', 'tabs', 'counter',
    'google_maps', 'social-icons', 'star-rating', 'rating', 'progress',
    'testimonial', 'image-gallery', 'image-carousel', 'alert', 'video', 'audio',
    'menu-anchor', 'wordpress',
    # Elementor Pro (Theme Builder, WooCommerce, formularios)
    'theme-site-logo', 'theme-post-title', 'theme-post-content', 'theme-post-excerpt',
    'theme-post-featured-image', 'theme-post-info', 'nav-menu', 'search-form',
    'breadcrumbs', 'archive-title', 'archive-description', 'archive-posts',
    'posts', 'portfolio', 'form', 'login', 'sitemap', 'page-title', 'popup',
    'woocommerce-products', 'woocommerce-product-title', 'woocommerce-product-images',
    'woocommerce-product-price', 'woocommerce-add-to-cart', 'woocommerce-product-rating',
    'woocommerce-product-stock', 'woocommerce-product-meta', 'woocommerce-product-content',
    'woocommerce-product-short-description', 'woocommerce-product-data-tabs',
    'woocommerce-product-additional-information', 'woocommerce-product-related',
    'woocommerce-product-upsell', 'woocommerce-menu-cart', 'woocommerce-cart',
    'woocommerce-checkout', 'woocommerce-my-account', 'woocommerce-purchase-summary',
    'woocommerce-breadcrumbs', 'woocommerce-notices', 'woocommerce-pages',
    'woocommerce-product-categories', 'woocommerce-archive-products',
}

PROIBIDOS = {'html', 'shortcode', 'sidebar', 'text-path', 'template'}

COR_HEX = re.compile(r'#[0-9a-fA-F]{3,8}\b')
ID_VALIDO = re.compile(r'^[a-z0-9]{7}$')


def carregar_globais(problemas):
    """Le o arquivo de globais e devolve os ids de cor e de fonte."""
    if not ARQ_GLOBAIS.exists():
        problemas.append(f'{ARQ_GLOBAIS.relative_to(RAIZ)} nao existe (rode tools/blocob_gera.py)')
        return set(), set()
    dados = json.loads(ARQ_GLOBAIS.read_text(encoding='utf-8'))
    ajustes = dados.get('settings', {})
    cores = {c['_id'] for c in ajustes.get('system_colors', [])}
    cores |= {c['_id'] for c in ajustes.get('custom_colors', [])}
    fontes = {f['_id'] for f in ajustes.get('system_typography', [])}
    fontes |= {f['_id'] for f in ajustes.get('custom_typography', [])}

    if len(ajustes.get('system_colors', [])) != 4:
        problemas.append('globais: o Elementor tem exatamente 4 cores de sistema')
    titulos = [c['title'] for c in ajustes.get('custom_colors', [])]
    if len(titulos) != len(set(titulos)):
        problemas.append('globais: titulo de cor personalizada repetido (o ajusta-ids precisa de titulo unico)')
    titulos = [f['title'] for f in ajustes.get('custom_typography', [])]
    if len(titulos) != len(set(titulos)):
        problemas.append('globais: titulo de fonte personalizada repetido')
    for chave, itens in (('custom_colors', ajustes.get('custom_colors', [])),
                         ('system_colors', ajustes.get('system_colors', []))):
        for item in itens:
            if not COR_HEX.fullmatch(item.get('color', '')):
                problemas.append(f'globais: {chave} {item.get("_id")} sem cor hexadecimal valida')
    return cores, fontes


def percorrer(elemento, caminho, achados):
    """Guarda cada elemento da arvore, com o caminho ate ele."""
    achados.append((caminho, elemento))
    for indice, filho in enumerate(elemento.get('elements', []) or []):
        percorrer(filho, f'{caminho}>{indice}', achados)


def conferir_arquivo(caminho, cores, fontes, problemas, resumo):
    dados = json.loads(caminho.read_text(encoding='utf-8'))
    nome = caminho.name

    # 1. envelope
    if not isinstance(dados, dict) or set(dados) != CHAVES_TOPO:
        problemas.append(f'{nome}: chaves do topo diferentes do export do Elementor '
                         f'({sorted(dados) if isinstance(dados, dict) else type(dados).__name__})')
        return
    if dados['version'] != VERSAO_FORMATO:
        problemas.append(f'{nome}: version "{dados["version"]}" (esperado "{VERSAO_FORMATO}")')
    if dados['type'] not in TIPOS:
        problemas.append(f'{nome}: tipo desconhecido "{dados["type"]}"')
    if not isinstance(dados['title'], str) or not dados['title'].strip():
        problemas.append(f'{nome}: titulo vazio')
    if not isinstance(dados['content'], list):
        problemas.append(f'{nome}: content nao e lista')
        return

    # 2. arvore
    elementos = []
    for indice, raiz in enumerate(dados['content']):
        percorrer(raiz, str(indice), elementos)

    usados = set()
    containers = 0
    widgets = 0
    for caminho_el, el in elementos:
        tipo = el.get('elType')
        if tipo == 'container':
            containers += 1
            if not el.get('settings', {}).get('_title'):
                problemas.append(f'{nome}: container sem nome (_title) em {caminho_el}')
        elif tipo == 'widget':
            widgets += 1
            wt = el.get('widgetType', '')
            if wt in PROIBIDOS or wt.startswith('e-'):
                problemas.append(f'{nome}: widget proibido "{wt}" em {caminho_el}')
            elif wt not in WIDGETS_PERMITIDOS:
                problemas.append(f'{nome}: widget "{wt}" fora da lista do projeto em {caminho_el}')
        else:
            problemas.append(f'{nome}: elType "{tipo}" em {caminho_el} '
                             f'(o projeto usa somente container e widget)')
        if el.get('elements') is None:
            problemas.append(f'{nome}: elemento sem lista de filhos em {caminho_el}')

    # 3. ids
    def conferir_ids(valor, contexto):
        if isinstance(valor, dict):
            if '_id' in valor and contexto.startswith('item'):
                i = valor['_id']
                if not ID_VALIDO.match(str(i)):
                    problemas.append(f'{nome}: _id "{i}" fora do padrao de 7 caracteres em {contexto}')
                elif i in usados:
                    problemas.append(f'{nome}: _id repetido "{i}" em {contexto}')
                else:
                    usados.add(i)
            for chave, filho in valor.items():
                conferir_ids(filho, f'{contexto}.{chave}')
        elif isinstance(valor, list):
            for indice, filho in enumerate(valor):
                conferir_ids(filho, f'{contexto}[{indice}]')

    for caminho_el, el in elementos:
        i = el.get('id')
        if not ID_VALIDO.match(str(i)):
            problemas.append(f'{nome}: id "{i}" fora do padrao de 7 caracteres em {caminho_el}')
        elif i in usados:
            problemas.append(f'{nome}: id repetido "{i}" em {caminho_el}')
        else:
            usados.add(i)
        conferir_ids(el.get('settings', {}), caminho_el)

    # 4. estilos: so globais, sem cor escrita na mao e sem CSS livre
    for caminho_el, el in elementos:
        ajustes = el.get('settings', {}) or {}
        for proibida in ('custom_css', 'custom_css_pro', '_custom_css'):
            if proibida in ajustes:
                problemas.append(f'{nome}: CSS livre em {caminho_el} (chave {proibida})')
        for chave, valor in ajustes.items():
            if chave == '__globals__':
                continue
            if isinstance(valor, str) and COR_HEX.search(valor) and len(valor) < 40:
                problemas.append(f'{nome}: cor escrita na mao em {caminho_el} '
                                 f'({chave}="{valor}"); usar Global Color')
        globais = ajustes.get('__globals__', {}) or {}
        for controle, referencia in globais.items():
            if not isinstance(referencia, str):
                problemas.append(f'{nome}: referencia de global invalida em {caminho_el} ({controle})')
                continue
            achado = re.match(r'^globals/(colors|typography)\?id=(.+)$', referencia)
            if not achado:
                problemas.append(f'{nome}: referencia "{referencia}" fora do padrao '
                                 f'globals/... ?id=... em {caminho_el}')
                continue
            grupo, apelido = achado.groups()
            if grupo == 'colors' and apelido not in cores:
                problemas.append(f'{nome}: cor global "{apelido}" nao existe nas globais '
                                 f'(em {caminho_el})')
            if grupo == 'typography' and apelido not in fontes:
                problemas.append(f'{nome}: fonte global "{apelido}" nao existe nas globais '
                                 f'(em {caminho_el})')

    # 4b. chaves de estilo por widget (conferidas no codigo-fonte do
    # Elementor; chave errada = tema impoe a fonte dele, foi a v0.3.11)
    for caminho_el, el in elementos:
        if el.get('elType') != 'widget':
            continue
        wt = el.get('widgetType', '')
        globais = (el.get('settings', {}) or {}).get('__globals__', {}) or {}
        if wt == 'icon-list':
            if 'typography' in globais:
                problemas.append(f'{nome}: icon-list com chave "typography" em {caminho_el}; '
                                 f'a certa e "icon_typography"')
            for item in (el.get('settings', {}) or {}).get('icon_list', []):
                if 'selected_icon' not in item:
                    problemas.append(f'{nome}: item de icon-list sem selected_icon em '
                                     f'{caminho_el} (o Elementor desenha o check padrao)')
        if wt in ('icon-box', 'image-box'):
            for errada in ('typography_title', 'typography_description'):
                if errada in globais:
                    problemas.append(f'{nome}: {wt} com chave "{errada}" em {caminho_el}; '
                                     f'as certas sao title_typography/description_typography')

    # 4c. pente fino de links e imagens (v0.3.13): o site esta em subpasta
    # (oeemax.com.br/iaracosta/), entao link interno que comeca com "/" cai
    # fora do site e quebra. Todo link interno precisa nascer de SITE_BASE.
    SITE_BASE = 'https://oeemax.com.br/iaracosta'

    def url_ok(url):
        return (url.startswith(SITE_BASE) or url.startswith('#')
                or url.startswith('mailto:') or url.startswith('tel:')
                or url.startswith('https://wa.me/')
                or url == '[PREENCHER]')

    def pente_fino(valor, caminho_el):
        if isinstance(valor, dict):
            if isinstance(valor.get('url'), str) and ('is_external' in valor or 'nofollow' in valor):
                url = valor['url']
                if not url:
                    problemas.append(f'{nome}: link sem endereco em {caminho_el}')
                elif not url_ok(url):
                    problemas.append(f'{nome}: link "{url}" fora do endereco do site '
                                     f'em {caminho_el} (site em subpasta: usar {SITE_BASE}/...)')
            for filho in valor.values():
                pente_fino(filho, caminho_el)
        elif isinstance(valor, list):
            for filho in valor:
                pente_fino(filho, caminho_el)
        elif isinstance(valor, str):
            for url in re.findall(r'href="([^"]+)"', valor):
                if not url_ok(url):
                    problemas.append(f'{nome}: link "{url}" dentro de texto em '
                                     f'{caminho_el} (fora do endereco do site)')

    for caminho_el, el in elementos:
        pente_fino(el.get('settings', {}) or {}, caminho_el)
        if el.get('widgetType') in ('image', 'image-box'):
            url_img = (el.get('settings', {}).get('image') or {}).get('url', '')
            if not url_img.startswith('http'):
                problemas.append(f'{nome}: widget de imagem sem foto em {caminho_el} '
                                 f'(a importacao mostra espaco vazio)')

    # 5. nada de link do prototipo
    texto = caminho.read_text(encoding='utf-8')
    if '.html' in texto:
        problemas.append(f'{nome}: link apontando para .html (resto do prototipo)')

    resumo.append((nome, dados['type'], dados['title'], containers, widgets))
    return None


def conferir_kit_globais(cores, fontes, problemas):
    """O pacote de importacao das configuracoes (Kit do Elementor)."""
    import zipfile
    caminho = PASTA_BLOCO_B / 'globais' / 'iara-costa-globais.zip'
    if not caminho.exists():
        problemas.append('globais/iara-costa-globais.zip nao existe (rode tools/blocob_gera_kit_globais.py)')
        return
    with zipfile.ZipFile(caminho) as z:
        nomes = z.namelist()
        if nomes != ['manifest.json', 'site-settings.json']:
            problemas.append(f'kit de globais: arquivos {nomes} (esperado manifest.json e site-settings.json)')
            return
        manifesto = json.loads(z.read('manifest.json'))
        settings = json.loads(z.read('site-settings.json')).get('settings', {})
    if manifesto.get('version') != '2.0':
        problemas.append('kit de globais: manifest sem version "2.0" (FORMAT_VERSION do Elementor)')
    ids_cores = {c['_id'] for c in settings.get('system_colors', []) + settings.get('custom_colors', [])}
    ids_fontes = {f['_id'] for f in settings.get('system_typography', []) + settings.get('custom_typography', [])}
    if ids_cores != cores:
        problemas.append('kit de globais: cores diferentes do arquivo de globais')
    if ids_fontes != fontes:
        problemas.append('kit de globais: fontes diferentes do arquivo de globais')


# Tipos de documento de tema: sem conditions no manifesto, a importacao
# do kit falha para eles (theme-document.php do Pro le conditions[0]).
TIPOS_DE_TEMA = {'header', 'footer', 'archive', 'single',
                 'search-results', 'error-404'}


def conferir_kit_completo(problemas):
    """O kit completo de importacao unica (v0.3.12)."""
    import zipfile
    caminho = PASTA_BLOCO_B / 'iara-costa-kit-completo.zip'
    if not caminho.exists():
        problemas.append('iara-costa-kit-completo.zip nao existe '
                         '(rode tools/blocob_gera_kit_completo.py)')
        return
    originais = {}
    for arq in sorted(PASTA_JSON.glob('*.json')):
        originais[arq.name] = json.loads(arq.read_text(encoding='utf-8'))
    with zipfile.ZipFile(caminho) as z:
        nomes = z.namelist()
        manifesto = json.loads(z.read('manifest.json'))
        settings = json.loads(z.read('site-settings.json')).get('settings', {})
        templates = {}
        for nome in nomes:
            if nome.startswith('templates/'):
                doc_id = nome[len('templates/'):-len('.json')]
                templates[doc_id] = json.loads(z.read(nome))
    if manifesto.get('version') != '2.0':
        problemas.append('kit completo: manifest sem version "2.0"')
    if not settings.get('system_colors') or not settings.get('custom_typography'):
        problemas.append('kit completo: site-settings sem cores ou fontes')
    css_kit = settings.get('custom_css', '')
    if '.iara-menu' not in css_kit or 'elementor-icon-list-item a' not in css_kit:
        problemas.append('kit completo: site-settings sem o CSS geral do '
                         'cabecalho (custom_css com as regras de link do menu)')
    if 'settings-custom-css' not in (manifesto.get('site-settings') or []):
        problemas.append('kit completo: manifesto sem a aba settings-custom-css')
    manifest_templates = manifesto.get('templates', {})
    if len(manifest_templates) != 24 or len(templates) != 24:
        problemas.append(f'kit completo: {len(manifest_templates)} no manifesto e '
                         f'{len(templates)} arquivos (esperado 24 e 24)')
        return
    if set(manifest_templates) != set(templates):
        problemas.append('kit completo: ids do manifesto diferentes dos arquivos')
    titulos_originais = {d['title']: d for d in originais.values()}
    for doc_id, resumo_tpl in manifest_templates.items():
        dados = templates[doc_id]
        original = titulos_originais.get(resumo_tpl.get('title'))
        if original is None:
            problemas.append(f'kit completo: template "{resumo_tpl.get("title")}" '
                             f'sem correspondente em bloco-b/json')
            continue
        if resumo_tpl.get('doc_type') != original['type']:
            problemas.append(f'kit completo: doc_type de "{original["title"]}" '
                             f'diferente do JSON original')
        if dados.get('content') != original['content']:
            problemas.append(f'kit completo: conteudo de "{original["title"]}" '
                             f'diferente do JSON original')
        if dados.get('metadata', {}).get('_elementor_template_type') != original['type']:
            problemas.append(f'kit completo: metadata de "{original["title"]}" '
                             f'sem _elementor_template_type certo')
        if original['type'] in TIPOS_DE_TEMA:
            conds = resumo_tpl.get('conditions') or []
            if not conds or conds[0].get('type') != 'include' or not conds[0].get('name'):
                problemas.append(f'kit completo: "{original["title"]}" e documento '
                                 f'de tema e esta sem conditions (a importacao falha)')
            if not resumo_tpl.get('location'):
                problemas.append(f'kit completo: "{original["title"]}" sem location')


def main():
    problemas = []
    cores, fontes = carregar_globais(problemas)
    conferir_kit_globais(cores, fontes, problemas)
    conferir_kit_completo(problemas)

    arquivos = sorted(PASTA_JSON.glob('*.json')) if PASTA_JSON.exists() else []
    if not arquivos:
        print('nenhum arquivo em bloco-b/json (rode tools/blocob_gera.py)')
        return 1

    resumo = []
    for caminho in arquivos:
        try:
            conferir_arquivo(caminho, cores, fontes, problemas, resumo)
        except json.JSONDecodeError as erro:
            problemas.append(f'{caminho.name}: JSON invalido ({erro.msg}, linha {erro.lineno})')

    for nome, tipo, titulo, containers, widgets in resumo:
        print(f'  ok  {nome:26s} tipo={tipo:14s} {containers:3d} containers, {widgets:3d} widgets   {titulo}')

    print()
    print(f'arquivos conferidos: {len(resumo)}')
    print(f'cores globais: {len(cores)}  |  fontes globais: {len(fontes)}')

    if problemas:
        print()
        for p in problemas:
            print(f'[ERRO] {p}')
        print()
        print(f'resultado: {len(problemas)} problema(s)')
        return 1

    print('resultado: tudo certo')
    return 0


if __name__ == '__main__':
    sys.exit(main())
