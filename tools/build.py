#!/usr/bin/env python3
"""
Gerador do protótipo HTML (Bloco A / Etapa E1) - Iara Costa.

Por que existe: as 22 páginas do protótipo compartilham o MESMO header e footer.
Se cada página tivesse o header copiado, uma correção exigiria editar 22 arquivos.
Aqui o header/footer ficam em tools/partials/ e o script monta as páginas finais
em seu-projeto/.

Uso:  python3 tools/build.py            (gera todas as páginas de todos os blocos)
      python3 tools/build.py --part 1   (gera somente a Parte 1)
      python3 tools/build.py --check    (só relata o que seria gerado)

O HTML gerado é o entregável. O time da Iara Costa pode editar as páginas finais
direto se preferir; neste caso, para não sobrescrever, rode --check antes.
"""

import argparse
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent
PROJECT = ROOT.parent / "seu-projeto"

# Aviso de protótipo que aparece no topo de todas as páginas.
# Remover em produção: é o Bloco B (Elementor) que vai ao ar, não este protótipo.
PROTO_BANNER = (
    '<div class="proto-banner" role="note">'
    "PROTÓTIPO · DADOS E TEXTOS DE EXEMPLO · NÃO PUBLICAR"
    "</div>"
)


def load(name: str) -> str:
    return (ROOT / "partials" / name).read_text(encoding="utf-8")


# --------------------------------------------------------------- CARDÚNICO
# Uma loja repete o mesmo card de produto em várias páginas. Se o card fosse
# copiado em cada arquivo, mudar o preço exigiria editar 8 lugares. Aqui o
# desenho do card vive em tools/partials/card.html e os dados em
# tools/produtos.json: a página escreve <!--CARD:slug--> e o gerador monta.

def carregar_produtos() -> dict:
    dados = json.loads((ROOT / "produtos.json").read_text(encoding="utf-8"))
    catalogo = {}
    for posicao, produto in enumerate(dados, start=1):
        # "ordem" preserva a sequência de Destaques na loja (filtros.js usa
        # data-ordem para o critério "Destaques").
        produto["ordem"] = posicao
        catalogo[produto["slug"]] = produto
    return catalogo


def estrelas(nota: int) -> str:
    """Estrelas cheias e vazias. A última vazia vai com aria-hidden para o
    leitor de tela não ler 'estrela estrela estrela'."""
    cheias = max(0, min(5, int(nota)))
    if cheias == 5:
        return "★" * 5
    return "★" * cheias + '<span aria-hidden="true">' + "★" * (5 - cheias) + "</span>"


def preco_html(produto: dict) -> str:
    de = produto.get("preco_de", "")
    if de:
        return f'<del>{de}</del>{produto["preco"]}'
    return produto["preco"]


def render_card(slug: str, produto: dict, nivel: str = "h3") -> str:
    badge = ""
    if produto.get("badge"):
        classe = "badge badge--promo" if produto["badge"].lower() == "oferta" else "badge"
        badge = f'\n          <span class="{classe}">{produto["badge"]}</span>'

    promo = " card__price--promo" if produto.get("preco_de") else ""

    preco_num = produto["preco"].replace("R$ ", "").replace(".", "").replace(",", ".")

    return f"""<li class="card" data-categoria="{produto['categoria_slug']}" data-preco="{preco_num}" data-nome="{produto['nome']}" data-ordem="{produto.get('ordem', 0)}">
          <a class="card__media" href="produto.html" aria-label="Ver {produto['nome']}">{badge}
            <img class="card__img" src="assets/img/{produto['img']}" alt="{produto['alt']}"
                 width="800" height="1000" loading="lazy" decoding="async">
          </a>
          <button class="card__wish" type="button" data-wish="{slug}" aria-pressed="false"
                  aria-label="Salvar {produto['nome']} nos desejos">
            <svg viewBox="0 0 24 24" width="17" height="17" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true" focusable="false"><path d="M12 20.5C7 16.5 3.5 13.3 3.5 9.6 3.5 7 5.5 5 8 5c1.6 0 3.1.9 4 2.3C12.9 5.9 14.4 5 16 5c2.5 0 4.5 2 4.5 4.6 0 3.7-3.5 6.9-8.5 10.9Z"></path></svg>
          </button>
          <div class="card__body">
            <p class="card__cat">{produto['categoria']}</p>
            <{nivel} class="card__name"><a href="produto.html">{produto['nome']}</a></{nivel}>
            <p class="card__rating">
              <span class="stars" role="img" aria-label="Avaliação {produto['avaliacoes'].split(' · ')[0]} de 5">{estrelas(produto['estrelas'])}</span>
              {produto['avaliacoes']}
            </p>
            <p class="card__price{promo}">{preco_html(produto)}</p>
            <p class="card__sizes">{produto['tamanhos']}</p>
            <p class="card__add"><a class="link-underline" href="carrinho.html" data-add="{slug}">Adicionar à sacola</a></p>
          </div>
        </li>"""


