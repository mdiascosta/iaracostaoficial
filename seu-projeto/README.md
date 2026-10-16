# Iara Costa: protótipo HTML (Bloco A)

Este é o **protótipo estático** da loja Iara Costa. Ele existe para validar
visual, conteúdo e acessibilidade **antes** de construir no WordPress. O que for
aprovado aqui é reproduzido no Elementor (Bloco B).

> **Aviso:** este protótipo **não vai para produção**. Nada aqui é importado no
> WordPress. Ele roda no navegador, sem banco de dados e sem servidor de
> aplicação: é só HTML, CSS e JavaScript puros.

---

## 1. Como abrir

**Do jeito mais simples:** dê duplo clique em `index.html`. Abre no navegador e
todos os links funcionam.

**Com servidor local** (recomendado, evita restrições do navegador em alguns
casos):

```bash
cd seu-projeto
python3 -m http.server 8080
```

Depois abra `http://localhost:8080` no navegador.

---

## 2. O que existe no protótipo

22 páginas, todas com o mesmo header, footer e sistema de cores:

| Grupo | Páginas |
|---|---|
| Loja | `index.html`, `loja.html`, `produto.html` |
| Compra | `carrinho.html`, `checkout.html`, `pedido-recebido.html` |
| Cliente | `conta.html`, `desejos.html` |
| Busca e erro | `busca.html`, `404.html` |
| Conteúdo | `blog.html`, `post.html`, `lookbook.html` |
| Institucional | `sobre.html`, `contato.html`, `faq.html`, `guia-medidas.html` |
| Políticas | `trocas.html`, `envio.html`, `privacidade.html`, `termos.html`, `cookies.html` |

### Novidades da v0.1.13 (cartões de envio e pagamento e regras de negócio fechadas)

| Peça | Como ficou |
|---|---|
| Checkout | Formas de envio e de pagamento em cartões clicáveis no padrão da imagem enviada: rádio, título, linha de apoio e valor |
| Envio | PAC, SEDEX e Retirar no ateliê, cada um com prazo e valor, e o endereço do ateliê no cartão da retirada |
| Pagamento | Pix com a etiqueta "5% off" e cartão de crédito com "6x sem juros" e parcela mínima de R$ 50,00 |
| Campos do cartão | Aparecem quando o cartão é escolhido, com máscaras de número, validade e CVV. São demonstração: sem `name`, nada é enviado nem guardado, e o aviso explica que no site publicado os campos são do Mercado Pago |
| Frete grátis | Passa a contar o valor líquido, depois do cupom e do desconto do Pix, em todas as páginas |
| R$ 15,00 | Confirmado como regra do PAC em SP, RJ, MG e ES; o SEDEX e as demais regiões saem pelo cálculo dos Correios |
| Prazos | 2 dias úteis para pronta entrega e de 5 a 7 dias úteis para peças sob encomenda |
| Trocas | 30 dias corridos para trocar de tamanho, primeira troca gratuita, e 7 dias de arrependimento com frete de retorno por conta da loja |
| Cuidados | Lavagem à mão ou ciclo delicado com sabão neutro, sem alvejante à base de cloro, secagem à sombra na horizontal e passar até 110°C |
| Privacidade | Encarregado de dados com o e-mail `dpo@iaracosta.com.br` e data das páginas legais em 16 de outubro de 2026 |
| Cabeçalho | Marca em 20px, sem `clamp()`, como a especificação da empresa pede |

**Valores conferidos na cesta de exemplo:** produtos R$ 974,00, cupom R$ 97,40,
Pix R$ 832,77, cartão R$ 876,60 e 6x de R$ 146,10 sem juros.

### Novidades da v0.1.12 (dados reais da empresa e regras de venda confirmadas)

