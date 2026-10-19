#!/usr/bin/env python3
"""
Gera os CSVs do Bloco C: produtos do WooCommerce e posts do blog.

Fontes:
  - tools/produtos.json (os 12 produtos de exemplo do prototipo aprovado,
    decisao D5 da fase E0: dados ficticios so para layout);
  - os titulos e resumos dos cartoes do blog no prototipo.

Regras:
  - produto variavel: 1 linha "variable" + 1 linha "variation" por combinacao
    de cor e tamanho, ligadas pelo SKU do pai;
  - tudo nasce como rascunho (Published = 0 nos produtos, draft nos posts):
    catalogo e textos de exemplo nunca podem ir ao ar sem revisao;
  - preco no formato do importador do WooCommerce (348.00);
  - peso e dimensoes ficam vazios: sao [PREENCHER] com os dados reais;
  - post nasce em Gutenberg (blocos), nunca em Elementor.

Uso:
    python3 tools/blococ_gera_csv.py
"""

import csv
import json
import pathlib
import sys

RAIZ = pathlib.Path(__file__).resolve().parents[1]
PASTA = RAIZ / 'bloco-c'

CORES = {
    'terracota': 'Terracota', 'salvia': 'Sálvia', 'cru': 'Cru',
    'carvao': 'Carvão', 'areia': 'Areia',
}
TAMANHOS = {'p': 'P', 'm': 'M', 'g': 'G', 'gg': 'GG', 'unico': 'Único'}

CABECALHO_PRODUTOS = [
    'ID', 'Type', 'SKU', 'Name', 'Published', 'Is featured?', 'Visibility in catalog',
    'Short description', 'Description', 'Tax status', 'In stock?', 'Stock',
    'Backorders allowed?', 'Sold individually?', 'Weight (kg)', 'Length (cm)',
    'Width (cm)', 'Height (cm)', 'Allow customer reviews?', 'Regular price',
    'Sale price', 'Categories', 'Tags', 'Images',
    'Attribute 1 name', 'Attribute 1 value(s)', 'Attribute 1 visible',
    'Attribute 1 global', 'Attribute 2 name', 'Attribute 2 value(s)',
    'Attribute 2 visible', 'Attribute 2 global', 'Parent',
    'Attribute 1 default', 'Attribute 2 default',
]


def preco(texto):
    """'R$ 348,00' -> '348.00' (formato do importador)."""
    limpo = texto.replace('R$', '').strip().replace('.', '').replace(',', '.')
    return limpo


def produtos():
    dados = json.loads((RAIZ / 'tools' / 'produtos.json').read_text(encoding='utf-8'))
    linhas = []
    for p in dados:
        cores = [CORES[c] for c in p['cores']]
        tamanhos = [TAMANHOS[t] for t in p['tamanhos_slug']]
        variavel = len(cores) > 1 or len(tamanhos) > 1
        sku = p['slug']
        base = {c: '' for c in CABECALHO_PRODUTOS}
        base.update({
            'Type': 'variable' if variavel else 'simple',
            'SKU': sku,
            'Name': p['nome'],
            'Published': '0',
            'Is featured?': '1' if p['slug'] in (
                'blusa-linho-terracota', 'vestido-midi-salvia',
                'calca-pantalona-salvia', 'colar-ceramica') else '0',
            'Visibility in catalog': 'visible',
            'Short description': (f"{p['categoria']} em tecido de alta gramatura, "
                                  + ('peca unica artesanal. ' if tamanhos == ['Único'] else 'do P ao GG. ')
                                  + 'Texto de exemplo do prototipo: substituir pela descricao curta real da peca.'),
            'Description': 'Descricao de exemplo do prototipo. A descricao final precisa ser escrita ou aprovada pela Iara Costa, com composicao e medidas reais do fornecedor [PREENCHER].',
            'Tax status': 'taxable',
            'In stock?': '1',
            'Allow customer reviews?': '1',
            'Regular price': preco(p['preco']) if not variavel else '',
            'Sale price': '',
            'Categories': p['categoria'],
            'Images': p['img'],
            'Attribute 1 name': 'Cor',
            'Attribute 1 value(s)': ', '.join(cores),
            'Attribute 1 visible': '1',
            'Attribute 1 global': '1',
            'Attribute 2 name': 'Tamanho',
            'Attribute 2 value(s)': ', '.join(tamanhos),
            'Attribute 2 visible': '1',
            'Attribute 2 global': '1',
            'Attribute 1 default': cores[0],
            'Attribute 2 default': tamanhos[0],
        })
        if p.get('preco_de'):
            base['Regular price'] = preco(p['preco_de']) if not variavel else base['Regular price']
            if not variavel:
                base['Sale price'] = preco(p['preco'])
        linhas.append(base)
        if variavel:
            regular = preco(p['preco_de']) if p.get('preco_de') else preco(p['preco'])
            sale = preco(p['preco']) if p.get('preco_de') else ''
            for cor in cores:
                for tam in tamanhos:
                    cor_slug = [k for k, v in CORES.items() if v == cor][0]
                    tam_slug = [k for k, v in TAMANHOS.items() if v == tam][0]
                    v = {c: '' for c in CABECALHO_PRODUTOS}
                    v.update({
                        'Type': 'variation',
                        'SKU': f'{sku}-{cor_slug}-{tam_slug}',
                        'Published': '0',
                        'In stock?': '1',
                        'Regular price': regular,
                        'Sale price': sale,
                        'Parent': sku,
                        'Attribute 1 name': 'Cor',
                        'Attribute 1 value(s)': cor,
                        'Attribute 2 name': 'Tamanho',
                        'Attribute 2 value(s)': tam,
                    })
                    linhas.append(v)
    return linhas


