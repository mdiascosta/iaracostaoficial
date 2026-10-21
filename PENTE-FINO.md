# Pente-fino: templates JSON x protótipo aprovado

## Conclusões (leia esta parte)

### 1. O CSS do template HTML está sendo injetado no Elementor?

**Não o CSS do protótipo como ele é, e nem poderia.** O protótipo tem
897 regras em 4 arquivos (style, header, comercio, pages). O Elementor
recebe **52 regras reescritas** no `iara-cabecalho.css` (embutido nos
24 JSON e no kit), mais as cores/fontes globais e os estilos declarados
widget a widget. As classes do protótipo (`.btn`, `.product-card`,
`.hero`...) **não existem na marcação que o Elementor gera**, então
colar o CSS cru do HTML não acertaria elemento nenhum: o equivalente
precisa ser construído por widget, e foi assim que o desenho foi
transportado.

### 2. O que foi corrigido depois deste pente-fino (v0.3.24)

- **Responsivo**: entraram 42 declarações `_mobile` geradas (colunas
  largas viram largura cheia no celular, títulos grandes encolhem) e
  3 blocos `@media` no CSS embutido (faixa de segurança 2 colunas no
  tablet e 1 no celular, logotipos menores, toques ajustados). Antes:
  zero dos dois lados. O desenho fino de loja/produto no celular
  continua sendo o do WooCommerce/Elementor e pede conferência visual.
- **Textos completos**: guia de medidas, trocas, envio e as três
  legais agora carregam o **texto integral do protótipo** (extraído
  do HTML aprovado durante a geração, com os links já convertidos
  para os endereços do site), e o FAQ virou as **20 perguntas reais
  em sanfonas por grupo** (antes eram 5 resumos de uma linha). As
  legais seguem com o aviso de rascunho para o jurídico.
  Os textos "fora" caíram de 956 para 536; o que resta é dinâmico
  (produtos, pedidos, posts) e as páginas escritas à mão no gerador
  (inicial, sobre, contato, coleção), cujo texto integral segue em
  `bloco-c/pages-conteudo.md`.

### 3. O que é dinâmico (não é falta)

Loja, produto, sacola, checkout, conta, desejos, busca, diário e
artigo mostram textos e imagens que nascem do WooCommerce e dos posts:
por isso aparecem como "faltando" e com 0 imagens no JSON.

---


Comparação automática dos 24 JSON do Elementor com as páginas HTML do protótipo (`seu-projeto/` e `tools/partials/`), mais a auditoria do CSS. Gerado por `tools/pente_fino.py`.

## 01-cabecalho.json  x  tools/partials/header.html

- Widgets: icon (2), icon-list (1), nav-menu (1), theme-site-logo (1), woocommerce-menu-cart (1), wp-widget-widget_top_wishlist (1)

- Textos do protótipo não encontrados no JSON: **3**
  - “lista de desejos wish count”
  - “pular para o conteudo”
  - “trocas e devolucoes”
- Textos do JSON que não estão no protótipo: 0 (dinâmicos, rótulos de acessibilidade e textos de sistema costumam aparecer aqui)
- Imagens: protótipo 0 | JSON 0

## 02-rodape.json  x  tools/partials/footer.html

- Widgets: button (1), form (1), heading (12), icon (6), icon-list (6), text-editor (15), theme-site-logo (1)

- Textos do protótipo não encontrados no JSON: **1**
  - “iara costa moda feminina ltda cnpj 12 345 678 0001 90 rua das flores no 140 sala 02 centro cerquilho sp cep 18”
- Textos do JSON que não estão no protótipo: 5 (dinâmicos, rótulos de acessibilidade e textos de sistema costumam aparecer aqui)
- Imagens: protótipo 0 | JSON 0

## 03-home.json  x  seu-projeto/index.html

- Widgets: accordion (1), button (6), heading (18), icon-box (4), icon-list (6), image (3), image-box (8), posts (1), testimonial (3), text-editor (8), woocommerce-products (1)

