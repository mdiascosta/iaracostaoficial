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
  Decisão pendente com a cliente: `[A DEFINIR]` manter 12 ou voltar a 10.
- **Regra de frete grátis unificada em R$ 299** em todo o protótipo (o dossiê
  previa R$ 199 e o header aprovado diz R$ 299). Confirmar qual vale:
  `[CONFIRMAR COM A EMPRESA]`.

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
| v0.1.4 | Ajustes finos a partir da conferência visual da cliente |
| v0.2.0 | Bloco B: JSONs de templates para Elementor |
| v0.3.0 | Bloco C: kit ZIP, produtos.csv, posts.csv e guias de instalação |
| v1.0.0 | Go-live: site publicado com dados reais e revisão jurídica concluída |

Estas previsões são referência de planejamento e podem mudar. O que vale é o
que estiver registrado como versão entregue neste arquivo.
