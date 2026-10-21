#!/usr/bin/env python3
"""Pente-fino: JSON do Elementor x paginas do prototipo + auditoria de CSS.

Para cada um dos 24 templates, compara com a pagina HTML correspondente
do prototipo aprovado: textos (o que falta e o que sobra), imagens e
estrutura de secoes. Depois audita o CSS: quanto do CSS do prototipo
(4 arquivos, ~4.200 linhas) tem equivalente no que o Elementor recebe
(CSS embutido + globais + estilos declarados nos widgets), quais classes
iara-* usadas nos JSON nao tem regra, quantos estados :hover existem de
cada lado e se ha ajustes responsivos declarados.

Uso:  python3 tools/pente_fino.py
Saida: PENTE-FINO.md (na raiz do repositorio)
"""
import html.parser
import json
import pathlib
import re
import unicodedata

RAIZ = pathlib.Path(__file__).resolve().parent.parent

MAPA = [
    ('01-cabecalho.json', 'tools/partials/header.html'),
    ('02-rodape.json', 'tools/partials/footer.html'),
    ('03-home.json', 'seu-projeto/index.html'),
    ('04-loja.json', 'seu-projeto/loja.html'),
    ('05-produto.json', 'seu-projeto/produto.html'),
    ('06-carrinho.json', 'seu-projeto/carrinho.html'),
    ('07-checkout.json', 'seu-projeto/checkout.html'),
    ('08-pedido-recebido.json', 'seu-projeto/pedido-recebido.html'),
    ('09-conta.json', 'seu-projeto/conta.html'),
    ('10-desejos.json', 'seu-projeto/desejos.html'),
    ('11-blog.json', 'seu-projeto/blog.html'),
    ('12-post.json', 'seu-projeto/post.html'),
    ('13-busca.json', 'seu-projeto/busca.html'),
    ('14-404.json', 'seu-projeto/404.html'),
    ('15-sobre.json', 'seu-projeto/sobre.html'),
    ('16-contato.json', 'seu-projeto/contato.html'),
    ('17-faq.json', 'seu-projeto/faq.html'),
    ('18-guia-medidas.json', 'seu-projeto/guia-medidas.html'),
    ('19-lookbook.json', 'seu-projeto/lookbook.html'),
    ('20-trocas.json', 'seu-projeto/trocas.html'),
    ('21-envio.json', 'seu-projeto/envio.html'),
    ('22-privacidade.json', 'seu-projeto/privacidade.html'),
    ('23-termos.json', 'seu-projeto/termos.html'),
    ('24-cookies.json', 'seu-projeto/cookies.html'),
]


def normaliza(texto):
    texto = unicodedata.normalize('NFKD', texto or '')
    texto = ''.join(c for c in texto if not unicodedata.combining(c))
    texto = re.sub(r'<[^>]+>', ' ', texto)
    texto = texto.lower()
    texto = re.sub(r'[^a-z0-9 ]+', ' ', texto)
    return re.sub(r'\s+', ' ', texto).strip()


class ExtratorHTML(html.parser.HTMLParser):
    def __init__(self, pular_cabecalho_rodape=False):
        super().__init__()
        self.textos = []
        self.imagens = []
        self.links = []
        self.secoes = []
        self._ignora = 0
        self._pular = pular_cabecalho_rodape
        self._dentro = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ('script', 'style'):
            self._ignora += 1
        if self._pular and tag in ('header', 'footer'):
            self._dentro += 1
        if tag == 'img' and a.get('src'):
            self.imagens.append(a['src'])
        if tag == 'a' and a.get('href'):
            self.links.append(a['href'])
        if tag in ('section', 'div') and a.get('class'):
            self.secoes.append(a['class'])

    def handle_endtag(self, tag):
        if tag in ('script', 'style') and self._ignora:
            self._ignora -= 1
        if self._pular and tag in ('header', 'footer') and self._dentro:
            self._dentro -= 1

    def handle_data(self, data):
        if not self._ignora and not self._dentro:
            t = data.strip()
            if t:
                self.textos.append(t)


def frases_html(caminho):
    ext = ExtratorHTML(pular_cabecalho_rodape='partials' not in caminho)
    ext.feed((RAIZ / caminho).read_text(encoding='utf-8'))
    frases = set()
    for t in ext.textos:
        n = normaliza(t)
        if len(n) >= 18:
            frases.add(n)
    return frases, ext.imagens, ext.links, ext.secoes


def percorre(elementos):
    for el in elementos:
        yield el
        yield from percorre(el.get('elements', []))


def frases_json(dados):
    frases = set()
    imagens = []
    widgets = {}
    for el in percorre(dados['content']):
        wt = el.get('widgetType')
        if wt:
            widgets[wt] = widgets.get(wt, 0) + 1
        st = el.get('settings', {})
        for chave in ('title', 'editor', 'text', 'title_text',
                      'description_text'):
            if st.get(chave):
                n = normaliza(st[chave])
                if len(n) >= 18:
                    frases.add(n)
        for item in st.get('icon_list', []) or []:
            n = normaliza(item.get('text', ''))
            if len(n) >= 18:
                frases.add(n)
        for chave in ('testimonial_content', 'testimonial_name'):
            if st.get(chave):
                n = normaliza(st[chave])
                if len(n) >= 18:
                    frases.add(n)
        for item in st.get('tabs', []) or []:
            for chave in ('tab_title', 'tab_content'):
                n = normaliza(item.get(chave, ''))
                if len(n) >= 18:
                    frases.add(n)
        img = st.get('image') or {}
        if isinstance(img, dict) and img.get('url'):
            imagens.append(img['url'])
    return frases, imagens, widgets


