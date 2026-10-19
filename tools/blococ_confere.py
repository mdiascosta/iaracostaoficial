#!/usr/bin/env python3
"""
Confere os CSVs do Bloco C (produtos e posts).

1. Os dois abrem como CSV UTF-8, com cabecalho completo.
2. Produto variavel tem SKU unico; toda variacao aponta para um pai que existe.
3. A combinacao cor x tamanho das variacoes bate com os atributos do pai,
   sem repeticao.
4. Preco de variacao e numero valido; nada publicado (Published = 0).
5. Sao 8 posts, slugs unicos, todos em rascunho, com blocos do Gutenberg
   abrindo e fechando em pares.
6. Nenhum travessao nos textos.

Uso:
    python3 tools/blococ_confere.py
"""

import csv
import pathlib
import re
import sys

RAIZ = pathlib.Path(__file__).resolve().parents[1]
PASTA = RAIZ / 'bloco-c'


def ler(nome, problemas):
    caminho = PASTA / nome
    if not caminho.exists():
        problemas.append(f'{nome} nao existe (rode tools/blococ_gera_csv.py)')
        return [], []
    with caminho.open(encoding='utf-8', newline='') as arq:
        leitor = csv.DictReader(arq)
        linhas = list(leitor)
        return leitor.fieldnames or [], linhas


def main():
    problemas = []

    campos, produtos = ler('produtos.csv', problemas)
    obrigatorios = {'Type', 'SKU', 'Name', 'Published', 'Regular price', 'Categories',
                    'Attribute 1 name', 'Attribute 1 value(s)', 'Attribute 2 name',
                    'Attribute 2 value(s)', 'Parent'}
    faltando = obrigatorios - set(campos)
    if faltando:
        problemas.append(f'produtos.csv: faltam colunas {sorted(faltando)}')

    skus = {}
    for i, l in enumerate(produtos, 2):
        if l['SKU'] in skus:
            problemas.append(f'produtos.csv: SKU repetido "{l["SKU"]}" (linha {i})')
        skus[l['SKU']] = l
        if l['Published'] != '0':
            problemas.append(f'produtos.csv: "{l["SKU"]}" nao esta em rascunho')
        if '—' in (l['Name'] + l['Description']) or '–' in (l['Name'] + l['Description']):
            problemas.append(f'produtos.csv: travessao em "{l["SKU"]}"')

    pais = {l['SKU']: l for l in produtos if l['Type'] in ('variable', 'simple')}
    variacoes = [l for l in produtos if l['Type'] == 'variation']
    for v in variacoes:
        pai = pais.get(v['Parent'])
        if not pai:
            problemas.append(f'produtos.csv: variacao "{v["SKU"]}" sem pai "{v["Parent"]}"')
            continue
        if pai['Type'] != 'variable':
            problemas.append(f'produtos.csv: pai "{pai["SKU"]}" nao e variavel')
        for attr in ('Attribute 1 value(s)', 'Attribute 2 value(s)'):
            permitidos = [x.strip() for x in pai[attr].split(',')]
            if v[attr] not in permitidos:
                problemas.append(f'produtos.csv: "{v["SKU"]}" com {v[attr]} fora do pai')
        try:
            float(v['Regular price'])
        except (TypeError, ValueError):
            problemas.append(f'produtos.csv: preco invalido em "{v["SKU"]}"')

    for pai in (l for l in produtos if l['Type'] == 'variable'):
        esperado = 1
        for attr in ('Attribute 1 value(s)', 'Attribute 2 value(s)'):
            esperado *= len([x for x in pai[attr].split(',') if x.strip()])
        achado = sum(1 for v in variacoes if v['Parent'] == pai['SKU'])
        if esperado != achado:
            problemas.append(f'produtos.csv: "{pai["SKU"]}" espera {esperado} variacoes, tem {achado}')

    campos_posts, posts = ler('posts.csv', problemas)
    if len(posts) != 8:
        problemas.append(f'posts.csv: {len(posts)} posts (esperado 8)')
    slugs = set()
    for l in posts:
        if l['post_name'] in slugs:
            problemas.append(f'posts.csv: slug repetido "{l["post_name"]}"')
        slugs.add(l['post_name'])
        if l['post_status'] != 'draft':
            problemas.append(f'posts.csv: "{l["post_name"]}" nao esta em rascunho')
        abertos = re.findall(r'<!-- wp:([a-z-]+)', l['post_content'])
        fechados = re.findall(r'<!-- /wp:([a-z-]+)', l['post_content'])
        if sorted(abertos) != sorted(fechados):
            problemas.append(f'posts.csv: blocos do Gutenberg abertos sem fechar em "{l["post_name"]}"')
        if '—' in l['post_content'] or '–' in l['post_content']:
            problemas.append(f'posts.csv: travessao em "{l["post_name"]}"')

    n_var = sum(1 for l in produtos if l['Type'] == 'variable')
    n_variacoes = len(variacoes)
    print(f'  produtos.csv: {len(produtos)} linhas ({n_var} variaveis, {n_variacoes} variacoes)')
    print(f'  posts.csv:    {len(posts)} posts em rascunho')

    if problemas:
        print()
        for p in problemas:
            print(f'[ERRO] {p}')
        print(f'\nresultado: {len(problemas)} problema(s)')
        return 1
    print('resultado: tudo certo')
    return 0


if __name__ == '__main__':
    sys.exit(main())
