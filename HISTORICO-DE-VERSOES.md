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

### v0.2.3 · 2026-10-16 · Bloco B, parte 4: o funil de compra

**O que entrou**

| O que | Onde |
|---|---|
| Sacola, com o widget clássico de carrinho e o campo de cupom | `bloco-b/json/06-carrinho.json` |
| Finalizar compra, com o widget clássico de checkout | `bloco-b/json/07-checkout.json` |
| Pedido recebido, com o resumo dinâmico do pedido | `bloco-b/json/08-pedido-recebido.json` |
| Minha conta, com pedidos, endereços e dados | `bloco-b/json/09-conta.json` |
| Lista de desejos, com o aviso de pendência do plugin | `bloco-b/json/10-desejos.json` |
| Ajustes do funil no WooCommerce (endereços das telas, compra como visitante, cupom, noindex) | `bloco-b/GUIA-IMPORTACAO.md`, seção 4.3 |

**Decisões**

- **Carrinho e checkout clássicos**, como pede a aceitação do dossiê: nada de
  blocos novos de carrinho e checkout nestas páginas.
- **A lista de desejos não finge que funciona.** Sem plugin aprovado, a página
  traz o aviso da pendência e o botão para a loja, e fica sem publicar.
- **Configuração de loja não vai em arquivo de template**: compra como
  visitante, cupom, endereços das telas e noindex são ajustes do WooCommerce e
  do Yoast, listados no guia.

**Verificado:** `tools/blocob_confere.py` passa nos 10 templates.
**Não verificado:** importação, renderização e qualquer pedido de teste, sem
WordPress. Pedido de teste de verdade só no staging, sem pagamento real.

### v0.2.2 · 2026-10-16 · Bloco B, parte 3: loja e página do produto

**O que entrou**

| O que | Onde |
|---|---|
| Arquivo da loja: cabeçalho, coluna de filtros, grade dinâmica com ordenação e paginação, faixa verde de ajuda | `bloco-b/json/04-loja.json` |
| Página do produto: trilha, galeria, nome, avaliação, preço, descrição curta, variações e compra, garantias, abas, relacionados e faixa de ajuda | `bloco-b/json/05-produto.json` |
| Decisão pendente dos filtros da loja, com os três caminhos possíveis | `bloco-b/GUIA-IMPORTACAO.md`, seção 4.4 |

**Decisões**

- **Nada de produto escrito à mão, também aqui.** Nome, preço, foto, estoque,
  variações e relacionados são widgets dinâmicos do WooCommerce.
- **Os filtros de preço, cor e tamanho não foram travados no arquivo.** O
  Elementor Pro não traz filtro por atributo dentro do canvas, então o arquivo
  marca o que configurar e o guia apresenta os três caminhos (blocos do
  WooCommerce, plugin aprovado ou links por atributo) para a equipe decidir.
- **Swatches não são nativos.** O seletor de cor e tamanho em botões, como o do
  protótipo, depende de plugin aprovado; sem ele, o WooCommerce mostra os
  seletores padrão.

**Verificado:** `tools/blocob_confere.py` passa nos 5 templates (111 containers,
145 widgets). **Não verificado:** importação e renderização, sem WordPress.

### v0.2.1 · 2026-10-16 · Bloco B, parte 2: página inicial

**De onde veio:** a cliente pediu para começar a segunda parte do Bloco B pela
home, e não pela loja.

**O que entrou**

| O que | Onde |
|---|---|
| Página inicial completa: hero, faixa de benefícios, categorias, produtos em destaque, ocasiões, editorial do ateliê, coleção, depoimentos, posts recentes e perguntas frequentes | `bloco-b/json/03-home.json` |
| Ajustes da home no editor (fotos, produtos em destaque, posts, links de categoria, depoimentos reais) | `bloco-b/GUIA-IMPORTACAO.md`, seção 4.3 |
| A home sai da lista de páginas futuras e entra na lista do que está pronto | `bloco-b/GUIA-IMPORTACAO.md`, seção 5 |

**Decisões**

- **Produto e post não são escritos à mão.** A seção Em destaque usa o widget de
  produtos do WooCommerce e a seção Do diário usa o widget de posts: os dois são
  dinâmicos e nascem do cadastro real.
- **A legenda do hero não foi sobreposta à foto.** No protótipo ela fica sobre a
  imagem; no Elementor, sobrepor texto à imagem sem CSS livre não é confiável,
  então a legenda entra abaixo da foto e a sobreposição fica como ajuste opcional
  no editor.
- **Os depoimentos continuam marcados como exemplo**, com o campo de cidade como
  `[PREENCHER]`, para ninguém publicar depoimento fictício sem perceber.

**Verificado:** `tools/blocob_confere.py` passa nos 3 templates (93 containers,
105 widgets, 15 cores, 10 fontes). **Não verificado:** importação e renderização,
sem acesso ao WordPress.

### v0.2.0 · 2026-10-16 · Bloco B, parte 1: cores, fontes, cabeçalho e rodapé

**De onde veio:** o Bloco A foi fechado e congelado na v0.1.20, e a cliente pediu
para seguir para o Bloco B. O Bloco B é a tradução do protótipo para o WordPress:
templates do Elementor, entregues em partes, começando pelo que todas as páginas
usam.

