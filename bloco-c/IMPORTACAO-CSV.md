# Bloco C, parte 1: produtos e posts em CSV

Estes dois arquivos alimentam a loja e o diário sem digitar item por item.
Eles trazem os **dados de exemplo do protótipo aprovado** (decisão D5 da fase
E0: dados fictícios só servem para layout). Por isso, **tudo nasce em
rascunho**: nenhum produto e nenhum post deste lote pode ser publicado sem
revisão.

> Nenhuma importação foi testada. Não tenho acesso ao WordPress, ao painel nem
> ao banco de dados. Importe em staging, confira linha por linha e só então
> repita com os dados reais.

## 1. produtos.csv (WooCommerce)

| O que | Como está |
|---|---|
| Linhas | 68: 10 produtos variáveis, 56 variações e 2 simples |
| Estrutura | 1 linha `variable` por produto e 1 linha `variation` por combinação de cor e tamanho, ligada ao pai pela coluna Parent (SKU do pai) |
| Atributos | Cor e Tamanho como atributos **globais** (são os que o plugin de swatches aprovado usa) |
| Preço | no formato do importador (`348.00`); o Cropped de Tricot Areia traz o preço cheio e o promocional do protótipo |
| Publicado | `0` em todas as linhas: importa como **rascunho** |
| Estoque | `In stock? = 1` e quantidade vazia: a gestão de estoque por variação é ligada com as quantidades reais no cadastro |
| Peso e dimensões | **vazios de propósito**: são `[PREENCHER]` com peso (kg) e medidas (cm) reais, que o frete usa |
| Imagem | **fora do CSV** (segunda tentativa, 2026-10-21: só o nome do arquivo fez o importador recusar o produto; anexar pela biblioteca de mídia, produto a produto) |
| Destaques | os 4 produtos da seção Em destaque da home marcados como `Is featured? = 1` |

### Como importar

1. WooCommerce > Produtos > Importar, escolher `bloco-c/produtos.csv`.
   **Não marcar** "Atualizar produtos existentes": o lote é de produtos
   novos. (A primeira tentativa, em 2026-10-21, falhou inteira porque o
   arquivo trazia a coluna ID vazia, o que o importador lê como pedido
   de atualização; a coluna foi removida.)
2. Conferir o mapeamento de colunas que o importador propõe; não trocar
   Parent, SKU nem os atributos.
3. Importar e conferir: 12 produtos em rascunho, cada variável com as suas
   variações. Conferir também se os atributos Cor e Tamanho nasceram globais.
4. Anexar a foto de cada produto pela biblioteca de mídia (ou colar o endereço completo da imagem numa coluna Images e reimportar marcando atualizar). Antes de publicar qualquer um: trocar descrição, foto, peso, dimensões e
   estoque pelos reais. Sandália com tamanho "Único" é dado do protótipo:
   conferir a numeração real de calçados antes.

## 2. posts.csv (diário)

| O que | Como está |
|---|---|
| Posts | 8, todos `draft` |
| Conteúdo | blocos do **Gutenberg** (parágrafo e título), nunca Elementor |
| Categorias | Tecidos e cuidados, Tamanhos e caimento, Estilo e Bastidores |
| Autor | `[PREENCHER: quem assina]`, em todos |
| Fecho | cada post termina lembrando que é texto de exemplo em rascunho |

Os títulos e resumos são os dos cartões aprovados no protótipo. O texto de
cada post foi escrito como rascunho de trabalho a partir desses cartões; ele
precisa de revisão e aprovação antes de qualquer publicação.

### Como importar

Posts não têm importador de CSV nativo. Caminhos honestos, em ordem:

1. **Manual assistido**: criar os 8 posts colando o conteúdo de
   `pages-conteudo` quando ele chegar, ou abrindo o CSV e colando título,
   resumo e texto. São só 8 posts.
2. **Plugin importador de CSV**: só com aprovação prévia, pela regra do
   projeto. Nenhum foi aprovado até aqui, então este caminho está fechado
   por enquanto.

## 3. O que estes arquivos não resolvem

- Categorias e atributos reais do catálogo definitivo (os de exemplo servem
  para testar a importação e os swatches).
- Fotos reais, peso, dimensões e estoque: sem isso, frete e página de
  produto não estão prontos.
- Quem assina os posts e a revisão dos textos.
- O kit de instalação e os guias (instalação, segurança, SEO, testes,
  desempenho, e-mail, go-live e nota fiscal) são as próximas partes do
  Bloco C.
