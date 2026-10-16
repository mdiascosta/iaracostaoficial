# Diário de Bordo - Iara Costa E-commerce

## [2026-10-16] - Rodapé, cabeçalhos de página, benefícios, depoimentos e diário

### Pedido da cliente
Cinco capturas de tela com ajustes: (1) a faixa de benefícios deve seguir a
largura do header, com os ícones centralizados; (2) as caixas de depoimento
precisam ficar mais bonitas, com fundo branco ou borda em destaque; (3) o fim
da home, onde estão os cartões do diário, está "comendo tudo" e precisa
melhorar muito; (4) o rodapé deve seguir a imagem enviada, com uma seção de
segurança e pagamento; (5) os cabeçalhos internos precisam melhorar, usando
ecommerce de marcas conhecidas como referência.

### O que foi feito (IMPLEMENTADO)
- **Referências olhadas.** Busca por páginas de categoria de moda: o padrão que
  se repete é trilha de navegação discreta acima do título, título grande,
  texto de apoio curto e a contagem de peças antes da grade. COS, Massimo
  Dutti e Aritzia usam bastante espaço em branco e trilha em caixa alta miúda.
- **Faixa de benefícios.** Os quatro itens agora se espalham pela largura do
  container de 1688px, cada um com ícone acima do texto centralizado e fio fino
  entre eles. Antes eram quatro itens agrupados no centro.
- **Depoimentos.** Cada frase virou cartão de papel com borda fina, aspas
  grandes em serifa e o nome separado por um fio. Sobre o fundo areia da seção
  o cartão ganha relevo sem precisar de sombra.
- **Diário.** Cada post virou cartão fechado: foto em cima na proporção 4:3,
  texto embaixo, fundo de papel e borda. O bloco ganhou fim visível, e a faixa
  sálvia recebeu uma camada própria para pintar na frente de qualquer sobra de
  altura das seções de cima.
- **Causa do "comendo tudo" encontrada.** Ao conferir a imagem 3, apareceu o
  motivo real da sobreposição: 70 imagens do protótipo tinham largura e altura
  escritas no HTML diferentes do arquivo de verdade (as medidas eram das
  ilustrações antigas, em SVG). O navegador reserva o espaço pela medida
  escrita, então a foto chegava, empurrava o layout e a seção seguinte subia
  por cima do texto. O gerador agora lê a medida direto do arquivo e reescreve
  o atributo de cada imagem; sobrou zero divergência. Isso também melhora a
  nota de estabilidade visual (CLS) exigida no go-live.
- **Caixa da foto garantida.** No cartão do diário, a altura passa a ser
  calculada pela largura em vez de depender do arquivo da foto. Nenhuma foto,
  em nenhum navegador, consegue mais empurrar a faixa de baixo.
- **Rodapé.** Refeito na ordem da imagem: newsletter em uma linha, quatro
  colunas (marca, institucional, categorias, atendimento com redes sociais),
  faixa de segurança e pagamento, e a base com copyright, razão social, CNPJ,
  endereço e os links de política.
- **Newsletter no rodapé.** Voltou, como a imagem pede. Para não repetir o
  mesmo convite duas vezes na home, a faixa sálvia ficou como lista de espera
  dos lançamentos e o rodapé como assinatura de conteúdo do ateliê. Se a
  cliente preferir só um dos dois, é uma linha de mudança.
- **Segurança e pagamento.** Quatro informações com ícone: formas de pagamento
  (Pix, cartão e boleto), dados protegidos, pedido rastreado e os 7 dias do
  CDC Art. 49. Sem bandeira de cartão e sem selo, com aviso escrito de que eles
  só entram no ar quando o gateway e o certificado estiverem contratados.
- **Cabeçalhos internos.** Aplicado em 17 páginas: mais respiro em cima e
  embaixo, título maior em serifa, texto de apoio estreito e trilha em caixa
  alta miúda. Na loja, a contagem de peças subiu para o canto direito do
  cabeçalho.

### O que foi verificado
- Geração das 22 páginas sem erro de estrutura.
- Medidas das imagens: 0 divergências entre o que o HTML declara e o arquivo
  real.
- Rodapé na mesma largura do header em todas as páginas, inclusive nas de
  leitura.
- Testes automatizados: 60 verificações passando, entre elas as rotinas de
  mini-sacola, desejos, busca, menu mobile, filtros da loja, gaveta, rodapé
  novo, cabeçalho de página, cartões e um H1 por página.
- Contraste dos pares novos conferido por cálculo: aspas do depoimento em
  terracota sobre o papel, ícones de benefício e de segurança, textos de apoio.

### O que ainda não foi verificado
- Conferência visual em navegador e medição de contraste por ferramenta
  (axe ou WAVE). O servidor local está no ar para isso.

### Próximo passo sugerido
Conferir as cinco telas no navegador e dizer o que ainda incomoda. Depois disso,
seguimos para o Bloco B (Elementor) ou para os ajustes que aparecerem.

---

## [2026-10-16] - Ajustes de layout: largura, cores, filtro da loja e rodapé

### Pedido da cliente
Quatro ajustes depois de olhar a v0.1.1: (1) as seções da home precisam seguir o
container do header; (2) as cores das seções precisam de mais sofisticação, com
fundos diferentes, mas dentro da paleta da marca; (3) a loja precisa do filtro à
esquerda, como no template de referência; (4) o rodapé ficou poluído e a
newsletter deveria sair ou ficar mais sofisticada.