POSTS = [
    ('Como lavar linho sem perder o caimento', 'como-lavar-linho', 'Tecidos e cuidados',
     'Água fria, pouca centrifugação e secagem na sombra resolvem quase tudo.',
     ['O linho é uma fibra forte, mas gosta de água fria e de pouco atrito. Lave do avesso, com sabão neutro, e evite torcer a peça.',
      'Na máquina, use o ciclo delicado e um saquinho de lavagem. Centrifugação curta, só para tirar o excesso de água.',
      'Seque na sombra, já no formato da peça. O linho amacia a cada lavagem e volta ao caimento com o vapor do ferro morno.']),
    ('Como escolher o caimento certo sem provar', 'caimento-sem-provar', 'Tamanhos e caimento',
     'Três medições resolvem a dúvida entre dois tamanhos.',
     ['Comprar roupa sem provar pede um método, e ele cabe em três medições: busto, cintura e quadril, tiradas sobre uma peça que já veste bem.',
      'Compare cada medida com a tabela da peça que você quer, que fica na página do produto. A tabela daquela peça é a que vale, não a tabela genérica.',
      'Na dúvida entre dois tamanhos, pense no tecido: linho cede um pouco com o uso; tricot acompanha o corpo. O Guia de Medidas do site traz o passo a passo com fotos [PREENCHER].']),
    ('Uma peça, três combinações: alfaiataria', 'uma-peca-tres-combinacoes', 'Estilo',
     'Do trabalho ao jantar, mudando só o sapato e o acessório.',
     ['Uma pantalona de alfaiataria leve resolve a semana se os acompanhamentos mudarem: camisa e sapato baixo para o trabalho, blusa de seda e sandália para o jantar.',
      'A terceira combinação é a do fim de semana: camiseta de algodão, a mesma pantalona e um acessório de cerâmica para quebrar a formalidade.',
      'A ideia não é ter mais roupa. É ter peças que conversam entre si.']),
    ('Por que o mesmo tamanho veste diferente em cada marca', 'mesmo-tamanho-veste-diferente', 'Tamanhos e caimento',
     'Modelagem não é padrão: entenda o que olhar antes de comprar.',
     ['Não existe um P universal. Cada marca desenha a própria modelagem, com folgas e proporções diferentes, e o tamanho da etiqueta é só um nome para essa escolha.',
      'Por isso a tabela de medidas de cada peça manda mais do que a letra. Dois vestidos M podem ter quatro centímetros de diferença no busto.',
      'Aqui, cada página de produto traz a tabela daquela peça, medida com a roupa esticada sobre a mesa.']),
    ('Como medir o corpo em casa, sem erro', 'como-medir-o-corpo-em-casa', 'Tamanhos e caimento',
     'Fita métrica paralela ao chão, sem apertar, e a ajuda de alguém para as costas.',
     ['Passe a fita em volta do busto na parte mais cheia, sem apertar e sem deixar cair nas costas. Peça ajuda para manter a fita reta.',
      'A cintura é medida na parte mais estreita do tronco, e o quadril na parte mais larga. Anote tudo em centímetros, sem arredondar para baixo.',
      'Com as três medidas, compare com a tabela da peça. Se ficar entre dois tamanhos, o atendimento ajuda a decidir pelo caimento daquela modelagem.']),
    ('Quatro peças que resolvem a semana inteira', 'quatro-pecas-para-a-semana', 'Estilo',
     'Combinações que funcionam para trabalho, almoço e imprevisto.',
     ['Uma camisa de linho, uma pantalona, um vestido midi e um blazer leve. Quatro peças, e a semana inteira se monta combinando e trocando acessórios.',
      'O segredo está na paleta: terracota, sálvia, cru e areia conversam entre si, e qualquer combinação das quatro peças funciona.',
      'Guarda-roupa bom não é guarda-roupa cheio. É guarda-roupa que combina consigo mesmo.']),
    ('Como guardar as peças para durarem mais', 'como-guardar-as-pecas', 'Tecidos e cuidados',
     'Cabides certos, dobras e o que nunca deve ir para o sol direto.',
     ['Linho e viscose gostam de cabide largo, que não marca o ombro. Tricot pede dobra, porque o próprio peso deforma a peça no cabide.',
      'Nada de sol direto para secar ou guardar: a luz desbota o tingimento e resseca a fibra. Sombra e vento bastam.',
      'Guarde as peças limpas e com espaço entre elas. Roupa apertada no armário amassa, abafa e envelhece antes da hora.']),
    ('Do barro à peça: como nasce uma coleção no ateliê', 'do-barro-a-peca', 'Bastidores',
     'Três capítulos, doze peças e um processo que começa na escolha do tecido.',
     ['[PROPOSTA] Texto de bastidores para escrever com a equipe do ateliê: o que pode ser afirmado já está no protótipo, como o tingimento com argila do Vale do Paraíba, confirmado pela empresa.',
      'Cada coleção começa pela gramatura do tecido e pela modelagem própria, desenhada, cortada e confeccionada no ateliê em Cerquilho (SP).',
      'Este texto nasce como rascunho e só é publicado depois de aprovado por quem faz.']),
]


