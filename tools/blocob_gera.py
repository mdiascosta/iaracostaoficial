#!/usr/bin/env python3
"""
Gera os arquivos JSON do Bloco B (templates para o Elementor).

Como funciona
-------------
Este script monta os arquivos .json que a equipe importa no Elementor. Ele existe
pelo mesmo motivo do tools/build.py: escrever o layout uma vez, de forma legivel,
e deixar o arquivo final sair igual toda vez que rodar de novo.

Formato de saida (conferido no codigo-fonte do Elementor, includes/db.php e
includes/template-library/sources/local.php):
    {
      "content":       [ ... elementos ... ],
      "page_settings": { ... },
      "version":       "0.4",
      "title":         "...",
      "type":          "page" | "header" | "footer" | "archive" | "single" |
                       "search-results" | "error-404"
    }

Regras que valem para todo arquivo gerado (secao 6 do super prompt):
  - somente containers, nunca section/column;
  - nenhum widget "html", "shortcode", "sidebar" ou de CSS livre;
  - cor e tipografia sempre por referencia a Global Color / Global Font
    ("globals/colors?id=..." e "globals/typography?id=...");
  - container nomeado (campo _title), para o navegador de estrutura ficar legivel;
  - id de elemento com 7 caracteres, unico no arquivo.

Uso:
    python3 tools/blocob_gera.py            # gera tudo
    python3 tools/blocob_gera.py --lista    # so mostra o que seria gerado
"""

import argparse
import hashlib
import json
import pathlib
import re
import sys

RAIZ = pathlib.Path(__file__).resolve().parents[1]
PASTA_BLOCO_B = RAIZ / 'bloco-b'
PASTA_JSON = PASTA_BLOCO_B / 'json'
PASTA_GLOBAIS = PASTA_BLOCO_B / 'globais'

VERSAO_FORMATO = '0.4'

# --------------------------------------------------------------------------
# 1. DESIGN SYSTEM
# Fonte: seu-projeto/assets/css/style.css (variaveis --iara-* e --fs-*).
# Nada aqui foi inventado: cada valor existe no prototipo aprovado.
# --------------------------------------------------------------------------

# Cores do sistema: os quatro lugares fixos do Elementor. O id nao pode ser
# trocado (o Elementor cria esses quatro), o valor sim.
CORES_SISTEMA = [
    {'_id': 'primary',   'title': 'Primary',   'color': '#a45f43'},  # Terracota
    {'_id': 'secondary', 'title': 'Secondary', 'color': '#546858'},  # Salvia
    {'_id': 'text',      'title': 'Text',      'color': '#2d2925'},  # Carvao
    {'_id': 'accent',    'title': 'Accent',    'color': '#78452f'},  # Terracota escuro
]

# Cores personalizadas. O id sugerido ("iara-papel") serve de apelido: ao criar
# as cores na tela, o Elementor sorteia um id proprio. O
# tools/ajusta-ids.py troca os apelidos pelos ids reais de uma vez.
CORES_CUSTOM = [
    ('iara-papel',           'Papel',              '#fffdf9'),
    ('iara-branco',          'Branco',             '#ffffff'),
    ('iara-texto-suave',     'Texto suave',        '#625a52'),
    ('iara-texto-discreto',  'Texto discreto',     '#776e64'),
    ('iara-linha',           'Linha',              '#ded8ce'),
    ('iara-fio',             'Fio claro',          '#eee9e1'),
    ('iara-fundo-suave',     'Fundo suave',        '#f7f4ef'),
    ('iara-terracota-claro', 'Terracota claro',    '#e4cbb5'),
    ('iara-menu',            'Link do menu',       '#554f49'),
    ('iara-numeral',         'Numeral',            '#9c8d7e'),
    ('iara-faixa-texto',     'Texto da faixa',     '#fffdf8'),
]

# Tipografia pelo mesmo principio: quatro lugares fixos + apelidos.
FONTES_SISTEMA = [
    ('primary',   'Titulo principal', 'Playfair Display', '400', 24, 1.10, 0.105, None),
    ('secondary', 'Titulo de secao',  'Playfair Display', '400', 18, 1.20, 0.02,  None),
    ('text',      'Texto do corpo',   'Jost',             '400', 15, 1.55, 0.0,   None),
    ('accent',    'Botao',            'Jost',             '600', 11, 1.20, 0.15,  'uppercase'),
]

