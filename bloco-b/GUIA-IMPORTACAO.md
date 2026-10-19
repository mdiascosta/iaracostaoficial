# Guia de importação: Bloco B (templates do Elementor)

Este guia acompanha os arquivos `.json` do Bloco B. Ele explica o que cada
arquivo é, **em que ordem** importar e o que precisa estar pronto antes.

> **Leia antes de tudo:** nenhuma importação foi testada. Não tenho acesso ao
> WordPress, ao painel nem ao banco de dados deste projeto (modo manual). O
> formato dos arquivos foi conferido no código-fonte do Elementor, não em um
> site real. Importe **em staging**, um arquivo por vez, e confira cada um antes
> de seguir para o próximo.

---

## 1. O que é o Bloco B

O Bloco A entregou o protótipo HTML: 22 páginas aprovadas, com cor, tipografia e
espaçamento definidos. O Bloco B transforma esse desenho em **templates do
Elementor**, prontos para importar no WordPress.

| Pasta | O que tem |
|---|---|
| `bloco-b/json/` | os templates, um arquivo por parte do site ou por página |
| `bloco-b/globais/` | as cores e as fontes globais do site, em um arquivo só |
| `bloco-b/GUIA-IMPORTACAO.md` | este guia |
| `bloco-b/LEIA-ME.txt` | resumo de uma página, para quem só quer abrir e usar |

As ferramentas que geram e conferem estes arquivos ficam em `tools/`:

```bash
python3 tools/blocob_gera.py       # regera os arquivos (não muda o resultado sem motivo)
python3 tools/blocob_confere.py    # confere formato, nomes e referências de cor
python3 tools/ajusta-ids.py        # casa os ids das cores com os do site (passo 2)
```

---

## 2. Antes de importar

### 2.1 O que precisa estar instalado (o time instala)

| Item | Por quê | Situação |
|---|---|---|
| WordPress com PHP 8.2 ou superior | exigência do dossiê | [CONFERIR no staging] |
| Tema **Hello Elementor** | tema neutro: o desenho vem do Elementor | [CONFERIR] |
| **Elementor** (versão gratuita) | construtor de base | [CONFERIR] |
| **Elementor Pro** com licença oficial | Theme Builder, widgets de WooCommerce e formulário | decisão D1 |
| **WooCommerce** | catálogo, sacola, checkout e conta | [CONFERIR] |
| **TI WooCommerce Wishlist** (gratuito) | lista de desejos | aprovado em 16/10/2026; a equipe instala no staging |
| **Variation Swatches for WooCommerce**, da GetWooPlugins (gratuito) | seletor de cor e tamanho em botões | aprovado em 16/10/2026; a equipe instala no staging |

Nada de plugin nulo ou pirata, conforme a regra do projeto.

### 2.2 O que precisa estar configurado

- **Permalink** em "Nome do post" (o endereço com o nome da página, sem número).
- **Staging com `noindex`** ligado, para nada aparecer no Google antes do go-live.
- **Logo do site** em Aparência > Personalizar > Identidade do site. O template do
  cabeçalho usa o widget "Site Logo", que pega o logo dali.
- Menu **principal** criado em Aparência > Menus, com os itens: Início, Loja,
  Coleção, Sobre, Contato. O template aponta para o menu de slug `principal`.
  Se o menu tiver outro slug, troque no editor do cabeçalho (widget Menu).

---

## 3. Passo 1: cores e fontes globais

Esta é a etapa mais importante do Bloco B. Todo o resto aponta para estas cores e
fontes pelo **id** do Elementor. Se elas não existirem com o id certo, o estilo do
template simplesmente não aparece (não quebra a página, mas fica sem cor).

### 3.1 Cores

Quatro lugares são fixos no Elementor (as "cores do sistema"). Os outros onze
são cores personalizadas, que a equipe cria na tela.

**Cores do sistema** (Site Settings > Global Colors: editar as quatro que já existem)

| Onde | Nome no projeto | Valor | Uso no site |
|---|---|---|---|
| Primary | Terracota | `#a45f43` | botões, links, destaques |
| Secondary | Sálvia | `#546858` | faixas de destaque |
| Text | Carvão | `#2d2925` | texto principal e títulos |
| Accent | Terracota Escuro | `#78452f` | hover, subtítulos, ênfase |

**Cores personalizadas** (mesma tela, no botão "+")