def bloco(tipo, **attrs):
    atributos = ' '.join(f'{k}="{v}"' for k, v in attrs.items())
    return f'<!-- wp:{tipo} {atributos} -->' if atributos else f'<!-- wp:{tipo} -->'


def conteudo_post(paragrafos):
    partes = []
    for i, texto in enumerate(paragrafos):
        if i == 1:
            partes.append('<!-- wp:heading --><h2>Na prática</h2><!-- /wp:heading -->')
        partes.append(f'<!-- wp:paragraph --><p>{texto}</p><!-- /wp:paragraph -->')
    partes.append('<!-- wp:paragraph --><p><em>Texto de exemplo do protótipo, em rascunho. Revisar e aprovar antes de publicar. [PREENCHER: quem assina]</em></p><!-- /wp:paragraph -->')
    return '\n'.join(partes)


def posts():
    linhas = []
    for titulo, slug, categoria, resumo, paragrafos in POSTS:
        linhas.append({
            'post_title': titulo,
            'post_name': slug,
            'post_status': 'draft',
            'post_category': categoria,
            'post_excerpt': resumo,
            'post_content': conteudo_post(paragrafos),
            'post_author': '[PREENCHER: quem assina]',
        })
    return linhas


def escrever_csv(nome, cabecalho, linhas):
    PASTA.mkdir(parents=True, exist_ok=True)
    caminho = PASTA / nome
    with caminho.open('w', encoding='utf-8', newline='') as arq:
        w = csv.DictWriter(arq, fieldnames=cabecalho, quoting=csv.QUOTE_MINIMAL)
        w.writeheader()
        for linha in linhas:
            w.writerow({c: linha.get(c, '') for c in cabecalho})
    return caminho


def main():
    linhas_produtos = produtos()
    escrever_csv('produtos.csv', CABECALHO_PRODUTOS, linhas_produtos)
    variaveis = sum(1 for l in linhas_produtos if l['Type'] == 'variable')
    variacoes = sum(1 for l in linhas_produtos if l['Type'] == 'variation')
    simples = sum(1 for l in linhas_produtos if l['Type'] == 'simple')
    print(f'  ok  produtos.csv  {len(linhas_produtos)} linhas '
          f'({variaveis} variaveis, {variacoes} variacoes, {simples} simples)')
    linhas_posts = posts()
    escrever_csv('posts.csv', list(linhas_posts[0]), linhas_posts)
    print(f'  ok  posts.csv     {len(linhas_posts)} posts em rascunho')
    print(f'arquivos gerados em {PASTA.relative_to(RAIZ)}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
