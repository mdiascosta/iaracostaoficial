# Histórico de versões: Iara Costa E-commerce

Este arquivo registra **o que mudou em cada versão** do projeto. Serve para duas
coisas: saber o que foi entregue quando, e poder voltar a uma versão anterior
sem depender da memória de ninguém.

---

## Como o versionamento funciona

Cada versão aprovada vira uma **etiqueta (tag)** no Git. A etiqueta é um marco
permanente: nada é sobrescrito, as versões antigas continuam acessíveis para
sempre.

### Formato: `vMAJOR.MINOR.PATCH`

| Parte | Muda quando | Exemplo |
|---|---|---|
| **MAJOR** | Um bloco inteiro é entregue ou o escopo muda de verdade | Bloco A pronto, Bloco B pronto, site publicado |
| **MINOR** | Novas páginas, novas seções ou ajustes visuais aprovados pela equipe | Header refeito, 9 páginas novas |
| **PATCH** | Correções pequenas, textos, ajustes de acessibilidade | Cor do ícone, tamanho do logo, erro de digitação |

### Exemplos de leitura das etiquetas

- `v0.1.0` significa: primeira versão antes do lançamento, primeiro conjunto de
  entregas. O zero inicial indica que o projeto ainda não foi publicado.
- `v0.1.1` seria uma correção pequena sobre a mesma base.
- `v1.0.0` será a **primeira versão publicada em produção**, no go-live.

---

## Como voltar a uma versão anterior

Se em algum momento você precisar ver como o site estava em uma versão antiga:

```bash
# Ver a lista de todas as versões guardadas
git tag -l

# Abrir uma versão específica para conferir (não apaga nada do que existe)
git checkout v0.1.0

# Voltar para a versão mais recente do trabalho
git checkout main
```

A v0.1.0 foi integrada à `main` pelo pull request #1 (16/10/2026). A partir
dela, cada nova versão nasce em uma branch própria e é integrada por pull
request, para a equipe poder comparar antes de aceitar.

Para consultar apenas um arquivo de uma versão antiga, sem mudar nada:

```bash
git show v0.1.0:seu-projeto/index.html
```

**Nada é perdido ao voltar.** O Git guarda todo o histórico; a troca de versão
apenas mostra os arquivos como estavam naquele momento.

---

## Versões registradas

### v0.1.10 · 2026-10-16 · Tipografia na escala do template e cabeçalho de página limpo

**Pedido da cliente:** com a imagem de uma página de produto do template do zip em
mãos, reduzir as fontes do site para a escala do template e deixar o cabeçalho de
página sem fundo, apenas com um fio embaixo, contendo só a trilha de navegação e o
nome da página, "bem clean".

| O que mudou | Onde |
|---|---|
| Títulos na escala do template: Display 24px e Heading 18px, no lugar de clamps que chegavam a 52px | `assets/css/style.css` § tokens e base |
| Título de página, título de produto, hero e faixas com o tratamento Display do zip: Playfair 400, 24px, entrelinha 1.1 e entreletra 0.105em | `style.css`, `pages.css`, `comercio.css` |
| Cabeçalho de página sem fundo e sem enfeites: só a trilha, o nome da página e um fio embaixo | `assets/css/style.css` |
| Texto de apoio saiu de dentro do cabeçalho e abre o conteúdo, logo abaixo do fio (`.page-intro`) | 17 arquivos em `tools/content/` |
| Contagem de peças e recado de tamanhos saíram do cabeçalho da loja e passaram para a barra da coleção, ao lado da ordenação | `tools/content/02-loja.html`, `pages.css` §06, `comercio.css` §13 |
| Faixas verdes (perguntas da home e pré-rodapé), números da página Sobre, frase de posicionamento e hero reduzidos para 24px ou 18px, conforme a tabela do template | `comercio.css`, `pages.css` |
| Contador da sacola e linha de ajuda do hero voltaram de 10px para 11px, o mínimo da decisão de acessibilidade | `header.css`, `comercio.css` |