FONTES_CUSTOM = [
    ('iara-titulo-h3',  'Titulo terciario', 'Jost', '400', 18, 1.20, 0.01, None),
    ('iara-rotulo',     'Rotulo',           'Jost', '600', 11, 1.40, 0.15, 'uppercase'),
    ('iara-menu',       'Link do menu',     'Jost', '400', 12, 1.20, 0.06, None),
    ('iara-texto-micro','Texto miudo',      'Jost', '400', 11, 1.45, 0.06, None),
    ('iara-preco',      'Preco',            'Jost', '400', 18, 1.20, 0.0,  None),
    ('iara-assinatura', 'Assinatura (tagline)', 'Jost', '400', 11, 1.40, 0.2, 'uppercase'),
]


def cor(apelido):
    """Referencia a uma Global Color."""
    return 'globals/colors?id=' + apelido


def fonte(apelido):
    """Referencia a uma Global Font."""
    return 'globals/typography?id=' + apelido


def tipografia(familia, peso, tamanho, entrelinha, espacamento, caixa=None):
    dados = {
        'typography_typography': 'custom',
        'typography_font_family': familia,
        'typography_font_weight': peso,
        'typography_font_size': {'unit': 'px', 'size': tamanho, 'sizes': []},
        'typography_line_height': {'unit': 'em', 'size': entrelinha, 'sizes': []},
        'typography_letter_spacing': {'unit': 'em', 'size': espacamento, 'sizes': []},
    }
    if caixa:
        dados['typography_text_transform'] = caixa
    return dados


def dimensoes(top=0, right=0, bottom=0, left=0, unidade='px'):
    return {
        'unit': unidade,
        'top': str(top), 'right': str(right), 'bottom': str(bottom), 'left': str(left),
        'isLinked': top == right == bottom == left,
    }


def medida(tamanho, unidade='px'):
    return {'unit': unidade, 'size': tamanho, 'sizes': []}


def lacuna(row=20, column=20, unidade='px'):
    """Controle de Gaps do container. O campo "size" vem do export real do
    Elementor (tests/elements-regression/tests/templates/container_flexbox.json)."""
    return {'row': str(row), 'column': str(column), 'isLinked': row == column,
            'unit': unidade, 'size': row if row == column else ''}


# --------------------------------------------------------------------------
# 2. ESTRUTURA
# --------------------------------------------------------------------------

class Documento:
    """Um arquivo JSON do Elementor."""

    def __init__(self, titulo, tipo, page_settings=None):
        self.titulo = titulo
        self.tipo = tipo
        self.page_settings = page_settings if page_settings is not None else []
        self.content = []
        self._usados = set()

    def id(self, caminho):
        """Id de 7 caracteres, estavel (o mesmo caminho gera sempre o mesmo id)."""
        base = hashlib.md5(f'{self.titulo}/{caminho}'.encode('utf-8')).hexdigest()
        for corte in range(0, 20):
            candidato = base[corte:corte + 7]
            if len(candidato) == 7 and candidato not in self._usados:
                self._usados.add(candidato)
                return candidato
        raise RuntimeError('sem id livre para ' + caminho)

    def container(self, nome, settings=None, elementos=None, caminho=None, interno=False):
        caminho = caminho or nome
        s = dict(settings or {})
        s['_title'] = nome
        return {
            'id': self.id(caminho),
            'elType': 'container',
            'settings': s,
            'elements': elementos or [],
            'isInner': bool(interno),
        }

    def item(self, campos, caminho):
        """Uma linha de campo repetidor (icon_list, form_fields): leva _id proprio."""
        linha = dict(campos)
        linha['_id'] = self.id('item/' + caminho)
        return linha

    def widget(self, tipo, settings=None, caminho=None):
        return {
            'id': self.id(caminho or tipo),
            'elType': 'widget',
            'widgetType': tipo,
            'settings': dict(settings or {}),
            'elements': [],
        }

    def dados(self):
        return {
            'content': self.content,
            'page_settings': self.page_settings,
            'version': VERSAO_FORMATO,
            'title': self.titulo,
            'type': self.tipo,
        }


def juntar_globais(settings, globais):
    """Junta referencias de estilo ao bloco __globals__ do Elementor."""
    s = dict(settings or {})
    if globais:
        s.setdefault('__globals__', {}).update(globais)
    return s


# --------------------------------------------------------------------------
# 3. PARTES DO SITE
# --------------------------------------------------------------------------