**O que entrou nesta parte**

| O que | Onde | Para que serve |
|---|---|---|
| As 15 cores e as 10 fontes do site, com nome e valor | `bloco-b/globais/cores-e-fontes.json` | é a base: todo template aponta para elas |
| Cabeçalho do site (faixa verde, logo, menu e os quatro ícones) | `bloco-b/json/01-cabecalho.json` | aparece em todas as páginas |
| Rodapé do site (newsletter, quatro colunas, segurança e formas de pagamento, base com CNPJ) | `bloco-b/json/02-rodape.json` | aparece em todas as páginas |
| Guia de importação, com ordem de trabalho e o que conferir | `bloco-b/GUIA-IMPORTACAO.md` | é o documento que a equipe segue no staging |
| Resumo de uma página | `bloco-b/LEIA-ME.txt` | orientação rápida de quem abre a pasta |
| Gerador dos arquivos | `tools/blocob_gera.py` | escrever o layout uma vez e gerar de novo quando mudar |
| Conferência automática dos arquivos | `tools/blocob_confere.py` | formato do Elementor, widgets permitidos, referências de cor |
| Casamento dos ids das cores com os do site | `tools/ajusta-ids.py` | resolve a diferença entre o apelido da cor e o id que o Elementor sorteia |

**O formato foi conferido no código-fonte do Elementor**, não em um site real: o
envelope de importação (`content`, `page_settings`, `version` 0.4, `title`,
`type`) vem de `includes/template-library/sources/local.php` e `includes/db.php`;
o padrão das referências de cor e de fonte (`globals/colors?id=...`) vem de
`core/files/css/base.php` e do editor; a forma das configurações de container veio
dos próprios arquivos de teste do plugin. Os widgets do Elementor Pro não são de
código aberto, então os ajustes deles ficaram fora do arquivo, com instrução no
guia. Nome de ajuste desconhecido não quebra a importação: é simplesmente
ignorado.

**O que foi verificado aqui:** `tools/blocob_confere.py` passa nos dois templates
(40 containers, 46 widgets, nenhum widget proibido, nenhuma cor escrita à mão,
todas as referências de cor e de fonte existindo nas globais). O gerador é
determinístico: rodar de novo produz exatamente os mesmos arquivos.

**O que não foi verificado:** nenhuma importação, nenhuma renderização e nenhuma
medida de desempenho, porque não há acesso ao WordPress, ao painel ou ao banco. A
importação é da equipe, em staging, um arquivo por vez.

**Decisão registrada sobre o número de arquivos:** o dossiê falava em 21 JSONs; a
conta página por página dá 24 (duas partes do site mais as 22 páginas do
protótipo). O guia traz a tabela completa (seção 5.2) e a alternativa de juntar as
três páginas legais em um modelo único, se a equipe preferir ficar em 21.

**Resultado das verificações:** `check.py` e o pente fino seguem em "tudo certo"
nas 22 páginas do protótipo; `node tools/test.js` com 1.043 verificações sem
falha; o Bloco B acrescenta a sua própria conferência, sem tocar no que já estava
aprovado.

### v0.1.20 · 2026-10-16 · Descrições de busca e área de toque dos botões

**De onde veio:** segunda rodada de pente fino no navegador de verdade. A v0.1.19
olhou o que estava quebrado; esta olha o que estava difícil de usar: o texto que
aparece no resultado do Google e o tamanho dos alvos de clique e toque. O método
foi o mesmo: abrir as 22 páginas em Chromium sem interface, medir cada elemento
clicável com o JavaScript do navegador e conferir com as diretrizes de
acessibilidade WCAG 2.2 (nível AA).

**Problema 1: as descrições de busca eram curtas demais**

Todo resultado no Google mostra duas ou três linhas de texto abaixo do título,
retiradas de uma descrição que fica no cabeçalho da página. Das 22 páginas do
protótipo, 11 tinham descrição com menos de 60 caracteres: o buscador preenchia o
espaço com pedaços aleatórios da página, e o resultado aparecia sem sentido. As
outras foram reescritas por qualidade, não por tamanho.

| Situação | Antes | Agora |
|---|---|---|
| Menor descrição do site | 37 caracteres | 111 caracteres |
| Maior descrição do site | 161 caracteres | 149 caracteres |
| Quantidade abaixo do mínimo recomendado | 11 páginas | nenhuma |
| Média | 96 caracteres | 122 caracteres |

As 22 descrições foram reescritas à mão, página por página, cada uma citando o
que existe de verdade naquela página, sem promessa que o site não faz e sem
palavra repetida em série. O padrão usado foi entre 110 e 155 caracteres, que é
onde o Google costuma mostrar o texto inteiro sem cortar.

**Problema 2: alvos de toque pequenos demais para o dedo**

A WCAG 2.2 criou um critério novo, o 2.5.8, que pede área de pelo menos 24 por 24
pixels para qualquer coisa clicável ou tocável. A varredura mediu cada elemento
interativo e encontrou cinco que ficavam abaixo disso:

| O que | Antes | Agora | Como |
|---|---|---|---|
| Botões de menos e mais da quantidade | 44 x 23 px | 44 x 44 px | altura mínima de 44px no conjunto |
| Links das colunas do rodapé | 21 px de altura | 31 px | espaço interno de 6px acima e abaixo |
| Links da faixa de texto miúdo do rodapé | 13 px | 24 px | caixa flexível com altura mínima |
| Convite "Adicionar à sacola" no cartão | 109 x 14 px | 24 px de altura | caixa flexível com altura mínima |
| Links da faixa de aviso no topo | 141 x 13 px | ~29 px | área ampliada com camada invisível, sem engrossar a faixa (que continua com 84px e o cabeçalho com 71px) |

**O que ficou de fora, com motivo:** os links que ficam dentro de um parágrafo ou
de um título (nome do produto no cartão, "Guia de medidas", aviso da newsletter)
medem apenas o texto, porque são texto no meio da frase. A própria WCAG 2.2 abre
exceção para esse caso, o que se chama de "texto em linha": ampliar esses links
mudaria a quebra de linha e o desenho do parágrafo. Ficam como estão e a decisão
está registrada. As caixas de seleção do checkout e da conta (20 x 20 px) estão
dentro do rótulo, que é a área de toque real: clicar no texto ao lado também
marca a caixa.

**Verificação automática:** a seção 26 do `test.js` cobre cada conserto acima
(11 verificações novas): as cinco áreas de toque, os limites de tamanho das 22
descrições, a ausência de travessão e a chegada da descrição longa no HTML da
home. Total do arquivo: 1.043 verificações, todas passando.

**Fechamento do Bloco A (mesma data, sem mudança no template).** Com a v0.1.20
aprovada, o Bloco A (protótipo HTML estático de 22 páginas) foi dado como
**concluído** e congelado:

| O que | Onde |
|---|---|
| Cópia integral do protótipo, idêntica a `seu-projeto/` (75 arquivos, 6,2 MB), com `LEIA-ME.txt` explicando a pasta | `template-v0.1.20/` |
| Tudo o que ainda depende de informação da empresa, em um documento só: 78 marcações nas 22 páginas, separadas por assunto e por quem resolve | `PENDENCIAS.md` |
| `README.md` da raiz reescrito para dizer que o Bloco A fechou, com a organização do repositório atualizada | `README.md` |

A cópia foi conferida com `diff -r`: é idêntica a `seu-projeto/`, fora o
`LEIA-ME.txt` da própria pasta. O `seu-projeto/` também foi conferido contra a
etiqueta `v0.1.20` (`git diff`): nada mudou desde a auditoria que originou a
versão. As verificações seguem em 1.043, sem falha, com `check.py` e o pente
fino em "tudo certo" nas 22 páginas. A pasta `template-v0.1.18/` fica guardada
como registro da versão anterior.

### v0.1.19 · 2026-10-16 · Pente fino no navegador: o que estava quebrado no celular

**De onde veio:** continuação dos ajustes no protótipo depois do merge. Desta
vez as páginas foram abertas em um navegador de verdade (Chromium sem interface)
nas larguras de 390, 768 e 1440 pixels, com teste de interação, teclado e
contraste. Até aqui tudo era conferido por leitura de código, então esta é a
primeira vez que o protótipo é medido como uma pessoa vê.

**O que estava quebrado e foi consertado**

| Problema | O que acontecia | Conserto |
|---|---|---|
| Marcador de pendência estourava a tela | Os textos `[PREENCHER: ...]`, que são longos, tinham `white-space: nowrap`: em 390px a página ficava 1.057px de largura e a pessoa precisava rolar de lado. Atingia Sobre, Contato, Trocas, Privacidade, Termos e Cookies | o marcador agora quebra linha como texto normal |
| Tabela com rolagem empurrava a coluna | Na Conta e no artigo, a grade deixava a tabela de medidas ditar a largura da coluna: a página inteira estourava (641px e 451px em uma tela de 390px) | `min-width: 0` nas duas grades, o que prende a tabela dentro da caixa com rolagem |
| Balão do WhatsApp cobria o que importa | Parado no topo, o balão tapava o valor no Pix do checkout (R$ 832,77), o botão "Criar minha conta" e o botão "Calcular" do frete no celular | o balão entra depois que a pessoa rola 160px (e o resumo preso no topo reserva 96px para ele). Sem JavaScript, aparece desde o início, como antes |
| Acordeão morto em três páginas | FAQ, Envio e Guia de Medidas têm acordeão, mas não carregavam o script que o abre: clicar não fazia nada. O da home funcionava, o que mascarava o problema | o script passou a ser carregado nas três páginas |
| Formulário de contato sem resposta | Com `novalidate` e campos obrigatórios, clicar em "Enviar mensagem" não mostrava nada: a pessoa achava que o site tinha travado | script de validação novo (`contato.js`): marca o campo, escreve a mensagem embaixo, liga a mensagem ao campo e leva o foco ao primeiro problema |
| Cor errada na página de produto | A peça é o Vestido Midi Sálvia (nome, foto e ficha), mas o grupo de cor abria com "Terracota" marcado e oferecia "Off-white" e "Preto", que não existem no catálogo nem na paleta | o grupo mostra a cor real (Sálvia); as duas cores inventadas saíram do CSS; a descrição da busca também foi corrigida |
| Botões da lista de desejos sem ação | "Adicionar à sacola" e "Remover" eram botões sem nenhum comportamento | os dois funcionam: adicionar abre a sacola lateral, remover tira a peça, atualiza o contador e avisa |