### O que foi feito (IMPLEMENTADO)
- **Largura única.** A grade de conteúdo saiu de 1280px e passou a usar a mesma
  medida da barra do header, 1688px. Páginas de leitura (legais, FAQ, guias de
  medidas e envio, contato, sobre) ficaram em 1180px: linha de 1688px é longa
  demais para ler.
- **Cores das seções.** Três fundos, todos tirados do dossiê, sem cor nova:
  Hover Soft na faixa de benefícios, em "Em destaque" e nos depoimentos;
  Accent Soft no editorial "Um ateliê, três gestos"; Sálvia na faixa de lista de
  espera. O contraste de cada combinação foi calculado antes de aplicar: Ink
  sobre Accent Soft 9,3:1, Accent Dark sobre Accent Soft 5,0:1. Dois pares que
  reprovavam por pouco foram trocados (Accent sobre Hover Soft e Ink Soft sobre
  Accent Soft).
- **Loja com filtro à esquerda.** Coluna de 240px com categorias (com contagem),
  faixa de preço, cor (amostras redondas) e tamanho, seguindo o template. A
  grade de 3 colunas ficou à direita, com contagem e ordenação acima. No celular
  e no tablet a coluna vira uma gaveta aberta pelo botão "Filtros". O filtro
  funciona na hora, sem recarregar a página.
- **Rodapé enxuto.** Saíram a newsletter e a faixa de selos de pagamento.
  Ficaram quatro colunas curtas, a identificação da empresa (Decreto
  7.962/2013) e a base com privacidade, termos, desistência em 7 dias (CDC
  Art. 49) e cookies.
- **Newsletter em um só lugar.** A captura de e-mail ficou apenas na faixa verde
  sálvia da home. Era ela que duplicava o pedido de e-mail na mesma página.
- Frase de frete grátis no rodapé acompanha a regra em uso (R$ 299), que segue
  pendente de confirmação com a empresa.

### Verificado (arquivos)
- `tools/check.py`: 22 páginas, "tudo certo".
- 53 testes automatizados passando, incluindo os novos: filtro por categoria,
  por tamanho, por faixa de preço e por cor, estado de "nenhuma peça", limpar
  filtros, ordenação por preço, gaveta de filtros no celular e as mudanças do
  rodapé. 1.118 links internos conferidos.
- 22 páginas respondendo HTTP 200 no servidor local.

### Ainda não verificado
- Conferência visual em navegador, feita pela cliente (é o próximo passo).
- Contraste calculado no papel; a conferência com ferramenta de acessibilidade
  (axe, WAVE) continua pendente e é exigência do dossiê para o go-live.
- Direitos das 31 fotos do template.

---

## [2026-10-16] - Super layout: fotos reais, blocos do template e v0.1.1

### Pedido da cliente
Depois de aprovar o header ("O header ficou perfeito"), a cliente pediu duas
coisas: centralizar os itens da faixa de benefícios (frete grátis, compra
consciente, envio) e aproveitar as ideias mais limpas do template de referência
que ela enviou (`template_.zip`), transformando o protótipo em um "super layout".
Ela pediu para conferir o resultado visualmente antes de qualquer outra coisa.

### O que foi feito (IMPLEMENTADO)
- **Faixa de benefícios centralizada** na home: os 4 itens ficam agrupados no
  centro, com largura máxima de 1080px e fio de separação entre eles.
- **Fotos**: as 47 imagens de exemplo em SVG foram removidas do projeto. Entraram
  31 fotos JPG do template de referência, com alt descritivo em português.
  Origem e direitos das fotos: `[CONFERIR]` antes de publicar.
- **Home reconstruída** no padrão do template: hero com selo "01", benefícios,
  categorias numeradas, em destaque (4 cards), compre por ocasião, editorial
  "Um ateliê, três gestos", coleção Terra & Linho, depoimentos, diário e faixa
  verde sálvia de lista de espera.
- **Card de produto novo**: selo (Novo, Mais vendida, Oferta), coração de
  desejos, nota com avaliações, preço promocional riscado, tamanhos e link de
  adicionar à sacola. O card agora é gerado por um molde único em
  `tools/partials` a partir de `tools/produtos.json`.
- **Mini-sacola lateral** com barra de progresso do frete grátis, subtotal,
  dois botões e aviso rápido (toast). Fecha com ESC, clique fora e circula o
  foco pelo teclado.
- **Rodapé novo**: 4 colunas, newsletter com nota de consentimento LGPD, selos
  ilustrativos, identificação da empresa e links de política.
- **Catálogo de exemplo**: 10 para 12 peças (padrão do template), em uma única
  fonte de dados. Loja, home, produto, sacola e busca usam a mesma lista.
- **Preço e frete coerentes em todo o protótipo**: sacola 974,00 menos
  BEMVINDO10 (97,40) = 876,60, com frete grátis.

### Decisões que precisam da cliente (2)
1. **Frete grátis: R$ 199 ou R$ 299?** O dossiê previa R$ 199; o header aprovado
   diz R$ 299. Unificamos em R$ 299 no protótipo inteiro. `[CONFIRMAR COM A EMPRESA]`
2. **Catálogo: 10 ou 12 peças?** O dossiê falava de 10 produtos; o template
   trouxe 12. Se a loja real tem 10, basta remover duas linhas de
   `tools/produtos.json`. `[A DEFINIR]`

### Verificado (arquivos)
- `tools/check.py`: 22 páginas, "tudo certo", nenhuma referência quebrada.
- Teste com jsdom: 1.250 links internos, mini-sacola (abre, lista, soma, fecha
  com ESC), coração de desejos (marca e desmarca), busca e menu mobile. Tudo OK.
