#!/usr/bin/env python3
"""Prévia local dos templates Elementor (bloco-b/json/*.json).

Lê os mesmos JSON que iriam para o WordPress e desenha uma página HTML
que aproxima a renderização do Elementor: resolve cores globais, aplica
a tipografia embutida em cada widget e inclui o CSS geral do kit
(bloco-b/css/iara-cabecalho.css), para os estados do menu (hover/ativo),
os ícones e as listas se comportarem como no site.

Serve para conferir o resultado ANTES de importar qualquer coisa no
WordPress. Não é o Elementor: widgets de loja/produto do WooCommerce e
similares aparecem como blocos rotulados, e detalhes de espaçamento
podem diferir um pouco da renderização real.

Uso:  python3 tools/blocob_preview.py [01 02 03]     (padrão: 01 02 03)
Saída: preview/index.html
"""
import html
import json
import pathlib
import sys

RAIZ = pathlib.Path(__file__).resolve().parent.parent
JSON_DIR = RAIZ / 'bloco-b' / 'json'
SAIDA = RAIZ / 'preview'


def carrega_cores():
    ref = json.loads((RAIZ / 'bloco-b' / 'globais' / 'cores-e-fontes.json')
                     .read_text(encoding='utf-8'))
    cores = {}
    for grupo in ('system_colors', 'custom_colors'):
        for item in ref['settings'].get(grupo, []):
            cores[item['_id']] = item['color']
    base = ['primary', 'secondary', 'text', 'accent']
    for i, apelido in enumerate(('globals/colors?id=primary',
                                 'globals/colors?id=secondary',
                                 'globals/colors?id=text',
                                 'globals/colors?id=accent')):
        pass
    return cores


CORES = carrega_cores()


def cor(st, chave):
    """Cor efetiva: global referenciada ou valor direto."""
    ref = st.get('__globals__', {}).get(chave, '')
    if ref.startswith('globals/colors?id='):
        return CORES.get(ref.split('id=')[-1], '')
    valor = st.get(chave, '')
    return valor if isinstance(valor, str) and valor.startswith('#') else ''


def medida(v):
    if isinstance(v, dict):
        tamanho = v.get('size', '')
        return f'{tamanho}{v.get("unit", "px")}' if tamanho != '' else ''
    return ''


def css_tipografia(st, prefixo):
    partes = []
    fam = st.get(f'{prefixo}_font_family')
    if fam:
        partes.append(f"font-family:'{fam}',sans-serif")
    peso = st.get(f'{prefixo}_font_weight')
    if peso:
        partes.append(f'font-weight:{peso}')
    tam = medida(st.get(f'{prefixo}_font_size', {}))
    if tam:
        partes.append(f'font-size:{tam}')
    lh = medida(st.get(f'{prefixo}_line_height', {}))
    if lh:
        partes.append(f'line-height:{lh}')
    ls = medida(st.get(f'{prefixo}_letter_spacing', {}))
    if ls:
        partes.append(f'letter-spacing:{ls}')
    caixa = st.get(f'{prefixo}_text_transform')
    if caixa:
        partes.append(f'text-transform:{caixa}')
    estilo = st.get(f'{prefixo}_font_style')
    if estilo:
        partes.append(f'font-style:{estilo}')
    return ';'.join(partes)


def estilo_container(st):
    partes = ['display:flex']
    direcao = st.get('flex_direction')
    if direcao:
        partes.append(f'flex-direction:{direcao}')
    if st.get('flex_justify_content'):
        partes.append(f"justify-content:{st['flex_justify_content']}")
    if st.get('flex_align_items'):
        partes.append(f"align-items:{st['flex_align_items']}")
    gap = st.get('flex_gap', {}) or {}
    if gap.get('size'):
        partes.append(f"gap:{gap['size']}px")
    pad = st.get('padding', {}) or {}
    if pad:
        partes.append('padding:%spx %spx %spx %spx' % (
            pad.get('top', 0) or 0, pad.get('right', 0) or 0,
            pad.get('bottom', 0) or 0, pad.get('left', 0) or 0))
    fundo = cor(st, 'background_color')
    if fundo:
        partes.append(f'background:{fundo}')
    base = st.get('_flex_basis', {}) or {}
    if base.get('size'):
        partes.append(f"flex:0 0 {base['size']}{base.get('unit', '%')}")
    if st.get('_flex_size') == 'grow':
        partes.append('flex:1 1 auto')
    if st.get('flex_wrap') == 'wrap':
        partes.append('flex-wrap:wrap')
    raio = st.get('border_radius', {}) or {}
    if raio.get('top'):
        partes.append(f"border-radius:{raio['top']}px")
    if st.get('content_width') == 'boxed':
        partes.append('max-width:1688px;margin-inline:auto;width:100%')
    bw = st.get('border_width', {}) or {}
    bc = cor(st, 'border_color')
    if st.get('border_border') == 'solid' and bc:
        partes.append('border:%spx solid %s' % (bw.get('bottom', 0) or 0, bc))
    return ';'.join(partes)