**Contraste (WCAG 2.2 AA, medido no navegador)**

| O que | Antes | Agora |
|---|---|---|
| Rótulo de seção em 11px (roxo acinzentado da paleta) | 4,27:1, abaixo do mínimo de 4,5:1 | tom ajustado para 4,92:1 no papel, 4,56:1 no hover soft e 5,00:1 no branco |

Os outros pontos que apareceram na varredura são decorativos e ficam como estão,
com nota no histórico: o ponto separador do aviso e o ponto da faixa da listagem
(ambos `aria-hidden`, redundantes com o texto ao lado), o numeral dos capítulos
(11px, 3,17:1) e a estrela da avaliação (ícone, com o texto "4,9 de 5" ao lado
para leitor de tela). As setas desligadas da paginação ficam em 1,39:1 de
propósito, para parecer o que são: fora de alcance.

**Verificação automática:** a seção 25 do `test.js` cobre cada conserto acima
(24 verificações novas). Também foi rodada uma varredura de página inteira em
22 páginas por 3 larguras: nenhuma página estoura a largura, nenhuma imagem
quebrada, nenhuma imagem sem texto alternativo e nenhum erro de JavaScript.

**Resultado das verificações:** `build.py` e `check.py` com as 22 páginas
certas; 1.032 verificações automáticas e zero falhas; `pente-fino.py` com as 12
seções zeradas.

### v0.1.18 · 2026-10-16 · Foto do hero quadrada, com corte centralizado

**Pedido da cliente:** "Pode reduzir a imagem para nao esticar muito deixe
quadrada ne fica melhor veja ai para nao ficar quebrado".

| O que mudou | Onde |
|---|---|
| A foto do hero passou a 1:1: entra quadrada, com corte centralizado (`object-position: center 50%`) | `pages.css` |
| Em tela grande (1021px ou mais) a foto fica com no máximo 560px de largura e alinhada à direita, para o hero não crescer em altura | `pages.css` |
| Enquadramento conferido na foto real, recorte por recorte: o corte central é o único que mantém o rosto, o cabelo e a blusa no quadro (o corte pelo topo corta o cabelo e o corte pelo pé corta a cabeça) | conferência |
| A spec da foto do hero passou de 1200×1400 para 1200×1200 (1:1) | `SPECS-DE-IMAGEM.md` |
| Verificação da seção 24 atualizada: quadrado, `cover`, corte central, nenhuma moldura retrato antiga e o limite de 560px | `tools/test.js` |

**Resultado das verificações:** `build.py` e `check.py` com as 22 páginas
certas; 997 verificações automáticas e zero falhas; `pente-fino.py` com as 12
seções zeradas.

**Organização do repositório (mesma data, sem mudança no template):** o template
ganhou uma pasta congelada com o número da versão, `template-v0.1.18/`, com a
cópia integral do protótipo e um `LEIA-ME.txt` explicando o que é a pasta e como
abrir. Daqui em diante, cada versão fechada ganha uma pasta como esta. O
`README.md` da raiz passou a explicar a organização do repositório.

### v0.1.17 · 2026-10-16 · Foto do hero inteira e a descrição por cima da imagem

**Pedido da cliente:** "tem que acertar a imagem e essa breve descricao em cima
da imagem que nao foi feito tb", com o print do hero do template: a foto com um
quadrinho branco no canto inferior direito, com o numeral "01" e a descrição da
peça.

**Duas decisões da cliente (respondidas em 16/10/2026):** a foto aparece
inteira, sem corte; e a legenda usa o texto do template, o que confirma que o
tingimento com argila do Vale do Paraíba é real.

| O que mudou | Onde |
|---|---|
| A foto saiu da moldura retrato (6:7 abaixo de 1021px, 5:6 acima) e do recorte: entra inteira, na proporção original (768×1376), ocupando a largura da coluna | `pages.css` |
| O selo virou caixa sobre a foto, no canto inferior direito: fundo de papel, borda fina, numeral 01 em linha própria, no máximo 220px de largura e 20px de recuo | `pages.css` |
| No celular o selo desce para baixo da foto, para não cobrir a modelo | `pages.css` |
| A legenda voltou ao texto do template: "Blusa de Linho Terracota, tingida com argila do Vale do Paraíba" | `01-home.html` |
| Verificação nova (seção 24) cobrindo a foto sem recorte, o selo sobre a foto e o texto confirmado | `tools/test.js` |

**Resultado das verificações:** `build.py` e `check.py` com as 22 páginas
certas; 993 verificações automáticas e zero falhas; `pente-fino.py` com as 12
seções zeradas.

**Continua fora do site, aguardando confirmação:** "tingimento natural" com
casca de cebola e folhas de eucalipto, "costura em pequenos lotes" (30 a 60
peças por edição, remuneração justa) e "fornecedores certificados".