- 22 páginas respondendo HTTP 200 no servidor local.
- Nenhuma imagem restante do tipo placeholder, exceto o favicon provisório.

### Ainda não verificado
- Conferência visual em navegador, feita pela cliente (é o próximo passo).
- Direitos das fotos do template.
- Tamanho das fotos: os JPG vieram do template e podem precisar de otimização
  (alvo de até 300 KB por arquivo) antes de produção.

---

## [2026-10-16] - Versionamento: v0.1.0 gravada e enviada ao GitHub

### O que foi feito (IMPLEMENTADO)
- Todo o trabalho até aqui estava apenas no workspace, sem histórico. Agora está
  versionado em 7 commits temáticos e enviado ao GitHub.
- Criado esquema de versionamento para preservar as versões anteriores:
  - `VERSION` (0.1.0) e `HISTORICO-DE-VERSOES.md` com a convenção
    `vMAJOR.MINOR.PATCH` e o passo a passo de como voltar a uma versão antiga.
  - Etiqueta (tag) anotada `v0.1.0` = primeiro entregável do projeto.
  - `.gitignore` para manter fora do repositório o que não é entregável.
- Branch `arena/557fb81d-iaracostaoficial` e a etiqueta `v0.1.0` enviadas para
  `origin` (github.com/mdiascosta/iaracostaoficial).

### Commits criados (na ordem)
1. `docs:` diário de bordo, histórico de versões e gitignore
2. `feat:` gerador do protótipo com header e footer compartilhados
3. `feat:` sistema visual do Bloco A (CSS, JS e tokens)
4. `chore:` imagens de exemplo (47 SVGs) e guia de fontes locais
5. `feat:` as 22 páginas do protótipo HTML
6. `chore:` conteúdo-fonte das 22 páginas em tools/content
7. `docs:` README do protótipo e lista das imagens a produzir

### Verificado
- `git status`: árvore limpa, nada pendente.
- `tools/check.py` rodado depois do commit: 22 páginas, tudo certo.
- Remoto confirmado: branch e etiqueta presentes no GitHub.
- 111 arquivos versionados. Tamanho do `.git`: 937 KB.

### Decisão tomada
- D24: versionamento com etiqueta anotada a cada entrega aprovada, em vez de
  pastas numeradas. Motivo: o Git guarda o histórico completo e permite abrir
  qualquer versão anterior sem duplicar arquivos. Impacto: a cada mudança
  aprovada sobe uma etiqueta nova (`v0.1.1` para ajustes, `v0.2.0` para o
  Bloco B, `v1.0.0` no go-live), e o `HISTORICO-DE-VERSOES.md` registra o que
  mudou.

### Próximo passo
- Conferência visual da equipe no protótipo. Depois: ajustes (v0.1.1) ou
  Bloco B (v0.2.0), conforme a escolha.

---

## [2026-10-15] - E1 - Bloco A, Parte 3/3 (institucional, guias, legais) - BLOCO A CONCLUÍDO

### O que foi feito (IMPLEMENTADO)
Dez páginas novas, fechando as 22 do protótipo:

| Página | O que tem |
|---|---|
| sobre.html | História (com espaço reservado para a equipe escrever), valores, critérios de escolha das peças, compromissos |
| contato.html | Formulário completo com assunto e número do pedido, canais, prazo de resposta, aviso sobre golpe de senha, estado "mensagem enviada" |
| faq.html | 18 perguntas em 5 grupos, com acordeão, atalhos de âncora e link para contato |
| guia-medidas.html | Método das 3 etapas, tabela de pontos de medição, 2 tabelas de tamanho, 4 dúvidas comuns, specs para a equipe |
| lookbook.html | 4 looks com peças clicáveis + guia de produção das fotos |
| trocas.html | CDC Art. 49, troca por tamanho, defeito, processo em 4 passos, reembolso, o que não troca, tabela de prazos |
| envio.html | Prazos e valores, frete grátis, rastreio, regras de entrega, 4 situações de problema, checklist para a equipe |
| privacidade.html | 10 seções: controlador, inventário de dados, operadores, transferência internacional, retenção, direitos do titular, segurança, cookies |
| termos.html | 14 seções: aceitação, identificação, uso, cadastro, produtos e preços, pagamento, entrega, trocas, cupons, propriedade intelectual, responsabilidades, conflitos, legislação |
| cookies.html | Categorias com tabela de exemplos, terceiros, como controlar, prévia visual do banner |

Mais três documentos de apoio:
- `seu-projeto/README.md`: como abrir, o que existe, o que o protótipo NÃO faz,
  decisões de acessibilidade, dados de exemplo, como editar, pendências.
- `seu-projeto/SPECS-DE-IMAGEM.md`: lista completa de 48 a 56 imagens a produzir,
  com tamanhos, convenções de nome, direitos e ordem de prioridade.
- `assets/fonts/LEIA-ME.md`: como hospedar Jost e Playfair localmente (LGPD),
  com o código `@font-face` pronto, tabela de solução de problemas e a via do
  Elementor.

### Verificado por mim (com teste automatizado, não só leitura)
- `tools/check.py`: **22 páginas, tudo certo.** Sem tag desbalanceada, 1 H1 por
  página, alt em todas as imagens, zero referência quebrada, zero travessão.
- Teste de links e header (`jsdom`): **1.100 links internos verificados entre as
  22 páginas, todos resolvem.** Todas as páginas alcançam home e loja.
- Header interativo: lupa abre, ESC fecha, foco volta para a lupa, menu mobile
  abre e fecha.
- Servidor local: as 22 páginas respondem 200.