| Nome a dar à cor | Valor | Uso no site |
|---|---|---|
| Papel | `#fffdf9` | fundo geral |
| Branco | `#ffffff` | fundo de cartão e do rodapé |
| Texto suave | `#625a52` | texto secundário |
| Texto discreto | `#776e64` | texto miúdo |
| Linha | `#ded8ce` | bordas |
| Fio claro | `#eee9e1` | fios divisórios |
| Fundo suave | `#f7f4ef` | fundo de destaque leve |
| Terracota claro | `#e4cbb5` | detalhe claro sobre fundo escuro |
| Link do menu | `#554f49` | links do menu |
| Numeral | `#9c8d7e` | numeral decorativo |
| Texto da faixa | `#fffdf8` | texto da faixa verde do topo |

> **O nome de cada cor importa.** É por ele que o `tools/ajusta-ids.py` encontra
> a cor certa e acerta os arquivos. Use exatamente os nomes da tabela.

### 3.2 Fontes

**Fontes do sistema** (Site Settings > Global Fonts)

| Onde | Família | Peso | Tamanho | Entrelinha | Espaçamento | Detalhe |
|---|---|---|---|---|---|---|
| Primary | Playfair Display | 400 | 24px | 1.1 | 0.105em | H1, título da página |
| Secondary | Playfair Display | 400 | 18px | 1.2 | 0.02em | H2, título de seção |
| Text | Jost | 400 | 15px | 1.55 | 0 | corpo do texto |
| Accent | Jost | 600 | 11px | 1.2 | 0.15em | botões (caixa alta) |

**Fontes personalizadas**

| Nome a dar à fonte | Família | Peso | Tamanho | Entrelinha | Espaçamento | Detalhe |
|---|---|---|---|---|---|---|
| Título terciário | Jost | 400 | 18px | 1.2 | 0.01em | H3 |
| Rótulo | Jost | 600 | 11px | 1.4 | 0.15em | rótulo em caixa alta |
| Link do menu | Jost | 400 | 12px | 1.2 | 0.06em | itens do menu |
| Texto miúdo | Jost | 400 | 11px | 1.45 | 0.06em | texto pequeno |
| Preço | Jost | 400 | 18px | 1.2 | 0 | preço da peça |
| Assinatura (tagline) | Jost | 400 | 11px | 1.4 | 0.2em | "Moda & Acessórios" |

Observação: as duas famílias são do Google Fonts. A regra do projeto é hospedar
as fontes localmente antes do go-live, pela velocidade e pela privacidade
(`[CONFERIR]` no Bloco C).

### 3.3 Acertar os ids (script de uma linha)

O Elementor sorteia um id próprio quando a cor é criada na tela. Como os
arquivos precisam apontar para o id real, existe um script que faz esse
casamento sozinho:

1. **Exportar** as configurações do site: Elementor > Ferramentas > Importar /
   Exportar Kit > Exportar > marcar **somente** "Configurações do site". Sai um
   `.zip`; dentro dele está `site-settings/site-settings.json`.
2. **Rodar** o script (primeiro em modo de conferência):

   ```bash
   python3 tools/ajusta-ids.py caminho/site-settings.json --simular
   python3 tools/ajusta-ids.py caminho/site-settings.json
   python3 tools/blocob_confere.py      # confere que continua tudo certo
   ```

O script casa cor por cor pelo **título**, mostra uma tabela do que muda e
reescreve as referências nos arquivos. Se alguma cor ainda não existir no site,
ele avisa em vez de adivinhar.

Alternativa, se preferir não rodar o script: o arquivo
`bloco-b/globais/cores-e-fontes.json` traz as cores e as fontes com os ids já
escritos (`iara-papel`, `iara-linha`, e assim por diante). Ele pode ser usado como
referência para criar as cores com calma e depois ajustar os arquivos à mão.
**Não** recomendamos importar esse arquivo pelo Importar/Exportar Kit sem antes
testar: a importação de kit substitui as configurações do site.

---

## 4. Passo 2: importar os templates

### 4.1 Como importar um arquivo

1. No painel: **Templates > Saved Templates > Import Templates**.
2. Escolha um arquivo `.json` da pasta `bloco-b/json/`.
3. O template aparece na lista. Confira o nome na coluna "Template Name".

Se o arquivo importado for um **cabeçalho** ou **rodapé** e não aparecer em
Templates > Theme Builder, faça o caminho alternativo (o import cria a peça, e a
peça ganha o lugar depois):

1. Templates > Theme Builder > Add New > escolha **Header** (ou Footer).
2. No editor, clique no ícone de pasta (**Add Template**), aba **My Templates** e
   insira o template importado.
3. Salve e defina a condição de exibição (passo 4.2).