| Peça | Como ficou |
|---|---|
| Identificação da empresa | Razão social, nome fantasia, CNPJ, inscrição estadual e endereço do ateliê no rodapé de todas as páginas, no Contato e nos Termos de uso (o Decreto 7.962/2013 exige que fiquem visíveis) |
| Atendimento | E-mail, telefone/WhatsApp e horário no rodapé e no Contato, com prazo de resposta de 24 horas úteis |
| Formas de pagamento | Pix com 5% de desconto e cartão em até 6x sem juros, pelo Mercado Pago. Boleto, transferência, PayPal e as bandeiras que não foram confirmadas saíram do site |
| Frete | Correios (PAC e SEDEX por CEP), R$ 15,00 no Sudeste e frete grátis acima de R$ 299. Os valores de exemplo de PAC e SEDEX saíram de todas as páginas |
| Cupom BEMVINDO10 | Regra fechada: 10% na primeira compra, para clientes novos, sem acúmulo com outras promoções nem com peças em liquidação |
| Página de Envio | Reescrita com as regras confirmadas, incluindo o que os Correios calculam e o que ainda depende da empresa |

**Dois pontos ficaram abertos de propósito:** o valor fixo de R$ 15,00 no Sudeste
está escrito como PAC, e a página pergunta se ele vale também para o SEDEX; e a
promessa de "troca fácil em 30 dias" que existia na home ficou marcada como
`[A DEFINIR]`, porque prazo e frete de troca são decisão da empresa, não número
que a gente possa inventar.

### Novidades da v0.1.11 (pente fino no HTML e no CSS e o JavaScript do template)

| Peça | Como ficou |
|---|---|
| Pente fino | As 22 páginas, 25 parciais, 4 CSS e 4 JS passaram por um conferidor com parser de verdade (html5lib e tinycss2). Placar: nenhum erro de sintaxe, nenhum id repetido, nenhuma âncora quebrada, nenhum campo sem rótulo, nenhum arquivo faltando |
| HTML quebrado | Termos e Cookies tinham `<p margin-bottom:0">`: um estilo escrito como se fosse atributo. Virou classe no CSS |
| Medidas das fotos | As duas fotos do resumo do checkout declaravam tamanho só em `style=""`; agora trazem as medidas reais do arquivo |
| Estilos no HTML | Quarenta estilos escritos direto no HTML viraram regras com nome, presas à tela pela classe `page-*` do `<body>` |
| CSS morto | Saíram o contador antigo da sacola, a classe de seção sem uso, quatro cores de swatch não usadas e o `style="width:0%"` da gaveta |
| Estados que faltavam | Carregando (esqueleto) e erro de campo ganharam desenho nas páginas, e os três estados de estoque agora aparecem lado a lado |
| JavaScript do template | Cada melhoria inicia isolada (uma falha não derruba as outras), botões + e − e remover peça na sacola, cupom BEMVINDO10, máscara de CEP e de telefone, cálculo de frete e recado que muda conforme o meio de pagamento |
| Sem pular de lado | A trava de rolagem da gaveta ficou em CSS (`scrollbar-gutter: stable`), sem script |
| Régua de verificação | O teste de navegador e o pente fino agora vivem no repositório: `tools/test.js` e `tools/pente-fino.py` |

**O que do template não foi copiado:** o JavaScript do zip calcula frete com valores
fixos (PAC e SEDEX) e pede o número do cartão na própria página. Aqui o frete só
responde a regra confirmada (grátis acima de R$ 299) e o resto fica `[A DEFINIR]`;
dados de cartão são digitados na página do gateway, que ainda não existe.

### Novidades da v0.1.10 (fontes na escala do template e cabeçalho limpo)

| Peça | Como ficou |
|---|---|
| Fontes | Tudo desceu para a escala do template: Display 24px (nome da página, título de produto, hero e faixas) e Heading 18px (títulos de seção e de card). Antes o nome da página chegava a 52px |
| Nome da página | Playfair Display 400, 24px, entrelinha 1.1 e entreletra 0.105em, o mesmo tratamento do título do template |
| Cabeçalho de página | Sem fundo e sem enfeites: só a trilha de navegação, o nome da página e um fio embaixo |
| Texto de apoio | Saiu de dentro do cabeçalho e abre o conteúdo, logo abaixo do fio |
| Loja | A contagem de peças e o recado "do P ao GG" passaram para a barra da coleção, ao lado de "Ordenar por" |
| Contador da sacola | 11px, o mínimo permitido pela regra de contraste |

