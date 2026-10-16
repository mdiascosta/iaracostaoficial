#!/usr/bin/env python3
"""
Gera as imagens de exemplo (SVG) do protótipo Iara Costa.

Por que SVG e não foto: a equipe ainda não tem as fotos reais (resposta q2 da
E0). Um placeholder em SVG deixa claro que ali vai entrar foto, pesa pouquíssimo
e é fácil de trocar: basta subir a foto real com o mesmo nome de arquivo.

Todas as peças levam a etiqueta "SUBSTITUIR" e o tamanho recomendado, para que
nenhuma imagem de exemplo chegue à produção por descuido.

Uso: python3 tools/make_placeholders.py
"""

import pathlib

ROOT = pathlib.Path(__file__).resolve().parent
IMG = ROOT.parent / "seu-projeto" / "assets" / "img"

PAPER = "#fffdf9"
LINE = "#ded8ce"
INK_SOFT = "#625a52"
MUTED = "#81786e"
ACCENT = "#a45f43"
ACCENT_SOFT = "#e4cbb5"
HAIRLINE = "#eee9e1"


def svg(width, height, label, note, tone=PAPER, ink=INK_SOFT):
    """Placeholder neutro: fundo do papel, moldura fina, rótulo e nota."""
    unit = min(width, height)
    title_size = max(18, round(unit * 0.045))
    note_size = max(12, round(unit * 0.024))
    tag_size = max(11, round(unit * 0.018))
    ratio = f"{width}x{height}"
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="Imagem de exemplo: {label}">
  <rect width="{width}" height="{height}" fill="{tone}"/>
  <rect x="1" y="1" width="{width - 2}" height="{height - 2}" fill="none" stroke="{LINE}" stroke-width="2"/>
  <circle cx="{width / 2}" cy="{height / 2 - unit * 0.13:.0f}" r="{unit * 0.055:.0f}" fill="none" stroke="{ACCENT_SOFT}" stroke-width="2"/>
  <path d="M{width / 2 - unit * 0.035:.0f} {height / 2 - unit * 0.10:.0f} l{unit * 0.07:.0f} 0 l0 {unit * 0.055:.0f} l-{unit * 0.07:.0f} 0 z" fill="none" stroke="{ACCENT_SOFT}" stroke-width="2"/>
  <text x="50%" y="{height / 2 + unit * 0.02:.0f}" text-anchor="middle" font-family="Helvetica Neue, Arial, sans-serif" font-size="{title_size}" letter-spacing="2" fill="{ink}">{label}</text>
  <text x="50%" y="{height / 2 + unit * 0.075:.0f}" text-anchor="middle" font-family="Helvetica Neue, Arial, sans-serif" font-size="{note_size}" fill="{MUTED}">{note}</text>
  <text x="50%" y="{height / 2 + unit * 0.115:.0f}" text-anchor="middle" font-family="Helvetica Neue, Arial, sans-serif" font-size="{tag_size}" letter-spacing="3" fill="{ACCENT}">SUBSTITUIR POR FOTO REAL · {ratio}</text>
</svg>
"""


FAVICON = f"""<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 512 512" role="img" aria-label="Marca Iara Costa">
  <rect width="512" height="512" fill="{PAPER}"/>
  <rect x="6" y="6" width="500" height="500" fill="none" stroke="{LINE}" stroke-width="6"/>
  <text x="50%" y="52%" text-anchor="middle" font-family="Georgia, Times New Roman, serif" font-size="184" letter-spacing="6" fill="{ACCENT}">IC</text>
  <text x="50%" y="70%" text-anchor="middle" font-family="Helvetica Neue, Arial, sans-serif" font-size="34" letter-spacing="8" fill="{INK_SOFT}">IARA COSTA</text>
</svg>
"""


def main() -> int:
    IMG.mkdir(parents=True, exist_ok=True)
    files = {"favicon.svg": FAVICON}

    # 1. Produtos: 10 itens, 3 ângulos cada (quadradas 1:1 conforme F2)
    for n in range(1, 11):
        for angle in ("a", "b", "c"):
            files[f"produto-{n:02d}-{angle}.svg"] = svg(
                1600, 1600,
                f"PRODUTO {n:02d} · ângulo {angle.upper()}",
                "Foto do produto, fundo claro consistente",
            )

    # 2. Categorias (4:5)
    for slug, nome in (
        ("vestidos", "VESTIDOS"),
        ("blusas", "BLUSAS E CAMISAS"),
        ("calcas", "CALÇAS E SAIAS"),
        ("acessorios", "ACESSÓRIOS"),
    ):
        files[f"categoria-{slug}.svg"] = svg(
            800, 1000, nome, "Foto da categoria, atmosfera da marca", tone=HAIRLINE
        )

    # 3. Banners do topo
    files["banner-home-desktop.svg"] = svg(
        1920, 800, "BANNER PRINCIPAL · DESKTOP", "Campanha atual, sem excesso de texto", tone=HAIRLINE
    )
    files["banner-home-mobile.svg"] = svg(
        800, 1000, "BANNER PRINCIPAL · CELULAR", "Versão vertical do mesmo banner", tone=HAIRLINE
    )

    # 4. Blocos editoriais
    files["editorial-atelie.svg"] = svg(
        1200, 1200, "ATELIÊ / DETALHE DE TECIDO", "Foto de apoio do bloco Como escolher"
    )
    files["sobre-atelie.svg"] = svg(1600, 900, "SOBRE · HISTÓRIA DA MARCA", "Foto ampla da marca ou da equipe")

    # 5. Blog
    for n in range(1, 4):
        files[f"blog-destaque-{n:02d}.svg"] = svg(
            1600, 900, f"IMAGEM DE DESTAQUE · POST {n:02d}", "Foto relacionada ao tema do texto"
        )

    # 6. Lookbook (4:5)
    for n in range(1, 5):
        files[f"lookbook-{n:02d}.svg"] = svg(
            1200, 1500, f"LOOK {n:02d}", "Produção de moda com as peças da coleção"
        )

    # 7. Compartilhamento social
    files["compartilhamento-social.svg"] = svg(
        1200, 630, "COMPARTILHAMENTO SOCIAL", "1200x630, logo + foto da marca"
    )

    for name, content in files.items():
        (IMG / name).write_text(content, encoding="utf-8")

    print(f"{len(files)} imagens de exemplo geradas em {IMG.relative_to(ROOT.parent)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