def icone_fa(selected, tamanho=''):
    if not selected:
        return ''
    valor = selected.get('value', '')
    if not valor:
        return ''
    return ('<i class="%s" style="font-size:%s"></i>'
            % (html.escape(valor), tamanho or '1em'))


def widget(el):
    tipo = el.get('widgetType')
    st = el.get('settings', {})
    classe = html.escape(st.get('css_classes', ''))
    titulo = html.escape(st.get('_title', tipo or ''))

    if tipo == 'heading':
        tag = st.get('header_size', 'h2')
        if tag not in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'span', 'div'):
            tag = 'h2'
        estilo = css_tipografia(st, 'typography')
        c = cor(st, 'title_color')
        if c:
            estilo += f';color:{c}'
        alin = st.get('align')
        if alin:
            estilo += f';text-align:{alin}'
        texto = html.escape(st.get('title', ''))
        link = (st.get('link') or {}).get('url')
        inner = (f'<a href="{html.escape(link)}" style="color:inherit;'
                 f'text-decoration:none">{texto}</a>' if link else texto)
        return (f'<{tag} class="pv-heading {classe}" '
                f'style="{estilo}">{inner}</{tag}>')

    if tipo == 'text-editor':
        estilo = css_tipografia(st, 'typography')
        c = cor(st, 'text_color')
        if c:
            estilo += f';color:{c}'
        alin = st.get('align')
        if alin:
            estilo += f';text-align:{alin}'
        corpo = st.get('editor') or st.get('text') or ''
        return f'<div class="pv-texto {classe}" style="{estilo}">{corpo}</div>'

    if tipo == 'icon':
        c = cor(st, 'primary_color')
        tam = medida(st.get('size', {})) or '17px'
        link = (st.get('link') or {}).get('url', '#')
        return (f'<a class="elementor-icon {classe}" href="{html.escape(link)}" '
                f'title="{titulo}" style="--pv-cor:{c}">'
                f'{icone_fa(st.get("selected_icon"), tam)}</a>')

    if tipo == 'icon-list':
        estilo = css_tipografia(st, 'icon_typography')
        texto_c = cor(st, 'text_color') or cor(st, 'icon_color')
        icone_c = cor(st, 'icon_color')
        inline = st.get('view') == 'inline'
        itens = []
        for item in st.get('icon_list', []):
            ic = icone_fa(item.get('selected_icon'))
            txt = html.escape(item.get('text', ''))
            link = (item.get('link') or {}).get('url')
            conteudo = (f'<span class="elementor-icon-list-icon">{ic}</span>'
                        f'<span class="elementor-icon-list-text">{txt}</span>')
            if link:
                conteudo = (f'<a href="{html.escape(link)}" '
                            f'style="color:inherit;text-decoration:none;'
                            f'display:inline-flex;gap:6px;align-items:center">'
                            f'{conteudo}</a>')
            itens.append(f'<li class="elementor-icon-list-item" '
                         f'style="{estilo};color:{texto_c}">{conteudo}</li>')
        direcao = 'row;flex-wrap:wrap' if inline else 'column'
        return (f'<ul class="pv-lista {classe}" style="display:flex;'
                f'flex-direction:{direcao};gap:{medida(st.get("space_between", {})) or "8px"};'
                f'list-style:none;margin:0;padding:0">{"".join(itens)}</ul>')

    if tipo == 'nav-menu':
        estilo = css_tipografia(st, 'menu_typography')
        itens = [('Home', True), ('Loja', False), ('Sobre', False),
                 ('Coleção', False), ('Contato', False)]
        links = ''.join(
            '<li class="menu-item"><a href="#" class="elementor-item%s" '
            'style="%s">%s</a></li>'
            % (' elementor-item-active' if ativo else '', estilo, nome)
            for nome, ativo in itens)
        # Estrutura igual a que o Elementor gera: a classe iara-menu-nav
        # fica no envoltório do widget e a lista .elementor-nav-menu--main
        # vem DENTRO dele. Sem isso, os seletores do CSS do kit
        # (.iara-menu-nav .elementor-nav-menu--main .elementor-item) nao
        # casam e o link fica no padrao azul do navegador, sem hover.
        return (f'<div class="iara-menu-nav {classe}" style="flex:1 1 auto">'
                f'<ul class="elementor-nav-menu--main" style="display:flex;'
                f'gap:28px;list-style:none;margin:0;padding:0;'
                f'justify-content:center">{links}</ul></div>')

    if tipo == 'form':
        campo = (st.get('form_fields') or [{}])[0]
        return (f'<form class="{classe}" style="display:flex;gap:10px;'
                f'flex:1 1 auto;max-width:520px" onsubmit="return false">'
                f'<input type="email" required placeholder="'
                f'{html.escape(campo.get("placeholder", "seu@email.com"))}" '
                f'style="flex:1;padding:12px 14px;border:1px solid #ded8ce;'
                f'border-radius:6px;font-family:Jost,sans-serif;'
                f'font-size:14px;background:#fff">'
                f'<button style="background:#a45f43;color:#fffdf9;border:0;'
                f'border-radius:6px;padding:12px 22px;font-family:Jost;'
                f'font-size:12px;font-weight:600;letter-spacing:.14em;'
                f'text-transform:uppercase;cursor:pointer">'
                f'{html.escape(st.get("button_text", "Assinar"))}</button></form>')

    if tipo == 'woocommerce-menu-cart':
        return ('<a class="elementor-icon iara-sacola" href="#" title="Sacola" '
                'style="position:relative"><i class="fas fa-shopping-bag" '
                'style="font-size:17px"></i>'
                '<span style="position:absolute;top:-4px;right:-6px;'
                'background:#a45f43;color:#fffdf9;font-size:10px;'
                'font-weight:600;min-width:16px;height:16px;line-height:16px;'
                'border-radius:50%;text-align:center">2</span></a>')

    if tipo == 'wp-widget-widget_top_wishlist':
        return ('<a class="elementor-icon iara-desejos" href="#" '
                'title="Lista de desejos" style="position:relative">'
                '<i class="far fa-heart" style="font-size:17px"></i>'
                '<span style="position:absolute;top:-4px;right:-6px;'
                'background:#a45f43;color:#fffdf9;font-size:10px;'
                'font-weight:600;min-width:16px;height:16px;line-height:16px;'
                'border-radius:50%;text-align:center">3</span></a>')

    if tipo == 'theme-site-logo':
        link = (st.get('link') or {}).get('url', '#')
        largura = (st.get('width') or {}).get('size', 210)
        return (f'<a href="{html.escape(link)}" class="{classe}">'
                f'<img src="logotipo.png" alt="Iara Costa" '
                f'style="width:{largura}px;height:auto;display:block"></a>')

    if tipo == 'button':
        estilo = css_tipografia(st, 'typography')
        fundo = cor(st, 'background_color')
        texto_c = cor(st, 'button_text_color') or cor(st, 'text_color')
        link = (st.get('link') or {}).get('url', '#')
        ic = icone_fa(st.get('selected_icon'), '16px')
        return (f'<a class="pv-botao {classe}" href="{html.escape(link)}" '
                f'style="{estilo};background:{fundo};color:{texto_c};'
                f'display:inline-flex;gap:8px;align-items:center;'
                f'padding:14px 26px;text-decoration:none">'
                f'{html.escape(st.get("text", "Botão"))} {ic}</a>')

    if tipo == 'image':
        img = st.get('image') or {}
        url = img.get('url', '') if isinstance(img, dict) else ''
        if not url:
            return (f'<div class="pv-falta">[imagem: {titulo}]</div>')
        link = (st.get('link') or {}).get('url')
        tag_img = (f'<img src="{html.escape(url)}" alt="" '
                   f'style="max-width:100%;height:auto;display:block">')
        if link:
            tag_img = f'<a href="{html.escape(link)}">{tag_img}</a>'
        return f'<div class="{classe}">{tag_img}</div>'

    if tipo in ('icon-box', 'image-box'):
        partes = []
        if tipo == 'image-box':
            img = st.get('image') or {}
            url = img.get('url', '') if isinstance(img, dict) else ''
            if url:
                partes.append(f'<img src="{html.escape(url)}" alt="" '
                              f'style="max-width:100%">')
        else:
            partes.append(icone_fa(st.get('selected_icon'), '26px'))
        tt = css_tipografia(st, 'title_typography')
        tc = cor(st, 'title_color')
        partes.append(f'<p style="{tt};color:{tc};margin:6px 0 2px">'
                      f'{html.escape(st.get("title_text", ""))}</p>')
        dt = css_tipografia(st, 'description_typography')
        dc = cor(st, 'description_color')
        partes.append(f'<p style="{dt};color:{dc};margin:0">'
                      f'{st.get("description_text", "")}</p>')
        return (f'<div class="pv-caixa {classe}" style="text-align:center;'
                f'flex:1 1 0">{"".join(partes)}</div>')

    if tipo == 'spacer':
        return (f'<div style="height:{medida(st.get("space", {})) or "20px"}">'
                f'</div>')

    if tipo == 'divider':
        return '<hr style="border:0;border-top:1px solid #ded8ce;margin:12px 0">'

    return (f'<div class="pv-falta">[{tipo}: {titulo}]</div>')


