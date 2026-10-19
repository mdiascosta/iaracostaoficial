#!/usr/bin/env python3
"""
Gera bloco-c/pages-conteudo.md a partir dos textos aprovados do prototipo.

Fonte: tools/content/*.html (o conteudo das paginas do Bloco A, sem cabecalho
e sem rodape). Nada e reescrito aqui: o script so transforma HTML em Markdown
legivel, mantendo os marcadores [PREENCHER], [PROPOSTA] e [CONFIRMAR].

Uso:
    python3 tools/blococ_gera_conteudo.py
"""

import pathlib
import re
import sys
from html.parser import HTMLParser

RAIZ = pathlib.Path(__file__).resolve().parents[1]

PAGINAS = [
    ('13-sobre.html', 'Sobre a Iara Costa', '/sobre/', '15-sobre.json',
     'Textos marcados [PROPOSTA]: publicar so depois da aprovacao da empresa.'),
    ('14-contato.html', 'Contato', '/contato/', '16-contato.json',
     'Conferir o e-mail de destino do formulario antes de publicar.'),
    ('15-faq.html', 'Perguntas frequentes', '/perguntas-frequentes/', '17-faq.json',
     'Conferir prazos e regras com as paginas de trocas e de envio.'),
    ('16-guia-medidas.html', 'Guia de medidas', '/guia-de-medidas/', '18-guia-medidas.json',
     'A tabela geral depende das medidas reais da modelagem [PREENCHER].'),
    ('17-lookbook.html', 'Coleção Terra & Linho', '/colecao/', '19-lookbook.json',
     'Confirmar nome da colecao e as fotos de cada capitulo.'),
    ('18-trocas.html', 'Trocas e devoluções', '/trocas-e-devolucoes/', '20-trocas.json',
     'Rascunho de trabalho: confirmar as regras marcadas antes de publicar.'),
    ('19-envio.html', 'Envio e entrega', '/envio-e-entrega/', '21-envio.json',
     'Prazos e valores finais sao calculados pelo CEP no WooCommerce.'),
    ('20-privacidade.html', 'Política de Privacidade', '/politica-de-privacidade/', '22-privacidade.json',
     'RASCUNHO PARA O JURIDICO: nao publicar sem revisao.'),
    ('21-termos.html', 'Termos de uso', '/termos-de-uso/', '23-termos.json',
     'RASCUNHO PARA O JURIDICO: nao publicar sem revisao.'),
    ('22-cookies.html', 'Política de Cookies', '/politica-de-cookies/', '24-cookies.json',
     'RASCUNHO PARA O JURIDICO: o banner de consentimento entra no go-live.'),
]

IGNORAR = {'script', 'style', 'svg', 'img', 'input', 'select', 'textarea', 'iframe'}


class Extrator(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.partes = []
        self.profundidade_ignorar = 0
        self.tag_atual = None
        self.buffer = []

    def _flush(self):
        texto = ' '.join(''.join(self.buffer).split())
        self.buffer = []
        if not texto:
            self.tag_atual = None
            return
        tag = self.tag_atual
        if tag == 'h1':
            self.partes.append(f'# {texto}')
        elif tag == 'h2':
            self.partes.append(f'## {texto}')
        elif tag in ('h3', 'h4', 'legend'):
            self.partes.append(f'### {texto}')
        elif tag == 'li':
            self.partes.append(f'- {texto}')
        elif tag == 'button':
            self.partes.append(f'### {texto}')
        elif tag in ('td', 'th'):
            self.partes.append(f'| {texto} ')
        else:
            self.partes.append(texto)
        self.tag_atual = None

    def handle_starttag(self, tag, attrs):
        if tag in IGNORAR:
            self.profundidade_ignorar += 1
            return
        if self.profundidade_ignorar:
            return
        classes = dict(attrs).get('class', '')
        if 'visually-hidden' in classes:
            self.profundidade_ignorar += 1
            return
        if tag in ('h1', 'h2', 'h3', 'h4', 'p', 'li', 'button', 'legend', 'td', 'th', 'caption'):
            self._flush()
            self.tag_atual = tag
        elif tag == 'tr':
            self._flush()
            self.partes.append('')

    def handle_endtag(self, tag):
        if tag in IGNORAR or self.profundidade_ignorar:
            if self.profundidade_ignorar:
                self.profundidade_ignorar -= 1
            return
        if tag in ('h1', 'h2', 'h3', 'h4', 'p', 'li', 'button', 'legend', 'td', 'th', 'caption', 'tr'):
            self._flush()
            if tag == 'tr':
                self.partes.append('')

    def handle_data(self, data):
        if not self.profundidade_ignorar:
            self.buffer.append(data)


def extrair(caminho):
    parser = Extrator()
    parser.feed(caminho.read_text(encoding='utf-8'))
    linhas = []
    for parte in parser.partes:
        if not parte:
            if linhas and linhas[-1] != '':
                linhas.append('')
            continue
        linhas.append(parte)
    # remove a trilha de navegacao (Início > pagina) do comeco
    while linhas and linhas[0].startswith('- '):
        linhas.pop(0)
    while linhas and linhas[0] == '':
        linhas.pop(0)
    texto = '\n'.join(linhas)
    texto = re.sub(r'\n{3,}', '\n\n', texto)
    texto = re.sub(r'\.html\b', '', texto)
    return texto.strip()


def main():
    saida = [
        '# Conteúdo das páginas (Bloco C)',
        '',
        'Este documento reúne o texto aprovado no protótipo (Bloco A) das páginas',
        'institucionais, de atendimento e legais, em Markdown, para revisar,',
        'aprovar e colar onde cada página nasce: as institucionais nos templates',
        'do Elementor (Bloco B) e as legais também como rascunho para o jurídico.',
        '',
        '**Regras deste documento**',
        '',
        '- Nada aqui foi reescrito: o texto vem das páginas aprovadas do protótipo.',
        '- Os marcadores `[PREENCHER]`, `[PROPOSTA]`, `[CONFIRMAR COM A EMPRESA]` e',
        '  `[CONFERIR]` são parte do texto e só saem quando a informação real entrar.',
        '- As três páginas legais são **rascunho para o jurídico**: não publicar',
        '  sem revisão, mesmo que o texto pareça pronto.',
        '- Nenhum travessão foi usado, como em todo o projeto.',
        '',
        '---',
        '',
    ]
    total_marcadores = 0
    for arquivo, titulo, endereco, template, nota in PAGINAS:
        corpo = extrair(RAIZ / 'tools' / 'content' / arquivo)
        marcadores = len(re.findall(r'\[[A-ZÃÕ ]+(?::|\])', corpo))
        total_marcadores += marcadores
        saida += [
            f'## {titulo}',
            '',
            f'- Endereço: `{endereco}`',
            f'- Template: `bloco-b/json/{template}`',
            f'- Situação: {nota}',
            '',
            corpo,
            '',
            '---',
            '',
        ]
    destino = RAIZ / 'bloco-c' / 'pages-conteudo.md'
    destino.write_text('\n'.join(saida), encoding='utf-8')
    print(f'  ok  pages-conteudo.md  {len(PAGINAS)} paginas, {total_marcadores} marcadores mantidos')
    return 0


if __name__ == '__main__':
    sys.exit(main())