### O que NÃO foi verificado
- Não abri navegador: a conferência visual (espaçamento, proporção entre header
  de 1688px e conteúdo de 1280px, telas estreitas) continua sendo da equipe.
- As três páginas legais são rascunho. Nenhuma foi revisada por advogado, e não
  substituem revisão jurídica.

### Decisões tomadas nesta parte
- D19: as páginas legais começam com uma faixa vermelha de aviso "RASCUNHO PARA
  REVISÃO JURÍDICA. NÃO PUBLICAR COMO ESTÁ". Motivo: evitar que um rascunho suba
  por descuido. Impacto: a faixa precisa ser removida só depois da revisão.
- D20: cada página legal termina com um checklist do que a equipe precisa
  decidir ou preencher. Motivo: transformar o rascunho em tarefa acionável.
- D21: a tabela de operadores (gateway, transportadora, e-mail, hospedagem)
  ficou com a coluna "Contratado?" vazia. Motivo: a lista só fecha depois das
  contratações, e inventar nomes violaria a regra de não inventar dados.
- D22: sobre.html tem o bloco "Como começou" com marcação explícita para a
  equipe escrever. Motivo: história de marca não se inventa, e texto genérico de
  agência não convence ninguém.
- D23: o banner de cookies aparece como referência visual na página de cookies,
  com a estrutura de botões sugerida (Aceitar todos, Somente necessários,
  Preferências). Motivo: a equipe precisa validar a proporção antes de instalar
  o plugin, e há uma armadilha registrada: o texto da política precisa ser
  compatível com o que o banner realmente oferece.

### Inventário do catálogo (atualizado)
- Total: 10 | Com variação: 8/10 (a definir quais no real) | Com imagens reais: 0/10
- Swatches: demonstrados em 3 produtos (modelo replicável) | Descrição aprovada: 0/10
- Preço: 10/10 com valores de EXEMPLO | Estoque: 10/10 de exemplo
- Dados fiscais: 0/10 (NCM e origem dependem do contador)

### Inventário do blog
- Posts de exemplo no protótipo: 6 no índice + 1 completo | Meta: 8 posts reais
- Categorias sugeridas: Tamanhos e caimento · Tecidos e cuidados · Estilo
- Títulos sugeridos (aguardam aprovação): os 6 do protótipo mais "Como montar um
  guarda-roupa com poucas peças" e "O que é alfaiataria e quando usar"

### Pendências / Bloqueios (consolidado)
Bloqueiam produção:
- [ ] Imagens reais (48 a 56 arquivos, ver SPECS-DE-IMAGEM.md) - equipe
- [ ] Razão social, CNPJ, endereço, e-mail e WhatsApp - equipe
- [ ] Gateway de pagamento e solução de frete - equipe
- [ ] Regime tributário e emissor de nota fiscal - contador
- [ ] Revisão jurídica de privacidade, termos, cookies e trocas - jurídico
- [ ] Regras de parcelamento, desconto no Pix, cupom e frete grátis - empresa
- [ ] Dados reais dos 10 produtos (substituir os de exemplo) - equipe

Não bloqueiam, mas precisam de decisão:
- [ ] Plugin de lista de desejos: aprovado ou o coração sai do header
- [ ] Manter a barra do topo em 1688px ou voltar para 1280px
- [ ] Ícone de loja física no header (existe ponto físico?)
- [ ] Textos de marca: história em sobre.html e boas-vindas da barra de anúncio
- [ ] Categorias reais do catálogo (as 5 atuais são suposição do protótipo)

### Artefatos gerados nesta parte
- seu-projeto/sobre.html, contato.html, faq.html, guia-medidas.html,
  lookbook.html, trocas.html, envio.html, privacidade.html, termos.html,
  cookies.html
- seu-projeto/README.md, seu-projeto/SPECS-DE-IMAGEM.md
- seu-projeto/assets/fonts/LEIA-ME.md
- seu-projeto/assets/css/pages.css (bloco novo da Parte 3)
- tools/content/13-sobre.html até 22-cookies.html

### Estado do Bloco A (Etapa E1): CONCLUÍDO
22 páginas · 3 CSS · 3 JS · 47 imagens de exemplo · 3 documentos · 948 KB no total.
Todos os estados de interface do dossiê representados. Verificação automática e
teste funcional sem falhas. Pronto para a conferência visual da equipe.

### Próximo passo
- E2: Bloco B (JSONs para Elementor) OU ajustes no protótipo a partir da
  conferência visual. Aguardando "pode seguir" ou a lista de ajustes.

---

## [2026-10-15] - E1 - Bloco A, Parte 2/3 (sacola, checkout, conta, blog, 404)

### O que foi feito (IMPLEMENTADO)
Nove páginas novas, todas usando o mesmo header, footer e sistema de cores:

| Página | O que tem |
|---|---|
| carrinho.html | 2 itens, quantidade, cupom, cálculo de frete por CEP, resumo, estado de sacola vazia |
| checkout.html | 4 etapas, dados do cliente, endereço completo, envio, pagamento, aceites e resumo lateral |
| pedido-recebido.html | número do pedido, situação, próximos passos em 3 etapas, ajuda |
| conta.html | menu lateral, visão geral, 3 pedidos (aguardando, enviado, cancelado), dados e endereços |
| desejos.html | 3 itens salvos, item esgotado, estado de lista vazia |
| busca.html | resultado com termo destacado e estado "sem resultado" com sugestões |
| blog.html | destaque + 6 posts, filtros por tema, paginação |
| post.html | artigo completo, autor, data, tempo de leitura, compartilhar, produtos do texto |
| 404.html | busca na própria página, 3 caminhos de saída e 6 atalhos |