### v0.1.16 · 2026-10-16 · Página da coleção em capítulos, como o zip

**Pedido da cliente:** "veja na imagem a pagina de coleção do template enviado
nao esta igaul verifique". A imagem mostrava o capítulo 1 do zip ("01 · Terracota
/ O barro que veste"), com foto grande de um lado, texto do outro, duas peças
embaixo e o convite "Comprar o capítulo". A nossa página de coleção ainda era uma
grade de quatro looks com etiquetas.

| O que mudou | Onde |
|---|---|
| A coleção deixou o cabeçalho de página e passou a abrir como editorial: capa centralizada com a trilha, o nome da coleção, a chamada e quatro fichas | `17-lookbook.html`, `pages.css` |
| Três capítulos, cada um com foto grande de um lado, texto e duas peças do catálogo do outro, e o convite "Comprar o capítulo" no fim | `17-lookbook.html` |
| O capítulo do meio inverte os lados, como no zip; abaixo de 1021px a foto vai para cima e o texto desce | `pages.css` |
| Cartão enxuto para os capítulos (foto, selo, coração, categoria, nome e preço), sem nota, tamanhos e convite da sacola, como no zip | `build.py` (`<!--CARDCAP:-->`) |
| Título da página: "Coleção Terra & Linho", igual ao rótulo do menu e ao link do rodapé | `pages.json` |
| Nota de produção das fotos reescrita para a estrutura de capítulos, no fim da página | `17-lookbook.html` |
| Fichas do zip que a empresa não confirmou (18 peças, tingimento natural, edições numeradas) não entraram | `17-lookbook.html` |

**Correções de conteúdo no mesmo dia (afirmações do zip sem confirmação):**

| Antes | Agora | Onde |
|---|---|---|
| "tingido com argila e costurado em pequenos lotes no Brasil" | "em linho, algodão egípcio e viscose de alta gramatura. Modelagem, corte e confecção próprios, no ateliê em Cerquilho (SP)" | capa da home |
| "Blusa de Linho Terracota, tingida com argila do Vale do Paraíba" | "de modelagem autoral, feita no ateliê" | selo da capa |
| "Tingimento natural" (argila, casca de cebola, eucalipto) | "Modelagem autoral" | bloco do ateliê |
| "Costura em pequenos lotes" (30 a 60 peças, remuneração justa) | "Tecidos de alta gramatura" | bloco do ateliê |
| "Rastreio da fibra" (fornecedores certificados) | "Compra tranquila" (troca em 30 dias e 7 dias para desistir) | bloco do ateliê |
| "Três capítulos em 18 peças" | "Três capítulos em doze peças" | vitrine da coleção na home |
| "Peças em pequenos lotes" no rodapé | tecidos, modelagem e produção próprios em Cerquilho | rodapé de todas as páginas |
| "troca em 7 dias" (carrinho e Sobre) | "troca em 30 dias" (7 dias é o arrependimento) | duas páginas |

**Resultado das verificações:** `build.py` e `check.py` com as 22 páginas certas;
`test.js` com 980 verificações e zero falhas (a seção 23 é nova e cobre os
capítulos); `pente-fino.py` com as 12 seções zeradas.

**Pontos que continuam como vieram do zip e merecem confirmação:** o nome da
coleção ("Terra & Linho"), a estação ("Outono · Inverno 2026", que não entrou na
capa) e os cenários sugeridos para as fotos.

### v0.1.15 · 2026-10-16 · Coleção com a paginação e a ordenação do zip

**Pedido da cliente:** "a pagina de coleção tem que seguir a do template que
enviei pode ajustar". Na v0.1.14 o layout do zip tinha sido seguido em tudo menos
na paginação, porque o dossiê pedia o catálogo inteiro em uma grade só. O pedido
de agora revê essa decisão.

| O que mudou | Onde |
|---|---|
| Linha da coleção logo abaixo do fio do cabeçalho, como no zip: faixa de peças visíveis, recado de tamanhos (do P ao GG) e atalho do guia de medidas | `02-loja.html`, `style.css` |
| Paginação no rodapé da grade, com o desenho do zip: nove peças por página, quadrados de 44px, página atual com fio de tinta e setas que desligam nas pontas | `02-loja.html`, `comercio.css`, `filtros.js` |
| Faixa "Mostrando 1–9 de 12 peças" acompanha filtros e página, e a grade volta ao topo ao trocar de página | `filtros.js` |
| Cinco formas de ordenar, as mesmas do zip e do WooCommerce: mais recentes, mais populares, menor preço, maior preço e melhor avaliados | `02-loja.html`, `filtros.js` |
| A ordenação por nome saiu: não existe no zip | `02-loja.html` |
| Nota e número de avaliações entraram nos cartões (`data-nota`, `data-avaliacoes`) para alimentar as duas ordenações novas | `build.py` |
| O recado de tamanhos saiu da barra de ferramentas (subiu para a linha da coleção) e o aviso interno sobre paginação saiu da página | `02-loja.html`, `pages.css`, `comercio.css` |
| O aviso do Diário sobre a loja não ter paginação foi corrigido | `10-blog.html` |