**Uma observação sobre o template:** o zip usa Caption 9px e Tagline 8px. Aqui esses
dois continuam em 11px, porque a decisão E0 do dossiê e a regra de contraste do
próprio projeto não permitem texto tão pequeno em fundo claro. Se a cliente quiser
os 9px e 8px do template, precisa ser uma decisão dela.

### Novidades da v0.1.9 (Minha conta, Contato e Sobre)

| Página | Como ficou |
|---|---|
| Minha conta | Dois cartões no topo: Entrar e Criar conta. Abaixo, o painel da cliente com navegação lateral (inclui Meus tamanhos), pedidos em tabela com selo de status e atalho para solicitar troca |
| Contato | Formulário em quadro de papel sobre fundo suave; canais de atendimento na coluna da direita, cada um em quadro com borda; seção do mapa com quadro de exemplo (o endereço entra depois); bloco de dúvidas rápidas com quatro respostas |
| Sobre | Primeiro bloco com texto à esquerda e imagem à direita; seção de missão, visão e compromisso em três cartões; faixa de frase com fundo suave; faixa com três fotos do processo |
| Coleção | Cabeçalho com "Vestuário feminino do P ao GG" e atalho para o guia de medidas, como no template de referência |

### Novidades da v0.1.8 (rodapé, cabeçalho de página e internas)

| Peça | Como ficou |
|---|---|
| Rodapé | A faixa de segurança ganhou "Formas de pagamento" (8 formas em quadros de texto) e "Segurança" (2 selos desenhados). Nenhuma marca de terceiro foi usada como imagem |
| Cabeçalho de página | Trilha de navegação dentro do bloco, fio curto em Terracota, linha de olho acima do título (ex.: "Central de ajuda" no FAQ) e faixa de fundo suave |
| Página Sobre | Galeria com duas fotos, faixa com quatro números da loja e frase de posicionamento |
| FAQ, guia de medidas, trocas, envio e páginas legais | Índice de leitura na coluna da esquerda, com atalhos que levam direto a cada seção |
| Guia de medidas | Os três passos aparecem numerados em 01, 02, 03 |
| Diário e lookbook | Destaque do Diário com texto próprio ao lado da foto; lookbook em ziguezague, com cada look numerado |
| Limpeza | As margens que estavam escritas dentro do HTML dessas páginas passaram para o CSS |

### Novidades da v0.1.7 (cabeçalho da loja, ordenação e trilha)

| Ajuste | Como ficou |
|---|---|
| Trilha de navegação | Separador visível em barra no tom Muted (4,3:1), mais respiro entre os itens e a página atual em Ink; a trilha entrou nas duas páginas que não tinham (Pedido recebido e Erro 404) |
| Cabeçalho de página | Título de 46px no máximo, respiro mais curto e contagem de peças alinhada pela base do texto, em todas as páginas internas |
| Linha de filtros e ordenação | "Filtros / Limpar" e "Ordenar por" abrem na mesma linha, com a mesma altura e o mesmo fio embaixo |
| Seletor de ordenação | Passou a usar a classe de campo do site: 46px de altura, borda de linha, seta em SVG e foco visível; no celular ocupa a linha inteira |

### Novidades da v0.1.6 (decisões da cliente)

| Decisão | Como ficou |
|---|---|
| Frete grátis | Acima de R$ 299, confirmado. O protótipo já estava em 299 do começo ao fim; o comentário do código e a lista de pendências foram atualizados |
| Catálogo | 12 peças visíveis, confirmado. A página 404 e a página Sobre, que ainda diziam 10 peças, foram corrigidas |
| Newsletter do rodapé | Fica, confirmado. A home continua com uma única faixa sálvia antes do rodapé |

### Novidades da v0.1.5 (ajustes pedidos pela cliente)

| Ajuste | Como ficou |
|---|---|
| Faixa antes do rodapé | Todas as 22 páginas fecham com uma faixa sálvia de largura total: o fundo ocupa a tela inteira e o texto fica na largura do header |
| Seção de newsletter | Saiu a faixa compacta de lista de espera que ficava no meio da home (v0.1.4); a newsletter do rodapé continua, como na referência |
| Largura do template | Todas as páginas passam a usar a mesma largura do header (1688px); nas páginas de leitura a linha do texto corrido fica em 72 caracteres |
| Revisão de CSS | Amostra de cor "carvão" corrigida, passos do pedido com estilo, caixa `.promo` substituída pela faixa e limpeza das regras sem uso |

