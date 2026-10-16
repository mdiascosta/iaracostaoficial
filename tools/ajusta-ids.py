#!/usr/bin/env python3
"""
Troca os apelidos de cor e de fonte pelos ids reais do site.

Por que isso existe
-------------------
Cada cor personalizada do Elementor tem um id proprio, e o Elementor sorteia
esse id quando a cor e criada na tela. Os arquivos do Bloco B precisam apontar
para o id certo, senao o estilo nao aparece. Este script le o arquivo de
configuracoes exportado do site da equipe, casa as cores pelo TITULO e reescreve
os arquivos do Bloco B com os ids reais.

Como usar
---------
1. No site (staging), criar as cores e as fontes globais seguindo a tabela do
   GUIA-IMPORTACAO.md.
2. Exportar as configuracoes: Elementor > Ferramentas > Importar / Exportar Kit >
   Exportar > marcar somente "Configuracoes do site". Sai um arquivo .zip; dentro
   dele esta o site-settings/site-settings.json.
3. Rodar:

       python3 tools/ajusta-ids.py caminho/para/site-settings.json

   Para so conferir o que mudaria, sem gravar nada:

       python3 tools/ajusta-ids.py caminho/para/site-settings.json --simular

O script cuida de:
  - conferir se as quatro cores de sistema estao com os valores do projeto;
  - casar as cores e as fontes personalizadas pelo titulo;
  - reescrever as referencias "globals/colors?id=..." e "globals/typography?id=..."
    nos arquivos de bloco-b/json;
  - atualizar os apelidos dentro de bloco-b/globais/cores-e-fontes.json.

Uso:
    python3 tools/ajusta-ids.py <arquivo-exportado> [--simular]
"""

import argparse
import json
import pathlib
import re
import sys

RAIZ = pathlib.Path(__file__).resolve().parents[1]
PASTA_BLOCO_B = RAIZ / 'bloco-b'
PASTA_JSON = PASTA_BLOCO_B / 'json'
ARQ_GLOBAIS = PASTA_BLOCO_B / 'globais' / 'cores-e-fontes.json'

SISTEMA = ['primary', 'secondary', 'text', 'accent']


def achar_ajustes(dados, origem):
    """Encontra o bloco de configuracoes dentro do arquivo exportado."""
    if isinstance(dados, dict):
        if 'settings' in dados and isinstance(dados['settings'], dict):
            return dados['settings']
        if 'custom_colors' in dados or 'system_colors' in dados:
            return dados
        for chave in ('content', 'kit'):
            if chave in dados:
                achado = achar_ajustes(dados[chave], origem)
                if achado:
                    return achado
    if isinstance(dados, list):
        for item in dados:
            achado = achar_ajustes(item, origem)
            if achado:
                return achado
    return {}


def mapa_por_titulo(itens):
    mapa = {}
    for item in itens or []:
        titulo = (item.get('title') or '').strip()
        apelido = item.get('_id')
        if titulo and apelido:
            mapa[titulo] = apelido
    return mapa


def trocar_referencias(texto, trocas, tipo):
    """troca: apelido_antigo -> apelido_novo. tipo: 'colors' ou 'typography'."""
    def substituir(achado):
        apelido = achado.group(2)
        return f'{achado.group(1)}{trocas.get(apelido, apelido)}'
    padrao = re.compile(r'(globals/' + tipo + r'\?id=)([a-z0-9_-]+)')
    return padrao.sub(substituir, texto)


