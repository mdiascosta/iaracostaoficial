#!/usr/bin/env python3
"""
Verificação automática do protótipo (o "VERIFICADO" do Diário de Bordo).

Checa, sem navegador:
1. Tags HTML balanceadas em cada página.
2. Todo arquivo referenciado em src/href existe no projeto.
3. Um único H1 por página.
4. Toda <img> tem atributo alt (mesmo que vazio, quando decorativa).
5. Nenhum HTML de widget/código colado indevidamente (contagem de <script> inline).
6. Nenhuma ocorrência de travessão (—) em textos de site.

Uso: python3 tools/check.py
"""

import html.parser
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
PROJECT = ROOT.parent / "seu-projeto"

VOID = {
    "area", "base", "br", "col", "embed", "hr", "img", "input",
    "link", "meta", "param", "source", "track", "wbr",
}


class Checker(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.errors = []
        self.h1 = 0
        self.img_without_alt = 0
        self.refs = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)

        if tag == "h1":
            self.h1 += 1

        if tag == "img" and "alt" not in attrs:
            self.img_without_alt += 1

        for key in ("src", "href"):
            value = attrs.get(key, "")
            if value and not value.startswith(("#", "http", "mailto:", "tel:", "data:")):
                self.refs.append(value)

        if tag not in VOID:
            self.stack.append((tag, self.getpos()[0]))

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if not self.stack:
            self.errors.append(f"linha {self.getpos()[0]}: </{tag}> sem abertura")
            return
        open_tag, line = self.stack.pop()
        if open_tag != tag:
            self.errors.append(
                f"linha {self.getpos()[0]}: esperava </{open_tag}> (aberta na linha {line}), veio </{tag}>"
            )


def planned_pages() -> set:
    """Páginas previstas em pages.json. Links para páginas ainda não geradas
    (das próximas partes) são pendência, não erro."""
    import json

    data = json.loads((ROOT / "pages.json").read_text(encoding="utf-8"))
    return {item["file"] for item in data}


def main() -> int:
    pages = sorted(PROJECT.glob("*.html"))
    if not pages:
        print("nenhuma página encontrada")
        return 1

    problems = 0
    pending = []

    for page in pages:
        source = page.read_text(encoding="utf-8")
        checker = Checker()
        checker.feed(source)

        unclosed = [f"<{tag}> linha {line}" for tag, line in checker.stack]

        if checker.errors or unclosed:
            problems += 1
            print(f"[ERRO] {page.name}")
            for item in checker.errors:
                print(f"       {item}")
            for item in unclosed:
                print(f"       não fechada: {item}")

        if checker.h1 != 1:
            problems += 1
            print(f"[ERRO] {page.name}: {checker.h1} elemento(s) h1 (esperado 1)")

        if checker.img_without_alt:
            problems += 1
            print(f"[ERRO] {page.name}: {checker.img_without_alt} img sem alt")

        planejadas = planned_pages()

        for ref in sorted(set(checker.refs)):
            arquivo = ref.split("?")[0]
            target = (page.parent / arquivo).resolve()
            if target.exists():
                continue
            if arquivo in planejadas:
                pending.append(arquivo)
            else:
                problems += 1
                print(f"[ERRO] {page.name}: referência quebrada -> {ref}")

        inline_scripts = len(re.findall(r"<script(?![^>]*\bsrc=)[^>]*>", source))
        if inline_scripts:
            problems += 1
            print(f"[ERRO] {page.name}: {inline_scripts} script inline (Bloco A usa só arquivos .js)")

        if "—" in source:
            problems += 1
            print(f"[ERRO] {page.name}: travessão (—) encontrado; usar vírgula ou ponto")

    print()
    print(f"páginas verificadas: {len(pages)}")

    if pending:
        unicas = sorted(set(pending))
        print(f"pendentes (páginas previstas para as próximas partes): {len(unicas)}")
        print("  " + ", ".join(unicas))

    print("resultado:", "tudo certo" if problems == 0 else f"{problems} problema(s)")

    return 0 if problems == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