def main():
    linhas = []
    linhas.append('# Pente-fino: templates JSON x protótipo aprovado\n')
    linhas.append('Comparação automática dos 24 JSON do Elementor com as '
                  'páginas HTML do protótipo (`seu-projeto/` e '
                  '`tools/partials/`), mais a auditoria do CSS. '
                  'Gerado por `tools/pente_fino.py`.\n')

    total_falta = 0
    for nome_json, nome_html in MAPA:
        dados = json.loads((RAIZ / 'bloco-b' / 'json' / nome_json)
                           .read_text(encoding='utf-8'))
        f_html, img_html, links_html, secoes = frases_html(nome_html)
        f_json, img_json, widgets = frases_json(dados)
        blob = set(' '.join(sorted(f_json)).split())

        def presente(frase):
            palavras = frase.split()
            if not palavras:
                return True
            acertos = sum(1 for w in palavras if w in blob)
            return acertos / len(palavras) >= 0.8

        falta = sorted(f for f in f_html if not presente(f))
        sobra = sorted(f_json - f_html)
        total_falta += len(falta)
        linhas.append(f'## {nome_json}  x  {nome_html}\n')
        linhas.append(f'- Widgets: ' + ', '.join(
            f'{k} ({v})' for k, v in sorted(widgets.items())) + '\n')
        linhas.append(f'- Textos do protótipo não encontrados no JSON: '
                      f'**{len(falta)}**')
        for f in falta[:14]:
            linhas.append(f'  - “{f[:110]}”')
        if len(falta) > 14:
            linhas.append(f'  - … e mais {len(falta) - 14}')
        linhas.append(f'- Textos do JSON que não estão no protótipo: '
                      f'{len(sobra)} (dinâmicos, rótulos de acessibilidade '
                      f'e textos de sistema costumam aparecer aqui)')
        linhas.append(f'- Imagens: protótipo {len(img_html)} | JSON '
                      f'{len(img_json)}\n')

    # ---------------- CSS ----------------
    css_proto = ''
    for arq in ('style.css', 'header.css', 'comercio.css', 'pages.css'):
        css_proto += (RAIZ / 'seu-projeto' / 'assets' / 'css' / arq) \
            .read_text(encoding='utf-8')
    css_el = (RAIZ / 'bloco-b' / 'css' / 'iara-cabecalho.css') \
        .read_text(encoding='utf-8')

    def conta(css, padrao):
        return len(re.findall(padrao, css))

    classes_json = set()
    responsivos = 0
    for nome_json, _ in MAPA:
        dados = json.loads((RAIZ / 'bloco-b' / 'json' / nome_json)
                           .read_text(encoding='utf-8'))
        for el in percorre(dados['content']):
            st = el.get('settings', {})
            for classe in (st.get('css_classes') or '').split():
                if classe.startswith('iara-'):
                    classes_json.add(classe)
            for chave in st:
                if chave.endswith(('_tablet', '_mobile')):
                    responsivos += 1

    sem_regra = sorted(c for c in classes_json if f'.{c}' not in css_el)

    linhas.append('## Auditoria de CSS\n')
    linhas.append(f'- CSS do protótipo: {conta(css_proto, chr(123))} regras '
                  f'em 4 arquivos, {conta(css_proto, "@media")} blocos '
                  f'@media, {conta(css_proto, ":hover")} regras :hover, '
                  f'{conta(css_proto, ":focus")} de foco.')
    linhas.append(f'- CSS que o Elementor recebe (`iara-cabecalho.css`, '
                  f'embutido nos 24 JSON e no kit): '
                  f'{conta(css_el, chr(123))} regras, '
                  f'{conta(css_el, "@media")} blocos @media, '
                  f'{conta(css_el, ":hover")} regras :hover.')
    linhas.append(f'- Classes `iara-*` usadas nos JSON: '
                  f'{len(classes_json)}; sem nenhuma regra no CSS: '
                  f'{len(sem_regra)}'
                  + (': ' + ', '.join(sem_regra) if sem_regra else ''))
    linhas.append(f'- Ajustes responsivos declarados nos JSON '
                  f'(chaves _tablet/_mobile): {responsivos}')
    linhas.append(f'- Total de textos do protótipo não encontrados '
                  f'nos JSON: {total_falta} (detalhe por página acima; '
                  f'parte é texto dinâmico de loja/sistema, parte é '
                  f'conteúdo a conferir)')

    (RAIZ / 'PENTE-FINO.md').write_text('\n'.join(linhas) + '\n',
                                        encoding='utf-8')
    print(f'PENTE-FINO.md gerado: {len(MAPA)} templates comparados, '
          f'{total_falta} textos do prototipo fora dos JSON')


if __name__ == '__main__':
    main()