- Textos do protótipo não encontrados no JSON: **16**
  - “adicionar a sacola”
  - “agua fria pouca centrifugacao e secagem na sombra resolvem quase tudo”
  - “calca pantalona salvia”
  - “como escolher o caimento certo sem provar”
  - “como lavar linho sem perder o caimento”
  - “do trabalho ao jantar mudando so o sapato e o acessorio”
  - “faltam r 299 00 para o frete gratis”
  - “frete calculado pelo cep no carrinho impostos incluidos no preco”
  - “iara costa moda feminina e acessorios”
  - “lista de desejos 0”
  - “na duvida entre dois tamanhos fale com o atendimento a gente diz qual costuma ficar melhor naquela peca especi”
  - “peca unica artesanal”
  - “pular para o conteudo”
  - “tamanhos e caimento”
  - … e mais 2
- Textos do JSON que não estão no protótipo: 15 (dinâmicos, rótulos de acessibilidade e textos de sistema costumam aparecer aqui)
- Imagens: protótipo 18 | JSON 11

## 04-loja.json  x  seu-projeto/loja.html

- Widgets: button (2), heading (7), text-editor (7), woocommerce-archive-products (1), woocommerce-breadcrumbs (1), woocommerce-product-categories (1)

- Textos do protótipo não encontrados no JSON: **28**
  - “12 pecas nesta selecao”
  - “adicionar a sacola”
  - “blazer de linho areia”
  - “blusa de linho terracota”
  - “bolsa artesanal em palha”
  - “brinco de argila torneado”
  - “calca pantalona salvia”
  - “camisa branca de linho”
  - “cropped de tricot areia”
  - “envio para todo o brasil”
  - “faltam r 299 00 para o frete gratis”
  - “frete calculado pelo cep no carrinho impostos incluidos no preco”
  - “frete gratis acima de r 299”
  - “lista de desejos 0”
  - … e mais 14
- Textos do JSON que não estão no protótipo: 6 (dinâmicos, rótulos de acessibilidade e textos de sistema costumam aparecer aqui)
- Imagens: protótipo 12 | JSON 0

## 05-produto.json  x  seu-projeto/produto.html

- Widgets: button (2), heading (2), icon-list (1), text-editor (4), woocommerce-add-to-cart (1), woocommerce-breadcrumbs (1), woocommerce-product-data-tabs (1), woocommerce-product-images (1), woocommerce-product-meta (1), woocommerce-product-price (1), woocommerce-product-rating (1), woocommerce-product-related (1), woocommerce-product-short-description (1), woocommerce-product-stock (1), woocommerce-product-title (1), woocommerce-product-upsell (1)

- Textos do protótipo não encontrados no JSON: **44**
  - “a producao da proxima remessa ainda nao tem data fechada deixe seu e mail para receber o aviso de reposicao”
  - “adicionar a sacola”
  - “ainda nao ha avaliacoes deste produto as avaliacoes passam por moderacao antes de aparecer aqui e nenhuma e cr”
  - “autorizo a publicacao do meu comentario e li a”
  - “blocos cinza no lugar da foto do nome e do preco enquanto a pagina carrega nada de tela branca nem de conteudo”
  - “bolsa artesanal em palha”
  - “brinco de argila torneado”
  - “camisa branca de linho”
  - “cor selecionada salvia”
  - “cuidados lavar a mao ou em ciclo delicado com sabao neutro sem alvejante a base de cloro secar a sombra e na h”
  - “deixe a sua avaliacao”
  - “envio para todo o brasil”
  - “esta peca esta esgotada”
  - “faltam r 299 00 para o frete gratis”
  - … e mais 30
- Textos do JSON que não estão no protótipo: 4 (dinâmicos, rótulos de acessibilidade e textos de sistema costumam aparecer aqui)
- Imagens: protótipo 8 | JSON 0

## 06-carrinho.json  x  seu-projeto/carrinho.html

- Widgets: heading (1), text-editor (2), woocommerce-cart (1), woocommerce-notices (1)