LINKS_MENU = [
    ('Início', '/'),
    ('Loja', '/loja/'),
    ('Coleção', '/colecao/'),
    ('Sobre', '/sobre/'),
    ('Contato', '/contato/'),
]

PAGINAS = {
    'home': '/',
    'loja': '/loja/',
    'colecao': '/colecao/',
    'conta': '/minha-conta/',
    'desejos': '/lista-de-desejos/',
    'sacola': '/sacola/',
    'guia': '/guia-de-medidas/',
    'trocas': '/trocas-e-devolucoes/',
    'envio': '/envio-e-entrega/',
    'privacidade': '/politica-de-privacidade/',
    'termos': '/termos-de-uso/',
    'cookies': '/politica-de-cookies/',
    'sobre': '/sobre/',
    'contato': '/contato/',
}


def cabecalho():
    """01. Cabecalho do site: faixa de aviso, marca, menu e acoes."""
    d = Documento('Cabeçalho do site', 'header')

    # --- faixa de aviso
    aviso_texto = (
        'Frete grátis acima de R$ 299 · <a href="' + PAGINAS['sobre'] + '">Compra consciente</a>'
        ' · <a href="' + PAGINAS['envio'] + '">Envio para todo o Brasil</a>'
    )
    aviso = d.widget('text-editor', juntar_globais({
        'editor': '<p>' + aviso_texto + '</p>',
        'align': 'center',
    }, {'text_color': cor('iara-faixa-texto'), 'typography': fonte('iara-texto-micro')}),
        caminho='faixa/aviso')

    faixa = d.container('Faixa de aviso', {
        'content_width': 'full',
        'flex_direction': 'row',
        'flex_justify_content': 'center',
        'flex_align_items': 'center',
        'flex_gap': lacuna(8, 8),
        'padding': dimensoes(10, 20, 10, 20),
        'background_background': 'classic',
        '__globals__': {'background_color': cor('secondary')},
    }, [aviso], caminho='faixa')

    # --- barra principal
    marca = d.container('Marca', {
        'flex_direction': 'row',
        'flex_align_items': 'center',
        'flex_gap': lacuna(12, 12),
        '_flex_size': 'grow',
        '_flex_align_self': 'center',
    }, [
        d.widget('theme-site-logo', {'_title': 'Logo'}, caminho='barra/logo'),
    ], caminho='barra/marca', interno=True)

    navegacao = d.container('Navegação principal', {
        'flex_direction': 'row',
        'flex_align_items': 'center',
        'flex_justify_content': 'center',
        'flex_gap': lacuna(28, 28),
    }, [
        d.widget('nav-menu', {
            '_title': 'Menu principal',
            'menu': 'principal',
            'layout': 'horizontal',
        }, caminho='barra/menu'),
    ], caminho='barra/navegacao', interno=True)

    acoes = d.container('Ações', {
        'flex_direction': 'row',
        'flex_justify_content': 'flex-end',
        'flex_align_items': 'center',
        'flex_gap': lacuna(14, 14),
        '_flex_size': 'grow',
        '_flex_align_self': 'center',
    }, [
        d.widget('search-form', {'_title': 'Busca', 'skin': 'minimal',
                                 'placeholder': 'O que você procura?'},
                 caminho='barra/busca'),
        d.widget('icon', {
            '_title': 'Minha conta',
            'selected_icon': {'value': 'fas fa-user', 'library': 'fa-solid'},
            'link': {'url': PAGINAS['conta'], 'is_external': '', 'nofollow': ''},
            'size': medida(21),
        }, caminho='barra/conta'),
        d.widget('icon', {
            '_title': 'Lista de desejos',
            'selected_icon': {'value': 'fas fa-heart', 'library': 'fa-solid'},
            'link': {'url': PAGINAS['desejos'], 'is_external': '', 'nofollow': ''},
            'size': medida(21),
        }, caminho='barra/desejos'),
        d.widget('woocommerce-menu-cart', {'_title': 'Sacola'}, caminho='barra/sacola'),
    ], caminho='barra/acoes', interno=True)

    linha = d.container('Linha do cabeçalho', {
        'content_width': 'boxed',
        'flex_direction': 'row',
        'flex_align_items': 'center',
        'flex_justify_content': 'space-between',
        'flex_gap': lacuna(24, 24),
    }, [marca, navegacao, acoes], caminho='barra/linha', interno=True)

    barra = d.container('Barra do cabeçalho', {
        'content_width': 'full',
        'flex_direction': 'column',
        'padding': dimensoes(16, 0, 16, 0),
        'background_background': 'classic',
        'border_border': 'solid',
        'border_width': {'unit': 'px', 'top': '0', 'right': '0', 'bottom': '1', 'left': '0', 'isLinked': False},
        '__globals__': {'background_color': cor('iara-papel'), 'border_color': cor('iara-fio')},
    }, [linha], caminho='barra')

    raiz = d.container('Cabeçalho', {
        'content_width': 'full',
        'flex_direction': 'column',
        'flex_gap': lacuna(0, 0),
        'padding': dimensoes(0, 0, 0, 0),
    }, [faixa, barra], caminho='raiz')

    d.content = [raiz]
    return d