### Novidades da v0.1.4 (ajustes pedidos pela cliente)

| Ajuste | Como ficou |
|---|---|
| Perguntas frequentes | Faixa sálvia antes do rodapé com cinco perguntas em acordeão, com as mesmas respostas da página Perguntas frequentes e link para ela |
| Lista de espera | Virou faixa compacta no meio da home, entre os destaques e a vitrine por ocasião, com o formulário em uma linha |
| Rodapé | A faixa de perguntas encosta no rodapé e passa a ser o separador verde, sem o vão branco e sem dois pedidos de e-mail em sequência |
| Cor sálvia | Continua sendo a única cor de faixa do site: uma pequena no meio e uma antes do rodapé |

### Novidades da v0.1.3 (ajustes pedidos pela cliente)

| Ajuste | Como ficou |
|---|---|
| Faixa de benefícios | Os quatro itens ocupam a largura do container do header, com o ícone centralizado acima do texto e fio fino entre eles |
| Depoimentos | Cada frase virou um cartão de papel com borda fina e aspas em serifa, sobre o fundo areia |
| Diário | Cada post virou cartão fechado: foto 4:3 em cima, texto embaixo, fundo de papel e borda |
| Rodapé | Newsletter em uma linha, quatro colunas, faixa de segurança e pagamento e a base com os dados da empresa |
| Segurança e pagamento | Quatro informações com ícone: formas de pagamento, dados protegidos, pedido rastreado e os 7 dias do CDC Art. 49, com aviso de que os selos entram no go-live |
| Cabeçalhos internos | Mais respiro, título maior em serifa, texto de apoio estreito e trilha em caixa alta miúda, em 17 páginas |
| Loja | A contagem de peças subiu para o canto direito do cabeçalho da página |

A newsletter voltou ao rodapé porque a referência enviada pela cliente mostra ela
ali. Para não pedir o mesmo e-mail duas vezes na home, os dois convites ficaram
com assuntos diferentes: a faixa sálvia é a lista de espera dos lançamentos e o
rodapé é a assinatura do conteúdo do ateliê.

### Novidades da v0.1.2 (ajustes pedidos pela cliente)

| Ajuste | Como ficou |
|---|---|
| Largura das seções | A grade acompanha a barra do header: 1688px. Páginas de leitura ficam em 1180px, para a linha não ficar longa demais |
| Cores das seções | Três fundos da própria paleta: areia claríssimo (Hover Soft), terracota claro (Accent Soft, no editorial) e sálvia (na faixa da lista de espera) |
| Loja | Filtro à esquerda em coluna de 240px: categorias, faixa de preço, cor e tamanho. No celular vira gaveta pelo botão "Filtros" |
| Rodapé | Enxuto: quatro colunas curtas, identificação da empresa e links de política. Saíram a newsletter e a faixa de selos (na v0.1.3 o rodapé foi refeito na estrutura da imagem enviada pela cliente) |
| Newsletter | Ficou só na faixa verde sálvia da home, para não pedir o mesmo e-mail duas vezes na mesma página (na v0.1.3 voltou também ao rodapé, em forma de assinatura do conteúdo) |

### Novidades da v0.1.1 (super layout)

| Bloco | Onde está |
|---|---|
| Faixa de benefícios centralizada (4 itens) | `index.html`, logo abaixo do hero |
| Categorias com numeral 01/02/03 | `index.html` |
| Card de produto com selo, coração, nota, tamanhos e preço promocional | `index.html`, `loja.html` e todas as grades |
| Vitrine por ocasião (dia a dia, trabalho, festa, acessórios) | `index.html` |
| Editorial "Um ateliê, três gestos" e coleção Terra & Linho | `index.html` |
| Faixa verde sálvia de lista de espera e newsletter | `index.html` e rodapé de todas as páginas |
| Mini-sacola lateral com barra do frete grátis | todas as páginas, ao clicar em "Adicionar à sacola" |
| Filtro lateral da loja (categoria, preço, cor, tamanho) | `loja.html`, coluna à esquerda |
| Aviso rápido (toast) ao salvar nos desejos | todas as páginas, ao clicar no coração |