**Resultado das verificações:** `build.py` e `check.py` com as 22 páginas certas;
`test.js` com 938 verificações e zero falhas (a seção 22 é nova e cobre a
paginação e as cinco ordenações); `pente-fino.py` com as 12 seções zeradas.

**Decisão revista:** a loja passa a paginar de 9 em 9, como o zip (52 peças em 6
páginas). Se a cliente preferir o catálogo inteiro em uma grade só, é uma linha
em `filtros.js` (`POR_PAGINA`).

### v0.1.14 · 2026-10-16 · Resumo fixo na sacola, coleção no layout do zip e artigo novo

**Pedido da cliente:** corrigir o alinhamento de dentro do card "Resumo" da sacola
e fazer com que ele fique preso na tela ao rolar; um layout novo e mais moderno
para a página do artigo; a página de coleção seguindo o layout do zip de
referência; e a "Especificação da Marca e Regras de Negócio" atualizada, agora com
retirada no ateliê, boleto, prazos de reembolso, tecidos e autoria do diário.

| O que mudou | Onde |
|---|---|
| Campo e botão do resumo alinhados pela base: o deslocamento de 26px que empurrava o botão "Calcular" para baixo do campo do CEP saiu do CSS | `pages.css` |
| Resumo da sacola preso abaixo do cabeçalho enquanto a página rola, com teto de altura para nunca esconder o botão de finalizar | `pages.css` |
| Causa do problema encontrada: `overflow-x: hidden` no `body` transformava o body numa caixa de rolagem e desligava todo `position: sticky` da página, inclusive o do cabeçalho. Trocado por `overflow-x: clip`, com reserva para navegador antigo | `style.css` |
| Valores do resumo em coluna, com número de largura fixa | `pages.css` |
| Página de coleção no layout do zip: a coluna de filtros acompanha a rolagem, começa direto em Categorias e fecha com as ações (Aplicar filtros e Limpar filtros) | `comercio.css`, `02-loja.html` |
| Contagem da listagem com o texto do zip: "12 peças nesta seleção" | `02-loja.html`, `filtros.js` |
| Cartão de produto em coluna, com 12px entre as partes, e grade com o espaçamento do zip (mais ar entre as linhas do que entre as colunas) | `style.css` |
| Layout novo do artigo: capa em duas colunas, índice que acompanha a leitura, barra fina de progresso, citação de respiro, chamada do guia de medidas, etiquetas de assunto, compartilhar e cartão de autoria | `11-post.html`, `pages.css`, `artigo.js` |
| Retirada no ateliê confirmada: segunda a sexta, das 10h às 17h, depois do aviso de "Pronto para Retirada" | checkout, Envio e Contato |
| Boleto bancário habilitado pelo Mercado Pago: vence em 2 dias úteis e o pedido é liberado depois da compensação. Valor cheio, sem o desconto do Pix | checkout, rodapé, Termos, Perguntas frequentes, Produto e Home |
| Prazos de reembolso: Pix em 2 dias úteis, cartão em 3 dias úteis (o lançamento depende da operadora) e boleto em 3 dias úteis | `18-trocas.html` |
| Peças de liquidação e bazar: troca pelo mesmo modelo em outro tamanho, e o cupom de troca vale o valor efetivamente pago | `18-trocas.html` |
| Tecidos e origem: linho, algodão egípcio e viscose de alta gramatura, modelagem, corte e confecção 100% autorais, feitos no Brasil, em Cerquilho - SP | `13-sobre.html`, `03-produto.html` |
| Autoria dos textos do diário confirmada: Iara Costa e Equipe de Criação | `10-blog.html`, `11-post.html` |

**Resultado das verificações:** `build.py` e `check.py` com as 22 páginas certas;
`test.js` com 907 verificações e zero falhas (a seção 21 é nova); `pente-fino.py`
com as 12 seções zeradas.

**Decisão revista na v0.1.15:** a loja chegou a ficar sem paginação, como o
dossiê pedia, mesmo com o zip mostrando paginação na listagem. A pedido da
cliente, a v0.1.15 passou a seguir a paginação do zip.

### v0.1.13 · 2026-10-16 · Cartões de envio e pagamento no checkout e as regras de negócio fechadas

**Pedido da cliente:** duas imagens de referência do fechamento de compra (cartões
de opção com rádio, título, linha de apoio e valor; campos do cartão aparecendo
quando o cartão é escolhido) mais a "Especificação da Marca e Regras de Negócio",
que respondeu frete, trocas, prazos, cuidados das peças, DPO e tipografia.