**Regra cumprida:** nenhuma fonte acima de 24px no site (as únicas exceções são
enfeites, como as aspas grandes do depoimento). A escala do zip (Caption 9px e
Tagline 8px) **não** foi copiada: a decisão E0 registrada no dossiê e a regra de
contraste (abaixo de 14px só Ink ou Ink Soft) mantêm Caption e Tagline em 11px.
Se a cliente quiser os 9px e os 8px do template, é uma decisão nova dela.

**Verificado em arquivo:** 22 páginas (`build.py` + `check.py`, "tudo certo") e
teste de navegador com 603 verificações, nenhuma falha, incluindo uma checagem
nova que reprova qualquer `font-size` acima de 24px nos quatro arquivos de CSS.

**Não entrou nesta versão:** o logotipo do header continua em 18px a 21px (o zip
usa 24px no nome da marca). O header foi aprovado pela cliente em 15/10 e o
aumento mexe no equilíbrio dele; fica como pergunta, não como mudança.

### v0.1.9 · 2026-10-16 · Minha conta, Contato e Sobre refeitos com as referências da cliente

**Pedido da cliente:** adaptar a página Minha conta às imagens 1 e 2, adaptar o
Contato às imagens 3, 4 e 5 (com bordas na coluna da direita, como os
depoimentos da home, e conferindo o fundo de cada seção), ajustar o Sobre com
texto à esquerda e imagem à direita e uma seção de missão, visão e compromisso, e
verificar a página de coleção conforme o template.

| O que mudou | Onde |
|---|---|
| Minha conta com dois cartões (Entrar e Criar conta), painel com tabela de pedidos e seção de medidas salvas | `tools/content/07-conta.html`, `pages.css` §01 e §02 |
| Contato com formulário em quadro de papel e canais de atendimento em quadros com borda, sobre fundo Hover Soft | `tools/content/14-contato.html`, `pages.css` §07 |
| Seção "O ateliê no mapa" com quadro de exemplo no lugar de um mapa com endereço inventado | `tools/content/14-contato.html`, `pages.css` §03 |
| Seção "Dúvidas rápidas" com quatro respostas copiadas da página de Perguntas frequentes | `tools/content/14-contato.html`, `pages.css` §04 |
| Sobre com o primeiro bloco em texto à esquerda e imagem à direita | `tools/content/13-sobre.html`, `pages.css` §05 |
| Seção "Missão, visão e compromisso" em três cartões, com selo [PROPOSTA] em cada texto | `tools/content/13-sobre.html`, `pages.css` §05 |
| Faixa de frase de posicionamento e faixa com três fotos do processo | `tools/content/13-sobre.html`, `pages.css` §05 |
| Cabeçalho da coleção com "Vestuário feminino do P ao GG" e atalho para o guia de medidas | `tools/content/02-loja.html`, `pages.css` §06 |
| Limpeza: CSS da galeria antiga, dos cartões de conta e da cabeça dos cartões de pedido, que saíram de uso | `assets/css/pages.css` |

**Regra cumprida:** telefone, e-mail, prazo de resposta, endereço e mapa seguem
como `[PREENCHER]`/`[A DEFINIR]`. O mapa não foi inventado: no lugar dele ficou um
quadro de exemplo com a instrução de onde o mapa real entra. Missão, visão e
compromisso estão marcados como `[PROPOSTA]`, para a equipe ajustar com as
próprias palavras antes de publicar.

**Verificado em arquivo:** 22 páginas (`build.py` + `check.py`, "tudo certo") e
teste de navegador com 527 verificações, nenhuma falha.

**Não entrou nesta versão:** carrinho, checkout, desejos, busca, produto e a
página do post seguem com o layout anterior.

### v0.1.8 · 2026-10-16 · Pagamento e segurança no rodapé, cabeçalho de página e internas renovadas

**Pedido da cliente:** acrescentar no rodapé as formas de pagamento e a área de
segurança (imagem enviada), melhorar o cabeçalho das páginas internas, que
estava "muito simples", e renovar o layout das páginas internas usando o
template do zip como referência.