- Todas as páginas de estado pedidas pelo dossiê (7.8) estão representadas:
  carregando, busca sem resultado, produto indisponível, sacola vazia, erro de
  pagamento, pedido confirmado e 404.
- Novos estilos em `pages.css`, num bloco identificado, para não misturar com o
  que já estava pronto.

### Verificado por mim
- `tools/check.py`: 12 páginas, "tudo certo". Sem tag desbalanceada, 1 H1 por
  página, alt em todas as imagens, zero referência quebrada.
- Teste de DOM do header repetido após as mudanças: 16 verificações, 0 falhas.
- Servidor local: as 12 páginas respondem 200.
- Conferência de aritmética do carrinho: 389,00 + 178,00 = 567,00;
  desconto de 10% = 56,70; total 510,30. Confere.

### O que NÃO foi verificado
- Nenhum cálculo é automático no protótipo: os valores estão escritos no HTML.
  No Bloco B quem calcula é o WooCommerce.
- Não abri navegador: layout do checkout em tela estreita precisa de conferência
  humana (é o formulário mais longo do protótipo).

### Decisões tomadas nesta parte
- D16: os filtros por tema no blog ficaram como LINKS (recarregam a página), e
  não como botões que filtram na hora. Motivo: no WordPress o arquivo do blog
  filtra por categoria de verdade. Impacto: visualmente idêntico, comportamento
  correto.
- D17: a nota de "cupom BEMVINDO10 aplicado" no carrinho cita a limitação da
  seção 8.1, para a equipe não esquecer que "primeira compra" não funciona
  nativamente no WooCommerce.
- D18: o protótipo mostra "Transferência bancária" com aviso [CONFERIR] de que
  essa forma deve ser ativada só para teste e desativada antes de publicar.

### Pendências / Bloqueios (atualizado)
- [ ] Plugin de lista de desejos aprovado? Sem ele, o coração sai do header e
      desejos.html não vai ao ar - equipe - [BLOQUEADOR DE PRODUÇÃO? Não, é
      escopo opcional]
- [ ] Parcelamento e desconto no Pix ([A DEFINIR]) continuam aparecendo como
      marcador, nunca como valor inventado.
- [ ] Regras finas do cupom (acumula com promoção? vale em item em promoção?
      valor mínimo? validade?) ainda abertas.

### Artefatos gerados
- seu-projeto/carrinho.html, checkout.html, pedido-recebido.html, conta.html,
  desejos.html, busca.html, blog.html, post.html, 404.html
- tools/content/04-carrinho.html até 12-404.html
- seu-projeto/assets/css/pages.css (bloco novo da Parte 2)

### Próximo passo
- Parte 3/3: sobre, contato, FAQ, guia de medidas, lookbook, trocas, envio,
  privacidade, termos, cookies, README, LEIA-ME das fontes e a lista de imagens
  a produzir.

---

## [2026-10-15] - E1 - Ajuste fino do header (2ª revisão da equipe)

### O que foi feito (IMPLEMENTADO)
- Tamanhos reduzidos, a pedido da equipe ("ficou ruim o tamanho"):
  - Logo: 18 a 21px (era 20 a 26px). Dossiê pedia 24px: desvio aprovado.
  - Barra de anúncio: 11px (era 12px), padding de 7px.
  - Header: padding vertical de 13px no desktop e 12px no celular.
  - Tagline: 11px com tracking 0.18em (era 0.22em) para não competir com o logo.
- Ícone da lupa e demais ícones do header refeitos mais limpos: sem caixa, sem
  borda e sem fundo (`appearance: none`, `border: 0`, `box-shadow: none`).
  O hover agora muda só a cor, para terracota escuro.
- Contador da sacola: 16px, mais discreto e melhor encaixado no ícone.
- Caixa de busca agora tem cara de caixa: fundo branco, borda fina de 1px,
  altura de 48px e lupa dentro do campo. A borda fica terracota quando o campo
  recebe o foco.
- Traços dos ícones do header reduzidos para 1.4, o que dá o aspecto mais leve
  que a equipe pediu.

### A BUSCA NÃO ABRIA: causa encontrada e resolvida
- Causa provável: o navegador estava servindo o `header.js` ANTIGO, do cache,
  de antes da faixa de busca existir. O arquivo no servidor sempre esteve certo.
- Resolvido de forma definitiva: o gerador agora coloca um selo de versão
  (hash do conteúdo) no fim de cada arquivo de CSS e JS, por exemplo
  `header.js?v=01af3b8f`. Quando o arquivo muda, o endereço muda, e o navegador
  é obrigado a baixar a versão nova. Isso elimina a necessidade de limpar cache.
- Blindagem extra no `header.js`: a checagem de largura de tela (`matchMedia`)
  deixou de ser obrigatória. Se o navegador não tiver esse recurso, o arquivo
  não quebra mais.

### Verificado por mim (agora com teste de verdade, não só leitura)
- Montei um teste automatizado do header com DOM simulado (`jsdom`, instalado
  fora do repositório). Resultado: 16 verificações, 0 falhas.
  Cobre: lupa encontrada, painel inicia fechado, clique abre, ESC fecha e
  devolve o foco para a lupa, clique fora fecha, botão Fechar funciona, clique
  dentro da caixa não fecha, painel dentro do `<header>`, menu mobile abre e
  fecha com ESC.
- `tools/check.py` passou a separar "erro" de "página prevista para as próximas
  partes". Agora o resultado é "tudo certo", com 14 páginas pendentes listadas.