def expandir_cards(html: str, produtos: dict) -> str:
    """Troca <!--CARD:slug--> e <!--CARD:slug:2--> pelo card montado."""
    import re

    def troca(match):
        partes = match.group(1).split(":")
        slug = partes[0]
        nivel = "h" + partes[1] if len(partes) > 1 and partes[1] in "234" else "h3"

        if slug not in produtos:
            raise SystemExit(f"erro: produto '{slug}' não existe em tools/produtos.json")

        return render_card(slug, produtos[slug], nivel)

    html = re.sub(r"<!--CARD:([a-z0-9-]+(?::[234])?)-->", troca, html)

    # <!--CARDS:a,b,c--> monta vários com indentação uniforme
    def troca_varios(match):
        slugs = [s.strip() for s in match.group(1).split(",") if s.strip()]
        blocos = []
        for slug in slugs:
            if slug not in produtos:
                raise SystemExit(f"erro: produto '{slug}' não existe em tools/produtos.json")
            blocos.append(render_card(slug, produtos[slug], "h3"))
        return "\n        ".join(blocos)

    return re.sub(r"<!--CARDS:([a-z0-9,\s-]+)-->", troca_varios, html)


def nav_markup(header: str, nav_key: str) -> str:
    """Marca o item de menu da página atual com aria-current (o CSS usa isso)."""
    if not nav_key:
        return header
    return header.replace(f'data-nav="{nav_key}"', f'data-nav="{nav_key}" aria-current="page"')


def cart_markup(header: str, count: int) -> str:
    """Preenche os contadores da sacola e dos desejos no header e no menu mobile."""
    if count <= 0:
        label = "nenhum item"
    elif count == 1:
        label = "1 item"
    else:
        label = f"{count} itens"
    return (
        header.replace("{{CART_COUNT}}", str(count))
        .replace("{{CART_LABEL}}", label)
        .replace("{{WISH_COUNT}}", "0")
    )


def asset_version(path: pathlib.Path) -> str:
    """Versão curta (hash do conteúdo) para forçar o navegador a baixar o arquivo
    quando ele muda. Sem isso, o navegador pode servir CSS/JS antigos e o site
    parece 'quebrado' mesmo com o arquivo novo no servidor."""
    import hashlib

    if not path.exists():
        return "0"
    return hashlib.md5(path.read_bytes()).hexdigest()[:8]


def page_html(meta: dict, header: str, footer: str, content: str, drawer: str) -> str:
    extra_css = meta.get("extra_css", [])
    extra_js = meta.get("extra_js", [])

    css_files = ["style.css", "header.css", "pages.css", "comercio.css"] + extra_css
    js_files = ["header.js", "loja.js"] + extra_js

    css_links = "\n".join(
        f'  <link rel="stylesheet" href="assets/css/{f}?v={asset_version(PROJECT / "assets" / "css" / f)}">'
        for f in css_files
    )
    js_tags = "\n".join(
        f'<script src="assets/js/{f}?v={asset_version(PROJECT / "assets" / "js" / f)}" defer></script>'
        for f in js_files
    )
    body_class = meta.get("body_class", "")
    return f"""<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{meta['title']}</title>
  <meta name="description" content="{meta['desc']}">
  <!-- Protótipo: não deve ser indexado. Em produção o controle é do Yoast. -->
  <meta name="robots" content="noindex, nofollow">
  <link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <!-- PRODUÇÃO: hospedar as fontes localmente (ver assets/fonts/LEIA-ME.md) -->
  <link href="https://fonts.googleapis.com/css2?family=Jost:wght@400;600&amp;family=Playfair+Display:wght@400&amp;display=swap" rel="stylesheet">
{css_links}
</head>
<body class="{body_class}">
{PROTO_BANNER}
{header}
  <main id="conteudo" tabindex="-1">
{content}
  </main>
{footer}
{drawer}
{js_tags}
</body>
</html>
"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--part", type=int, default=None, help="gerar somente uma parte")
    ap.add_argument("--check", action="store_true", help="não escreve, só relata")
    args = ap.parse_args()

    pages = json.loads((ROOT / "pages.json").read_text(encoding="utf-8"))
    header_tpl = load("header.html")
    footer_tpl = load("footer.html")
    drawer_tpl = load("drawer.html")
    produtos = carregar_produtos()

    built, skipped = [], []
    for meta in pages:
        if args.part and meta.get("part") != args.part:
            continue
        content_path = ROOT / "content" / meta["content"]
        if not content_path.exists():
            skipped.append(meta["file"])
            continue
        content = expandir_cards(content_path.read_text(encoding="utf-8"), produtos)
        header = cart_markup(nav_markup(header_tpl, meta.get("nav", "")), meta.get("cart_count", 0))
        html = page_html(
            meta,
            header,
            footer_tpl,
            content,
            drawer_tpl,
        )
        if not args.check:
            out = PROJECT / meta["file"]
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(html, encoding="utf-8")
        built.append(meta["file"])

    print(f"geradas: {len(built)}")
    for f in built:
        print(f"  ok  {f}")
    if skipped:
        print(f"sem conteúdo ainda (chegam nas próximas partes): {len(skipped)}")
        for f in skipped:
            print(f"  --  {f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