### 4.2 Condições de exibição (Theme Builder)

| Template | Tipo | Condição |
|---|---|---|
| Cabeçalho do site | Header | Include > **Entire Site** |
| Rodapé do site | Footer | Include > **Entire Site** |

### 4.3 Ajustes que são feitos no editor (uma vez por template)

Estes pontos não vão no arquivo porque dependem do site e do gosto de quem
monta. São rápidos:

| Onde | O que ajustar |
|---|---|
| Cabeçalho: widget Menu | apontar para o menu `principal`; ligar o menu sanfona no celular e escolher o ponto de quebra (sugestão: 1020px, igual ao protótipo) |
| Cabeçalho: widget Site Logo | conferir tamanho do logo e o espaço ao lado |
| Cabeçalho: widget Busca | escolher a pele "Minimal" (aparece só a lupa e abre ao clique) |
| Cabeçalho: widget Sacola | conferir se some o texto e fica só o ícone com o contador |
| Rodapé: formulário da newsletter | escolher o destino do e-mail e o serviço de newsletter (o campo está como `[PREENCHER]`) |
| Rodapé: links de redes sociais | trocar os `[PREENCHER]` pelos endereços reais |
| Home: fotos do hero, do editorial e da coleção | escolher as imagens reais na biblioteca de mídia; a legenda do hero entra sobre a foto no editor, se a equipe quiser manter o selo do protótipo |
| Home: bloco Em destaque | escolher a fonte de produtos "Em destaque" do WooCommerce, 4 colunas e 1 linha; nenhum produto é escrito à mão no template |
| Home: bloco Do diário | escolher os 3 posts mais recentes; os textos nascem no Gutenberg, nunca no Elementor |
| Home: categorias e ocasiões | apontar cada cartão para a categoria certa da loja (hoje todos apontam para `/loja/`) |
| Home: depoimentos | substituir os 3 depoimentos de exemplo pelos reais, com autorização de uso |
| Loja: grade de produtos | 9 peças por página, 3 colunas e as 5 ordenações do protótipo (mais recentes, mais populares, menor preço, maior preço, melhor avaliados) |
| Loja: filtros de preço, cor e tamanho | ver a decisão abaixo: o Elementor não traz filtro de atributo pronto, e este item precisa de definição da equipe |
| Produto: galeria | ligar zoom e lightbox nativos do WooCommerce e conferir o corte 1:1 das fotos |
| Produto: variações | cor e tamanho nascem dos atributos globais Cor (tipo cor) e Tamanho (tipo botão); o plugin **Variation Swatches for WooCommerce** (aprovado) troca os seletores padrão pelos botões do protótipo. Conferir esgotado riscado ou esmaecido, como no protótipo |
| Produto: tabela de medidas | preencher com as medidas reais de cada peça (nada de tabela de exemplo) |
| Sacola: cupom | deixar o campo de cupom visível: é por ele que entra o BEMVINDO10 |
| Sacola, checkout e conta: endereços do WooCommerce | em WooCommerce > Configurações > Avançado, apontar cada tela para a página certa (sacola, finalizar compra e minha conta) |
| Checkout: compra como visitante | ligar em WooCommerce > Configurações > Contas e privacidade, como pede o dossiê |
| Checkout: pagamento | conferir Pix, cartão e boleto ativos na conta do Mercado Pago antes de qualquer teste |
| Pedido recebido | conferir se o resumo aparece depois de um pedido de teste e se o e-mail de confirmação sai com o remetente da loja |
| Conta, sacola e checkout fora do Google | marcar `noindex` no Yoast nestas três páginas e deixar fora do sitemap |
| Desejos | instalar o **TI WooCommerce Wishlist** (aprovado), gerar a página da lista com o endereço `/lista-de-desejos/` e conferir o contador do coração no cabeçalho; só publicar depois desse teste |
| Site inteiro: botão do WhatsApp | usar **Floating Elements** do Elementor (Site Settings), com o número (15) 99123-4567 e a entrada depois de rolar a página, como no protótipo |

### 4.4 Uma decisão pendente: os filtros da loja

O protótipo tem filtros por categoria, faixa de preço, cor e tamanho. No arquivo
`04-loja.json`, a **categoria** já entra dinâmica (widget de categorias do
WooCommerce). Os outros três filtros estão marcados como
`[CONFIGURAR NO EDITOR]`, porque o Elementor Pro não traz filtro por atributo
pronto dentro do canvas. Caminhos possíveis, para a equipe decidir:

| Caminho | Como funciona | Custo |
|---|---|---|
| Blocos de filtro do próprio WooCommerce | são blocos do Gutenberg (filtrar por preço, por atributo e por estoque) | funcionam na página da loja montada com blocos, não dentro do template do Elementor |
| Plugin de filtros para WooCommerce | entra como widget no template e filtra sem recarregar a página | precisa de aprovação prévia, pela regra do projeto |
| Links por atributo | cada cor e tamanho vira um link com o atributo no endereço (o WooCommerce entende `?filter_cor=...`) | sem plugin, mas sem contagem dinâmica nem limpar filtros elegante |

Nenhum caminho foi escolhido neste arquivo. Enquanto a decisão não sai, a loja
publica com categoria, ordenação e paginação, que já vêm do WooCommerce.

### 4.5 Plugins aprovados (decisão de 16/10/2026)

Dois plugins foram aprovados para funções que o WooCommerce não traz prontas.
Os dois começam na **versão gratuita**, instalada pela equipe no staging:

| Função | Plugin | Por que ele | Limite da versão gratuita |
|---|---|---|---|
| Lista de desejos | **TI WooCommerce Wishlist** | bem avaliado, lista para visitante e logado, página própria da lista | uma lista por cliente (basta para esta loja); listas múltiplas e analytics são do Premium |
| Cor e tamanho em botões (swatches) | **Variation Swatches for WooCommerce** (GetWooPlugins) | é o mais usado da categoria, troca o seletor padrão por cor, imagem e botão, e trata variação esgotada | esgotado tratado até 30 variações por produto (basta para o catálogo previsto); swatches na grade da loja são do Pro |

Regras de uso: instalar um por vez, testar a loja depois de cada um e medir o
peso da página antes e depois (meta de desempenho do dossiê). Versão Pro só
entra se o teste mostrar falta real, com nova aprovação.

---

## 5. As partes e as páginas

### 5.1 O que já está pronto

| Arquivo | Título | Tipo | O que é |
|---|---|---|---|
| `01-cabecalho.json` | Cabeçalho do site | Header | faixa verde do topo, logo, menu e os quatro ícones (busca, conta, desejos, sacola) |
| `02-rodape.json` | Rodapé do site | Footer | newsletter, quatro colunas, faixa de segurança e formas de pagamento, base com CNPJ e links de política |
| `03-home.json` | Página inicial | Página | hero, faixa de benefícios, categorias, produtos em destaque, ocasiões, editorial do ateliê, coleção, depoimentos, posts recentes e perguntas frequentes |
| `04-loja.json` | Arquivo da loja | Arquivo de produtos | cabeçalho da loja, coluna de filtros, grade dinâmica com ordenação e paginação e a faixa verde de ajuda |
| `05-produto.json` | Página do produto | Produto único | trilha, galeria, nome, avaliação, preço, descrição curta, variações e compra, garantias, abas do produto, relacionados e a faixa de ajuda de tamanho |
| `06-carrinho.json` | Sacola | Página | título e o widget clássico de carrinho do WooCommerce, com campo de cupom |
| `07-checkout.json` | Finalizar compra | Página | título e o widget clássico de checkout, com compra como visitante |
| `08-pedido-recebido.json` | Pedido recebido | Página | resumo dinâmico do pedido e os botões para pedidos e loja |
| `09-conta.json` | Minha conta | Página | título e o widget My Account, com pedidos, endereços e dados |
| `10-desejos.json` | Lista de desejos | Página | título e aviso de pendência: a lista em si depende de plugin aprovado |

### 5.2 As páginas (próximas partes)

A página inicial (`03-home.json`) foi entregue na parte 2, e a loja e a página do produto (`04-loja.json` e `05-produto.json`) na parte 3. O funil de compra (`06` a `10`) entrou na parte 4. Faltam:

Cada página do protótipo vira um arquivo. Os endereços sugeridos são os mesmos do
protótipo, para o site nascer com os links certos.