| O que mudou | Onde |
|---|---|
| Formas de pagamento e segurança no rodapé, em quadros de texto e selos desenhados | `tools/partials/footer.html`, `assets/css/header.css` §11.1a |
| Cabeçalho de página novo: trilha dentro do bloco, fio em Terracota, linha de olho e faixa de fundo suave | `assets/css/style.css`, 17 páginas de `tools/content/` |
| Página Sobre com galeria de duas fotos, faixa de números e frase de posicionamento | `tools/content/13-sobre.html`, `assets/css/pages.css` |
| Índice de leitura na coluna da esquerda em FAQ, guia de medidas, trocas, envio, privacidade, termos e cookies | `tools/content/15` a `22`, `assets/css/pages.css` |
| Guia de medidas com passos numerados; Diário com destaque de texto próprio; lookbook em ziguezague com look numerado | `assets/css/pages.css` |
| Margens escritas no HTML das páginas renovadas passaram para o CSS | `assets/css/pages.css` §07 |

**Regra cumprida:** nenhuma marca de terceiros (Visa, Mastercard, Pix e afins)
foi reproduzida como imagem. As formas de pagamento aparecem em texto e os dois
selos são desenhos próprios, com o aviso de conferência com a empresa mantido.
No go-live, com o gateway contratado, os distintivos oficiais entram no lugar.

**Verificado em arquivo:** 22 páginas (`build.py` + `check.py`, "tudo certo") e
teste de navegador com 479 verificações, nenhuma falha.

**Não entrou nesta versão:** carrinho, checkout, conta, desejos, busca, contato,
produto e post seguem com o layout que já tinham; são telas de tarefa e ficam
para uma próxima rodada, se a cliente quiser o mesmo tratamento.

### v0.1.7 · 2026-10-16 · Cabeçalho da loja, ordenação e trilha de navegação

**O que mudou em relação à v0.1.6:**

- **Trilha de navegação visível (pedido da cliente).** O separador entre as
  migalhas era um ponto em Accent Soft, que sobre o papel fica em 1,5:1 e
  praticamente desaparecia: "Início Loja" parecia duas palavras soltas. Agora o
  separador é uma barra em Muted (4,3:1), com mais respiro entre os itens e a
  página atual em Ink. O rótulo da trilha passou a ser o padrão da língua
  ("Trilha de navegação", no lugar de "Você está aqui"). A trilha foi criada
  nas duas páginas que ainda não tinham: Pedido recebido e a página de erro.
- **Cabeçalho de página mais justo.** O título caiu de 54px para 46px no
  tamanho máximo (não briga mais com a grade), o respiro em cima e embaixo
  ficou mais curto e a contagem de peças ficou alinhada pela base do texto de
  apoio, sem flutuar no canto. Mudança aplicada às 21 páginas internas, não só
  à loja.
- **Linha de filtros e ordenação alinhada.** Na captura original, "Filtros /
  Limpar" (coluna da esquerda) e "Ordenar por" (coluna da direita) apareciam em
  alturas diferentes, com dois fios desencontrados. Agora as duas colunas abrem
  na mesma linha, com a mesma altura e o mesmo fio embaixo.
- **Seletor de ordenação com a cara do site.** Era o campo nativo do navegador,
  com a seta do sistema. Agora usa a classe de campo do projeto, com altura de
  46px, borda de linha, seta desenhada em SVG e foco visível. No celular o
  seletor ocupa a linha inteira.
- **Verificação em todas as páginas.** As 22 páginas foram conferidas para
  cabeçalho, trilha e espaçamentos; a varredura de estilos inline mostrou 69
  usos de margem direta no HTML, que ficam anotados como limpeza opcional.

**Verificado nesta versão:** 22 páginas sem erro de estrutura; 272 verificações
automatizadas passando, incluindo as novas (trilha em todas as páginas internas
e ausente só na home, cabeçalho da loja com título, texto de apoio e contagem,
seletor de ordenação com a classe de campo e as quatro opções).

**Ainda não verificado:** conferência visual em navegador e contraste medido por
ferramenta (axe ou WAVE).

---

### v0.1.6 · 2026-10-16 · Decisões da cliente confirmadas

**O que mudou em relação à v0.1.5:**