- Textos do protótipo não encontrados no JSON: **32**
  - “10 de desconto na primeira compra para clientes novos cadastrados nao e cumulativo com outras ofertas ativas c”
  - “adicionar a sacola”
  - “bolsa artesanal em palha”
  - “calca pantalona salvia”
  - “camisa branca de linho”
  - “confira as pecas aplique o cupom e veja o frete antes de finalizar”
  - “continuar comprando”
  - “cor salvia tamanho m”
  - “cupom bemvindo10 aplicado”
  - “desconto bemvindo10”
  - “envio para todo o brasil”
  - “falar com o atelie”
  - “fale com o atelie para qualquer duvida antes de finalizar”
  - “faltam r 299 00 para o frete gratis”
  - … e mais 18
- Textos do JSON que não estão no protótipo: 2 (dinâmicos, rótulos de acessibilidade e textos de sistema costumam aparecer aqui)
- Imagens: protótipo 6 | JSON 0

## 07-checkout.json  x  seu-projeto/checkout.html

- Widgets: heading (1), text-editor (2), woocommerce-checkout (1), woocommerce-notices (1)

- Textos do protótipo não encontrados no JSON: **48**
  - “1x de r 876 60 sem juros”
  - “antes de finalizar”
  - “aprovacao na hora qr code depois de confirmar o pedido”
  - “calculado pelo cep”
  - “confira o e mail falta o final depois do arroba”
  - “demonstracao visual no site publicado estes campos sao gerados pelo mercado pago e o numero do cartao nunca pa”
  - “em ate 6x sem juros parcela minima de r 50 00”
  - “endereco de entrega”
  - “entendi a politica de”
  - “enviamos a confirmacao e o codigo de rastreio para este e mail”
  - “envio para todo o brasil”
  - “falar com o atelie”
  - “falar com o atendimento”
  - “fale com o atelie para qualquer duvida antes de finalizar”
  - … e mais 34
- Textos do JSON que não estão no protótipo: 2 (dinâmicos, rótulos de acessibilidade e textos de sistema costumam aparecer aqui)
- Imagens: protótipo 2 | JSON 0

## 08-pedido-recebido.json  x  seu-projeto/pedido-recebido.html

- Widgets: button (2), heading (1), text-editor (2), woocommerce-notices (1), woocommerce-purchase-summary (1)

- Textos do protótipo não encontrados no JSON: **31**
  - “a nota fiscal acompanha o pedido duvidas sobre dados fiscais”
  - “aguardando pagamento”
  - “assim que o pagamento for aprovado voce recebe um e mail com o comprovante e o pedido entra em separacao”
  - “contato iaracosta com br”
  - “duvidas depois da compra”
  - “em ate 2 dias uteis a peca e conferida embalada e a nota fiscal e emitida pecas sob encomenda ou sob medida le”
  - “enviamos a confirmacao para o seu e mail se ela nao aparecer em alguns minutos confira a caixa de spam e o e m”
  - “envio para todo o brasil”
  - “falar com o atendimento”
  - “faltam r 299 00 para o frete gratis”
  - “forma de pagamento”
  - “frete calculado pelo cep no carrinho impostos incluidos no preco”
  - “frete gratis acima de r 299”
  - “frete gratis pac prazo dos correios pelo cep”
  - … e mais 17
- Textos do JSON que não estão no protótipo: 3 (dinâmicos, rótulos de acessibilidade e textos de sistema costumam aparecer aqui)
- Imagens: protótipo 0 | JSON 0

## 09-conta.json  x  seu-projeto/conta.html

- Widgets: heading (1), text-editor (2), woocommerce-my-account (1), woocommerce-notices (1)

- Textos do protótipo não encontrados no JSON: **39**
  - “a troca de senha e feita por link enviado ao e mail cadastrado nao pedimos senha por whatsapp e mail ou telefo”
  - “acompanhe pedidos enderecos e dados de acesso em um so lugar”
  - “adicionar endereco”
  - “aguardando pagamento”
  - “alteracao so pelo atendimento para evitar fraude”
  - “alterar o e mail pede confirmacao por link por seguranca”
  - “aqui voce acompanha entregas repete um pedido favorito e resolve trocas sem precisar falar com ninguem”
  - “as medidas que voce salvar ficam aqui e ajudam a sugerir tamanho nas proximas compras sem voce medir tudo de n”
  - “bairro cidade estado cep”
  - “cadastro em um minuto 10 na primeira compra com”
  - “conferir cadastro de teste desligado antes de publicar”
  - “continuar comprando”
  - “endereco de exemplo o cadastro real guarda apenas o necessario para entrega e nota fiscal”
  - “endereco principal”
  - … e mais 25