def rodape():
    """02. Rodape do site: newsletter, colunas, seguranca e base."""
    d = Documento('Rodapé do site', 'footer')

    # --- newsletter
    texto_news = d.container('Convite da newsletter', {
        'flex_direction': 'column',
        'flex_gap': lacuna(8, 8),
    }, [
        d.widget('heading', juntar_globais({
            '_title': 'Rótulo',
            'title': 'Newsletter',
            'header_size': 'p',
        }, {'title_color': cor('iara-texto-discreto'), 'typography': fonte('iara-rotulo')}),
            caminho='news/rotulo'),
        d.widget('text-editor', juntar_globais({
            'editor': '<p>Cartas do ateliê: lançamentos, guia de medidas e cuidados com o linho.</p>',
        }, {'text_color': cor('iara-texto-suave'), 'typography': fonte('text')}),
            caminho='news/texto'),
    ], caminho='news/texto', interno=True)

    formulario = d.widget('form', {
        '_title': 'Assinar a newsletter',
        'form_name': 'Newsletter do rodapé',
        'form_fields': [
            d.item({
                'custom_id': 'email',
                'field_type': 'email',
                'field_label': 'Seu e-mail',
                'placeholder': 'seu@email.com',
                'required': 'true',
                'width': '100',
            }, 'news/campo-email'),
        ],
        'button_text': 'Assinar',
        'button_size': 'sm',
        'email_to': '[CONFERIR: e-mail de destino]',
        'form_id': 'newsletter',
    }, caminho='news/formulario')

    newsletter = d.container('Newsletter', {
        'flex_direction': 'row',
        'flex_wrap': 'wrap',
        'flex_justify_content': 'space-between',
        'flex_align_items': 'center',
        'flex_gap': lacuna(24, 24),
        'padding': dimensoes(0, 0, 28, 0),
        'border_border': 'solid',
        'border_width': {'unit': 'px', 'top': '0', 'right': '0', 'bottom': '1', 'left': '0', 'isLinked': False},
        '__globals__': {'border_color': cor('iara-fio')},
    }, [texto_news, formulario], caminho='news', interno=True)

    # --- colunas
    col_marca = d.container('Coluna da marca', {
        'flex_direction': 'column',
        'flex_gap': lacuna(10, 10),
        '_flex_size': 'custom',
        '_flex_basis_type': 'custom',
        '_flex_basis': medida(25, '%'),
    }, [
        d.widget('heading', juntar_globais({
            '_title': 'Iara Costa',
            'title': 'IARA COSTA',
            'header_size': 'p',
        }, {'title_color': cor('text'), 'typography': fonte('primary')}), caminho='colunas/marca/marca'),
        d.widget('heading', juntar_globais({
            '_title': 'Moda e acessórios',
            'title': 'Moda & Acessórios',
            'header_size': 'p',
        }, {'title_color': cor('iara-texto-discreto'), 'typography': fonte('iara-assinatura')}),
            caminho='colunas/marca/assinatura'),
        d.widget('text-editor', juntar_globais({
            'editor': ('<p>Vestuário feminino autoral em linho, algodão egípcio e viscose de alta '
                       'gramatura. Modelagem, corte e confecção próprios, no ateliê em Cerquilho (SP).</p>'),
        }, {'text_color': cor('iara-texto-suave'), 'typography': fonte('text')}),
            caminho='colunas/marca/sobre'),
    ], caminho='colunas/marca', interno=True)

    def coluna_links(nome, itens, caminho):
        lista = d.widget('icon-list', {
            '_title': nome,
            'icon_list': [
                d.item({'text': texto, 'link': {'url': url, 'is_external': '', 'nofollow': ''}},
                       caminho + '/' + str(indice))
                for indice, (texto, url) in enumerate(itens)
            ],
            'space_between': medida(10),
            '__globals__': {'text_color': cor('iara-texto-suave')},
        }, caminho=caminho + '/lista')
        titulo = d.widget('heading', juntar_globais({
            'title': nome, 'header_size': 'p', '_title': nome,
        }, {'title_color': cor('text'), 'typography': fonte('iara-texto-micro')}),
            caminho=caminho + '/titulo')
        return d.container(nome, {
            'flex_direction': 'column',
            'flex_gap': lacuna(14, 14),
            '_flex_size': 'custom',
            '_flex_basis_type': 'custom',
            '_flex_basis': medida(21, '%'),
        }, [titulo, lista], caminho=caminho, interno=True)

    col_inst = coluna_links('Institucional', [
        ('Sobre a marca', PAGINAS['sobre']),
        ('Coleção Terra & Linho', PAGINAS['colecao']),
        ('Guia de medidas', PAGINAS['guia']),
        ('Trocas e devoluções', PAGINAS['trocas']),
        ('Contato', PAGINAS['contato']),
    ], 'colunas/institucional')

    col_cat = coluna_links('Categorias', [
        ('Vestidos', PAGINAS['loja']),
        ('Blusas & Camisas', PAGINAS['loja']),
        ('Saias & Calças', PAGINAS['loja']),
        ('Acessórios', PAGINAS['loja']),
        ('Ver tudo', PAGINAS['loja']),
    ], 'colunas/categorias')

    col_atend = d.container('Atendimento', {
        'flex_direction': 'column',
        'flex_gap': lacuna(14, 14),
        '_flex_size': 'custom',
        '_flex_basis_type': 'custom',
        '_flex_basis': medida(24, '%'),
    }, [
        d.widget('heading', juntar_globais({
            'title': 'Atendimento', 'header_size': 'p', '_title': 'Atendimento',
        }, {'title_color': cor('text'), 'typography': fonte('iara-texto-micro')}),
            caminho='colunas/atendimento/titulo'),
        d.widget('icon-list', juntar_globais({
            '_title': 'Contatos',
            'icon_list': [
                d.item({'text': 'contato@iaracosta.com.br',
                        'link': {'url': 'mailto:contato@iaracosta.com.br', 'is_external': '', 'nofollow': ''}},
                       'colunas/atendimento/contatos/1'),
                d.item({'text': '(15) 99123-4567',
                        'link': {'url': 'https://wa.me/5515991234567', 'is_external': 'on', 'nofollow': ''}},
                       'colunas/atendimento/contatos/2'),
                d.item({'text': 'Segunda a sexta, das 9h às 18h'},
                       'colunas/atendimento/contatos/3'),
            ],
            'space_between': medida(10),
        }, {'text_color': cor('iara-texto-suave')}), caminho='colunas/atendimento/contatos'),
        d.widget('icon-list', juntar_globais({
            '_title': 'Redes sociais',
            'icon_list': [
                d.item({'text': 'Instagram', 'selected_icon': {'value': 'fab fa-instagram', 'library': 'fa-brands'},
                        'link': {'url': '[PREENCHER]', 'is_external': 'on', 'nofollow': ''}},
                       'colunas/atendimento/redes/1'),
                d.item({'text': 'Pinterest', 'selected_icon': {'value': 'fab fa-pinterest', 'library': 'fa-brands'},
                        'link': {'url': '[PREENCHER]', 'is_external': 'on', 'nofollow': ''}},
                       'colunas/atendimento/redes/2'),
                d.item({'text': 'WhatsApp', 'selected_icon': {'value': 'fab fa-whatsapp', 'library': 'fa-brands'},
                        'link': {'url': 'https://wa.me/5515991234567', 'is_external': 'on', 'nofollow': ''}},
                       'colunas/atendimento/redes/3'),
            ],
            'space_between': medida(10),
            'icon_size': medida(16),
        }, {'text_color': cor('iara-texto-suave')}), caminho='colunas/atendimento/redes'),
    ], caminho='colunas/atendimento', interno=True)

    colunas = d.container('Colunas do rodapé', {
        'content_width': 'full',
        'flex_direction': 'row',
        'flex_wrap': 'wrap',
        'flex_gap': lacuna(24, 24),
        'padding': dimensoes(40, 0, 40, 0),
    }, [col_marca, col_inst, col_cat, col_atend], caminho='colunas', interno=True)

    # --- seguranca e pagamento
    itens_seguranca = [
        ('Pix, cartão e boleto', 'Pix com 5% de desconto, cartão em até 6x sem juros e boleto pelo Mercado Pago.',
         'fas fa-credit-card', 'seg/1'),
        ('Ambiente protegido', 'Seus dados trafegam criptografados e não são compartilhados.',
         'fas fa-shield-alt', 'seg/2'),
        ('Pedido rastreado', 'Código de rastreio por e-mail assim que a peça é postada.',
         'fas fa-truck', 'seg/3'),
        ('7 dias para desistir', 'Direito de arrependimento previsto no CDC, Art. 49.',
         'fas fa-heart', 'seg/4'),
    ]
    caixas = []
    for titulo, texto, icone, caminho in itens_seguranca:
        caixas.append(d.container(titulo, {
            'content_width': 'full',
            'flex_direction': 'row',
            'flex_align_items': 'flex-start',
            'flex_gap': lacuna(12, 12),
            '_flex_size': 'custom',
            '_flex_basis_type': 'custom',
            '_flex_basis': medida(23, '%'),
        }, [
            d.widget('icon', juntar_globais({
                '_title': 'Ícone',
                'selected_icon': {'value': icone, 'library': 'fa-solid'},
                'size': medida(20),
            }, {'primary_color': cor('primary')}), caminho=caminho + '/icone'),
            d.container('Texto', {'flex_direction': 'column', 'flex_gap': lacuna(4, 4)}, [
                d.widget('heading', juntar_globais({
                    'title': titulo, 'header_size': 'p', '_title': titulo,
                }, {'title_color': cor('text'), 'typography': fonte('iara-texto-micro')}),
                    caminho=caminho + '/titulo'),
                d.widget('text-editor', juntar_globais({
                    'editor': '<p>' + texto + '</p>',
                }, {'text_color': cor('iara-texto-suave'), 'typography': fonte('text')}),
                    caminho=caminho + '/texto'),
            ], caminho=caminho + '/texto', interno=True),
        ], caminho=caminho, interno=True))

    pagamentos = d.container('Formas de pagamento', {
        'content_width': 'full',
        'flex_direction': 'column',
        'flex_gap': lacuna(12, 12),
        '_flex_size': 'custom',
        '_flex_basis_type': 'custom',
        '_flex_basis': medida(48, '%'),
    }, [
        d.widget('heading', juntar_globais({
            'title': 'Formas de pagamento', 'header_size': 'p', '_title': 'Formas de pagamento',
        }, {'title_color': cor('text'), 'typography': fonte('iara-texto-micro')}),
            caminho='seg/pag/titulo'),
        d.container('Quadros', {
            'content_width': 'full',
            'flex_direction': 'row',
            'flex_wrap': 'wrap',
            'flex_gap': lacuna(8, 8),
        }, [
            d.container(nome, {
                'flex_direction': 'row',
                'flex_align_items': 'center',
                'flex_justify_content': 'center',
                'padding': dimensoes(10, 16, 10, 16),
                'border_border': 'solid',
                'border_width': {'unit': 'px', 'top': '1', 'right': '1', 'bottom': '1', 'left': '1', 'isLinked': True},
                'border_radius': dimensoes(2, 2, 2, 2),
            }, [
                d.widget('text-editor', juntar_globais({
                    'editor': '<p>' + nome + '</p>',
                }, {'text_color': cor('text'), 'typography': fonte('iara-texto-micro')}),
                    caminho='seg/pag/' + nome + '/texto'),
            ], caminho='seg/pag/' + nome, interno=True)
            for nome in ('Mercado Pago', 'Pix', 'Cartão de crédito', 'Boleto bancário')
        ], caminho='seg/pag/quadros', interno=True),
    ], caminho='seg/pag', interno=True)

    selos = d.container('Selos de segurança', {
        'content_width': 'full',
        'flex_direction': 'column',
        'flex_gap': lacuna(12, 12),
        '_flex_size': 'custom',
        '_flex_basis_type': 'custom',
        '_flex_basis': medida(48, '%'),
    }, [
        d.widget('heading', juntar_globais({
            'title': 'Segurança', 'header_size': 'p', '_title': 'Segurança',
        }, {'title_color': cor('text'), 'typography': fonte('iara-texto-micro')}),
            caminho='seg/selos/titulo'),
        d.container('Distintivos', {
            'content_width': 'full',
            'flex_direction': 'row',
            'flex_wrap': 'wrap',
            'flex_gap': lacuna(8, 8),
        }, [
            d.container(nome, {
                'flex_direction': 'row',
                'flex_align_items': 'center',
                'flex_gap': lacuna(8, 8),
                'padding': dimensoes(10, 16, 10, 16),
                'border_border': 'solid',
                'border_width': {'unit': 'px', 'top': '1', 'right': '1', 'bottom': '1', 'left': '1', 'isLinked': True},
                'border_radius': dimensoes(2, 2, 2, 2),
            }, [
                d.widget('icon', juntar_globais({
                    'selected_icon': {'value': icone, 'library': 'fa-solid'},
                    'size': medida(18),
                    '_title': 'Ícone',
                }, {'primary_color': cor('primary')}), caminho='seg/selos/' + nome + '/icone'),
                d.container('Texto', {'flex_direction': 'column', 'flex_gap': lacuna(0, 0)}, [
                    d.widget('heading', juntar_globais({
                        'title': nome, 'header_size': 'p', '_title': nome,
                    }, {'title_color': cor('text'), 'typography': fonte('iara-texto-micro')}),
                        caminho='seg/selos/' + nome + '/titulo'),
                    d.widget('text-editor', juntar_globais({
                        'editor': '<p>' + sub + '</p>',
                    }, {'text_color': cor('iara-texto-discreto'), 'typography': fonte('iara-texto-micro')}),
                        caminho='seg/selos/' + nome + '/sub'),
                ], caminho='seg/selos/' + nome + '/texto', interno=True),
            ], caminho='seg/selos/' + nome, interno=True)
            for nome, sub, icone in (
                ('Site seguro', 'SSL 256 bits', 'fas fa-lock'),
                ('Navegação verificada', 'Sem páginas suspeitas', 'fas fa-shield-alt'),
            )
        ], caminho='seg/selos/distintivos', interno=True),
    ], caminho='seg/selos', interno=True)

    seguranca = d.container('Segurança e formas de pagamento', {
        'content_width': 'full',
        'flex_direction': 'column',
        'flex_gap': lacuna(20, 20),
        'padding': dimensoes(28, 0, 28, 0),
        'border_border': 'solid',
        'border_width': {'unit': 'px', 'top': '1', 'right': '0', 'bottom': '1', 'left': '0', 'isLinked': False},
        '__globals__': {'border_color': cor('iara-fio')},
    }, [
        d.container('Faixa de segurança', {
            'content_width': 'full',
            'flex_direction': 'row',
            'flex_wrap': 'wrap',
            'flex_gap': lacuna(20, 20),
        }, caixas, caminho='seg/faixa', interno=True),
        d.container('Pagamento e selos', {
            'content_width': 'full',
            'flex_direction': 'row',
            'flex_wrap': 'wrap',
            'flex_gap': lacuna(24, 24),
        }, [pagamentos, selos], caminho='seg/linha', interno=True),
    ], caminho='seg', interno=True)

    # --- base
    base = d.container('Base do rodapé', {
        'content_width': 'full',
        'flex_direction': 'row',
        'flex_wrap': 'wrap',
        'flex_justify_content': 'space-between',
        'flex_align_items': 'center',
        'flex_gap': lacuna(16, 16),
        'padding': dimensoes(20, 0, 20, 0),
    }, [
        d.widget('text-editor', juntar_globais({
            '_title': 'Direitos e identificação',
            'editor': ('<p>© 2026 Iara Costa. Todos os direitos reservados.</p>'
                       '<p>Iara Costa Moda Feminina LTDA · CNPJ 12.345.678/0001-90 · '
                       'Rua das Flores, nº 140, Sala 02, Centro, Cerquilho - SP, CEP 18520-000</p>'),
        }, {'text_color': cor('iara-texto-discreto'), 'typography': fonte('iara-texto-micro')}),
            caminho='base/direitos'),
        d.widget('icon-list', juntar_globais({
            '_title': 'Links de política',
            'icon_list': [
                d.item({'text': 'Política de privacidade',
                        'link': {'url': PAGINAS['privacidade'], 'is_external': '', 'nofollow': ''}},
                       'base/links/1'),
                d.item({'text': 'Termos de uso',
                        'link': {'url': PAGINAS['termos'], 'is_external': '', 'nofollow': ''}},
                       'base/links/2'),
                d.item({'text': 'Trocas e devoluções',
                        'link': {'url': PAGINAS['trocas'], 'is_external': '', 'nofollow': ''}},
                       'base/links/3'),
                d.item({'text': 'Cookies',
                        'link': {'url': PAGINAS['cookies'], 'is_external': '', 'nofollow': ''}},
                       'base/links/4'),
            ],
            'space_between': medida(10),
        }, {'text_color': cor('iara-texto-discreto')}), caminho='base/links'),
    ], caminho='base', interno=True)

    miolo = d.container('Conteúdo do rodapé', {
        'content_width': 'boxed',
        'flex_direction': 'column',
        'flex_gap': lacuna(0, 0),
    }, [newsletter, colunas, seguranca, base], caminho='miolo', interno=True)

    raiz = d.container('Rodapé', {
        'content_width': 'full',
        'flex_direction': 'column',
        'flex_gap': lacuna(0, 0),
        'padding': dimensoes(0, 0, 0, 0),
        'background_background': 'classic',
        '__globals__': {'background_color': cor('iara-branco')},
    }, [miolo], caminho='raiz')

    d.content = [raiz]
    return d