def elemento(el):
    if el.get('elType') == 'container':
        st = el.get('settings', {})
        filhos = ''.join(elemento(x) for x in el.get('elements', []))
        return (f'<div class="{html.escape(st.get("css_classes", ""))}" '
                f'style="{estilo_container(st)}">{filhos}</div>')
    return widget(el)


def pagina(arquivo):
    dados = json.loads((JSON_DIR / arquivo).read_text(encoding='utf-8'))
    corpo = ''.join(elemento(el) for el in dados['content'])
    return dados.get('title', arquivo), corpo


def main():
    numeros = sys.argv[1:] or ['01', '02', '03']
    todos = sorted(p.name for p in JSON_DIR.glob('*.json'))
    escolhidos = [n for n in todos
                  if any(n.startswith(num) for num in numeros)]
    css_kit = (RAIZ / 'bloco-b' / 'css' / 'iara-cabecalho.css') \
        .read_text(encoding='utf-8')

    secoes = []
    for arquivo in escolhidos:
        titulo, corpo = pagina(arquivo)
        secoes.append(
            f'<section class="pv-template"><h2 class="pv-rotulo">'
            f'{html.escape(titulo)} <small>({arquivo})</small></h2>'
            f'<div class="pv-folha">{corpo}</div></section>')

    doc = f'''<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Prévia dos templates: Iara Costa</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Jost:wght@300;400;500;600&family=Playfair+Display:ital,wght@0,400;0,500;1,400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css">
<style>
* {{ box-sizing: border-box; }}
body {{ margin:0; background:#e9e4db; font-family:'Jost',sans-serif; }}
.pv-aviso {{ max-width:1100px; margin:22px auto 6px; padding:0 20px;
  color:#2d2925; font-size:15px; line-height:1.55; }}
.pv-aviso b {{ color:#78452f; }}
.pv-template {{ max-width:1360px; margin:0 auto 40px; padding:0 20px; }}
.pv-rotulo {{ font-size:13px; letter-spacing:.12em; text-transform:uppercase;
  color:#554f49; margin:26px 0 8px; }}
.pv-rotulo small {{ text-transform:none; letter-spacing:0; color:#776e64; }}
.pv-folha {{ background:#fffdf9; box-shadow:0 6px 30px rgba(45,41,37,.14);
  overflow:hidden; }}
.pv-heading, .pv-texto p {{ margin:0; }}
.pv-texto p {{ margin:0 0 8px; }}
.pv-lista li {{ display:inline-flex; gap:6px; align-items:center; }}
.pv-falta {{ border:1px dashed #c9bda9; color:#776e64; padding:10px 14px;
  font-size:13px; background:#f7f4ef; }}
img {{ max-width:100%; }}
/* O widget de menu gera a cor base do item a partir da global; aqui ela
   entra como regra, para o hover/ativo do CSS do kit poderem vencer. */
.iara-menu-nav .elementor-nav-menu--main .elementor-item {{
  color:#554f49; text-decoration:none; display:inline-block;
  padding:6px 2px;
}}
.pv-folha .iara-barra {{ padding-left:24px !important; padding-right:24px !important; }}
/* Hover da faixa e dos icones na previa: as cores base entram por regra
   (nao fixas no elemento), senao o :hover nunca aparece. Os valores sao
   os mesmos das globais do kit. */
.elementor-icon {{ color:var(--pv-cor,#2d2925); }}
.iara-acoes .elementor-icon {{ color:#554f49; }}
.iara-faixa-lista li a:hover {{ color:#e4cbb5 !important; }}
{css_kit}
</style></head><body>
<div class="pv-aviso">
<p><b>Prévia local dos templates JSON</b> (gerada de <code>bloco-b/json/</code>,
sem WordPress). Ela aproxima a renderização do Elementor usando a
tipografia embutida em cada widget, as cores globais e o CSS do kit.
Passe o mouse no menu para ver o <b>hover</b>; o item sublinhado em claro
é o <b>ativo</b>. Widgets de loja do WooCommerce aparecem como blocos
rotulados. O menu abaixo mostra a Coleção como o desenho prevê; no
WordPress, ela entra no Menu Principal.</p>
</div>
{''.join(secoes)}
</body></html>'''

    SAIDA.mkdir(exist_ok=True)
    (SAIDA / 'index.html').write_text(doc, encoding='utf-8')
    logo = RAIZ / 'bloco-b' / 'imagens' / 'iara-costa-logotipo.png'
    if logo.exists():
        (SAIDA / 'logotipo.png').write_bytes(logo.read_bytes())
    print(f'previa gerada: preview/index.html '
          f'({len(escolhidos)} templates: {", ".join(escolhidos)})')


if __name__ == '__main__':
    main()