- Textos do JSON que não estão no protótipo: 2 (dinâmicos, rótulos de acessibilidade e textos de sistema costumam aparecer aqui)
- Imagens: protótipo 0 | JSON 0

## 10-desejos.json  x  seu-projeto/desejos.html

- Widgets: button (1), heading (1), text-editor (2)

- Textos do protótipo não encontrados no JSON: **22**
  - “adicionar a sacola”
  - “as pecas que voce salvou elas continuam aqui quando voce volta desde que esteja com a conta aberta”
  - “calca pantalona salvia”
  - “envio para todo o brasil”
  - “esgotado o botao de compra fica desabilitado e o aviso aparece em texto”
  - “esta pagina depende de um plugin de lista de desejos aprovado item 13 da lista de plugins sem essa aprovacao o”
  - “faltam r 299 00 para o frete gratis”
  - “frete calculado pelo cep no carrinho impostos incluidos no preco”
  - “frete gratis acima de r 299”
  - “lista de desejos 0”
  - “lista de desejos iara costa”
  - “prototipo dados e textos de exemplo nao publicar”
  - “pular para o conteudo”
  - “referencia de estado lista vazia”
  - … e mais 8
- Textos do JSON que não estão no protótipo: 2 (dinâmicos, rótulos de acessibilidade e textos de sistema costumam aparecer aqui)
- Imagens: protótipo 3 | JSON 0

## 11-blog.json  x  seu-projeto/blog.html

- Widgets: archive-posts (1), heading (2), text-editor (2)

- Textos do protótipo não encontrados no JSON: **28**
  - “agua fria pouca centrifugacao e secagem na sombra resolvem quase tudo”
  - “as pecas citadas nos textos estao todas na loja”
  - “cabides certos dobras e o que nunca deve ir para o sol direto”
  - “combinacoes que funcionam para trabalho almoco e imprevisto”
  - “como escolher o caimento certo sem provar”
  - “como guardar as pecas para durarem mais”
  - “como lavar linho sem perder o caimento”
  - “como medir o corpo em casa sem erro”
  - “conteudo para comprar melhor e cuidar das pecas caimento tecidos medidas e combinacoes sem promessa de milagre”
  - “do trabalho ao jantar mudando so o sapato e o acessorio”
  - “envio para todo o brasil”
  - “faltam r 299 00 para o frete gratis”
  - “fita metrica paralela ao chao sem apertar e a ajuda de alguem para as costas”
  - “frete calculado pelo cep no carrinho impostos incluidos no preco”
  - … e mais 14
- Textos do JSON que não estão no protótipo: 2 (dinâmicos, rótulos de acessibilidade e textos de sistema costumam aparecer aqui)
- Imagens: protótipo 7 | JSON 0

## 12-post.json  x  seu-projeto/post.html

- Widgets: heading (1), posts (1), theme-post-content (1), theme-post-featured-image (1), theme-post-info (1), theme-post-title (1)

- Textos do protótipo não encontrados no JSON: **44**
  - “a etiqueta diz o tamanho a fita metrica diz se a peca veste”
  - “abrir o guia de medidas”
  - “adicionar a sacola”
  - “as pecas citadas nos textos estao todas na loja”
  - “as tres medicoes que importam”
  - “blusa de linho terracota”
  - “calca pantalona salvia”
  - “camisa branca de linho”
  - “como escolher o caimento certo sem provar”
  - “como escolher o caimento certo sem provar iara costa”
  - “como lavar linho sem perder o caimento”
  - “como medir o corpo em casa sem erro”
  - “deite uma peca sua na cama e meca esses tres pontos compare com a tabela do produto se a diferenca entre dois ”
  - “envio para todo o brasil”
  - … e mais 30