### O que NÃO foi verificado
- Não abri navegador: o aspecto final (proporção do logo, altura da barra) ainda
  precisa dos olhos da equipe. Se o logo ainda parecer grande, dá para baixar
  para 18px fixo em uma linha.

### Decisões tomadas nesta revisão
- D14: aceitar desvio do dossiê no tamanho do logo (18 a 21px em vez de 24px),
  por pedido da equipe, registrado como ajuste de equilíbrio visual.
- D15: selo de versão nos arquivos de CSS/JS. Motivo: cache do navegador fazia
  o site parecer quebrado. Impacto: nenhum no site final (o Bloco B não usa
  estes arquivos); é prática normal em produção.

### Artefatos gerados
- tools/build.py (selo de versão por hash)
- tools/check.py (pendências separadas de erros)
- seu-projeto/assets/css/header.css, assets/js/header.js (blindagem),
  tools/partials/header.html (ícones mais leves, caixa de busca)

### Próximo passo
- Aguardar a conferência visual da equipe. Em seguida, Parte 2/3.

---

## [2026-10-15] - E1 - Ajuste do header (revisão da equipe, Parte 1/3)

### O que foi feito (IMPLEMENTADO)
- Header reestruturado no padrão pedido pela equipe (referência: site de moda
  com logo à esquerda, navegação ao centro e ícones à direita):
  - Logo Playfair "IARA COSTA" alinhado à esquerda no desktop.
  - Navegação ao centro (Início, Loja, Lookbook, Guia de medidas, Diário, Sobre).
  - Ações à direita, só com ícone: lupa, coração (desejos), conta e sacola.
  - Sacola com contador em círculo terracota.
- Barra do topo mais larga que o conteúdo: `.header-shell` até 1688px,
  centralizada, com `align-items: center`, conforme a referência da equipe.
  A grade de conteúdo continua em 1280px (token próprio, fácil de reverter).
- Busca deixou de ocupar espaço fixo na barra: agora é SÓ a lupa. Ao clicar,
  abre uma faixa clara abaixo do header (lupa à esquerda, campo grande,
  "Fechar" e "Buscar" à direita), sobrepondo o conteúdo sem empurrar a página.
- Desejos e conta saem da barra no celular e passam para o painel do menu,
  o que libera espaço para logo e sacola.
- Acessibilidade da busca: `aria-expanded` na lupa, `aria-controls` apontando
  para a faixa, foco automático no campo ao abrir, ESC fecha, clique fora
  fecha, e o foco volta para a lupa. Campo com 16px no celular.

### Verificado por mim (apenas nos arquivos)
- `python3 tools/check.py`: nenhum erro de estrutura (sem tag desbalanceada,
  1 H1 por página, alt em todas as imagens, zero script inline, zero travessão).
- As 40 ocorrências restantes do verificador são apenas os links para as
  páginas das Partes 2 e 3, que ainda não existem: esperado.
- Servidor local responde 200 em index, loja e produto.

### O que NÃO foi verificado
- Não abri navegador: a proporção entre a barra de 1688px e o conteúdo de
  1280px precisa da conferência da equipe em tela larga (acima de 1700px) e
  em telas de 1280 a 1440px, onde a diferença é quase nula.
- Comportamento do ESC e do foco na faixa de busca: precisa de teste humano
  com teclado e leitor de tela.

### Decisões tomadas nesta revisão
- D11: barra do topo em 1688px e conteúdo em 1280px. Motivo: pedido da equipe
  e padrão de sites de moda. Impacto: em telas muito largas as laterais do
  header ficam mais vazias que o conteúdo; reversível mudando um token.
- D12: ícones de desejos e conta saem da barra no celular. Motivo: evitar
  barra apertada; no celular o padrão é deixar só lupa e sacola.
- D13: desejos no header depende do plugin de wishlist estar aprovado (item 13
  da lista de plugins). O ícone fica como [A DEFINIR]: se o plugin não for
  aprovado, o coração deve sair do header e do menu.

### Pendências abertas por este ajuste
- [ ] Definir se haverá ícone de "loja física" no header. Na referência existe
      (Morena Rosa tem lojas). A Iara Costa é só online? [A DEFINIR]
- [ ] A faixa superior da referência mostra marcas parceiras (IÓDICE, MARIA
      VALENTINA, ZINCO). Só faz sentido se a Iara Costa passar a vender outras
      marcas. Caso contrário, mantemos só a barra de anúncio em verde sálvia.
- [ ] Aprovar (ou reverter) a barra de 1688px.

### Artefatos gerados
- tools/partials/header.html (reescrito)
- seu-projeto/assets/css/header.css (reescrito, agora com .header-shell,
  .icon-btn e .search-panel)
- seu-projeto/assets/js/header.js (ganhou o bloco da faixa de busca)
- seu-projeto/assets/css/style.css (novo token --iara-header-max)

### Próximo passo
- Parte 2/3: sacola, checkout, pedido recebido, minha conta, lista de desejos,
  busca (com "sem resultado"), blog, post e 404.

---

## [2026-10-15] - E1 - Bloco A, Parte 1/3 (base + Home, Loja, Produto)

### O que foi feito (IMPLEMENTADO)
- Estrutura do protótipo criada em `seu-projeto/`, gerada a partir de `tools/`.
  O header e o footer existem em UM só lugar (`tools/partials/`): corrigir uma vez
  atualiza todas as páginas. Comando: `python3 tools/build.py`.
- 3 páginas no ar: `index.html`, `loja.html`, `produto.html`.
- CSS: `assets/css/style.css` (tokens, tipografia, botões, formulários, cards,
  estados), `header.css` (announcement, header, menu mobile, footer, trust bar)
  e `pages.css` (blocos de página).