- **Frete grátis definido: acima de R$ 299.** O protótipo já usava 299 em todo
  lugar (barra do topo, página do produto, carrinho, checkout, pedido recebido,
  página de envio, descrição para busca e a conta do frete no JavaScript). O que
  mudou foi a pendência: o comentário no código e a lista de decisões abertas
  passaram a registrar o valor confirmado. Nenhum preço de produto mudou.
- **Catálogo definido: 12 peças visíveis.** A loja já mostrava as 12. Dois
  textos ainda diziam 10 peças e foram corrigidos: o atalho da página 404
  ("Loja completa, 12 peças") e o item da página Sobre ("Doze peças bem
  escolhidas valem mais que cem peças iguais").
- **Newsletter do rodapé mantida.** Confirmado pela cliente em 16/10/2026: a
  linha de newsletter fica no rodapé e a home continua com uma única faixa
  sálvia, a de perguntas frequentes, antes do rodapé.

**Verificado nesta versão:** 22 páginas sem erro de estrutura; 189 verificações
automatizadas passando; nenhuma referência a 10 peças restante nos textos do
site.

**Ainda não verificado:** conferência visual em navegador e contraste medido por
ferramenta (axe ou WAVE).

---

### v0.1.5 · 2026-10-16 · Faixa verde antes do rodapé em todas as páginas

**O que mudou em relação à v0.1.4:**

- **Faixa sálvia em todas as páginas (pedido da cliente).** Antes só a home
  fechava com uma faixa verde antes do rodapé; as outras páginas tinham uma
  caixa arredondada dentro do container. Agora as 22 páginas terminam com a
  mesma faixa de largura total: o fundo vai de ponta a ponta da tela e o texto
  fica na largura do header. Nas seis páginas que já tinham a caixa (lookbook,
  sobre, perguntas frequentes, guia de medidas, trocas e envio) o texto foi
  mantido; nas outras 15 a faixa entrou com um convite curto, ligado ao assunto
  da própria página.
- **Faixa compacta de lista de espera saiu.** A faixa curta criada na v0.1.4 no
  meio da home foi removida a pedido da cliente. A home fica com uma única
  faixa sálvia, a de perguntas frequentes, antes do rodapé. A newsletter do
  rodapé continua, como na referência enviada na v0.1.3.
- **Mesma largura do header em todas as páginas.** As páginas de leitura
  (legais, perguntas frequentes, guia de medidas, trocas, envio, contato e
  sobre) usavam um container de 1180px, mais estreito que o header de 1688px.
  Agora todas usam 1688px; o que continua limitado é a linha do texto corrido,
  em 72 caracteres, incluindo as caixas de aviso e os rascunhos legais.
- **Revisão de CSS (pedido da cliente).** Correções e limpeza:
  - a amostra de cor "carvão" aparecia sem cor: o CSS tinha `.sw-carvalho` e o
    HTML usa `.sw-carvao`;
  - os passos do pedido (página Pedido recebido) não tinham estilo nenhum e o
    número escrito aparecia ao lado do número da lista do navegador;
  - a caixa `.promo` saiu do CSS junto com as seis ocorrências no HTML,
    substituídas pela faixa de largura total;
  - o botão claro das faixas virou uma classe de verdade (`.btn--paper`), em vez
    de funcionar só dentro de um seletor específico;
  - saíram as regras que nenhuma página usava: contador antigo da loja, tabela
    antiga de carrinho, cartões de avaliação, esqueletos de carregamento,
    utilitários de margem, régua solta e uma variante antiga de seção.
- **Rodapé alinhado ao header**, com o verde encostando nele em todas as
  páginas, sem vão branco.

**Verificado nesta versão:** 22 páginas sem erro de estrutura; 189 verificações
automatizadas passando, incluindo as novas (uma única faixa na home, a faixa
fechando cada uma das 22 páginas e a newsletter presente no rodapé de todas
elas); a varredura de classes não encontrou nenhuma classe usada no HTML sem
estilo no CSS.

**Ainda não verificado:** conferência visual em navegador e contraste medido por
ferramenta (axe ou WAVE).

---

### v0.1.4 · 2026-10-16 · Perguntas frequentes na home e faixas verdes

**O que mudou em relação à v0.1.3:**

- **Perguntas frequentes na home (pedido da cliente).** Nova faixa sálvia antes
  do rodapé com cinco perguntas do atendimento, em acordeão: conta, tabela de
  medidas, troca, entrega e tratamento de dados. As respostas são as mesmas da
  página Perguntas frequentes, e há um link para ela no fim da faixa.
- **Lista de espera em faixa compacta.** O conteúdo da faixa antiga ("Cada
  coleção nasce uma vez", que a cliente achou que não estava no lugar certo)
  virou uma faixa curta no meio da home, entre os destaques e a vitrine por
  ocasião: título à esquerda e formulário em uma linha à direita. A faixa
  colorida da cor sálvia continua, agora com menos altura.
- **Rodapé resolvido.** A faixa de perguntas encosta no rodapé e passa a ser o
  separador verde entre o conteúdo e o fim da página. Antes havia um vão branco
  grande e dois pedidos de e-mail seguidos (lista de espera e newsletter do
  rodapé); agora a faixa perto do rodapé é conteúdo, não captura de e-mail.
- **Formulário que não quebrava bem.** Na faixa compacta, campo e botão ficam
  na mesma linha a partir de 721px; abaixo disso continuam empilhados.

**Verificado nesta versão:** 22 páginas sem erro de estrutura; 81 verificações
automatizadas passando (incluindo as novas: as duas faixas, as cinco perguntas,
o acordeão abrindo e fechando no clique e a ordem das seções); contraste
conferido nos pares novos (papel sobre sálvia 5,9:1; resposta do acordeão
5,45:1; Accent Soft sobre sálvia foi descartado, 3,86:1).

**Ainda não verificado:** conferência visual em navegador e contraste medido
por ferramenta (axe/WAVE).

---

### v0.1.3 · 2026-10-16 · Refinamento de rodapé, cabeçalhos e cartões

**O que mudou em relação à v0.1.2:**

- **Faixa de benefícios (imagem 1 da cliente).** O grupo estreito e agrupado
  no centro, feito na v0.1.1, deu lugar a quatro itens distribuídos por toda a
  largura do container do header, cada um com ícone acima de um texto
  centralizado. Retomada de direção pedida pela cliente com a imagem 1; o fio
  fino entre os itens continua.
- **Depoimentos (imagem 2).** Cada frase virou um cartão de papel com borda
  fina e aspas em serifa, sobre o fundo areia. Antes eram três blocos de texto
  soltos, sem moldura.
- **Diário (imagem 3).** Cada post virou um cartão fechado: foto em cima,
  texto embaixo, fundo de papel e borda. O fim da seção agora é evidente e
  nada parece invadir o bloco seguinte. A faixa sálvia também ganhou uma
  camada própria para pintar na frente de qualquer sobra de altura.
- **Rodapé (imagem 4).** Reorganizado na estrutura da referência: newsletter
  em uma linha (texto à esquerda, formulário à direita), quatro colunas,
  faixa de segurança e pagamento, e a base com copyright, identificação da
  empresa e links de política.
- **Faixa de segurança e pagamento (pedido novo).** Quatro informações curtas
  com ícone: formas de pagamento, ambiente protegido, pedido rastreado e os
  7 dias do CDC Art. 49. Com aviso de que selos e bandeiras só entram no ar
  quando gateway e certificado estiverem contratados.
- **Correção de base (achado na conferência).** 70 imagens tinham largura e
  altura no HTML diferentes do arquivo real, herdadas das ilustrações antigas
  em SVG. Era isso que fazia a faixa sálvia subir por cima dos cartões do
  diário na imagem 3. O gerador passou a ler a medida de cada arquivo e a
  reescrever o atributo; a caixa da foto do diário também ganhou altura
  calculada pela largura, que nenhuma foto consegue estourar. Bônus: melhora a
  estabilidade visual (CLS) exigida no go-live.
- **Cabeçalhos de página (imagem 5).** Todos os 17 cabeçalhos internos foram
  refeitos: mais espaço em branco, título maior em serifa, texto de apoio mais
  estreito e a contagem de peças à direita na loja. A trilha de navegação virou
  caixa alta miúda, como em COS, Massimo Dutti e Aritzia.
- **Newsletter de volta ao rodapé.** A referência enviada mostra a newsletter
  ali. Para não repetir o mesmo convite duas vezes na home, os dois ficaram com
  assuntos diferentes: a faixa verde sálvia é a lista de espera dos
  lançamentos; o rodapé é o conteúdo do ateliê.

**Verificado nesta versão:** 22 páginas sem erro de estrutura, 60 testes
automatizados passando (mini-sacola, desejos, busca, menu mobile, filtros da
loja, gaveta, rodapé novo, cabeçalho de página, cartões e 1 H1 por página),
contraste conferido nos pares novos (aspas do depoimento, ícones de benefício
e de segurança).

**Ainda não verificado:** conferência visual em navegador e contraste medido
por ferramenta (axe/WAVE).

---

### v0.1.2 · 2026-10-16 · Ajustes de layout pedidos pela cliente

**O que mudou em relação à v0.1.1:**

- **Largura única no site.** A grade de conteúdo passou de 1280px para 1688px,
  a mesma medida da barra do header, para logo, menu e produtos ficarem
  alinhados na mesma margem. Páginas de leitura (legais, FAQ, guias) continuam
  estreitas, em 1180px, porque linha de texto muito longa cansa a vista.
- **Cores das seções da home.** Ritmo novo, sem inventar cor: a paleta do
  dossiê passa a marcar o ritmo da página com três fundos.
  - *Hover Soft* (areia claríssimo) na faixa de benefícios, em "Em destaque" e
    nos depoimentos;
  - *Accent Soft* (terracota claro) no editorial "Um ateliê, três gestos";
  - *Sálvia* na faixa de lista de espera, como já era.
  Contraste conferido em AA antes de aplicar: Ink sobre Accent Soft dá 9,3:1 e
  Accent Dark sobre Accent Soft dá 5,0:1. Dois pares que reprovavam por pouco
  foram corrigidos (Accent sobre Hover Soft e Ink Soft sobre Accent Soft).
- **Loja com filtro à esquerda**, como no template de referência: coluna de
  240px com categorias, faixa de preço, cor e tamanho, mais a grade de 3
  colunas à direita e a barra de contagem e ordenação. No celular e no tablet a
  coluna vira uma gaveta aberta pelo botão Filtros.
- **Rodapé enxuto.** Saíram a newsletter e a faixa de selos de pagamento. Ficou
  o essencial: quatro colunas curtas, a identificação da empresa (exigida pelo
  Decreto 7.962/2013) e a base com os links de política, incluindo a
  desistência em 7 dias (CDC Art. 49).
- **Newsletter em um só lugar.** A captura de e-mail ficou apenas na faixa
  verde sálvia da home ("Cada coleção nasce uma vez"). Pedir o mesmo e-mail
  duas vezes na mesma página era o principal motivo da poluição do rodapé.

**Verificado nesta versão:** 22 páginas sem erro de estrutura, 1.118 links
internos e imagens conferidos, 53 testes automatizados passando (mini-sacola,
desejos, busca, menu mobile, filtros da loja, gaveta de filtros, rodapé, 1 H1
por página, alt em imagens, contraste dos pares de cor usados).

**Ainda não verificado:** conferência visual em navegador (é o próximo passo,
com a cliente).

---

### v0.1.1 · 2026-10-16 · Super layout com fotos e faixa de benefícios centralizada

**O que mudou em relação à v0.1.0:**

- **Faixa de benefícios centralizada** (pedido da cliente): os quatro itens
  (frete grátis, troca fácil, pagamento, do P ao GG) passam a ficar agrupados no
  centro da faixa, com fio de separação entre eles, em vez de esticados de ponta
  a ponta.
- **Fotos de exemplo de verdade**: as 47 imagens de exemplo em SVG (retângulos
  cinza escritos "SUBSTITUIR") saíram do projeto. Entraram 31 fotos em JPG
  extraídas do template de referência enviado pela cliente. Direitos e origem
  destas fotos: `[CONFERIR]` antes de qualquer uso em produção.
- **Home no padrão do template**: hero com selo numerado, categorias numeradas,
  vitrine por ocasião, editorial "Um ateliê, três gestos" com pilares numerados,
  coleção "Terra & Linho" em bloco duplo, depoimentos e faixa verde sálvia de
  lista de espera.
- **Card de produto completo**: selo (Novo, Mais vendida, Oferta), coração de
  lista de desejos, nota com avaliações, preço promocional riscado, tamanhos e
  link "Adicionar à sacola".
- **Mini-sacola lateral (drawer)** com barra de progresso do frete grátis,
  subtotal, aviso rápido (toast) e circulação de foco por teclado.
- **Rodapé em 4 colunas**, newsletter com nota de consentimento, selos de
  pagamento ilustrativos e identificação da empresa.
- **Catálogo de exemplo ampliado** de 10 para 12 peças, alinhado ao template.
  **Confirmado pela cliente em 16/10/2026: ficam 12 peças visíveis.**
- **Regra de frete grátis unificada em R$ 299** em todo o protótipo (o dossiê
  previa R$ 199 e o header aprovado diz R$ 299). **Confirmado pela cliente em
  16/10/2026: frete grátis acima de R$ 299.**

**Arquivos novos:** `assets/css/comercio.css`, `assets/js/loja.js`,
`tools/produtos.json`, `tools/partials/drawer.html`.

**Verificado nesta versão:** 22 páginas sem erro de estrutura (`check.py`),
1.250 links internos e imagens conferidos, mini-sacola, coração de desejos,
busca e menu mobile testados por script, 1 H1 por página, alt em todas as
imagens não decorativas.

**Ainda não verificado:** conferência visual em navegador (é o próximo passo,
com a cliente) e direitos das fotos.

---

### v0.1.0 · 2026-10-16 · Bloco A concluído (protótipo HTML)

**O que está nesta versão:**

- Protótipo com **22 páginas** HTML, estáticas, navegáveis sem servidor.
- Identidade visual aplicada: 4 cores de sistema, 9 customizadas, Jost e
  Playfair Display.
- Header no padrão de site de moda: logo à esquerda, navegação ao centro,
  lupa, coração, conta e sacola à direita. Busca expansível ao clicar na lupa.
- Todos os estados de interface exigidos pelo dossiê: carregando, busca sem
  resultado, produto esgotado, sacola vazia, pagamento recusado, pedido
  confirmado e 404.
- Acessibilidade WCAG 2.2 AA: skip link, foco visível, área de toque de 44px,
  menu com ESC e controle de foco, `prefers-reduced-motion`, 16px no celular.
- Gerador de páginas (`tools/build.py`) com header e footer em um só lugar.
- Verificador automático (`tools/check.py`) e teste funcional do header.
- 47 imagens de exemplo em SVG, todas marcadas para substituição.
- Documentos: README do protótipo, lista de imagens a produzir, guia de fontes
  locais e os 3 rascunhos legais marcados para revisão jurídica.

**Verificado nesta versão:** 22 páginas sem erro de estrutura, 1.100 links
internos funcionando, 1 H1 por página, alt em todas as imagens, 22 páginas
respondendo 200 no servidor local.

**Ainda não verificado:** conferência visual em navegador, feita pela equipe.

**O que trava o lançamento:** imagens reais, dados legais da empresa, gateway
de pagamento, solução de frete, dados reais dos produtos e revisão jurídica das
páginas legais.

---

## Próximas versões previstas

| Versão | Conteúdo esperado |
|---|---|
| v0.1.5 | Ajustes finos a partir da conferência visual da cliente |
| v0.2.0 | Bloco B: JSONs de templates para Elementor |
| v0.3.0 | Bloco C: kit ZIP, produtos.csv, posts.csv e guias de instalação |
| v1.0.0 | Go-live: site publicado com dados reais e revisão jurídica concluída |

Estas previsões são referência de planejamento e podem mudar. O que vale é o
que estiver registrado como versão entregue neste arquivo.