- Textos do JSON que não estão no protótipo: 0 (dinâmicos, rótulos de acessibilidade e textos de sistema costumam aparecer aqui)
- Imagens: protótipo 9 | JSON 0

## 13-busca.json  x  seu-projeto/busca.html

- Widgets: archive-posts (1), button (1), heading (1), search-form (1), text-editor (2)

- Textos do protótipo não encontrados no JSON: **23**
  - “a loja tem a colecao completa com filtro por cor tamanho e faixa de preco”
  - “busque pelo tecido linho alfaiataria algodao”
  - “como buscar melhor”
  - “confira a grafia ou tente um termo mais simples como calca ou couro voce tambem pode falar com o atendimento s”
  - “envio para todo o brasil”
  - “estado busca com resultados”
  - “estado busca sem resultado”
  - “falar com o atendimento”
  - “faltam r 299 00 para o frete gratis”
  - “frete calculado pelo cep no carrinho impostos incluidos no preco”
  - “frete gratis acima de r 299”
  - “lista de desejos 0”
  - “mostrando 2 de 3 pecas encontradas”
  - “nao encontramos nada para calca de couro”
  - … e mais 9
- Textos do JSON que não estão no protótipo: 2 (dinâmicos, rótulos de acessibilidade e textos de sistema costumam aparecer aqui)
- Imagens: protótipo 2 | JSON 0

## 14-404.json  x  seu-projeto/404.html

- Widgets: button (3), heading (2), text-editor (1)

- Textos do protótipo não encontrados no JSON: **18**
  - “a colecao esta na loja e os textos do atelie no diario”
  - “combinacoes prontas”
  - “envio para todo o brasil”
  - “falar com o atendimento”
  - “faltam r 299 00 para o frete gratis”
  - “frete calculado pelo cep no carrinho impostos incluidos no preco”
  - “frete gratis acima de r 299”
  - “lista de desejos 0”
  - “no wordpress esta pagina e o template 404 do tema com busca e atalhos se voce chegou aqui por um link do propr”
  - “o endereco pode ter mudado a peca pode ter saido do catalogo ou o link veio com um errinho nada de beco sem sa”
  - “pagina nao encontrada”
  - “pagina nao encontrada iara costa”
  - “perguntas frequentes”
  - “prototipo dados e textos de exemplo nao publicar”
  - … e mais 4
- Textos do JSON que não estão no protótipo: 3 (dinâmicos, rótulos de acessibilidade e textos de sistema costumam aparecer aqui)
- Imagens: protótipo 0 | JSON 0

## 15-sobre.json  x  seu-projeto/sobre.html

- Widgets: heading (5), text-editor (6)

- Textos do protótipo não encontrados no JSON: **32**
  - “ajustar com as palavras da marca”
  - “cada peca entra no catalogo depois de conferir tecido costura caimento e comportamento depois de lavar se a pe”
  - “dias para desistir da compra”
  - “doze pecas bem escolhidas valem mais que cem pecas iguais”
  - “e feitos no brasil no atelie de cerquilho sp”
  - “enquanto a historia nao esta escrita o que da para dizer com seguranca e o que esta nesta pagina como as pecas”
  - “envio para todo o brasil”
  - “este bloco e seu texto generico de marca nao convence ninguem e o dossie proibe inventar a historia da empresa”
  - “falar com o atendimento”
  - “faltam r 299 00 para o frete gratis”
  - “frete calculado pelo cep no carrinho impostos incluidos no preco”
  - “frete gratis a partir deste valor”
  - “frete gratis acima de r 299”
  - “imagem de exemplo substituir por foto propria da marca ou da equipe”
  - … e mais 18
- Textos do JSON que não estão no protótipo: 6 (dinâmicos, rótulos de acessibilidade e textos de sistema costumam aparecer aqui)
- Imagens: protótipo 4 | JSON 0

## 16-contato.json  x  seu-projeto/contato.html

- Widgets: button (1), form (1), heading (3), icon-list (1), text-editor (3)