### Estados de interface demonstrados

O dossiê pede que todos os estados de tela estejam representados. Onde procurar:

| Estado | Onde ver |
|---|---|
| Carregando | `produto.html`, referência do estado carregando (esqueleto) |
| Busca sem resultado | `busca.html`, seção final |
| Produto esgotado | `produto.html`, final da página, com os três estados de estoque juntos |
| Erro em campo de formulário | `checkout.html`, final da página |
| Cupom não reconhecido | `carrinho.html`, ao aplicar um código que não existe |
| CEP incompleto | `carrinho.html`, ao calcular o frete com menos de 8 números |
| Variação indisponível | `produto.html`, tamanho GG desabilitado |
| Sacola vazia | `carrinho.html`, final da página |
| Pagamento recusado | `checkout.html`, final da página |
| Pedido confirmado | `pedido-recebido.html` |
| Lista de desejos vazia | `desejos.html`, final da página |
| Mensagem enviada | `contato.html`, após o formulário |

---

## 3. Estrutura de arquivos

```
seu-projeto/
├── *.html                     (22 páginas)
├── README.md                  (este arquivo)
├── SPECS-DE-IMAGEM.md         (lista de fotos a produzir)
├── assets/
│   ├── css/
│   │   ├── style.css          (tokens, base, componentes)
│   │   ├── header.css         (header, busca, menu, footer)
│   │   ├── pages.css          (blocos específicos de página)
│   │   └── comercio.css       (benefícios, categorias, card, ocasião, mini-sacola)
│   ├── js/
│   │   ├── header.js          (menu mobile e faixa de busca)
│   │   ├── swatches.js        (galeria, variações, abas)
│   │   ├── filtros.js         (filtro lateral e ordenação da loja)
│   │   └── loja.js            (desejos, sacola e mini-sacola)
│   ├── fonts/
│   │   └── LEIA-ME.md         (instruções de hospedagem local das fontes)
│   └── img/                   (31 fotos de exemplo em JPG + favicon)
├── custom-code/               (reservado)
├── docs/                      (reservado)
└── templates/                 (reservado)
```

---

## 4. Identidade visual aplicada

Todas as cores estão em variáveis CSS no topo de `style.css`. Mudar a paleta em
um lugar muda o site inteiro.

| Token | HEX | Uso |
|---|---|---|
| `--iara-accent` | #a45f43 | Terracota, marca e botões principais |
| `--iara-sage` | #546858 | Verde sálvia, barra de anúncio e destaques |
| `--iara-ink` | #2d2925 | Texto principal |
| `--iara-accent-dark` | #78452f | Hover e interação |
| `--iara-paper` | #fffdf9 | Fundo |
| `--iara-ink-soft` | #625a52 | Texto secundário |
| `--iara-muted` | #81786e | Legendas, só em texto de 18px ou maior |
| `--iara-line` | #ded8ce | Bordas |
| `--iara-accent-soft` | #e4cbb5 | Separadores |

**Regra de acessibilidade:** `--iara-muted` nunca em texto menor que 18px,
porque o contraste fica abaixo do mínimo exigido pela WCAG AA. Nesses casos use
`--iara-ink-soft`.

Fontes: **Jost** (400 e 600) para interface, **Playfair Display** (400) para
títulos e logo. Ver `assets/fonts/LEIA-ME.md`.

**Escala de tamanhos** (tabela do template, aplicada na v0.1.10): Display 24px,
Heading 18px, Body 15px, Small 12px, Micro 11px. Caption e Tagline ficam em 11px
no lugar dos 9px e 8px do template, por causa da regra de contraste abaixo.

---

## 5. Decisões de acessibilidade (WCAG 2.2 AA)