- JS: `header.js` (menu mobile com ESC, trap de focus e focus-visible),
  `swatches.js` (galeria, cor/tamanho, quantidade, abas, acordeão) e
  `filtros.js` (filtro por categoria e ordenação da loja).
- 47 imagens de exemplo em SVG (`tools/make_placeholders.py`), todas com a
  etiqueta "SUBSTITUIR POR FOTO REAL" e o tamanho recomendado.
- 10 produtos de exemplo com nome, categoria, preço, variações e estoque.
- Verificador automático `tools/check.py`: tags balanceadas, 1 H1 por página,
  alt em todas as imagens, referências de arquivo existentes, zero script inline,
  zero travessão.

### Verificado por mim (apenas nos arquivos)
- Tags HTML balanceadas nas 3 páginas: sim.
- Um único H1 por página: sim.
- Todas as imagens com alt: sim.
- Nenhum script inline e nenhuma referência quebrada de CSS/JS/imagem: sim.
- Referências para páginas das Partes 2 e 3 aparecem como pendentes no
  `check.py`: esperado, elas ainda não foram geradas.
- Servidor local de conferência no ar (porta 8080).

### O que NÃO foi verificado
- Não abri navegador: o visual (cores, espaçamento, quebras) precisa da
  conferência da equipe nos 3 modos (desktop, tablet, celular).
- Google Fonts: no protótipo as fontes vêm do Google. Sem internet, o navegador
  cai nas fontes de reserva (Avenir/Segoe UI/Georgia).

### Decisões tomadas nesta parte
- D6: header e footer gerados por script a partir de parciais. Motivo: 22 páginas
  compartilham o mesmo cabeçalho. Impacto: rodar `python3 tools/build.py` depois
  de mexer nos parciais.
- D7: padding horizontal do header segue o gutter do container (até 84px no
  desktop) em vez dos 40px fixos do dossiê 7.2. Motivo: alinhar o logo com a
  grade de conteúdo. Impacto: desvio visual pequeno, reversível com uma linha de
  CSS. Pendente de aprovação da equipe.
- D8: tagline (11px) e copyright (11px) usam Ink Soft, e não Muted. Motivo: a
  regra 10.2 proíbe Muted em texto menor que 14px. Impacto: 3 pontos do dossiê
  (tagline, numerais, copyright) seguem Ink Soft.
- D9: faixa fixa "PROTÓTIPO · DADOS DE EXEMPLO · NÃO PUBLICAR" no topo de todas
  as páginas, para nenhum dado fictício passar por real.
- D10: amostras de cor dos produtos viraram classes (`.sw-terracota` etc.), sem
  estilo solto no HTML.

### Suposições adotadas
- Suposição: 5 categorias (Vestidos, Blusas e camisas, Calças, Saias,
  Acessórios) distribuem bem os 10 produtos de exemplo. | Por quê: teste de
  filtro e grade. | Bloqueador de produção? Não, categorias reais são [A DEFINIR].
- Suposição: os textos institucionais e de produto são exemplo, escritos por mim.
  | Por quê: a marca ainda não enviou conteúdo. | Bloqueador de produção? Sim.

### Artefatos gerados
- seu-projeto/index.html, loja.html, produto.html
- seu-projeto/assets/css/style.css, header.css, pages.css
- seu-projeto/assets/js/header.js, swatches.js, filtros.js
- seu-projeto/assets/img/ (47 SVGs de exemplo + favicon)
- tools/build.py, tools/check.py, tools/make_placeholders.py, tools/pages.json
- tools/partials/header.html, tools/partials/footer.html
- tools/content/01-home.html, 02-loja.html, 03-produto.html

### Próximo passo
- Parte 2/3: sacola, checkout, pedido recebido, minha conta, lista de desejos,
  busca (com "sem resultado"), blog, post e 404.

---

## [2026-10-15] - E0 - Coleta inicial de informações

### Informações coletadas da equipe
- WordPress: [A DEFINIR] | PHP: [A DEFINIR] | Tema: [A DEFINIR]
- Hospedagem/servidor: [A DEFINIR - já existe host/domínio COM staging] | Domínio: [A DEFINIR] | Staging: SIM (confirmado na E0)
- Plugins ativos: [A DEFINIR]
- Elementor Pro / Pro Elements: SIM - licença oficial (confirmado na E0). Plano B não aplicável.
- Editor Atômico V4: [A DEFINIR]
- WooCommerce: [A DEFINIR]

### O que foi feito
- Repositório inicializado (apenas README.md). Nenhum entregável gerado ainda.
- DIARIO-DE-BORDO.md aberto conforme seção 13 do super prompt.
- Fase E0 concluída: 8 perguntas prioritárias enviadas à equipe (seção 14) e respondidas. Decisões D1 a D5 registradas.
- Documento de escopo v2.6.0 (super prompt) recebido e adotado como regra vigente.