- Textos do protótipo não encontrados no JSON: **53**
  - “a peca nao serviu posso trocar”
  - “a resposta chega no e mail informado em ate 24 horas uteis de segunda a sexta se o assunto for urgente use o w”
  - “acompanhar meu pedido”
  - “ajuda a resolver mais rapido”
  - “as duvidas mais comuns estao respondidas nas perguntas frequentes”
  - “autorizo o uso dos meus dados para responder esta mensagem conforme a”
  - “cerquilho sp cep 18520 000”
  - “cnpj 12 345 678 0001 90 ie 123 456 789 110”
  - “como uso o cupom de primeira compra”
  - “conferir visitas somente com agendamento previo se a empresa receber no local”
  - “contato iara costa”
  - “dados pessoais e privacidade”
  - “digite bemvindo10 no campo de cupom na sacola e clique em aplicar o desconto aparece no resumo antes de voce f”
  - “dpo iaracosta com br”
  - … e mais 39
- Textos do JSON que não estão no protótipo: 6 (dinâmicos, rótulos de acessibilidade e textos de sistema costumam aparecer aqui)
- Imagens: protótipo 0 | JSON 0

## 17-faq.json  x  seu-projeto/faq.html

- Widgets: accordion (6), button (1), heading (8), text-editor (2)

- Textos do protótipo não encontrados no JSON: **5**
  - “frete calculado pelo cep no carrinho impostos incluidos no preco”
  - “lista de desejos 0”
  - “manda a pergunta para o atendimento se ela aparecer muito entra aqui nesta pagina”
  - “prototipo dados e textos de exemplo nao publicar”
  - “pular para o conteudo”
- Textos do JSON que não estão no protótipo: 20 (dinâmicos, rótulos de acessibilidade e textos de sistema costumam aparecer aqui)
- Imagens: protótipo 0 | JSON 0

## 18-guia-medidas.json  x  seu-projeto/guia-medidas.html

- Widgets: heading (10), text-editor (11)

- Textos do protótipo não encontrados no JSON: **4**
  - “comprar sem provar da certo quando voce compara medidas e nao tamanhos o caminho mais confiavel e medir uma pe”
  - “envio para todo o brasil”
  - “lista de desejos 0”
  - “pular para o conteudo”
- Textos do JSON que não estão no protótipo: 12 (dinâmicos, rótulos de acessibilidade e textos de sistema costumam aparecer aqui)
- Imagens: protótipo 0 | JSON 0

## 19-lookbook.json  x  seu-projeto/lookbook.html

- Widgets: button (4), heading (9), image (3), text-editor (5)

- Textos do protótipo não encontrados no JSON: **34**
  - “a colecao so vai ao ar com as fotos reais das pecas como produzir essas fotos esta no fim desta pagina”
  - “alfaiataria leve e vestidos midi em verde salvia do escritorio ao jantar sem trocar de roupa”
  - “ate 300 kb depois de converter para webp sem perder qualidade visivel”
  - “blusa de linho terracota”
  - “calca pantalona salvia”
  - “camisa branca de linho”
  - “cenario dos capitulos”
  - “colecao capitulo 01 terracota webp e peca blusa linho terracota webp seguindo o padrao minusculas hifen sem ac”
  - “colecao terra linho iara costa”
  - “como produzir as fotos desta colecao”
  - “confirmar com a empresa”
  - “direitos de imagem”
  - “envio para todo o brasil”
  - “faltam r 299 00 para o frete gratis”
  - … e mais 20
- Textos do JSON que não estão no protótipo: 6 (dinâmicos, rótulos de acessibilidade e textos de sistema costumam aparecer aqui)
- Imagens: protótipo 9 | JSON 3

## 20-trocas.json  x  seu-projeto/trocas.html

- Widgets: heading (14), text-editor (15)

- Textos do protótipo não encontrados no JSON: **7**
  - “envio para todo o brasil”
  - “este texto foi escrito para organizar as informacoes e precisa de revisao do juridico da empresa antes de publ”
  - “lista de desejos 0”
  - “prototipo dados e textos de exemplo nao publicar”
  - “pular para o conteudo”
  - “rascunho para revisao juridica”
  - “se a peca nao serviu ou voce mudou de ideia tem prazo e processo definidos sem letra miuda e sem precisar just”
