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


def nav_markup(header: str, nav_key: str) -> str:
    """Marca o item de menu da página atual com aria-current (o CSS usa isso)."""
    if not nav_key:
        return header
    return header.replace(f'data-nav="{nav_key}"', f'data-nav="{nav_key}" aria-current="page"')


def cart_markup(header: str, count: int) -> str:
    """Preenche o contador da sacola no header e no painel mobile."""
    if count <= 0:
        label = "nenhum item"
    elif count == 1:
        label = "1 item"
    else:
        label = f"{count} itens"
    return header.replace("{{CART_COUNT}}", str(count)).replace("{{CART_LABEL}}", label)


def asset_version(path: pathlib.Path) -> str:
    """Versão curta (hash do conteúdo) para forçar o navegador a baixar o arquivo
    quando ele muda. Sem isso, o navegador pode servir CSS/JS antigos e o site
    parece 'quebrado' mesmo com o arquivo novo no servidor."""
    import hashlib

    if not path.exists():
        return "0"
    return hashlib.md5(path.read_bytes()).hexdigest()[:8]


def page_html(meta: dict, header: str, footer: str, content: str) -> str:
    extra_css = meta.get("extra_css", [])
    extra_js = meta.get("extra_js", [])

    css_files = ["style.css", "header.css", "pages.css"] + extra_css
    js_files = ["header.js"] + extra_js

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

    built, skipped = [], []
    for meta in pages:
        if args.part and meta.get("part") != args.part:
            continue
        content_path = ROOT / "content" / meta["content"]
        if not content_path.exists():
            skipped.append(meta["file"])
            continue
        content = content_path.read_text(encoding="utf-8")
        header = cart_markup(nav_markup(header_tpl, meta.get("nav", "")), meta.get("cart_count", 0))
        html = page_html(
            meta,
            header,
            footer_tpl,
            content,
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