| O que mudou | Onde |
|---|---|
| Cartões de opção no padrão da imagem: rádio, título, linha de apoio e valor; o cartão escolhido ganha borda e fundo (`:has()` no CSS e `.is-selected` pelo JS, para navegador sem `:has()`) | `pages.css`, `05-checkout.html` |
| Três formas de envio em cartões: PAC, SEDEX e Retirar no ateliê, com prazo, valor e o endereço do ateliê | `05-checkout.html` |
| Duas formas de pagamento em cartões: Pix com etiqueta "5% off" e Cartão de crédito com "6x sem juros" e parcela mínima de R$ 50,00 | `05-checkout.html` |
| Campos do cartão que aparecem só quando o cartão é escolhido, com máscaras e aviso de que são demonstração: sem `name`, nada é enviado nem guardado | `05-checkout.html`, `loja.js` |
| Valores conferidos no protótipo: produtos R$ 974,00, cupom R$ 97,40, Pix R$ 832,77, cartão R$ 876,60 e 6x de R$ 146,10 sem juros | `loja.js` |
| Frete grátis passou a contar o valor líquido (depois de cupom e do desconto do Pix), em todas as páginas | `loja.js`, `19-envio.html`, `04-carrinho.html`, `15-faq.html` |
| R$ 15,00 confirmado como regra só do PAC, em SP, RJ, MG e ES; SEDEX e demais regiões pelo cálculo dos Correios | `19-envio.html`, `15-faq.html`, `04-carrinho.html`, `loja.js` |
| Prazos de produção: 2 dias úteis para pronta entrega e 5 a 7 dias úteis para peças sob encomenda | `19-envio.html`, `03-produto.html`, `06-pedido-recebido.html`, `15-faq.html` |
| Troca por tamanho em 30 dias corridos, com a primeira troca gratuita e postagem reversa dos Correios; arrependimento em 7 dias com frete por conta da loja | `18-trocas.html`, `15-faq.html`, `03-produto.html`, `01-home.html` |
| Cuidados das peças: lavagem à mão ou ciclo delicado com sabão neutro, sem alvejante à base de cloro, secagem à sombra na horizontal e passar até 110°C | `03-produto.html` |
| Encarregado de dados (DPO) com e-mail próprio `dpo@iaracosta.com.br` no lugar do canal genérico | `20-privacidade.html`, `22-cookies.html`, `15-faq.html`, `14-contato.html` |
| Data de aprovação das páginas legais: 16 de outubro de 2026 | `20-privacidade.html`, `21-termos.html`, `22-cookies.html` |
| Parcela mínima de R$ 50,00 nas condições de pagamento dos Termos | `21-termos.html` |
| Marca do cabeçalho em 20px, como a especificação pede, sem `clamp()` | `header.css` |
| Regras `.radio` retiradas do CSS: o checkout usa `.choice` desde esta versão | `style.css` |
| Suíte de testes ganhou a seção 20 (cartões, valores, campos do cartão, regras novas e marca do cabeçalho) | `tools/test.js` |

**Resultado das verificações:** `build.py` e `check.py` com as 22 páginas certas;
`test.js` com 819 verificações e zero falhas; `pente-fino.py` com as 12 seções
zeradas.

**Marcadores que continuam abertos nesta versão:** dias e horários de retirada no
ateliê, composição e origem das peças, autoria dos textos do diário, prazo de
reembolso detalhado, peças de liquidação na troca, e os itens de privacidade que
dependem das ferramentas escolhidas (analytics, pixels, retenção).

### v0.1.12 · 2026-10-16 · Dados reais da empresa e regras de venda confirmadas

**Pedido da cliente:** informou os dados da empresa e as regras comerciais que
faltavam (identificação, atendimento, frete, gateway e cupom), para tirar os
marcadores `[PREENCHER]` do lugar onde eles já têm resposta.

| O que mudou | Onde |
|---|---|
| Razão social, nome fantasia, CNPJ, inscrição estadual e endereço do ateliê no rodapé de todas as páginas | `tools/partials/footer.html` |
| E-mail, telefone/WhatsApp e horário de atendimento no rodapé e no Contato | `tools/partials/footer.html`, `tools/content/14-contato.html` |
| Prazo de resposta de 24 horas úteis (segunda a sexta) nas páginas de atendimento, nos Termos e no Envio | `14-contato.html`, `20-privacidade.html`, `21-termos.html`, `19-envio.html` |
| Formas de pagamento: Pix com 5% de desconto e cartão em até 6x sem juros, pelo Mercado Pago | rodapé, `01-home.html`, `03-produto.html`, `05-checkout.html`, `15-faq.html`, `19-envio.html`, `21-termos.html` |
| Boleto, transferência bancária, PayPal e bandeiras não confirmadas saíram do site | rodapé, `05-checkout.html`, `15-faq.html`, `18-trocas.html` |
| Frete: Correios com cálculo por CEP, R$ 15,00 no Sudeste e grátis acima de R$ 299, com a tabela de exemplo reescrita | `19-envio.html`, `04-carrinho.html`, `05-checkout.html`, `06-pedido-recebido.html` |
| Regra do cupom BEMVINDO10 fechada: primeira compra, sem acúmulo com outras promoções nem com peças em liquidação | `04-carrinho.html`, `15-faq.html`, `21-termos.html` |
| Identificação completa da empresa nos Termos e na Política de Privacidade, com canal de privacidade | `21-termos.html`, `20-privacidade.html` |
| Endereço do ateliê no quadro do mapa do Contato | `14-contato.html` |
| `loja.js` passa a reconhecer a faixa de CEP do Sudeste para o recado do frete | `assets/js/loja.js` |
| Promessa de "troca fácil em 30 dias" na home marcada como `[A DEFINIR]` | `01-home.html` |