- Textos do JSON que não estão no protótipo: 16 (dinâmicos, rótulos de acessibilidade e textos de sistema costumam aparecer aqui)
- Imagens: protótipo 0 | JSON 0

## 21-envio.json  x  seu-projeto/envio.html

- Widgets: heading (13), text-editor (13)

- Textos do protótipo não encontrados no JSON: **3**
  - “lista de desejos 0”
  - “prototipo dados e textos de exemplo nao publicar”
  - “pular para o conteudo”
- Textos do JSON que não estão no protótipo: 14 (dinâmicos, rótulos de acessibilidade e textos de sistema costumam aparecer aqui)
- Imagens: protótipo 0 | JSON 0

## 22-privacidade.json  x  seu-projeto/privacidade.html

- Widgets: heading (17), text-editor (18)

- Textos do protótipo não encontrados no JSON: **7**
  - “como a iara costa coleta usa guarda e exclui os seus dados pessoais conforme a lei geral de protecao de dados ”
  - “este documento foi escrito para dar estrutura e cobrir os pontos obrigatorios da lgpd ele”
  - “prototipo dados e textos de exemplo nao publicar”
  - “pular para o conteudo”
  - “sao dados que ainda dependem da empresa data da versao aprovada e”
  - “sao decisoes internas”
  - “ultima atualizacao 16 de outubro de 2026”
- Textos do JSON que não estão no protótipo: 18 (dinâmicos, rótulos de acessibilidade e textos de sistema costumam aparecer aqui)
- Imagens: protótipo 0 | JSON 0

## 23-termos.json  x  seu-projeto/termos.html

- Widgets: heading (21), text-editor (22)

- Textos do protótipo não encontrados no JSON: **8**
  - “as condicoes para usar este site e comprar na iara costa escrito para ser lido nao para esconder informacao”
  - “conferir no go live a data muda quando o juridico aprovar a versao final”
  - “estrutura pronta para revisao do juridico da empresa nenhuma clausula aqui pode reduzir direitos garantidos pe”
  - “lista de desejos 0”
  - “pular para o conteudo”
  - “sao dados que ainda dependem da empresa e”
  - “sao decisoes internas”
  - “ultima atualizacao 16 de outubro de 2026”
- Textos do JSON que não estão no protótipo: 22 (dinâmicos, rótulos de acessibilidade e textos de sistema costumam aparecer aqui)
- Imagens: protótipo 0 | JSON 0

## 24-cookies.json  x  seu-projeto/cookies.html

- Widgets: heading (14), text-editor (15)

- Textos do protótipo não encontrados no JSON: **6**
  - “conferir no go live a data muda quando o juridico aprovar a versao final”
  - “envio para todo o brasil”
  - “esta politica precisa estar alinhada palavra por palavra com o que o banner de cookies realmente faz se o bann”
  - “lista de desejos 0”
  - “pular para o conteudo”
  - “ultima atualizacao 16 de outubro de 2026”
- Textos do JSON que não estão no protótipo: 15 (dinâmicos, rótulos de acessibilidade e textos de sistema costumam aparecer aqui)
- Imagens: protótipo 0 | JSON 0

## Auditoria de CSS

- CSS do protótipo: 897 regras em 4 arquivos, 74 blocos @media, 53 regras :hover, 11 de foco.
- CSS que o Elementor recebe (`iara-cabecalho.css`, embutido nos 24 JSON e no kit): 52 regras, 3 blocos @media, 12 regras :hover.
- Classes `iara-*` usadas nos JSON: 16; sem nenhuma regra no CSS: 1: iara-barra
- Ajustes responsivos declarados nos JSON (chaves _tablet/_mobile): 42
- Total de textos do protótipo não encontrados nos JSON: 536 (detalhe por página acima; parte é texto dinâmico de loja/sistema, parte é conteúdo a conferir)
