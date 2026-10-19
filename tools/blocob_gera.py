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
    'checkout': '/finalizar-compra/',
    'pedido': '/pedido-recebido/',
    'guia': '/guia-de-medidas/',
    'trocas': '/trocas-e-devolucoes/',
    'envio': '/envio-e-entrega/',
    'privacidade': '/politica-de-privacidade/',
    'termos': '/termos-de-uso/',
    'cookies': '/politica-de-cookies/',
    'sobre': '/sobre/',
    'contato': '/contato/',
    'blog': '/diario/',
    'faq': '/perguntas-frequentes/',
    'guia-medidas': '/guia-de-medidas/',
    'post': '/diario/',
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
    }, {'text_color': cor('iara-faixa-texto'), 'link_color': cor('iara-faixa-texto'),
        'typography': fonte('iara-texto-micro')}),
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
        'flex_direction': 'column',
        'flex_gap': lacuna(2, 2),
        '_flex_size': 'grow',
        '_flex_align_self': 'center',
    }, [
        d.widget('heading', juntar_globais({
            '_title': 'IARA COSTA',
            'title': 'IARA COSTA',
            'header_size': 'p',
            'link': {'url': PAGINAS['home'], 'is_external': '', 'nofollow': ''},
        }, {'title_color': cor('text'), 'typography': fonte('primary')}), caminho='barra/marca-nome'),
        d.widget('heading', juntar_globais({
            '_title': 'Moda e acessorios',
            'title': 'Moda & Acessórios',
            'header_size': 'p',
        }, {'title_color': cor('iara-texto-discreto'), 'typography': fonte('iara-assinatura')}),
            caminho='barra/marca-tagline'),
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
# 3.1 PAGINAS DE CONTEUDO
# --------------------------------------------------------------------------

def rotulo(d, texto, caminho, cor_apelido='iara-texto-discreto'):
    return d.widget('heading', juntar_globais({
        '_title': texto,
        'title': texto,
        'header_size': 'p',
    }, {'title_color': cor(cor_apelido), 'typography': fonte('iara-rotulo')}), caminho=caminho)


def titulo_secao(d, texto, caminho, nivel='h2'):
    return d.widget('heading', juntar_globais({
        '_title': texto,
        'title': texto,
        'header_size': nivel,
    }, {'title_color': cor('text'), 'typography': fonte('secondary')}), caminho=caminho)


def paragrafo(d, texto, caminho, fonte_apelido='text', cor_apelido='iara-texto-suave'):
    globais = {'text_color': cor(cor_apelido), 'typography': fonte(fonte_apelido)}
    if '<a ' in texto:
        # o Elementor tem controle proprio de cor de link; sem ele, o link
        # herda a cor padrao do tema (foi o rosa da primeira importacao)
        globais['link_color'] = cor(cor_apelido)
    return d.widget('text-editor', juntar_globais({
        'editor': '<p>' + texto + '</p>',
    }, globais), caminho=caminho)


def botao(d, texto, url, caminho, estilo='primary'):
    globais = {'typography': fonte('accent')}
    if estilo == 'primary':
        globais['button_background_color'] = cor('primary')
        globais['text_color'] = cor('iara-branco')
    else:
        globais['text_color'] = cor('text')
    return d.widget('button', juntar_globais({
        '_title': texto,
        'text': texto,
        'link': {'url': url, 'is_external': '', 'nofollow': ''},
        'size': 'md',
    }, globais), caminho=caminho)


def cabecalho_secao(d, rotulo_texto, titulo, caminho, link_texto=None, link_url=None):
    esquerda = d.container('Titulo da secao', {
        'flex_direction': 'column',
        'flex_gap': lacuna(8, 8),
        '_flex_size': 'grow',
    }, [
        rotulo(d, rotulo_texto, caminho + '/rotulo'),
        titulo_secao(d, titulo, caminho + '/titulo'),
    ], caminho=caminho + '/esquerda', interno=True)
    filhos = [esquerda]
    if link_texto:
        filhos.append(d.container('Link da secao', {
            'flex_direction': 'row',
            'flex_align_items': 'flex-end',
            '_flex_align_self': 'center',
        }, [
            d.widget('button', juntar_globais({
                '_title': link_texto,
                'text': link_texto,
                'link': {'url': link_url, 'is_external': '', 'nofollow': ''},
                'size': 'sm',
                'button_type': 'text',
            }, {'text_color': cor('primary'), 'typography': fonte('iara-rotulo')}),
                caminho=caminho + '/link'),
        ], caminho=caminho + '/direita', interno=True))
    return d.container('Cabecalho da secao', {
        'content_width': 'full',
        'flex_direction': 'row',
        'flex_wrap': 'wrap',
        'flex_justify_content': 'space-between',
        'flex_align_items': 'flex-end',
        'flex_gap': lacuna(16, 16),
        'padding': dimensoes(0, 0, 24, 0),
    }, filhos, caminho=caminho, interno=True)


def cartao_imagem(d, titulo, descricao, caminho, url):
    """Cartao de categoria/ocasiao: imagem, titulo e texto, tudo clicavel."""
    return d.widget('image-box', juntar_globais({
        '_title': titulo,
        'title_text': titulo,
        'description_text': descricao,
        'link': {'url': url, 'is_external': '', 'nofollow': ''},
        'image_size': 'large',
        'title_tag': 'h3',
    }, {
        'title_color': cor('text'),
        'description_color': cor('iara-texto-suave'),
        'typography_title': fonte('iara-titulo-h3'),
        'typography_description': fonte('text'),
    }), caminho=caminho)


def home():
    """03. Página inicial: hero, beneficios, categorias, destaques, ocasiões,
    editorial, colecao, depoimentos, diário e perguntas frequentes."""
    d = Documento('Página inicial', 'page')

    # --- hero
    hero_texto = d.container('Texto do hero', {
        'flex_direction': 'column',
        'flex_gap': lacuna(20, 20),
        '_flex_size': 'custom',
        '_flex_basis_type': 'custom',
        '_flex_basis': medida(52, '%'),
        '_flex_align_self': 'center',
    }, [
        rotulo(d, 'Coleção Terra & Linho', 'hero/rotulo', 'primary'),
        d.widget('heading', juntar_globais({
            '_title': 'Vestir o barro, habitar a natureza',
            'title': 'Vestir o barro, habitar a natureza',
            'header_size': 'h1',
        }, {'title_color': cor('text'), 'typography': fonte('primary')}), caminho='hero/titulo'),
        paragrafo(d, ('Vestuário feminino autoral em linho, algodão egípcio e viscose de alta '
                      'gramatura. Modelagem, corte e confecção próprios, no ateliê em '
                      'Cerquilho, no interior de São Paulo.'), 'hero/intro'),
        d.container('Botões do hero', {
            'content_width': 'full',
            'flex_direction': 'row',
            'flex_wrap': 'wrap',
            'flex_gap': lacuna(12, 12),
        }, [
            botao(d, 'Ver a colecao', PAGINAS['loja'], 'hero/botao-loja'),
            botao(d, 'Nossa historia', PAGINAS['sobre'], 'hero/botao-sobre', 'outline'),
        ], caminho='hero/botoes', interno=True),
        d.widget('icon-list', juntar_globais({
            '_title': 'Resumo do hero',
            'icon_list': [
                d.item({'text': 'Vestidos, blusas e saias'}, 'hero/meta/1'),
                d.item({'text': 'Do P ao GG'}, 'hero/meta/2'),
                d.item({'text': 'Troca fácil em 30 dias'}, 'hero/meta/3'),
            ],
            'space_between': medida(8),
        }, {'text_color': cor('iara-texto-discreto'), 'typography': fonte('iara-texto-micro')}),
            caminho='hero/meta'),
    ], caminho='hero/texto', interno=True)

    hero_midia = d.container('Foto do hero', {
        'flex_direction': 'column',
        'flex_gap': lacuna(8, 8),
        '_flex_size': 'custom',
        '_flex_basis_type': 'custom',
        '_flex_basis': medida(44, '%'),
    }, [
        d.widget('image', {
            '_title': 'Foto principal (escolher no editor)',
            'image': {'url': '', 'id': ''},
            'image_size': 'full',
            'caption_source': 'none',
            'link_to': 'none',
        }, caminho='hero/foto'),
        # Legenda sobre a foto no prototipo. Aqui ela entra abaixo da imagem,
        # porque sobrepor texto à imagem sem CSS livre não é confiável.
        paragrafo(d, ('01 · Blusa de Linho Terracota, tingida com argila do Vale do Paraíba. '
                      'Legenda da foto: conferir posição no editor.'), 'hero/legenda',
                  'iara-texto-micro', 'iara-numeral'),
    ], caminho='hero/midia', interno=True)

    hero = d.container('Hero', {
        'content_width': 'boxed',
        'flex_direction': 'row',
        'flex_wrap': 'wrap',
        'flex_align_items': 'center',
        'flex_gap': lacuna(40, 40),
        'padding': dimensoes(56, 0, 56, 0),
    }, [hero_texto, hero_midia], caminho='hero', interno=True)

    # --- beneficios
    beneficios_itens = [
        ('Frete grátis acima de R$ 299', 'Para todo o Brasil, com rastreio.', 'fas fa-truck'),
        ('Troca fácil em 30 dias', 'Primeira troca com frete nosso, pelo código de postagem dos Correios.', 'fas fa-shield-alt'),
        ('5% off no Pix e 6x sem juros', 'No cartão, em até 6x; boleto também aceito.', 'fas fa-credit-card'),
        ('Do P ao GG', 'Guia de medidas por peça, na página de cada produto.', 'fas fa-ruler'),
    ]
    beneficios = d.container('Faixa de beneficios', {
        'content_width': 'boxed',
        'flex_direction': 'row',
        'flex_wrap': 'wrap',
        'flex_gap': lacuna(20, 20),
        'padding': dimensoes(24, 0, 24, 0),
        'border_border': 'solid',
        'border_width': {'unit': 'px', 'top': '1', 'right': '0', 'bottom': '1', 'left': '0', 'isLinked': False},
        '__globals__': {'border_color': cor('iara-fio')},
    }, [
        d.container(titulo, {
            'flex_direction': 'column',
            '_flex_size': 'custom',
            '_flex_basis_type': 'custom',
            '_flex_basis': medida(23, '%'),
        }, [
            d.widget('icon-box', juntar_globais({
                '_title': titulo,
                'selected_icon': {'value': icone, 'library': 'fa-solid'},
                'title_text': titulo,
                'description_text': texto,
                'position': 'top',
                'title_tag': 'p',
            }, {
                'primary_color': cor('primary'),
                'title_color': cor('text'),
                'description_color': cor('iara-texto-suave'),
                'typography_title': fonte('iara-titulo-h3'),
                'typography_description': fonte('text'),
            }), caminho='beneficios/' + str(i)),
        ], caminho='beneficios/caixa-' + str(i), interno=True)
        for i, (titulo, texto, icone) in enumerate(beneficios_itens, 1)
    ], caminho='beneficios', interno=True)

    # --- categorias
    categorias = d.container('Categorias', {
        'content_width': 'boxed',
        'flex_direction': 'column',
        'flex_gap': lacuna(0, 0),
        'padding': dimensoes(56, 0, 56, 0),
    }, [
        cabecalho_secao(d, 'Navegue por', 'Categorias', 'categorias/cabecalho',
                        'Ver tudo', PAGINAS['loja']),
        d.container('Grade de categorias', {
            'content_width': 'full',
            'flex_direction': 'row',
            'flex_wrap': 'wrap',
            'flex_gap': lacuna(20, 20),
        }, [
            d.container(titulo, {
                'flex_direction': 'column',
                '_flex_size': 'custom',
                '_flex_basis_type': 'custom',
                '_flex_basis': medida(23, '%'),
            }, [cartao_imagem(d, titulo, texto, 'categorias/' + slug, PAGINAS['loja'])],
                caminho='categorias/caixa-' + slug, interno=True)
            for titulo, texto, slug in [
                ('Vestidos', 'Midi, longos e curtos, do P ao GG.', 'vestidos'),
                ('Blusas & Camisas', 'Linho lavado, cropped e tricô de algodão.', 'blusas'),
                ('Saias & Calças', 'Cintura alta, pregas e alfaiataria leve.', 'saias-calcas'),
                ('Acessórios', 'Cerâmica, argila e fibras naturais.', 'acessorios'),
            ]
        ], caminho='categorias/grade', interno=True),
    ], caminho='categorias', interno=True)

    # --- em destaque (produtos reais do WooCommerce)
    destaques = d.container('Em destaque', {
        'content_width': 'boxed',
        'flex_direction': 'column',
        'flex_gap': lacuna(0, 0),
        'padding': dimensoes(56, 0, 56, 0),
        'background_background': 'classic',
        '__globals__': {'background_color': cor('iara-fundo-suave')},
    }, [
        cabecalho_secao(d, 'Seleção da semana', 'Em destaque', 'destaques/cabecalho',
                        'Ver a loja', PAGINAS['loja']),
        d.widget('woocommerce-products', {
            '_title': 'Produtos em destaque (configurar no editor)',
            'columns': '4',
            'rows': '1',
            'paginate': 'no',
            'orderby': 'menu_order',
            'order': 'ASC',
        }, caminho='destaques/produtos'),
        paragrafo(d, ('Bloco dinâmico: no editor, escolher a fonte de produtos '
                      '"Em destaque" e 4 colunas. Nada de produto escrito à mão aqui.'),
                  'destaques/nota', 'iara-texto-micro'),
    ], caminho='destaques', interno=True)

    # --- ocasiões
    ocasiões = d.container('Compre por ocasião', {
        'content_width': 'boxed',
        'flex_direction': 'column',
        'flex_gap': lacuna(0, 0),
        'padding': dimensoes(56, 0, 56, 0),
    }, [
        cabecalho_secao(d, 'Para cada momento', 'Compre por ocasião', 'ocasiões/cabecalho',
                        'Ver tudo', PAGINAS['loja']),
        d.container('Grade de ocasiões', {
            'content_width': 'full',
            'flex_direction': 'row',
            'flex_wrap': 'wrap',
            'flex_gap': lacuna(20, 20),
        }, [
            d.container(titulo, {
                'flex_direction': 'column',
                '_flex_size': 'custom',
                '_flex_basis_type': 'custom',
                '_flex_basis': medida(23, '%'),
            }, [cartao_imagem(d, titulo, '', 'ocasiões/' + slug, PAGINAS['loja'])],
                caminho='ocasiões/caixa-' + slug, interno=True)
            for titulo, slug in [
                ('Dia a dia', 'dia-a-dia'), ('Trabalho', 'trabalho'),
                ('Festa', 'festa'), ('Acessórios', 'acessorios'),
            ]
        ], caminho='ocasiões/grade', interno=True),
    ], caminho='ocasiões', interno=True)

    # --- editorial
    editorial_itens = [
        ('01 · Modelagem autoral', 'Desenho, corte e confecção próprios, no ateliê em Cerquilho (SP).'),
        ('02 · Tecidos de alta gramatura', 'Linho, algodão egípcio e viscose escolhidos pela gramatura e pelo toque.'),
        ('03 · Compra tranquila', 'Troca em 30 dias, a primeira por nossa conta, e 7 dias para desistir da compra.'),
    ]
    editorial = d.container('Editorial do atelie', {
        'content_width': 'boxed',
        'flex_direction': 'row',
        'flex_wrap': 'wrap',
        'flex_gap': lacuna(40, 40),
        'padding': dimensoes(56, 0, 56, 0),
        'background_background': 'classic',
        '__globals__': {'background_color': cor('iara-terracota-claro')},
    }, [
        d.container('Foto do editorial', {
            'flex_direction': 'column',
            '_flex_size': 'custom',
            '_flex_basis_type': 'custom',
            '_flex_basis': medida(44, '%'),
        }, [
            d.widget('image', {
                '_title': 'Foto do ateliê (escolher no editor)',
                'image': {'url': '', 'id': ''},
                'image_size': 'full',
                'caption_source': 'none',
                'link_to': 'none',
            }, caminho='editorial/foto'),
        ], caminho='editorial/midia', interno=True),
        d.container('Texto do editorial', {
            'flex_direction': 'column',
            'flex_gap': lacuna(16, 16),
            '_flex_size': 'custom',
            '_flex_basis_type': 'custom',
            '_flex_basis': medida(52, '%'),
        }, [
            rotulo(d, 'Da terra à peça', 'editorial/rotulo', 'primary'),
            titulo_secao(d, 'Um ateliê, três gestos', 'editorial/titulo'),
            paragrafo(d, ('Três coisas sustentam cada peça: modelagem propria, tecidos escolhidos '
                          'pela gramatura e produção no Brasil.'), 'editorial/intro'),
            d.widget('icon-list', juntar_globais({
                '_title': 'Três gestos',
                'icon_list': [
                    d.item({'text': titulo + '. ' + texto}, 'editorial/itens/' + str(i))
                    for i, (titulo, texto) in enumerate(editorial_itens, 1)
                ],
                'space_between': medida(12),
            }, {'text_color': cor('iara-texto-suave'), 'typography': fonte('text')}),
                caminho='editorial/itens'),
            d.widget('button', juntar_globais({
                '_title': 'Conhecer o atelie',
                'text': 'Conhecer o atelie',
                'link': {'url': PAGINAS['sobre'], 'is_external': '', 'nofollow': ''},
                'size': 'sm',
                'button_type': 'text',
            }, {'text_color': cor('primary'), 'typography': fonte('iara-rotulo')}),
                caminho='editorial/botao'),
        ], caminho='editorial/texto', interno=True),
    ], caminho='editorial', interno=True)

    # --- colecao
    colecao = d.container('Coleção Terra e Linho', {
        'content_width': 'boxed',
        'flex_direction': 'row',
        'flex_wrap': 'wrap',
        'flex_gap': lacuna(40, 40),
        'padding': dimensoes(56, 0, 56, 0),
    }, [
        d.container('Foto da colecao', {
            'flex_direction': 'column',
            '_flex_size': 'custom',
            '_flex_basis_type': 'custom',
            '_flex_basis': medida(44, '%'),
        }, [
            d.widget('image', {
                '_title': 'Foto da colecao (escolher no editor)',
                'image': {'url': '', 'id': ''},
                'image_size': 'full',
                'caption_source': 'none',
                'link_to': 'none',
            }, caminho='colecao/foto'),
        ], caminho='colecao/midia', interno=True),
        d.container('Texto da colecao', {
            'flex_direction': 'column',
            'flex_gap': lacuna(16, 16),
            '_flex_size': 'custom',
            '_flex_basis_type': 'custom',
            '_flex_basis': medida(52, '%'),
            '_flex_align_self': 'center',
        }, [
            rotulo(d, 'Outono e Inverno 2026', 'colecao/rotulo', 'primary'),
            titulo_secao(d, 'Coleção Terra & Linho', 'colecao/titulo'),
            paragrafo(d, ('Três capítulos em doze peças: terracota do barro, sálvia da mata, cru do '
                          'linho. Veja o editorial completo e monte seus looks com as peças à venda.'),
                      'colecao/intro'),
            d.container('Botões da coleção', {
                'content_width': 'full',
                'flex_direction': 'row',
                'flex_wrap': 'wrap',
                'flex_gap': lacuna(12, 12),
            }, [
                botao(d, 'Ver o editorial', PAGINAS['colecao'], 'colecao/botao-editorial'),
                botao(d, 'Comprar a colecao', PAGINAS['loja'], 'colecao/botao-loja', 'outline'),
            ], caminho='colecao/botoes', interno=True),
        ], caminho='colecao/texto', interno=True),
    ], caminho='colecao', interno=True)

    # --- depoimentos (exemplos do prototipo: substituir pelos reais)
    depoimentos_textos = [
        'A blusa de linho é a peça que mais uso. O terracota não desbotou depois de um ano de lavagens.',
        'Comprei o vestido midi sálvia pelo guia de medidas e acertou. Caiu como se fosse feito para mim.',
        'Gosto de saber de onde vem o tecido. A etiqueta diz a origem da fibra, e isso faz diferença para mim.',
    ]
    depoimentos = d.container('Depoimentos', {
        'content_width': 'boxed',
        'flex_direction': 'column',
        'flex_gap': lacuna(0, 0),
        'padding': dimensoes(56, 0, 56, 0),
        'background_background': 'classic',
        '__globals__': {'background_color': cor('iara-fundo-suave')},
    }, [
        cabecalho_secao(d, 'Quem veste', 'Palavras de quem usa', 'depoimentos/cabecalho'),
        paragrafo(d, 'Depoimentos de exemplo no prototipo. Publicar apenas os reais.',
                  'depoimentos/nota', 'iara-texto-micro'),
        d.container('Grade de depoimentos', {
            'content_width': 'full',
            'flex_direction': 'row',
            'flex_wrap': 'wrap',
            'flex_gap': lacuna(20, 20),
        }, [
            d.container('Depoimento de exemplo ' + str(i), {
                'flex_direction': 'column',
                '_flex_size': 'custom',
                '_flex_basis_type': 'custom',
                '_flex_basis': medida(31, '%'),
            }, [
                d.widget('testimonial', juntar_globais({
                    '_title': 'Depoimento de exemplo ' + str(i) + ' (substituir)',
                    'testimonial_content': texto,
                    'testimonial_name': 'Exemplo, substituir',
                    'testimonial_job': '[PREENCHER: cidade e estado]',
                }, {'text_color': cor('iara-texto-suave'), 'typography': fonte('text')}),
                    caminho='depoimentos/' + str(i)),
            ], caminho='depoimentos/caixa-' + str(i), interno=True)
            for i, texto in enumerate(depoimentos_textos, 1)
        ], caminho='depoimentos/grade', interno=True),
    ], caminho='depoimentos', interno=True)

    # --- diário (posts recentes, dinamico)
    diário = d.container('Do diário', {
        'content_width': 'boxed',
        'flex_direction': 'column',
        'flex_gap': lacuna(0, 0),
        'padding': dimensoes(56, 0, 56, 0),
    }, [
        cabecalho_secao(d, 'Do diário', 'Cartas do ateliê', 'diário/cabecalho',
                        'Ver todos os textos', PAGINAS['blog']),
        d.widget('posts', {
            '_title': 'Posts recentes (configurar no editor)',
            'posts_per_page': '3',
            'columns': '3',
        }, caminho='diário/posts'),
        paragrafo(d, ('Bloco dinâmico de posts: no editor, escolher os 3 posts mais recentes. '
                      'Os textos do blog sao escritos no Gutenberg, nunca no Elementor.'),
                  'diário/nota', 'iara-texto-micro'),
    ], caminho='diário', interno=True)

    # --- perguntas frequentes
    perguntas = [
        ('Preciso criar conta para comprar?',
         'Nao. Voce pode comprar como visitante. Criar conta ajuda a acompanhar pedidos e guardar '
         'enderecos, mas e opcional e nao muda o preco nem o prazo.'),
        ('As peças vêm com a tabela de medidas?',
         'Sim, cada página de produto traz a tabela daquela peça. Meça uma peca que ja veste bem e '
         'compare com a tabela. O passo a passo está no Guia de Medidas. Na duvida entre dois '
         'tamanhos, fale com o atendimento.'),
        ('A peça não serviu. Posso trocar?',
         'Sim. Você tem 7 dias corridos, contando do recebimento, para desistir da compra sem precisar '
         'justificar, conforme o Art. 49 do Codigo de Defesa do Consumidor. Os prazos e as condicoes '
         'de troca estao em Trocas e devolucoes.'),
        ('Vocês entregam em todo o Brasil?',
         'Sim, enviamos para todo o território nacional. Antes de finalizar, confira o prazo calculado '
         'para o seu CEP.'),
        ('Como vocês tratam os meus dados?',
         'Usamos os seus dados para entregar o pedido, emitir nota fiscal e responder ao seu contato. '
         'O detalhamento esta na Politica de Privacidade.'),
    ]
    faq = d.container('Perguntas frequentes da home', {
        'content_width': 'boxed',
        'flex_direction': 'row',
        'flex_wrap': 'wrap',
        'flex_gap': lacuna(40, 40),
        'padding': dimensoes(56, 0, 56, 0),
        'background_background': 'classic',
        '__globals__': {'background_color': cor('secondary')},
    }, [
        d.container('Introdução das perguntas', {
            'flex_direction': 'column',
            'flex_gap': lacuna(16, 16),
            '_flex_size': 'custom',
            '_flex_basis_type': 'custom',
            '_flex_basis': medida(38, '%'),
        }, [
            rotulo(d, 'Perguntas frequentes', 'faq/rotulo', 'iara-terracota-claro'),
            d.widget('heading', juntar_globais({
                '_title': 'Dúvidas antes de escolher',
                'title': 'Dúvidas antes de escolher',
                'header_size': 'h2',
            }, {'title_color': cor('iara-faixa-texto'), 'typography': fonte('secondary')}),
                caminho='faq/titulo'),
            d.widget('text-editor', juntar_globais({
                'editor': '<p>As perguntas que mais chegam no ateliê, respondidas direto ao ponto.</p>',
            }, {'text_color': cor('iara-faixa-texto'), 'typography': fonte('text')}),
                caminho='faq/intro'),
            d.widget('button', juntar_globais({
                '_title': 'Ver todas as perguntas',
                'text': 'Ver todas as perguntas',
                'link': {'url': PAGINAS['faq'], 'is_external': '', 'nofollow': ''},
                'size': 'sm',
                'button_type': 'text',
            }, {'text_color': cor('iara-faixa-texto'), 'typography': fonte('iara-rotulo')}),
                caminho='faq/botao'),
        ], caminho='faq/intro', interno=True),
        d.container('Sanfona de perguntas', {
            'flex_direction': 'column',
            '_flex_size': 'custom',
            '_flex_basis_type': 'custom',
            '_flex_basis': medida(56, '%'),
        }, [
            d.widget('accordion', juntar_globais({
                '_title': 'Perguntas e respostas',
                'tabs': [
                    d.item({'tab_title': pergunta, 'tab_content': '<p>' + resposta + '</p>'},
                           'faq/item-' + str(i))
                    for i, (pergunta, resposta) in enumerate(perguntas, 1)
                ],
            }, {'text_color': cor('iara-faixa-texto'), 'typography': fonte('text')}),
                caminho='faq/sanfona'),
        ], caminho='faq/sanfona', interno=True),
    ], caminho='faq', interno=True)

    raiz = d.container('Página inicial', {
        'content_width': 'full',
        'flex_direction': 'column',
        'flex_gap': lacuna(0, 0),
        'padding': dimensoes(0, 0, 0, 0),
    }, [hero, beneficios, categorias, destaques, ocasiões, editorial, colecao,
        depoimentos, diário, faq], caminho='raiz')

    d.content = [raiz]
    return d



def faixa_ajuda(d, titulo, texto, botao_texto, url, caminho):
    """Faixa verde antes do rodape, igual a do prototipo."""
    return d.container('Faixa de ajuda', {
        'content_width': 'boxed',
        'flex_direction': 'column',
        'flex_align_items': 'center',
        'flex_gap': lacuna(16, 16),
        'padding': dimensoes(48, 0, 48, 0),
        'background_background': 'classic',
        '__globals__': {'background_color': cor('secondary')},
    }, [
        d.widget('heading', juntar_globais({
            '_title': titulo, 'title': titulo, 'header_size': 'h2', 'align': 'center',
        }, {'title_color': cor('iara-faixa-texto'), 'typography': fonte('secondary')}),
            caminho=caminho + '/titulo'),
        d.widget('text-editor', juntar_globais({
            'editor': '<p>' + texto + '</p>', 'align': 'center',
        }, {'text_color': cor('iara-faixa-texto'), 'typography': fonte('text')}),
            caminho=caminho + '/texto'),
        botao(d, botao_texto, url, caminho + '/botao'),
    ], caminho=caminho, interno=True)


def loja():
    """04. Arquivo da loja: cabecalho, filtros, grade de produtos e paginacao."""
    d = Documento('Arquivo da loja', 'archive')

    cabecalho_loja = d.container('Cabecalho da loja', {
        'content_width': 'boxed',
        'flex_direction': 'column',
        'flex_gap': lacuna(12, 12),
        'padding': dimensoes(40, 0, 8, 0),
    }, [
        d.widget('woocommerce-breadcrumbs', {'_title': 'Trilha de navegacao'},
                 caminho='loja/trilha'),
        d.widget('heading', juntar_globais({
            '_title': 'Todas as pecas', 'title': 'Todas as peças', 'header_size': 'h1',
        }, {'title_color': cor('text'), 'typography': fonte('primary')}),
            caminho='loja/titulo'),
        paragrafo(d, ('Vestuário feminino do P ao GG, em linho, algodão egípcio e viscose de alta '
                      'gramatura. A contagem de peças, a ordenação e a paginação vêm do próprio '
                      'WooCommerce, conforme os filtros escolhidos.'), 'loja/intro'),
        d.widget('button', juntar_globais({
            '_title': 'Guia de medidas', 'text': 'Guia de medidas',
            'link': {'url': PAGINAS['guia'], 'is_external': '', 'nofollow': ''},
            'size': 'sm', 'button_type': 'text',
        }, {'text_color': cor('primary'), 'typography': fonte('iara-rotulo')}),
            caminho='loja/guia'),
    ], caminho='loja/cabecalho', interno=True)

    def grupo_filtro(titulo, texto, caminho):
        return d.container(titulo, {
            'flex_direction': 'column', 'flex_gap': lacuna(8, 8),
            'padding': dimensoes(16, 0, 16, 0),
            'border_border': 'solid',
            'border_width': {'unit': 'px', 'top': '1', 'right': '0', 'bottom': '0', 'left': '0', 'isLinked': False},
            '__globals__': {'border_color': cor('iara-fio')},
        }, [
            d.widget('heading', juntar_globais({
                '_title': titulo, 'title': titulo, 'header_size': 'p',
            }, {'title_color': cor('text'), 'typography': fonte('iara-rotulo')}),
                caminho=caminho + '/titulo'),
            paragrafo(d, texto, caminho + '/texto', 'iara-texto-micro'),
        ], caminho=caminho, interno=True)

    filtros = d.container('Filtros da loja', {
        'flex_direction': 'column',
        'flex_gap': lacuna(0, 0),
        '_flex_size': 'custom', '_flex_basis_type': 'custom',
        '_flex_basis': medida(23, '%'),
    }, [
        d.widget('heading', juntar_globais({
            '_title': 'Filtros', 'title': 'Filtros', 'header_size': 'h2',
        }, {'title_color': cor('text'), 'typography': fonte('secondary')}),
            caminho='filtros/titulo'),
        d.container('Categorias', {
            'flex_direction': 'column', 'flex_gap': lacuna(8, 8),
            'padding': dimensoes(16, 0, 16, 0),
        }, [
            d.widget('heading', juntar_globais({
                '_title': 'Categorias', 'title': 'Categorias', 'header_size': 'p',
            }, {'title_color': cor('text'), 'typography': fonte('iara-rotulo')}),
                caminho='filtros/categorias/titulo'),
            d.widget('woocommerce-product-categories', {
                '_title': 'Categorias de produtos (dinamico)',
            }, caminho='filtros/categorias/lista'),
        ], caminho='filtros/categorias', interno=True),
        grupo_filtro('Faixa de preço',
                     '[CONFIGURAR NO EDITOR] Filtro de preço do WooCommerce, com os valores '
                     'mínimo e máximo do catálogo real.', 'filtros/preco'),
        grupo_filtro('Cor',
                     '[CONFIGURAR NO EDITOR] Filtro pelo atributo Cor cadastrado nos produtos '
                     '(terracota, sálvia, areia, cru e carvão).', 'filtros/cor'),
        grupo_filtro('Tamanho',
                     '[CONFIGURAR NO EDITOR] Filtro pelo atributo Tamanho cadastrado nos '
                     'produtos (P, M, G, GG e Único).', 'filtros/tamanho'),
        paragrafo(d, ('Os três filtros de atributo e de preço não foram travados neste arquivo '
                      'porque dependem dos atributos reais do catálogo. O guia de importação '
                      'traz as opções e o que precisa de aprovação.'), 'filtros/nota',
                  'iara-texto-micro'),
    ], caminho='filtros', interno=True)

    grade = d.container('Grade de produtos', {
        'flex_direction': 'column',
        'flex_gap': lacuna(16, 16),
        '_flex_size': 'grow',
    }, [
        paragrafo(d, ('Grade dinâmica do WooCommerce: 9 peças por página, com ordenação por '
                      'mais recentes, mais populares, menor preço, maior preço e melhor avaliados, '
                      'igual ao protótipo aprovado.'), 'grade/nota', 'iara-texto-micro'),
        d.widget('woocommerce-archive-products', {
            '_title': 'Produtos da loja (configurar no editor)',
            'columns': '3',
            'rows': '3',
            'paginate': 'yes',
            'orderby': 'date',
            'order': 'DESC',
        }, caminho='grade/produtos'),
    ], caminho='grade', interno=True)

    miolo = d.container('Loja com filtros', {
        'content_width': 'boxed',
        'flex_direction': 'row',
        'flex_wrap': 'wrap',
        'flex_gap': lacuna(32, 32),
        'padding': dimensoes(24, 0, 56, 0),
    }, [filtros, grade], caminho='loja/miolo', interno=True)

    ajuda = faixa_ajuda(d, 'Quer uma ajuda para escolher?',
                        'Fale com o ateliê e a gente indica o tamanho e a peça certa.',
                        'Falar com o ateliê', PAGINAS['contato'], 'loja/ajuda')

    raiz = d.container('Arquivo da loja', {
        'content_width': 'full', 'flex_direction': 'column',
        'flex_gap': lacuna(0, 0), 'padding': dimensoes(0, 0, 0, 0),
    }, [cabecalho_loja, miolo, ajuda], caminho='raiz')
    d.content = [raiz]
    return d


def produto():
    """05. Pagina da peca: galeria, compra, abas e relacionados."""
    d = Documento('Página do produto', 'single')

    trilha = d.container('Trilha do produto', {
        'content_width': 'boxed',
        'padding': dimensoes(24, 0, 8, 0),
    }, [
        d.widget('woocommerce-breadcrumbs', {'_title': 'Trilha de navegacao'},
                 caminho='produto/trilha'),
    ], caminho='produto/cabecalho', interno=True)

    galeria = d.container('Galeria do produto', {
        'flex_direction': 'column',
        '_flex_size': 'custom', '_flex_basis_type': 'custom',
        '_flex_basis': medida(48, '%'),
    }, [
        d.widget('woocommerce-product-images', {
            '_title': 'Galeria de fotos (dinamica)',
        }, caminho='produto/galeria'),
        paragrafo(d, ('Galeria nativa do WooCommerce, com zoom e lightbox. As fotos são as do '
                      'cadastro de cada peça.'), 'produto/galeria-nota', 'iara-texto-micro'),
    ], caminho='produto/coluna-galeria', interno=True)

    compra = d.container('Informacoes e compra', {
        'flex_direction': 'column',
        'flex_gap': lacuna(16, 16),
        '_flex_size': 'custom', '_flex_basis_type': 'custom',
        '_flex_basis': medida(48, '%'),
    }, [
        d.widget('woocommerce-product-title', juntar_globais({
            '_title': 'Nome da peca (dinamico)', 'header_size': 'h1',
        }, {'title_color': cor('text'), 'typography': fonte('primary')}),
            caminho='produto/nome'),
        d.widget('woocommerce-product-rating', {'_title': 'Avaliacoes (dinamico)'},
                 caminho='produto/avaliacao'),
        d.widget('woocommerce-product-price', juntar_globais({
            '_title': 'Preco (dinamico)',
        }, {'text_color': cor('text'), 'typography': fonte('iara-preco')}),
            caminho='produto/preco'),
        paragrafo(d, ('Pix com 5% de desconto, cartão em até 6x sem juros e boleto. '
                      'Confira no editor se o texto acompanha o que estiver ativo na conta '
                      'do Mercado Pago.'), 'produto/parcelamento', 'iara-texto-micro'),
        d.widget('woocommerce-product-short-description', juntar_globais({
            '_title': 'Descricao curta (dinamica)',
        }, {'text_color': cor('iara-texto-suave'), 'typography': fonte('text')}),
            caminho='produto/descricao-curta'),
        d.widget('woocommerce-add-to-cart', {
            '_title': 'Variacoes, quantidade e botao de compra (dinamico)',
        }, caminho='produto/comprar'),
        d.widget('woocommerce-product-stock', {'_title': 'Estoque (dinamico)'},
                 caminho='produto/estoque'),
        d.widget('button', juntar_globais({
            '_title': 'Ver o Guia de Medidas', 'text': 'Ver o Guia de Medidas',
            'link': {'url': PAGINAS['guia'], 'is_external': '', 'nofollow': ''},
            'size': 'sm', 'button_type': 'text',
        }, {'text_color': cor('primary'), 'typography': fonte('iara-rotulo')}),
            caminho='produto/guia'),
        d.widget('woocommerce-product-meta', {'_title': 'Codigo e categorias (dinamico)'},
                 caminho='produto/meta'),
        d.widget('icon-list', juntar_globais({
            '_title': 'Garantias da compra',
            'icon_list': [
                d.item({'text': 'PAC pelos Correios, com frete grátis acima de R$ 299. Postagem em até 2 dias úteis.'}, 'produto/garantias/1'),
                d.item({'text': '7 dias para desistir da compra (CDC, Art. 49) e 30 dias para trocar de tamanho, com a primeira troca por nossa conta.'}, 'produto/garantias/2'),
                d.item({'text': 'Pagamento processado por gateway com antifraude. Não guardamos dados do seu cartão.'}, 'produto/garantias/3'),
            ],
            'space_between': medida(10),
        }, {'text_color': cor('iara-texto-suave'), 'typography': fonte('text')}),
            caminho='produto/garantias'),
    ], caminho='produto/coluna-compra', interno=True)

    principal = d.container('Produto', {
        'content_width': 'boxed',
        'flex_direction': 'row',
        'flex_wrap': 'wrap',
        'flex_gap': lacuna(32, 32),
        'padding': dimensoes(16, 0, 40, 0),
    }, [galeria, compra], caminho='produto/principal', interno=True)

    abas = d.container('Descricao e avaliacoes', {
        'content_width': 'boxed',
        'flex_direction': 'column',
        'padding': dimensoes(0, 0, 40, 0),
    }, [
        d.widget('woocommerce-product-data-tabs', {
            '_title': 'Abas do produto (dinamicas)',
        }, caminho='produto/abas'),
        paragrafo(d, ('As abas trazem a descrição, as informações adicionais e as avaliações de '
                      'cada peça. A tabela de medidas da peça entra nas informações adicionais '
                      'ou na descrição, com os valores reais do fornecedor.'), 'produto/abas-nota',
                  'iara-texto-micro'),
    ], caminho='produto/secao-abas', interno=True)

    relacionados = d.container('Combina com', {
        'content_width': 'boxed',
        'flex_direction': 'column',
        'flex_gap': lacuna(8, 8),
        'padding': dimensoes(40, 0, 56, 0),
        'background_background': 'classic',
        '__globals__': {'background_color': cor('iara-fundo-suave')},
    }, [
        titulo_secao(d, 'Combina com', 'produto/relacionados-titulo'),
        d.widget('woocommerce-product-related', {
            '_title': 'Produtos relacionados (dinamico)', 'posts_per_page': '4', 'columns': '4',
        }, caminho='produto/relacionados'),
        d.widget('woocommerce-product-upsell', {
            '_title': 'Sugestoes de compra (dinamico)', 'posts_per_page': '4', 'columns': '4',
        }, caminho='produto/upsell'),
    ], caminho='produto/secao-relacionados', interno=True)

    ajuda = faixa_ajuda(d, 'Ficou em dúvida no tamanho?',
                        'Confira o Guia de Medidas ou fale com o ateliê antes de fechar a compra.',
                        'Ver o Guia de Medidas', PAGINAS['guia'], 'produto/ajuda')

    raiz = d.container('Pagina do produto', {
        'content_width': 'full', 'flex_direction': 'column',
        'flex_gap': lacuna(0, 0), 'padding': dimensoes(0, 0, 0, 0),
    }, [trilha, principal, abas, relacionados, ajuda], caminho='raiz')
    d.content = [raiz]
    return d



def pagina_compra(titulo_doc, titulo_pagina, intro, widget_tipo, widget_titulo,
                  nota, caminho):
    """Base das paginas do funil: titulo, avisos e um widget do WooCommerce."""
    d = Documento(titulo_doc, 'page')
    raiz = d.container(titulo_doc, {
        'content_width': 'full', 'flex_direction': 'column',
        'flex_gap': lacuna(0, 0), 'padding': dimensoes(0, 0, 0, 0),
    }, [
        d.container('Cabecalho da pagina', {
            'content_width': 'boxed', 'flex_direction': 'column',
            'flex_gap': lacuna(12, 12), 'padding': dimensoes(40, 0, 8, 0),
        }, [
            d.widget('heading', juntar_globais({
                '_title': titulo_pagina, 'title': titulo_pagina, 'header_size': 'h1',
            }, {'title_color': cor('text'), 'typography': fonte('primary')}),
                caminho=caminho + '/titulo'),
            paragrafo(d, intro, caminho + '/intro'),
        ], caminho=caminho + '/cabecalho', interno=True),
        d.container('Conteudo da pagina', {
            'content_width': 'boxed', 'flex_direction': 'column',
            'flex_gap': lacuna(16, 16), 'padding': dimensoes(16, 0, 56, 0),
        }, [
            d.widget('woocommerce-notices', {'_title': 'Avisos do WooCommerce'},
                     caminho=caminho + '/avisos'),
            d.widget(widget_tipo, {'_title': widget_titulo}, caminho=caminho + '/widget'),
            paragrafo(d, nota, caminho + '/nota', 'iara-texto-micro'),
        ], caminho=caminho + '/conteudo', interno=True),
    ], caminho='raiz')
    d.content = [raiz]
    return d


def carrinho():
    """06. Sacola: widget classico Cart do WooCommerce/Elementor Pro."""
    return pagina_compra(
        'Sacola', 'Sacola',
        'Confira as peças, ajuste as quantidades e use o seu cupom antes de seguir. '
        'O frete é calculado pelo CEP aqui mesmo.',
        'woocommerce-cart', 'Sacola (dinâmica)',
        'Widget clássico de carrinho do WooCommerce. No editor, conferir o campo de '
        'cupom ativo: é por ele que entra o BEMVINDO10, com a limitação de primeira '
        'compra registrada no guia. Nada de carrinho em blocos novos nesta página.',
        'sacola')


def checkout():
    """07. Finalizar compra: widget classico Checkout."""
    return pagina_compra(
        'Finalizar compra', 'Finalizar compra',
        'Preencha os seus dados e escolha a forma de pagamento. Você pode comprar '
        'como visitante, sem criar conta.',
        'woocommerce-checkout', 'Finalizar compra (dinâmico)',
        'Widget clássico de checkout do WooCommerce. Compra como visitante, campos '
        'e formas de pagamento são configurados no WooCommerce e no Mercado Pago, '
        'não neste arquivo: o guia traz a lista de conferência.',
        'checkout')


def pedido_recebido():
    """08. Pedido recebido: resumo da compra depois do pagamento."""
    d = pagina_compra(
        'Pedido recebido', 'Pedido recebido',
        'Obrigada pela sua compra. Assim que o pagamento for confirmado, você '
        'recebe os detalhes por e-mail.',
        'woocommerce-purchase-summary', 'Resumo do pedido (dinâmico)',
        'Este resumo mostra o pedido real de quem acabou de comprar. Os e-mails de '
        'confirmação são do WooCommerce: remetente, SPF, DKIM e DMARC entram na '
        'lista de conferência do go-live, no Bloco C.',
        'pedido')
    # botoes de saida, depois do resumo
    conteudo = d.content[0]['elements'][1]
    conteudo['elements'].append(
        d.container('Saidas do pedido', {
            'content_width': 'full', 'flex_direction': 'row', 'flex_wrap': 'wrap',
            'flex_gap': lacuna(12, 12),
        }, [
            botao(d, 'Acompanhar meus pedidos', PAGINAS['conta'], 'pedido/botao-pedidos'),
            botao(d, 'Continuar comprando', PAGINAS['loja'], 'pedido/botao-loja', 'outline'),
        ], caminho='pedido/saidas', interno=True))
    return d


def conta():
    """09. Minha conta: pedidos, enderecos e dados, pelo WooCommerce."""
    return pagina_compra(
        'Minha conta', 'Minha conta',
        'Acompanhe os seus pedidos, guarde endereços e atualize os seus dados.',
        'woocommerce-my-account', 'Minha conta (dinâmica)',
        'Pedidos, downloads desligados, endereços e detalhes da conta são as telas '
        'nativas do WooCommerce. Esta página fica fora do sitemap e com noindex, '
        'como pede o dossiê.',
        'conta')


def desejos():
    """10. Lista de desejos: depende de plugin aprovado."""
    d = Documento('Lista de desejos', 'page')
    raiz = d.container('Lista de desejos', {
        'content_width': 'full', 'flex_direction': 'column',
        'flex_gap': lacuna(0, 0), 'padding': dimensoes(0, 0, 0, 0),
    }, [
        d.container('Cabecalho da pagina', {
            'content_width': 'boxed', 'flex_direction': 'column',
            'flex_gap': lacuna(12, 12), 'padding': dimensoes(40, 0, 8, 0),
        }, [
            d.widget('heading', juntar_globais({
                '_title': 'Lista de desejos', 'title': 'Lista de desejos',
                'header_size': 'h1',
            }, {'title_color': cor('text'), 'typography': fonte('primary')}),
                caminho='desejos/titulo'),
            paragrafo(d, 'As peças que você salvou ficam guardadas aqui.', 'desejos/intro'),
        ], caminho='desejos/cabecalho', interno=True),
        d.container('Conteudo da pagina', {
            'content_width': 'boxed', 'flex_direction': 'column',
            'flex_gap': lacuna(16, 16), 'padding': dimensoes(16, 0, 56, 0),
        }, [
            paragrafo(d, ('[CONFIGURAR NO EDITOR] Lista gerada pelo plugin TI WooCommerce '
                          'Wishlist, aprovado para este projeto. Ao instalar, apontar a página '
                          'da lista para este endereço; o bloco de produtos salvos entra aqui, '
                          'no lugar deste aviso, e o coração do cabeçalho já aponta para ela.'), 'desejos/aviso'),
            botao(d, 'Ver a loja', PAGINAS['loja'], 'desejos/botao'),
        ], caminho='desejos/conteudo', interno=True),
    ], caminho='raiz')
    d.content = [raiz]
    return d



def cab_pagina(d, titulo, intro, caminho, rotulo_texto=None):
    filhos = []
    if rotulo_texto:
        filhos.append(rotulo(d, rotulo_texto, caminho + '/rotulo', 'primary'))
    filhos.append(d.widget('heading', juntar_globais({
        '_title': titulo, 'title': titulo, 'header_size': 'h1',
    }, {'title_color': cor('text'), 'typography': fonte('primary')}), caminho=caminho + '/titulo'))
    if intro:
        filhos.append(paragrafo(d, intro, caminho + '/intro'))
    return d.container('Cabecalho da pagina', {
        'content_width': 'boxed', 'flex_direction': 'column',
        'flex_gap': lacuna(12, 12), 'padding': dimensoes(40, 0, 8, 0),
    }, filhos, caminho=caminho, interno=True)


def secao_texto(d, titulo, texto, caminho):
    return d.container(titulo, {
        'content_width': 'boxed', 'flex_direction': 'column',
        'flex_gap': lacuna(10, 10), 'padding': dimensoes(24, 0, 24, 0),
    }, [
        titulo_secao(d, titulo, caminho + '/titulo'),
        paragrafo(d, texto, caminho + '/texto'),
    ], caminho=caminho, interno=True)


def pagina_documento(titulo_doc, intro, secoes, caminho, aviso=None):
    """Pagina de texto longo: titulo e secoes numeradas, texto revisado."""
    d = Documento(titulo_doc, 'page')
    filhos = [cab_pagina(d, titulo_doc, intro, caminho + '/cab')]
    if aviso:
        filhos.append(d.container('Aviso de revisao', {
            'content_width': 'boxed', 'padding': dimensoes(16, 0, 16, 0),
        }, [paragrafo(d, aviso, caminho + '/aviso', 'iara-texto-micro')], caminho=caminho + '/aviso-box', interno=True))
    for i, (titulo, texto) in enumerate(secoes, 1):
        filhos.append(secao_texto(d, titulo, texto, caminho + '/s' + str(i)))
    raiz = d.container(titulo_doc, {
        'content_width': 'full', 'flex_direction': 'column',
        'flex_gap': lacuna(0, 0), 'padding': dimensoes(0, 0, 40, 0),
    }, filhos, caminho='raiz')
    d.content = [raiz]
    return d


def blog():
    """11. Diario: arquivo de posts (textos nascem no Gutenberg)."""
    d = Documento('Diário', 'archive')
    raiz = d.container('Diário', {
        'content_width': 'full', 'flex_direction': 'column',
        'flex_gap': lacuna(0, 0), 'padding': dimensoes(0, 0, 0, 0),
    }, [
        cab_pagina(d, 'Diário', 'Cartas do ateliê: tecidos, cuidados, tamanhos e bastidores da produção em Cerquilho.', 'blog/cab', 'Do ateliê'),
        d.container('Lista de textos', {
            'content_width': 'boxed', 'flex_direction': 'column',
            'flex_gap': lacuna(12, 12), 'padding': dimensoes(24, 0, 56, 0),
        }, [
            d.widget('archive-posts', {'_title': 'Textos do diário (dinâmico)', 'posts_per_page': '9', 'columns': '3'}, caminho='blog/posts'),
            paragrafo(d, 'Grade dinâmica de posts. Os textos são escritos e publicados no Gutenberg, nunca no Elementor; este arquivo só desenha a vitrine.', 'blog/nota', 'iara-texto-micro'),
        ], caminho='blog/lista', interno=True),
    ], caminho='raiz')
    d.content = [raiz]
    return d


def post():
    """12. Artigo: post unico com cabecalho, texto Gutenberg e relacionados."""
    d = Documento('Artigo do diário', 'single')
    raiz = d.container('Artigo do diário', {
        'content_width': 'full', 'flex_direction': 'column',
        'flex_gap': lacuna(0, 0), 'padding': dimensoes(0, 0, 0, 0),
    }, [
        d.container('Cabecalho do artigo', {
            'content_width': 'boxed', 'flex_direction': 'column',
            'flex_gap': lacuna(12, 12), 'padding': dimensoes(40, 0, 16, 0),
        }, [
            d.widget('theme-post-title', juntar_globais({'_title': 'Titulo do artigo (dinamico)', 'header_size': 'h1'}, {'title_color': cor('text'), 'typography': fonte('primary')}), caminho='post/titulo'),
            d.widget('theme-post-info', {'_title': 'Data e autor (dinamico)'}, caminho='post/info'),
            d.widget('theme-post-featured-image', {'_title': 'Imagem de capa (dinamica)'}, caminho='post/capa'),
        ], caminho='post/cab', interno=True),
        d.container('Texto do artigo', {
            'content_width': 'boxed', 'padding': dimensoes(16, 0, 40, 0),
        }, [
            d.widget('theme-post-content', {'_title': 'Conteudo do Gutenberg (dinamico)'}, caminho='post/conteudo'),
        ], caminho='post/texto', interno=True),
        d.container('Continue lendo', {
            'content_width': 'boxed', 'flex_direction': 'column',
            'flex_gap': lacuna(8, 8), 'padding': dimensoes(40, 0, 56, 0),
            'background_background': 'classic', '__globals__': {'background_color': cor('iara-fundo-suave')},
        }, [
            titulo_secao(d, 'Continue lendo', 'post/continue-titulo'),
            d.widget('posts', {'_title': 'Outros textos (dinamico)', 'posts_per_page': '3', 'columns': '3'}, caminho='post/relacionados'),
        ], caminho='post/continue', interno=True),
    ], caminho='raiz')
    d.content = [raiz]
    return d


def busca():
    """13. Resultados de busca de produtos e textos."""
    d = Documento('Busca', 'search-results')
    raiz = d.container('Busca', {
        'content_width': 'full', 'flex_direction': 'column',
        'flex_gap': lacuna(0, 0), 'padding': dimensoes(0, 0, 0, 0),
    }, [
        cab_pagina(d, 'Busca', 'Resultados para a sua busca em peças e textos do diário.', 'busca/cab'),
        d.container('Campo e resultados', {
            'content_width': 'boxed', 'flex_direction': 'column',
            'flex_gap': lacuna(20, 20), 'padding': dimensoes(24, 0, 56, 0),
        }, [
            d.widget('search-form', {'_title': 'Buscar de novo', 'placeholder': 'O que você procura?'}, caminho='busca/campo'),
            d.widget('archive-posts', {'_title': 'Resultados (dinâmico)', 'posts_per_page': '9', 'columns': '3'}, caminho='busca/resultados'),
            paragrafo(d, 'Sem resultado, confira a grafia ou tente uma palavra mais geral, como linho, vestido ou cerâmica. A loja completa está a um clique.', 'busca/sem-resultado'),
            botao(d, 'Ver todas as peças', PAGINAS['loja'], 'busca/botao'),
        ], caminho='busca/miolo', interno=True),
    ], caminho='raiz')
    d.content = [raiz]
    return d


def erro404():
    """14. Pagina nao encontrada."""
    d = Documento('Página não encontrada', 'error-404')
    raiz = d.container('Página não encontrada', {
        'content_width': 'full', 'flex_direction': 'column',
        'flex_gap': lacuna(0, 0), 'padding': dimensoes(0, 0, 0, 0),
    }, [
        d.container('Mensagem', {
            'content_width': 'boxed', 'flex_direction': 'column',
            'flex_align_items': 'center', 'flex_gap': lacuna(16, 16),
            'padding': dimensoes(72, 0, 72, 0),
        }, [
            rotulo(d, '404', '404/rotulo', 'primary'),
            d.widget('heading', juntar_globais({'_title': 'Esta página não está mais aqui', 'title': 'Esta página não está mais aqui', 'header_size': 'h1', 'align': 'center'}, {'title_color': cor('text'), 'typography': fonte('primary')}), caminho='404/titulo'),
            paragrafo(d, 'Talvez o endereço tenha mudado ou a página tenha saído do ar. As peças e os textos continuam por aqui:', '404/texto'),
            d.container('Saidas', {'content_width': 'full', 'flex_direction': 'row', 'flex_wrap': 'wrap', 'flex_gap': lacuna(12, 12)}, [
                botao(d, 'Ver a loja', PAGINAS['loja'], '404/botao-loja'),
                botao(d, 'Voltar para o início', PAGINAS['home'], '404/botao-home', 'outline'),
                botao(d, 'Falar com o ateliê', PAGINAS['contato'], '404/botao-contato', 'outline'),
            ], caminho='404/saidas', interno=True),
        ], caminho='404/miolo', interno=True),
    ], caminho='raiz')
    d.content = [raiz]
    return d


def sobre():
    """15. Sobre a marca."""
    return pagina_documento('Sobre a Iara Costa',
        'Vestuário feminino autoral em linho, algodão egípcio e viscose de alta gramatura, feito no ateliê em Cerquilho (SP).',
        [
            ('Como começou', '[PROPOSTA] Texto de abertura aguardando a história real da marca. O protótipo aprovado traz a versão de referência: quem escreve o texto final é a empresa.'),
            ('Missão, visão e compromisso', '[PROPOSTA] Missão, visão e compromisso aguardando aprovação da empresa, sem inventar promessa, selo ou garantia.'),
            ('O ateliê e o processo', 'Modelagem, corte e confecção próprios. O processo completo, da escolha do tecido à peça pronta, entra aqui com os detalhes reais do ateliê [PREENCHER].'),
            ('Como escolhemos as peças', 'Tecidos escolhidos pela gramatura e pelo toque, em três famílias: linho, algodão egípcio e viscose de alta gramatura. Do P ao GG, com guia de medidas por peça.'),
        ], 'sobre',
        aviso='Página com textos [PROPOSTA] do protótipo: publicar só depois da aprovação da empresa.')


def contato():
    """16. Contato: formulario, canais e atalhos."""
    d = Documento('Contato', 'page')
    formulario = d.widget('form', {
        '_title': 'Formulario de contato',
        'form_name': 'Contato do site',
        'form_fields': [
            d.item({'custom_id': 'nome', 'field_type': 'text', 'field_label': 'Nome', 'placeholder': 'Seu nome', 'required': 'true', 'width': '100'}, 'contato/f-nome'),
            d.item({'custom_id': 'email', 'field_type': 'email', 'field_label': 'E-mail', 'placeholder': 'seu@email.com', 'required': 'true', 'width': '100'}, 'contato/f-email'),
            d.item({'custom_id': 'assunto', 'field_type': 'text', 'field_label': 'Assunto', 'placeholder': 'Sobre o que você quer falar?', 'required': 'true', 'width': '100'}, 'contato/f-assunto'),
            d.item({'custom_id': 'mensagem', 'field_type': 'textarea', 'field_label': 'Mensagem', 'placeholder': 'Conte para a gente', 'required': 'true', 'width': '100', 'rows': '5'}, 'contato/f-mensagem'),
        ],
        'button_text': 'Enviar mensagem',
        'email_to': '[CONFERIR: e-mail de destino]',
        'form_id': 'contato',
    }, caminho='contato/formulario')
    raiz = d.container('Contato', {
        'content_width': 'full', 'flex_direction': 'column',
        'flex_gap': lacuna(0, 0), 'padding': dimensoes(0, 0, 0, 0),
    }, [
        cab_pagina(d, 'Fale com a gente', 'Envie uma mensagem ou use um dos canais abaixo. Respondemos em dias úteis, das 9h às 18h.', 'contato/cab'),
        d.container('Formulario e canais', {
            'content_width': 'boxed', 'flex_direction': 'row', 'flex_wrap': 'wrap',
            'flex_gap': lacuna(32, 32), 'padding': dimensoes(24, 0, 56, 0),
        }, [
            d.container('Envie uma mensagem', {'flex_direction': 'column', 'flex_gap': lacuna(12, 12), '_flex_size': 'custom', '_flex_basis_type': 'custom', '_flex_basis': medida(56, '%')}, [
                titulo_secao(d, 'Envie uma mensagem', 'contato/form-titulo'), formulario,
                paragrafo(d, 'Ao enviar, você concorda com a Política de Privacidade. O campo de consentimento entra no editor conforme a ferramenta de formulários usada.', 'contato/consent', 'iara-texto-micro'),
            ], caminho='contato/col-form', interno=True),
            d.container('Outros canais', {'flex_direction': 'column', 'flex_gap': lacuna(12, 12), '_flex_size': 'custom', '_flex_basis_type': 'custom', '_flex_basis': medida(38, '%')}, [
                titulo_secao(d, 'Outros canais', 'contato/canais-titulo'),
                d.widget('icon-list', juntar_globais({'_title': 'Canais', 'icon_list': [
                    d.item({'text': 'contato@iaracosta.com.br', 'link': {'url': 'mailto:contato@iaracosta.com.br', 'is_external': '', 'nofollow': ''}}, 'contato/canais/1'),
                    d.item({'text': '(15) 99123-4567, telefone e WhatsApp', 'link': {'url': 'https://wa.me/5515991234567', 'is_external': 'on', 'nofollow': ''}}, 'contato/canais/2'),
                    d.item({'text': 'Segunda a sexta, das 9h às 18h'}, 'contato/canais/3'),
                    d.item({'text': 'Cerquilho, interior de São Paulo'}, 'contato/canais/4'),
                ], 'space_between': medida(10)}, {'text_color': cor('iara-texto-suave'), 'typography': fonte('text')}), caminho='contato/canais'),
                paragrafo(d, 'O endereço completo para devolução entra na confirmação com a empresa [PREENCHER]. O mapa, se for usado, entra como bloco do editor, sem widget de HTML.', 'contato/mapa', 'iara-texto-micro'),
                botao(d, 'Perguntas frequentes', PAGINAS['faq'], 'contato/botao-faq', 'outline'),
            ], caminho='contato/col-canais', interno=True),
        ], caminho='contato/miolo', interno=True),
    ], caminho='raiz')
    d.content = [raiz]
    return d


def faq_pagina():
    """17. Perguntas frequentes completas."""
    grupos = [
        ('Pedidos e pagamento', 'Compra como visitante, Pix com 5% de desconto, cartão em até 6x sem juros e boleto pelo Mercado Pago.'),
        ('Entrega e frete', 'Envio para todo o Brasil pelos Correios, frete grátis acima de R$ 299 e código de rastreio por e-mail.'),
        ('Trocas e devoluções', '7 dias para desistir (CDC, Art. 49) e 30 dias para trocar de tamanho, com a primeira troca por nossa conta.'),
        ('Produtos e tamanhos', 'Cada peça traz a própria tabela de medidas; o Guia de Medidas ensina a medir uma peça sua e comparar.'),
        ('Atendimento e privacidade', 'Atendimento de segunda a sexta, das 9h às 18h. Seus dados seguem a Política de Privacidade.'),
    ]
    d = Documento('Perguntas frequentes', 'page')
    raiz = d.container('Perguntas frequentes', {
        'content_width': 'full', 'flex_direction': 'column',
        'flex_gap': lacuna(0, 0), 'padding': dimensoes(0, 0, 0, 0),
    }, [
        cab_pagina(d, 'Perguntas frequentes', 'As dúvidas que mais chegam no ateliê, organizadas por assunto.', 'faq/cab'),
        d.container('Grupos de perguntas', {
            'content_width': 'boxed', 'flex_direction': 'column',
            'flex_gap': lacuna(12, 12), 'padding': dimensoes(24, 0, 40, 0),
        }, [
            d.widget('accordion', juntar_globais({'_title': 'Perguntas por assunto', 'tabs': [
                d.item({'tab_title': titulo, 'tab_content': '<p>' + texto + '</p>'}, 'faq-pagina/item-' + str(i))
                for i, (titulo, texto) in enumerate(grupos, 1)
            ]}, {'text_color': cor('iara-texto-suave'), 'typography': fonte('text')}), caminho='faq-pagina/sanfona'),
            paragrafo(d, 'As perguntas e respostas completas, iguais às do protótipo aprovado, entram aba por aba no editor a partir do texto final aprovado. Não inventar prazo, garantia ou política nova aqui.', 'faq-pagina/nota', 'iara-texto-micro'),
        ], caminho='faq-pagina/miolo', interno=True),
        faixa_ajuda(d, 'Não encontrou a sua dúvida?', 'Fale com o ateliê e a gente responde em dias úteis.', 'Falar com o ateliê', PAGINAS['contato'], 'faq-pagina/ajuda'),
    ], caminho='raiz')
    d.content = [raiz]
    return d


def guia_medidas():
    """18. Guia de medidas."""
    return pagina_documento('Guia de medidas',
        'Meça uma peça que já veste bem e compare com a tabela de cada produto.',
        [
            ('Como medir em casa', 'Estique a peça sobre a mesa, sem puxar. Meça busto, cintura, quadril e comprimento com a fita sem apertar, e anote em centímetros.'),
            ('Tabela de medidas', '[PREENCHER] A tabela geral entra com as medidas reais da modelagem da marca. Cada página de produto traz a tabela daquela peça, que é a que vale na hora de escolher.'),
            ('Dúvidas comuns sobre tamanho', 'Na dúvida entre dois tamanhos, compare as medidas com a peça medida em casa. Se ainda assim ficar em dúvida, fale com o atendimento antes de fechar: a troca de tamanho em 30 dias existe, mas acertar de primeira é melhor.'),
        ], 'guia-medidas',
        aviso='A tabela desta página depende das medidas reais da modelagem [PREENCHER]: não publicar com valores de exemplo.')


def lookbook():
    """19. Colecao Terra e Linho: editorial em capitulos."""
    d = Documento('Coleção Terra & Linho', 'page')
    capitulos = [
        ('Capítulo 01', 'O barro que veste', 'Terracota em linho e algodão, nas peças de abertura da coleção.'),
        ('Capítulo 02', 'Verde que acalma', 'Sálvia em vestidos e pantalona, para o dia inteiro.'),
        ('Capítulo 03', 'O branco que não é básico', 'Cru e areia em camadas leves, com acessórios de cerâmica.'),
    ]
    filhos = [cab_pagina(d, 'Terra & Linho', 'Três capítulos em doze peças: terracota do barro, sálvia da mata, cru do linho.', 'lookbook/cab', 'Coleção')]
    for i, (rotulo_cap, titulo, texto) in enumerate(capitulos, 1):
        filhos.append(d.container(titulo, {
            'content_width': 'boxed', 'flex_direction': 'row', 'flex_wrap': 'wrap',
            'flex_gap': lacuna(32, 32), 'padding': dimensoes(40, 0, 40, 0),
            **({'background_background': 'classic', '__globals__': {'background_color': cor('iara-fundo-suave')}} if i % 2 == 0 else {}),
        }, [
            d.container('Foto do capitulo', {'flex_direction': 'column', '_flex_size': 'custom', '_flex_basis_type': 'custom', '_flex_basis': medida(48, '%')}, [
                d.widget('image', {'_title': 'Foto do capítulo (escolher no editor)', 'image': {'url': '', 'id': ''}, 'image_size': 'full', 'caption_source': 'none', 'link_to': 'none'}, caminho='lookbook/foto-' + str(i)),
            ], caminho='lookbook/midia-' + str(i), interno=True),
            d.container('Texto do capitulo', {'flex_direction': 'column', 'flex_gap': lacuna(12, 12), '_flex_size': 'custom', '_flex_basis_type': 'custom', '_flex_basis': medida(48, '%'), '_flex_align_self': 'center'}, [
                rotulo(d, rotulo_cap, 'lookbook/rotulo-' + str(i), 'primary'),
                titulo_secao(d, titulo, 'lookbook/titulo-' + str(i)),
                paragrafo(d, texto, 'lookbook/texto-' + str(i)),
                botao(d, 'Comprar as peças do capítulo', PAGINAS['loja'], 'lookbook/botao-' + str(i)),
            ], caminho='lookbook/texto-box-' + str(i), interno=True),
        ], caminho='lookbook/cap-' + str(i), interno=True))
    filhos.append(faixa_ajuda(d, 'Viu algo que gostou?', 'Todas as peças do editorial estão à venda na loja.', 'Ir para a loja', PAGINAS['loja'], 'lookbook/ajuda'))
    raiz = d.container('Coleção Terra & Linho', {'content_width': 'full', 'flex_direction': 'column', 'flex_gap': lacuna(0, 0), 'padding': dimensoes(0, 0, 0, 0)}, filhos, caminho='raiz')
    d.content = [raiz]
    return d


def trocas():
    return pagina_documento('Trocas e devoluções',
        'Trocar ou devolver uma peça é simples. Os prazos abaixo seguem o Código de Defesa do Consumidor.',
        [
            ('Desistência em 7 dias (direito de arrependimento)', 'Você tem 7 dias corridos, contando do recebimento, para desistir da compra sem precisar justificar, conforme o Art. 49 do CDC. A peça precisa voltar sem uso, com as etiquetas.'),
            ('Troca por tamanho ou por outra peça', 'Em até 30 dias do recebimento, a primeira troca de tamanho é por nossa conta, pelo código de postagem dos Correios. [CONFIRMAR COM A EMPRESA: peças de bazar e peças íntimas entram nesta regra?]'),
            ('Peça com defeito de fabricação', 'Se a peça chegar com defeito, fale com o atendimento com fotos do problema. Defeito de fabricação tem o tratamento previsto no CDC.'),
            ('Como solicitar', 'Pela Minha conta ou pelo atendimento, informando o número do pedido. Você recebe as instruções e o código de postagem.'),
            ('Reembolso', 'Depois que a peça chega e é conferida, o reembolso segue a forma de pagamento original, nos prazos do gateway.'),
        ], 'trocas', aviso='Rascunho para revisão: confirmar as regras marcadas antes de publicar.')


def envio():
    return pagina_documento('Envio e entrega',
        'Enviamos para todo o Brasil pelos Correios, com rastreio em todos os pedidos.',
        [
            ('Prazos e valores', 'O prazo e o valor do frete são calculados pelo seu CEP na sacola e no fechamento, antes do pagamento. Postagem em até 2 dias úteis depois da confirmação.'),
            ('Frete grátis acima de R$ 299', 'Pedidos a partir de R$ 299 têm frete grátis no PAC para todo o Brasil.'),
            ('Como acompanhar o pedido', 'Assim que a peça é postada, o código de rastreio vai para o seu e-mail e fica na Minha conta.'),
            ('Se algo der errado', 'Se o pedido atrasar, voltar ou chegar danificado, fale com o atendimento com o número do pedido que a gente resolve com a transportadora.'),
        ], 'envio')


def privacidade():
    return pagina_documento('Política de Privacidade',
        'Como tratamos os seus dados, em linguagem direta.',
        [(t, '[PREENCHER: texto jurídico aprovado] Este é o esqueleto da seção. O texto final vem da revisão jurídica e entra aqui antes de publicar.') for t in (
            '1. Quem é o controlador dos seus dados', '2. Quais dados coletamos', '3. Com quem compartilhamos',
            '4. Transferência internacional', '5. Por quanto tempo guardamos', '6. Seus direitos como titular',
            '7. Segurança', '8. Encarregado e contato')],
        'privacidade', aviso='RASCUNHO PARA O JURÍDICO: não publicar sem revisão. Os dados da empresa entram como [PREENCHER].')


def termos():
    return pagina_documento('Termos de uso',
        'As regras de uso desta loja.',
        [(t, '[PREENCHER: texto jurídico aprovado] Esqueleto da seção para revisão jurídica; o texto final entra aqui antes de publicar.') for t in (
            '1. Aceitação', '2. Identificação da empresa', '3. Uso do site', '4. Cadastro e conta',
            '5. Produtos, preços e disponibilidade', '6. Pagamento', '7. Entrega', '8. Trocas e devoluções')],
        'termos', aviso='RASCUNHO PARA O JURÍDICO: não publicar sem revisão.')


def cookies():
    return pagina_documento('Política de Cookies',
        'Quais cookies usamos e como você controla isso.',
        [(t, '[PREENCHER: texto jurídico aprovado] Esqueleto da seção para revisão; o banner de cookies da LGPD é configurado no go-live e precisa apontar para esta página.') for t in (
            '1. O que são cookies', '2. Categorias de cookies', '3. Cookies de terceiros',
            '4. Como controlar os cookies', '5. Alterações nesta política', '6. Dúvidas')],
        'cookies', aviso='RASCUNHO PARA O JURÍDICO: não publicar sem revisão. O banner de consentimento é item de aceitação do go-live.')


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
    ('03-home.json', home),
    ('04-loja.json', loja),
    ('05-produto.json', produto),
    ('06-carrinho.json', carrinho),
    ('07-checkout.json', checkout),
    ('08-pedido-recebido.json', pedido_recebido),
    ('09-conta.json', conta),
    ('10-desejos.json', desejos),
    ('11-blog.json', blog),
    ('12-post.json', post),
    ('13-busca.json', busca),
    ('14-404.json', erro404),
    ('15-sobre.json', sobre),
    ('16-contato.json', contato),
    ('17-faq.json', faq_pagina),
    ('18-guia-medidas.json', guia_medidas),
    ('19-lookbook.json', lookbook),
    ('20-trocas.json', trocas),
    ('21-envio.json', envio),
    ('22-privacidade.json', privacidade),
    ('23-termos.json', termos),
    ('24-cookies.json', cookies),
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