# --------------------------------------------------------------------------
# 4. ARQUIVOS GLOBAIS (Site Settings)
# --------------------------------------------------------------------------

def site_settings():
    """Cores e fontes globais, no formato do site-settings.json do Elementor."""
    return {
        'content': [],
        'settings': {
            'system_colors': CORES_SISTEMA,
            'custom_colors': [
                {'_id': apelido, 'title': titulo, 'color': valor}
                for apelido, titulo, valor in CORES_CUSTOM
            ],
            'system_typography': [
                dict({'_id': apelido, 'title': titulo},
                     **tipografia(familia, peso, tamanho, entrelinha, espacamento, caixa))
                for apelido, titulo, familia, peso, tamanho, entrelinha, espacamento, caixa in FONTES_SISTEMA
            ],
            'custom_typography': [
                dict({'_id': apelido, 'title': titulo},
                     **tipografia(familia, peso, tamanho, entrelinha, espacamento, caixa))
                for apelido, titulo, familia, peso, tamanho, entrelinha, espacamento, caixa in FONTES_CUSTOM
            ],
            'container_width': {'unit': 'px', 'size': 1688, 'sizes': []},
            'space_between_widgets': {'row': '20', 'column': '20', 'unit': 'px', 'isLinked': True},
            'body_background_background': 'classic',
            'body_background_color': '#fffdf9',
            'default_generic_fonts': 'Sans-serif',
            'site_name': 'Iara Costa',
            'site_description': 'Moda feminina e acessórios',
        },
    }