| # | Página | Arquivo previsto | Tipo no Elementor | Endereço |
|---|---|---|---|---|
| 11 | Diário | `11-blog.json` | arquivo de posts | `/diario/` |
| 12 | Artigo | `12-post.json` | post único | `/diario/<artigo>/` |
| 13 | Busca | `13-busca.json` | resultados de busca | `/busca/` |
| 14 | Página não encontrada | `14-404.json` | página 404 | 404 |
| 15 | Sobre | `15-sobre.json` | página | `/sobre/` |
| 16 | Contato | `16-contato.json` | página | `/contato/` |
| 17 | Perguntas frequentes | `17-faq.json` | página | `/perguntas-frequentes/` |
| 18 | Guia de medidas | `18-guia-medidas.json` | página | `/guia-de-medidas/` |
| 19 | Coleção | `19-lookbook.json` | página | `/colecao/` |
| 20 | Trocas e devoluções | `20-trocas.json` | página | `/trocas-e-devolucoes/` |
| 21 | Envio e entrega | `21-envio.json` | página | `/envio-e-entrega/` |
| 22 | Política de privacidade | `22-privacidade.json` | página | `/politica-de-privacidade/` |
| 23 | Termos de uso | `23-termos.json` | página | `/termos-de-uso/` |
| 24 | Política de cookies | `24-cookies.json` | página | `/politica-de-cookies/` |

**Sobre o número de arquivos.** O dossiê falava em 21 arquivos JSON. A conta
página por página dá 24: as duas partes do site (cabeçalho e rodapé) mais as 22
páginas do protótipo. Preferimos não juntar páginas diferentes em um arquivo só,
porque no Elementor cada página tem o seu. Se a ideia for ficar exatamente nas 21,
o jeito mais natural é juntar as três páginas legais (privacidade, termos e
cookies) em um modelo único de "página de documento", com o texto vindo do
`pages-conteudo.md` do Bloco C. Fica a critério da equipe, e é uma decisão
registrada no diário.

---

## 6. Regras que os arquivos seguem

Todas conferidas por `python3 tools/blocob_confere.py`:

| Regra | Como aparece no arquivo |
|---|---|
| Só containers, nunca section/column | todo elemento é `container` ou `widget` |
| Nenhum widget proibido | nada de HTML, shortcode, CSS livre ou widgets Atomics (`e-...`) |
| Cor e tipografia por Global Colors / Global Fonts | cada cor aponta para `globals/colors?id=...` |
| Container nomeado | todo container tem `_title`, o nome que aparece na estrutura |
| Id de elemento único | 7 caracteres, sem repetição no arquivo |
| Nada do protótipo | nenhum link terminando em `.html` |

---

## 7. O que **não** foi verificado (leitura obrigatória)

- **Importação:** nenhuma. Não tenho WordPress, painel nem banco de dados.
- **Renderização no navegador real:** o que o Elementor desenha depois de
  importar só a equipe vê.
- **Nomes de controles dos widgets do Elementor Pro:** o Elementor Pro não é
  aberto, então os nomes de ajuste dos widgets Pro (menu, sacola, busca, produto)
  foram escritos a partir da documentação. Um ajuste com nome diferente não
  quebra nada: ele é simplesmente ignorado na importação, e o time escolhe no
  editor. Isso está previsto na tabela da seção 4.3.
- **Widgets do WooCommerce:** a sacola, o checkout e a conta usam os widgets
  oficiais do Elementor Pro. Se a versão instalada não tiver algum deles
  (`[CONFERIR]`), o caminho é a página clássica do WooCommerce com o mesmo
  cabeçalho e rodapé, que é o que o dossiê já previa como plano B.
- **Peso e desempenho:** sem site montado não há medição de LCP, CLS ou INP.
  A meta do dossiê continua valendo e é medida no Bloco C.

---

## 8. Ordem recomendada de trabalho

1. Confirmar versões e tema no staging (seção 2).
2. Criar as cores e as fontes globais (seção 3).
3. Rodar o `ajusta-ids.py` (seção 3.3) e conferir com o `blocob_confere.py`.
4. Importar o cabeçalho, definir a condição e ajustar o menu.
5. Importar o rodapé, definir a condição e ajustar a newsletter.
6. Conferir o site no navegador: cabeçalho e rodapé aparecendo em todas as páginas.
7. Importar a página inicial (`03-home.json`), criar a página Início, definir como página inicial do site e fazer os ajustes da seção 4.3.
8. Conferir a home no celular e no computador antes de seguir.
9. Importar a loja e a página do produto pelo Theme Builder e definir as
   condições: arquivo de produtos (loja e categorias) e produto único (todas as
   peças). Decidir o caminho dos filtros (seção 4.4).

10. Importar as cinco páginas do funil como páginas comuns, publicar e apontar
    cada uma no WooCommerce (Configurações > Avançado). Não publicar a lista de
    desejos até o plugin ser aprovado.

Quando o funil estiver no ar, o próximo lote é o conteúdo editorial e
institucional: diário, artigo, busca, 404, sobre, contato, perguntas frequentes,
guia de medidas e coleção.