**Reconciliação com decisões anteriores:** o dossiê previa frete grátis acima de
R$ 199 (superado pela decisão de R$ 299 em 16/10) e não fixava gateway. O rodapé
mostrava oito formas de pagamento como ilustração; agora mostra só as confirmadas.
Os valores de exemplo de PAC e SEDEX (R$ 24,90 e R$ 39,90, com prazos de 5 a 9 e
2 a 4 dias úteis) saíram de todas as páginas.

**Regra cumprida:** nada foi inventado para preencher marcador. Prazo e frete da
troca por tamanho, prazo de produção, encarregado de dados (DPO), data de
aprovação das páginas legais, composição e cuidados das peças, autoria dos textos
do diário e valor/prazo por região fora do Sudeste continuam como
`[A DEFINIR]`/`[PREENCHER]`.

**Verificado em arquivo:** 22 páginas (`build.py` e `check.py`, "tudo certo"); teste
de navegador com **720 verificações, nenhuma falha**, incluindo o bloco novo (§19)
que confere os dados da empresa no rodapé das 22 páginas, a ausência de boleto,
PayPal e transferência bancária, a ausência dos valores de exemplo que saíram e as
regras de frete no `loja.js`; pente fino com as doze conferências zeradas.

### v0.1.11 · 2026-10-16 · Pente fino no HTML e no CSS e as melhorias de JavaScript do template

**Pedido da cliente:** fazer um pente fino em todos os arquivos do template para
ver se existe HTML ou CSS quebrado, e conferir os arquivos de JavaScript do
template enviado (zip) para ajustar o que fizer sentido no nosso.

| O que mudou | Onde |
|---|---|
| Pente fino com parser de verdade (html5lib + tinycss2) nas 22 páginas, 25 parciais, 4 CSS e 4 JS: nenhum erro de sintaxe, nenhum id repetido, nenhuma âncora quebrada, nenhum `aria-*` ou `for` órfão, nenhum campo sem rótulo, nenhuma imagem ou arquivo faltando | `tools/pente-fino.py` (novo) |
| Dois quebrados de HTML corrigidos: `<p margin-bottom:0">` em Termos e Cookies: era um estilo escrito como se fosse atributo, o navegador lia como resto de tag | `tools/content/21-termos.html`, `22-cookies.html` |
| Duas fotos do resumo do checkout não declaravam medida (o tamanho estava só em `style=""`); agora trazem as medidas reais do arquivo | `tools/content/05-checkout.html` |
| Quarenta estilos escritos direto no HTML saíram e viraram regras com nome, por tela: `.summary__row--stack`, `.summary__action`, `.cart-item--compact`, `.info-box__links`, `.info-box__title`, `.field--wide` | `tools/content/04` a `14`, `style.css`, `pages.css` |
| CSS sem uso removido: `.cart-count` (contador antigo da sacola), `.section--sage`, quatro cores de swatch não usadas e o `style="width:0%"` da gaveta | `header.css`, `comercio.css`, `pages.css`, `tools/partials/drawer.html` |
| Estados de interface que faltavam ganharam desenho: carregando (esqueleto) e erro de campo; os três estados de estoque passaram a aparecer lado a lado na referência da equipe | `tools/content/03-produto.html`, `05-checkout.html`, `pages.css` |
| JavaScript do template adotado: cada melhoria inicia isolada (uma falha não derruba as outras), botões + e − da sacola, remover peça, cupom BEMVINDO10, cálculo de frete com máscara de CEP, máscara de CEP e telefone no checkout e recado que muda conforme o meio de pagamento | `assets/js/loja.js`, `swatches.js`, `header.js`, `filtros.js` |
| Trava de rolagem da gaveta sem o conteúdo pular de lado, agora em CSS (`scrollbar-gutter: stable`) no lugar do script de compensação que o template usa | `assets/css/style.css` |
| Régua de verificação versionada: o teste de navegador (jsdom) e o pente fino passaram a viver no repositório, com o `package.json` que instala o jsdom | `tools/test.js`, `tools/pente-fino.py`, `package.json` |

**Regra cumprida (o que do template NÃO foi copiado):** o JavaScript do zip calcula
frete com valores fixos (PAC R$ 24,90 e SEDEX R$ 39,90) e pede o número do cartão
na própria página. Nada disso entrou. O frete aqui continua só com a regra
confirmada pela empresa (grátis acima de R$ 299) e o resto como `[A DEFINIR]` até a
conta de frete ser contratada; dados de cartão são digitados na página do gateway,
que ainda não existe. Cupom: só o BEMVINDO10 documentado no dossiê, 10% na primeira
compra. Nenhum valor, prazo ou desconto foi inventado.

**Verificado em arquivo:** 22 páginas (`build.py` e `check.py`, "tudo certo"); teste
de navegador com **649 verificações, nenhuma falha**, com bloco novo (§18) para o
pente fino e para o JavaScript adotado; `tools/pente-fino.py` com as doze
conferências zeradas.

**Não entrou nesta versão:** os arquivos de JavaScript do zip têm 15 KB e 24 KB de
recursos que dependem de um WordPress instalado (carrinho do WooCommerce, painel de
conta, filtros por URL). Isso é trabalho do Bloco B, quando houver site para testar.

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