- Link "Pular para o conteúdo" como primeiro elemento focável.
- Contorno de foco visível em tudo, em terracota escuro.
- Área de toque mínima de 44x44 pixels em botões, ícones e campos.
- Menu mobile fecha com ESC e devolve o foco para o botão que o abriu.
- Faixa de busca: abre pela lupa, foco vai para o campo, ESC fecha.
- Campo de busca com 16px no celular, o que evita o zoom automático do iOS.
- Nada depende só de cor: a variação escolhida sempre aparece escrita.
- `prefers-reduced-motion` respeitado: quem pede menos animação não recebe.
- Um único H1 por página e hierarquia de títulos correta.
- Toda imagem com texto alternativo descritivo.

---

## 6. O que o protótipo NÃO faz

Importante para não gerar expectativa errada:

- **Não há banco de dados.** Nada é salvo. Recarregue a página e tudo volta.
- **Não há cálculo automático de verdade.** Preços e totais saem de contas
  simples feitas no navegador, para a tela reagir ao que você clica. O frete real
  é dos Correios e quem calcula é o WooCommerce: no protótipo, o recado mostra só
  a regra confirmada (R$ 15,00 no Sudeste e grátis acima de R$ 299).
- **Não há pagamento.** Nenhum gateway está conectado. Nenhuma cobrança acontece.
- **Não há envio de formulário.** Os formulários validam no navegador e param aí.
- **Não há login.** A página de conta mostra dados de exemplo.
- **Não há busca real.** O campo leva para uma página com resultados de exemplo.

---

## 7. Dados de exemplo

**Todos** os dados são de exemplo, autorizados pela equipe na fase de coleta:

- Os **12 produtos** de exemplo (nomes, preços, estoque, variações) são
  fictícios e vivem em um só lugar: `tools/produtos.json`.
- Depoimentos são fictícios e estão marcados como tal na página.
- Imagens são **fotos de exemplo vindas do template de referência** enviado pela
  cliente. Direitos e origem: `[CONFERIR]` antes de publicar.
- **Os dados da empresa são reais** (informados em 16/10/2026) e estão no rodapé,
  no Contato e nos Termos: razão social, nome fantasia, CNPJ, inscrição estadual,
  endereço do ateliê, e-mail, telefone e horário de atendimento.
- **As regras de venda confirmadas** também são reais: Pix com 5% de desconto,
  cartão em até 6x sem juros pelo Mercado Pago, Correios com R$ 15,00 no Sudeste,
  frete grátis acima de R$ 299 e a regra do cupom BEMVINDO10.
- O que continua marcado: prazo de produção e de troca, valores e prazos por
  região fora do Sudeste, encarregado de dados (DPO), composição e cuidados das
  peças, autoria dos textos do diário e a data de aprovação das páginas legais.

Faixa de aviso no topo de todas as páginas: **PROTÓTIPO · DADOS E TEXTOS DE
EXEMPLO · NÃO PUBLICAR**. Remover essa faixa é um dos passos do go-live, e só
depois que os dados forem reais.

---

## 8. Como editar o protótipo

O header e o footer aparecem em 22 arquivos. Para não corrigir 22 vezes, eles
vivem em um só lugar, em `tools/partials/`, e são montados por um script:

```bash
python3 tools/build.py            # gera todas as páginas
python3 tools/build.py --part 2   # gera só a parte 2
python3 tools/build.py --check    # mostra o que seria gerado, sem escrever
```

Depois de mexer em qualquer arquivo de CSS ou JS, rode o gerador de novo: ele
acrescenta um selo de versão no endereço dos arquivos, o que força o navegador a
baixar a versão nova em vez de usar a do cache.

**Card de produto em um só lugar.** O mesmo card aparece em 8 páginas. Em vez de
copiar o HTML, as páginas escrevem um marcador:

```html
<ul class="product-grid product-grid--four">
  <!--CARDS:blusa-linho-terracota,vestido-midi-salvia,colar-ceramica-->
</ul>
```

O gerador troca cada marcador pelo card montado, usando os dados de
`tools/produtos.json`. Mudar um preço lá muda o site inteiro.

### Verificação automática

```bash
python3 tools/check.py
```

Confere: tags HTML balanceadas, um H1 por página, alt em todas as imagens,
referências de arquivo válidas, ausência de script inline e ausência de travessão
nos textos.

Resultado esperado hoje: **tudo certo**.

**Teste de navegador (jsdom).** Abre as 22 páginas, carrega os scripts que cada
página chama e simula cliques: menu, busca, filtros da loja, desejos, sacola,
cupom, frete, máscaras do checkout e acordeão.