def escrever(caminho, dados):
    caminho.parent.mkdir(parents=True, exist_ok=True)
    texto = json.dumps(dados, ensure_ascii=False, indent=2) + '\n'
    caminho.write_text(texto, encoding='utf-8')
    return len(texto)


# --------------------------------------------------------------------------
# 5. PROGRAMA
# --------------------------------------------------------------------------

FABRICAS = [
    ('01-cabecalho.json', cabecalho),
    ('02-rodape.json', rodape),
]


def main():
    ap = argparse.ArgumentParser(description='Gera os JSONs do Bloco B.')
    ap.add_argument('--lista', action='store_true', help='so lista o que seria gerado')
    args = ap.parse_args()

    total = 0
    for nome, fabrica in FABRICAS:
        doc = fabrica()
        dados = doc.dados()
        if args.lista:
            print(f'  {nome:24s} {doc.titulo:24s} tipo={doc.tipo:14s} {len(json.dumps(dados))} bytes')
        else:
            tamanho = escrever(PASTA_JSON / nome, dados)
            total += tamanho
            print(f'  ok  {nome:24s} {doc.titulo:24s} {tamanho} bytes')
    if not args.lista:
        tamanho = escrever(PASTA_GLOBAIS / 'cores-e-fontes.json', site_settings())
        print(f'  ok  globais/cores-e-fontes.json   {len(CORES_SISTEMA) + len(CORES_CUSTOM)} cores, '
              f'{len(FONTES_SISTEMA) + len(FONTES_CUSTOM)} fontes, {tamanho} bytes')
        print(f'arquivos gerados em {PASTA_BLOCO_B.relative_to(RAIZ)}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
