#!/usr/bin/env python3
"""
Monta bloco-c/iara-costa-kit.zip: o pacote que a equipe recebe.

Conteudo:
  - os 24 templates do Elementor e as globais (Bloco B);
  - o guia de importacao do Bloco B;
  - produtos.csv, posts.csv, pages-conteudo.md e IMPORTACAO-CSV.md (Bloco C);
  - um LEIA-ME dentro do zip com a ordem de uso.

O zip e deterministico: data fixa e ordem fixa, para gerar igual sempre.

Uso:
    python3 tools/blococ_monta_kit.py
"""

import hashlib
import pathlib
import sys
import zipfile

RAIZ = pathlib.Path(__file__).resolve().parents[1]
DATA_FIXA = (2026, 10, 19, 12, 0, 0)

LEIA_ME = """KIT IARA COSTA · INSTALACAO DO SITE
Gerado a partir do repositorio do projeto (Blocos B e C).


ORDEM DE USO

  1. Ler bloco-b/GUIA-IMPORTACAO.md e seguir a ordem dele: conferir versoes,
     criar cores e fontes globais, acertar os ids e importar os templates
     um por vez, em staging.
  2. Importar bloco-c/produtos.csv e criar os posts de bloco-c/posts.csv,
     seguindo bloco-c/IMPORTACAO-CSV.md. Tudo nasce em rascunho.
  3. Usar bloco-c/pages-conteudo.md para revisar e aprovar os textos das
     paginas institucionais e legais. As legais sao rascunho para o juridico.


AVISO

Nada neste kit foi testado em um WordPress real: a importacao e a conferencia
sao da equipe, em staging, um arquivo por vez. Produtos, textos e posts sao
os de exemplo do prototipo aprovado e nao podem ser publicados como estao.
"""


def arquivos():
    itens = []
    for caminho in sorted((RAIZ / 'bloco-b' / 'json').glob('*.json')):
        itens.append((caminho, f'bloco-b/json/{caminho.name}'))
    itens.append((RAIZ / 'bloco-b' / 'globais' / 'cores-e-fontes.json',
                  'bloco-b/globais/cores-e-fontes.json'))
    itens.append((RAIZ / 'bloco-b' / 'GUIA-IMPORTACAO.md', 'bloco-b/GUIA-IMPORTACAO.md'))
    for nome in ('produtos.csv', 'posts.csv', 'pages-conteudo.md', 'IMPORTACAO-CSV.md'):
        itens.append((RAIZ / 'bloco-c' / nome, f'bloco-c/{nome}'))
    for caminho in sorted((RAIZ / 'bloco-c' / 'guias').glob('*.md')):
        itens.append((caminho, f'bloco-c/guias/{caminho.name}'))
    return itens


def main():
    itens = arquivos()
    faltando = [str(c) for c, _ in itens if not c.exists()]
    if faltando:
        print('faltam arquivos: ' + ', '.join(faltando))
        return 1
    destino = RAIZ / 'bloco-c' / 'iara-costa-kit.zip'
    linhas = []
    with zipfile.ZipFile(destino, 'w', zipfile.ZIP_DEFLATED) as z:
        info = zipfile.ZipInfo('LEIA-ME.txt', DATA_FIXA)
        z.writestr(info, LEIA_ME)
        for caminho, nome in itens:
            dados = caminho.read_bytes()
            info = zipfile.ZipInfo(nome, DATA_FIXA)
            info.external_attr = 0o644 << 16
            z.writestr(info, dados)
            linhas.append(f'{hashlib.sha256(dados).hexdigest()[:12]}  {nome}')
    print(f'  ok  iara-costa-kit.zip  {len(itens) + 1} arquivos, {destino.stat().st_size} bytes')
    for linha in linhas:
        print('      ' + linha)
    return 0


if __name__ == '__main__':
    sys.exit(main())