```bash
npm install          # uma vez só, instala o jsdom
node tools/test.js   # imprime PASS/FAIL e sai com erro se algo falhar
```

Resultado esperado hoje: **649 verificações, nenhuma falha**.

**Pente fino de HTML e CSS.** Lê os arquivos com parser de verdade (`html5lib` e
`tinycss2`) e confere doze pontos: sintaxe, ids repetidos, links e âncoras, rótulos
de acessibilidade, imagens e arquivos, classes sem CSS, CSS sem uso e ganchos
`data-*` que nenhum script lê. Ele só aponta; a correção é feita à mão.

```bash
python3 -m venv .venv && .venv/bin/pip install html5lib tinycss2   # uma vez só
.venv/bin/python tools/pente-fino.py
```

Resultado esperado hoje: **todas as doze conferências sem nenhum achado**.

### Imagens de exemplo

```bash
python3 tools/make_placeholders.py
```

Recria os retângulos SVG de exemplo da v0.1.0. **Não é mais necessário:** na
v0.1.1 as fotos de exemplo vieram do template de referência e os SVGs saíram do
projeto. O script fica guardado caso seja preciso gerar imagem provisória para
alguma peça nova.

---

## 9. Próximos passos

1. **Conferir o visual** nas três larguras: celular, tablet e desktop, com
   atenção à faixa de benefícios centralizada e aos blocos novos da home.
2. **Aprovar ou pedir ajustes** em cada grupo de página.
3. **Produzir as fotos** seguindo `SPECS-DE-IMAGEM.md`.
4. **Bloco B:** reproduzir no Elementor, usando Global Colors e Global Fonts.
   Este CSS e este JS não são carregados no WordPress.
5. **Bloco C:** kit, CSV de produtos, guias de instalação e segurança.

---

## 10. Pendências que travam a publicação

Nada nesta lista impede a conferência visual do protótipo. Tudo aqui impede o
go-live:

- [ ] Fotos reais de produto, categoria, banner e logo.
- [x] **Razão social, CNPJ e endereço** informados em 16/10/2026 e já no rodapé,
      no Contato e nos Termos (exigência do Decreto 7.962/2013).
- [x] **E-mail e WhatsApp de atendimento, com horário**, informados em 16/10/2026
      (24 horas úteis, segunda a sexta, das 9h às 18h).
- [x] **Gateway definido: Mercado Pago** (16/10/2026). Falta ligar a conta e testar
      em ambiente de teste antes do go-live.
- [x] **Regras de pagamento definidas:** Pix com 5% de desconto e cartão em até 6x
      sem juros (16/10/2026).
- [x] **Frete definido:** Correios com cálculo por CEP, R$ 15,00 no Sudeste e
      grátis acima de R$ 299 (16/10/2026).
- [x] **Frete grátis definido: acima de R$ 299** (confirmado pela empresa em
      16/10/2026; o dossiê previa R$ 199). O protótipo já estava todo em 299.
- [x] **Catálogo definido: 12 peças visíveis** (confirmado em 16/10/2026, igual
      ao template). Textos que ainda diziam 10 peças foram corrigidos.
- [x] **Newsletter do rodapé mantida** (confirmado em 16/10/2026).
- [ ] **Direitos das 31 fotos** vindas do template de referência.
- [x] **Regras do cupom BEMVINDO10 definidas** (16/10/2026): 10% na primeira
      compra, para clientes novos, sem acúmulo com outras promoções nem com peças
      em liquidação.
- [ ] Duas dúvidas de frete: se o valor fixo de R$ 15,00 no Sudeste vale também
      para o SEDEX e se o frete grátis conta o subtotal antes ou depois do cupom.
- [ ] Prazo e frete da troca por tamanho (a home anunciava 30 dias sem confirmar).
- [ ] Encarregado de dados (DPO), para a Política de Privacidade.
- [ ] Regime tributário e emissão de nota fiscal definidos com o contador.
- [ ] Revisão jurídica das três páginas legais e de trocas.
- [ ] Plugin de lista de desejos aprovado, ou o coração sai do header.