### Decisões tomadas
- D1: Elementor Pro com licença oficial -> Bloco B segue com Theme Builder/Pro widgets (sem Plano B). Motivo: resposta E0 q4. Impacto: header/footer/single product/etc. usam widgets Pro.
- D2: Ambiente de staging disponível -> construir e testar em staging com noindex; produção só após go-live. Motivo: resposta E0 q3. Impacto: fluxo de migração staging->produção necessário.
- D3: Tamanhos 8-9px do dossiê AUMENTADOS para 11-12px (decisão de acessibilidade, ponto 1 da seção 2.7). Motivo: resposta E0 q8 ("aumentar"). Impacto: tagline, anúncio e numerais mobile passam para mínimo 11-12px; registrar como desvio aprovado do dossiê.
- D4: Políticas/termos serão RASCUNHOS gerados pela IA para revisão jurídica. Motivo: resposta E0 q7. Impacto: marcar "RASCUNHO - revisão jurídica" no topo de cada página legal.
- D5: Produtos serão preenchidos com dados FICTÍCIOS para validar o layout (autorização explícita da equipe na E0 q1). Motivo: não há planilha real ainda. Impacto: TODOS os dados de produto (nome, preço, estoque, variações) são placeholders fictícios a substituir antes da publicação; marcar claramente no CSV e no Diário. NÃO publicar como reais.

### Suposições adotadas
- Suposição: a equipe responderá às 8 perguntas em bloco ou parcialmente. | Por quê: prompt permite resposta em bloco. | Bloqueador de produção? Não (define escopo).
- Suposição: data de criação do kit 2026-10-15 (conforme prompt). | Por quê: data informada. | Bloqueador de produção? Não.
- Suposição: imagens reais NÃO estão prontas (E0 q2 = "não"). | Por quê: resposta E0. | Bloqueador de produção? Sim (imagens reais são obrigatórias antes do go-live; protótipo pode usar placeholders).
- Suposição: dados da empresa NÃO estão prontos (E0 q6 = "não"). | Por quê: resposta E0. | Bloqueador de produção? Sim (razão social, CNPJ, endereço no footer são obrigatórios pelo Decreto 7.962/2013).
- Suposição: gateway de pagamento e frete AINDA NÃO definidos (E0 q5 = "indefinido"). | Por quê: resposta E0. | Bloqueador de produção? Sim (instalar desativado e conectar depois).
- Suposição: categorias do blog e títulos dos 8 posts AINDA NÃO decididos (pendente). | Por quê: resposta E0 q8 cobriu apenas o tamanho de fonte. | Bloqueador de produção? Não (posso sugerir para aprovação).

### Inventário do catálogo
- Total: 10 | Com variação: [A DEFINIR]/10 | Com imagens reais: [A DEFINIR]/10
- Swatches aplicados: [A DEFINIR]/10 | Descrição aprovada: [A DEFINIR]/10
- Preço: [A DEFINIR]/10 | Estoque: [A DEFINIR]/10 | Dados fiscais: [A DEFINIR]/10

### Inventário do blog
- Posts publicados: 0/8 | Categorias: [A DEFINIR]
- Datas distribuídas: [A DEFINIR]

### Plugins recomendados/instalados nesta fase
- Nenhum ainda.

### Código personalizado (se houver)
- Nenhum ainda.

### Testes de acessibilidade/desempenho informados pela equipe
- Nenhum ainda.

### Pendências / Bloqueios
- [ ] Imagens reais (produtos, logo, favicon, banners) - equipe - sem prazo - [BLOQUEADOR DE PRODUÇÃO? Sim]
- [ ] Dados legais da empresa (razão social, CNPJ, endereço, e-mail, WhatsApp, regime tributário) - equipe - sem prazo - [BLOQUEADOR DE PRODUÇÃO? Sim]
- [ ] Definição de gateway de pagamento e solução de frete - equipe - sem prazo - [BLOQUEADOR DE PRODUÇÃO? Sim]
- [ ] Dados reais dos 10 produtos (substituir os fictícios) - equipe - sem prazo - [BLOQUEADOR DE PRODUÇÃO? Sim]
- [ ] Versões de WP/PHP/tema/plugins no staging - equipe - sem prazo - [BLOQUEADOR DE PRODUÇÃO? Não, mas bloqueia ajustes finos de JSON/kit]

### Perguntas abertas (pós-E0)
1. RESPOVIDA (q1): não há planilha pronta; a equipe autorizou preencher o layout com dados FICTÍCIOS de produto para validar visual. Dados reais entram depois.
2. RESPOVIDA (q2): imagens reais ainda não estão prontas. Bloco A usará placeholders claramente marcados; troca antes do go-live.
3. RESPOVIDA (q3): hospedagem e domínio já existem, COM staging. Versões exatas (PHP, cache, Redis) ainda por informar.
4. RESPOVIDA (q4): Elementor Pro com licença oficial. Plano B não será aplicado.
5. RESPOVIDA (q5): gateway e frete ainda indefinidos. Serão entregues candidatos + instalação desativada.
6. RESPOVIDA (q6): dados da empresa ainda não disponíveis. Usar [PREENCHER] no footer e nos rascunhos legais.
7. RESPOVIDA (q7): a equipe aceita rascunhos para revisão jurídica.
8. RESPOVIDA (q8, parte 1): tamanhos 8-9px serão AUMENTADOS para 11-12px.
   ABERTA (q8, parte 2): categorias do blog e títulos dos 8 posts. Sugestão da IA será enviada para aprovação na F6.
9. ABERTA: parcelamento ("em até Nx sem juros") e desconto no Pix. Permanece [A DEFINIR]; nada será exibido no site antes de confirmar.
10. ABERTA: regras finas do cupom BEMVINDO10 (acumula com promoções? vale em itens em promoção? valor mínimo? validade?) e do frete grátis (subtotal antes ou depois do cupom?).

### Erros encontrados e como foram resolvidos
- Nenhum até o momento.

### Próximo passo
- E1: plano curto apresentado à equipe. Aguardando "pode seguir" para iniciar o Bloco A (protótipo HTML).

### Artefatos gerados
- DIARIO-DE-BORDO.md