def main():
    ap = argparse.ArgumentParser(description='Casa os ids das cores e fontes globais com os arquivos do Bloco B.')
    ap.add_argument('exportado', help='site-settings.json exportado do site')
    ap.add_argument('--simular', action='store_true', help='mostra o que mudaria, sem gravar')
    args = ap.parse_args()

    caminho_export = pathlib.Path(args.exportado)
    if not caminho_export.exists():
        print(f'[ERRO] arquivo nao encontrado: {caminho_export}')
        return 1

    exportado = json.loads(caminho_export.read_text(encoding='utf-8'))
    ajustes = achar_ajustes(exportado, caminho_export.name)
    if not ajustes:
        print('[ERRO] nao achei o bloco de configuracoes no arquivo. Exporte pela opcao '
              '"Configuracoes do site" (Importar / Exportar Kit).')
        return 1

    propostas = json.loads(ARQ_GLOBAIS.read_text(encoding='utf-8'))['settings']

    # --- cores de sistema: id fixo, confere o valor
    problemas = []
    sistemas_no_site = {c['_id']: c.get('color', '').lower()
                        for c in ajustes.get('system_colors', [])}
    for cor in propostas['system_colors']:
        real = sistemas_no_site.get(cor['_id'])
        if not real:
            problemas.append(f'cor de sistema "{cor["_id"]}" nao existe no site')
        elif real.lstrip('#') != cor['color'].lstrip('#'):
            problemas.append(f'cor de sistema "{cor["_id"]}" esta {real} no site e devia ser {cor["color"]}')

    # --- cores e fontes personalizadas: casa pelo titulo
    cores_site = mapa_por_titulo(ajustes.get('custom_colors'))
    fontes_site = mapa_por_titulo(ajustes.get('custom_typography'))
    trocas_cor, trocas_fonte, faltando = {}, {}, []

    for cor in propostas['custom_colors']:
        real = cores_site.get(cor['title'])
        if real:
            trocas_cor[cor['_id']] = real
        else:
            faltando.append(f'cor "{cor["title"]}"')
    for fonte in propostas['custom_typography']:
        real = fontes_site.get(fonte['title'])
        if real:
            trocas_fonte[fonte['_id']] = real
        else:
            faltando.append(f'fonte "{fonte["title"]}"')

    print(f'cores de sistema conferidas: {len(propostas["system_colors"])}')
    mudam_cor = {a: b for a, b in trocas_cor.items() if a != b}
    mudam_fonte = {a: b for a, b in trocas_fonte.items() if a != b}
    print(f'cores personalizadas casadas: {len(trocas_cor)} ({len(mudam_cor)} com id diferente do apelido)')
    print(f'fontes personalizadas casadas: {len(trocas_fonte)} ({len(mudam_fonte)} com id diferente do apelido)')
    for antigo, novo in sorted(mudam_cor.items()):
        print(f'   cor   {antigo:22s} -> {novo}')
    for antigo, novo in sorted(mudam_fonte.items()):
        print(f'   fonte {antigo:22s} -> {novo}')

    if faltando:
        print()
        for item in faltando:
            print(f'[AVISO] {item} ainda nao existe no site; crie e rode de novo')
    if problemas:
        print()
        for item in problemas:
            print(f'[ERRO] {item}')

    if not any((mudam_cor, mudam_fonte)):
        print()
        print('nada a trocar: os ids do site ja sao os que os arquivos usam.')
        return 1 if problemas else 0

    if args.simular:
        print()
        print('simulacao: nenhum arquivo foi gravado.')
        return 1 if problemas else 0

    # --- reescreve os templates
    alterados = 0
    for caminho in sorted(PASTA_JSON.glob('*.json')):
        texto = original = caminho.read_text(encoding='utf-8')
        texto = trocar_referencias(texto, trocas_cor, 'colors')
        texto = trocar_referencias(texto, trocas_fonte, 'typography')
        if texto != original:
            caminho.write_text(texto, encoding='utf-8')
            alterados += 1
            print(f'   gravado {caminho.name}')

    # --- atualiza os apelidos no arquivo de globais
    for chave, trocas in (('custom_colors', trocas_cor), ('custom_typography', trocas_fonte)):
        for item in propostas[chave]:
            if item['_id'] in trocas:
                item['_id'] = trocas[item['_id']]
    ARQ_GLOBAIS.write_text(json.dumps({'content': [], 'settings': propostas},
                                      ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    print()
    print(f'arquivos reescritos: {alterados} de {len(list(PASTA_JSON.glob("*.json")))}')
    print('agora rode: python3 tools/blocob_confere.py')
    return 1 if problemas else 0


if __name__ == '__main__':
    sys.exit(main())
