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
- **Marca do cabeçalho**: a marca deste projeto é **texto** ("IARA COSTA" com a
  assinatura "Moda & Acessórios"), como no protótipo, e já vai escrita no
  template. Não é preciso subir imagem de logo. Se um dia a empresa tiver um
  logotipo em imagem, ele substitui a marca em texto no editor.
- Menu **Menu Principal** criado em Aparência > Menus, com os itens: Início,
  Loja, Coleção, Sobre, Contato. O widget identifica o menu pelo **slug**:
  o menu chamado "Menu Principal" tem o slug automático `menu-principal`,
  e é para ele que o cabeçalho aponta desde a v0.3.16. Se um dia o menu
  for renomeado, confira o slug (ele aparece na tela de edição do menu)
  e troque no editor do cabeçalho (widget Menu).

---

## 2.9 O jeito de uma vez só: o kit completo (recomendado, v0.3.12)

> **Pedido que originou esta seção:** "não tem como criar algo que possa
> apenas importar, pois cada alteração tenho que ficar fazendo isso".
> Tem: o `bloco-b/iara-costa-kit-completo.zip` é um **Kit do Elementor**
> de verdade (o mesmo formato que o botão Exportar Kit gera), com as
> configurações globais **e os 24 templates de uma vez**, cabeçalho e
> rodapé já com a condição Entire Site e os templates da loja, do produto,
> do blog, da busca e do 404 já com as condições deles. Um arquivo, uma
> importação. Ele também vai dentro do `iara-costa-kit.zip` do Bloco C.

Como importar:

1. **Segurança primeiro:** Elementor > Ferramentas > Importar/Exportar
   Kit > Exportar (o kit atual inteiro) e guarde o `.zip`.
2. Na mesma tela, **Importar** e escolha o `iara-costa-kit-completo.zip`.
3. Marque **Templates** e **Configurações do site** (Settings) e conclua.
   (Templates de kit pedem Elementor Pro ativo, que é o seu caso.)
4. Confira em **Templates**: os 24 arquivos da Iara Costa, o cabeçalho já
   valendo para o site inteiro. Depois siga da seção 5 deste guia em
   diante (criar as páginas e apontar cada uma para o template dela).

**Nas próximas correções, é este arquivo que você importa de novo.** Um
aviso honesto sobre como o Elementor funciona com qualquer kit: cada
importação **cria cópias novas** dos templates, ela não atualiza os
existentes. Então, antes de importar uma versão nova, apague em Templates
os 24 templates da Iara Costa da versão anterior (filtre por "Iara" /
pelos títulos), senão ficam duplicados e a condição Entire Site pode
continuar apontando para o antigo. Apagar os antigos e importar o kit:
dois gestos, em vez de 24 importações.

Os caminhos antigos continuam neste guia como alternativa e plano B: o
pacote só de globais (seção 3.0) e os JSONs um por um (seção 4).

**O CSS geral agora viaja dentro do kit (v0.3.14).** O arquivo
`bloco-b/css/iara-cabecalho.css` entra no `site-settings.json` do kit
completo (chave `custom_css` das Configurações do site): importar o kit
já aplica o CSS no site inteiro, sem colar nada na mão. Era esse o furo
das rodadas anteriores: o CSS ia num arquivo separado, fora de qualquer
importação, então "o CSS não pegava". Se um dia precisar mexer no CSS,
é em Elementor > Configurações do site > CSS personalizado que ele está.

**Endereço dos links (v0.3.13):** o site está em
`https://oeemax.com.br/iaracosta/` (subpasta). Todos os links internos
dos templates nascem desse endereço, porque link que começa com `/`
apontaria para a raiz do domínio, fora do site (foi a causa dos "links
todos quebrados"). A conferência reprova qualquer link interno fora do
endereço. Quando o site ganhar o domínio próprio, a troca é uma vez só,
com a ferramenta oficial: Elementor > Ferramentas > **Substituir URL**
(de `https://oeemax.com.br/iaracosta` para o domínio novo), e os
templates seguintes já devem nascer com o endereço novo: avise para
atualizar o `SITE_BASE` do gerador.

## 3. Passo 1: cores e fontes globais

Esta é a etapa mais importante do Bloco B. Todo o resto aponta para estas cores e
fontes pelo **id** do Elementor. Se elas não existirem com o id certo, o estilo do
template simplesmente não aparece (não quebra a página, mas fica sem cor).

### 3.0 O jeito rápido: importar o pacote de configurações (recomendado)

> **Atenção, erro comum:** o arquivo `cores-e-fontes.json` **não é um template**.
> Importá-lo em Templates > Importar dá o erro **"Tipo de modelo inválido"**, e é
> assim mesmo: ele é só a referência dos valores. Quem se importa é o pacote
> abaixo, e por outro caminho, o Importar/Exportar **Kit**.

O pacote é `bloco-b/globais/iara-costa-globais.zip` (também vai dentro do
`iara-costa-kit.zip` do Bloco C). Ele foi montado no formato que o Elementor
espera de um kit, conferido no código-fonte do plugin: `manifest.json` com
`version: "2.0"` e `site-settings.json` com as configurações.

1. **Antes, exporte o que já existe** (Elementor > Ferramentas > Importar /
   Exportar Kit > Exportar, só "Configurações do site") e guarde o `.zip`: é o
   seu caminho de volta. A importação **cria um kit novo e mistura** as
   configurações antigas com as novas, então isto é a rede de segurança.
2. Na mesma tela, use **Importar**, escolha o `iara-costa-globais.zip` e avance.
3. Quando ele perguntar o que importar, marque **Configurações do site**
   (Settings) e conclua.
4. Confira: abra uma página no Elementor > Configurações do site > Cores globais.
   Precisam estar lá as 15 cores (4 do sistema com os valores novos e 11
   personalizadas, incluindo "Papel" e "Linha") e, em Fontes globais, as 11
   fontes.

**Por que os templates nascem certos neste caminho:** na importação de kit, o
Elementor mantém o `_id` de cada cor e fonte personalizada, e neste pacote os
ids já são `iara-papel`, `iara-linha` e os demais que os 24 templates usam.
Conferido no código-fonte do plugin; **não testado em site real**. Se depois de
importar alguma cor não aparecer na lista, ou aparecer duplicada, use o plano B
da seção 3.3 (criar à mão e rodar o `ajusta-ids.py`).

Faça isso **num site ainda sem cores próprias** (staging novo é o ideal). Se o
site já tiver cores personalizadas, a importação **acrescenta** as novas sem
apagar as antigas: sobra cor duplicada para limpar depois.

Se preferir criar à mão, ou se a importação não funcionar na sua versão, as
tabelas das seções 3.1 e 3.2 são o plano B completo.

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

### 3.3 Plano B: criar à mão e acertar os ids (script de uma linha)

Este caminho só é necessário se você criou as cores na tela (seções 3.1 e 3.2)
ou se a importação da seção 3.0 não trouxe os ids certos. Criando na tela, o
Elementor sorteia um id próprio para cada cor, e o script abaixo faz o
casamento sozinho:

1. **Exportar** as configurações do site: Elementor > Ferramentas > Importar /
   Exportar Kit > Exportar > marcar **somente** "Configurações do site". Sai um
   `.zip`; dentro dele está o `site-settings.json`.
2. **Rodar** o script (primeiro em modo de conferência):

   ```bash
   python3 tools/ajusta-ids.py caminho/site-settings.json --simular
   python3 tools/ajusta-ids.py caminho/site-settings.json
   python3 tools/blocob_confere.py      # confere que continua tudo certo
   ```

O script casa cor por cor pelo **título**, mostra uma tabela do que muda e
reescreve as referências nos arquivos. Se alguma cor ainda não existir no site,
ele avisa em vez de adivinhar.

O arquivo `bloco-b/globais/cores-e-fontes.json` continua sendo a referência dos
valores e dos ids (`iara-papel`, `iara-linha`, e assim por diante). Ele **não se
importa em lugar nenhum**: quem se importa é o pacote da seção 3.0.

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
| Cabeçalho: marca em texto | a marca já vai escrita; trocar por imagem de logotipo só se a empresa tiver um |
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
| Diário e artigo | textos escritos no Gutenberg; o template só desenha a capa, o título e a vitrine. Nunca escrever post no Elementor |
| Coleção | escolher as fotos reais dos três capítulos e apontar cada botão para a categoria certa |
| Páginas legais | substituir todos os `[PREENCHER]` pelo texto aprovado pelo jurídico antes de publicar; elas nascem como rascunho |
| Busca e 404 | conferir a busca com e sem resultado, e abrir um endereço inexistente para ver a página 404 no ar |
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

### 4.6 Se o cabeçalho importou torto (diagnóstico da primeira importação real)

A primeira importação de verdade mostrou três problemas, já corrigidos na
v0.3.5. Se você importou uma versão anterior, apague o template antigo e
importe o `01-cabecalho.json` novo:

| O que aparece | Causa | Correção |
|---|---|---|
| Um retângulo gigante escrito "Logo." | versões antigas usavam o widget Site Logo sem logo definido | corrigido: a marca agora é texto, como no protótipo |
| Links da faixa verde em rosa ou vermelho | a cor do link não estava definida e herdou o padrão do tema | corrigido: `link_color` igual à cor do texto nos widgets de texto com link |
| Recados da faixa verde como texto corrido | versões até a v0.3.5 usavam um widget de texto | corrigido na v0.3.6: a faixa é uma **lista de ícones em linha** (`view: inline`), um recado ao lado do outro, com ícone em cada um |
| Cabeçalho com container demais e espaçamento solto | a estrutura tinha 7 containers (raiz, barra, linha e embrulho do menu) | enxugado na v0.3.7 para **4 containers**: faixa, barra, marca e ações. Marca com 24% à esquerda, menu no meio, ações com 24% à direita e 18px entre os ícones |
| Menu empilhado, em fonte serifada e gigante; tagline "Moda & Acessórios" serifada | o widget de menu e os títulos herdaram a fonte do tema, e o menu não tinha largura para ficar em linha | corrigido na v0.3.8: o menu ocupa o miolo da barra (`grow`), com sublinhado no item atual. **Ordem importa:** importe o pacote de globais (seção 3.0) ANTES do cabeçalho, senão título e tagline caem na fonte do tema |
| Caixa de busca aberta na barra ("O que você procura?") e sacola com caixa e "R$ 0,00" | o protótipo aprovado não tem nada disso: busca é só a lupa, sacola é só o ícone com o contador | corrigido na v0.3.8: lupa (ícone) que leva à página de busca, conta e desejos em ícone de traço (contorno), sacola sem mostrar o valor (`show_subtotal` desligado). Quem quiser a busca que abre em painel troca o ícone pelo widget Search no editor (ajuste 4.3) |
| Faixa verde com ícones (caminhão, folha, globo) | a cliente comparou com o protótipo: lá a faixa é texto em caixa alta separado por pontos, sem ícone | corrigido na v0.3.8: texto igual ao do protótipo, com a fonte global nova **Texto da faixa** (Jost 12px, caixa alta). A lista de ícones da v0.3.6 saiu |
| Containers demais nos outros 23 arquivos | embrulhos de um elemento só, sem fundo, borda nem respiro | a v0.3.8 achata esses embrulhos na geração: de **216 para 176 containers** nos 24 arquivos, sem mudar o desenho (a largura do embrulho passa para o elemento de dentro) |
| Menu certo, mas hover sem a linha escura e ícones da direita "pesados" | o CSS do kit só pintava o hover, sem sublinhar (o protótipo sublinha em Terracota escuro no hover e em Terracota claro no item ativo), e busca/sacola são glifos **cheios** no Font Awesome gratuito (não existe contorno deles; conta e coração já são contorno) | v0.3.19: estados do link completos no CSS do kit (hover e foco com linha escura, ativo com linha clara) e ícones a 17px com alvo de toque de 41px, sem caixa. Se um dia quiserem o traço fino idêntico ao desenho, o caminho é subir os 4 SVGs do protótipo na Mídia e trocar o ícone de cada ação no editor (o widget aceita SVG enviado) |
| Falta "Coleção" no menu | o menu do cabeçalho é o **Menu Principal** do WordPress, e ele foi criado com 4 itens | incluir o item Coleção em Aparência > Menus, apontando para a página `/colecao/` (que precisa existir; hoje ela dá 404, ver roteiro das páginas) |
| Todas as páginas de uma vez (v0.3.23) | `bloco-b/iara-costa-todos-os-templates.zip`: os 24 JSON, todos com o CSS embutido; importe o zip em Templates > Importar. Os templates de tema (cabeçalho, rodapé, loja, produto, busca, 404) ganham condições pelo kit completo; os de página entram na biblioteca e são aplicados página a página pelo roteiro deste guia. Dinâmico continua dinâmico: menu, logotipo, sacola, desejos (plugin TI), produtos e preços |
| Só o cabeçalho e o rodapé finais (v0.3.20, aprovados) | use `bloco-b/iara-costa-cabecalho-rodape.zip` descompactado: importe `01-cabecalho.json` e `02-rodape.json` em Templates > Importar Template, ou importe o kit completo (que já os inclui com as condições). Antes, apague as cópias antigas dos dois templates. O coração com número pede o plugin TI WooCommerce Wishlist ativo; a sacola com número é o Carrinho do Menu do WooCommerce e abre a gaveta lateral ao clicar |
| **Tudo gigante e serifado de novo: menu enorme, títulos do rodapé em Playfair grande** | diagnóstico da v0.3.18, com duas causas prováveis que se somam: (1) as fontes personalizadas (Jost miúda etc.) não estão mandando no site, e widget sem fonte declarada cai no padrão do tema ou na global Primary (Playfair 24); era literalmente o padrão do widget de menu, conferido no código dele. (2) **templates duplicados**: cada importação de kit cria cópias, e a condição pode continuar apontando para a cópia antiga, então o site segue mostrando a versão velha mesmo importando a nova | correção estrutural: a geração passou a **embutir o padrão de fonte em cada widget** (família, tamanho, peso, espaçamento e caixa declarados, da mesma tabela das globais); o menu declara Jost 12px em caixa alta no próprio widget, e as cores continuam globais (que funcionavam). E a regra de ouro da importação: em **Templates**, apague TODAS as cópias antigas dos templates da Iara Costa antes de importar (se a lista mostrar dois "Cabeçalho do site", é duplicado: apague os dois e importe o kit) |
| Rodapé com títulos de coluna fracos, sem a notinha da newsletter e sem a faixa demonstrativa de segurança | a comparação com o protótipo (v0.3.17) achou: títulos das colunas na fonte miúda em vez do rótulo em caixa alta, a nota "Um e-mail por mês..." e a nota da faixa de segurança fora do arquivo, e os subtítulos "Formas de pagamento/Segurança" em Jost em vez de Playfair | tudo restaurado no `02-rodape.json`: títulos em rótulo, listas na fonte miúda, as duas notas de volta, subtítulos em Playfair, redes sociais só com os ícones em linha, links de política em linha, fundo no papel (não branco puro) e a identificação da empresa com `[PREENCHER]` no CNPJ e no endereço (o CNPJ de mentirinha do protótipo não vai para o site) |
| Cabeçalho não fica fixo ao rolar a página | no protótipo a barra é `sticky` | o CSS geral do kit (v0.3.17) fixa o bloco do cabeçalho no topo (`.elementor-location-header`), faixa e barra juntas |
| Hero da home com a foto embaixo do texto (e duas colunas quebrando em outras páginas) | as colunas somavam 52% + 44% e, com o respiro de 40px, passavam de 100%: a linha quebrava e a foto caía | corrigido na v0.3.15 na geração: linha de colunas que somam ~100% nasce **sem quebra** (`nowrap`). Vale para hero, editorial, coleção, lookbook e produto |
| Menu sem a linha embaixo do item atual (página ativa) | menu em lista de ícones não tem como saber em que página a pessoa está; quem marca o item atual é o WordPress | na v0.3.15 o menu voltou a ser o **widget de menu do WordPress** (slug `menu-principal`), com a fonte Jost e o sublinhado do item ativo pelo CSS geral do kit (classe `iara-menu-nav`). Pré-requisito que voltou a valer: o menu **Menu Principal** precisa existir em Aparência > Menus com Início, Loja, Coleção, Sobre, Contato |
| Links rosas/magenta na Minha Conta (e no carrinho/checkout) | são os links que o WooCommerce desenha, com a cor de link do tema; não passam por nenhum widget nosso | corrigidos no CSS geral que viaja no kit (v0.3.15): navegação da conta sem marcador, links em Terracota Escuro, item atual sublinhado. Se ainda sobrar rosa, é a cor de link do tema falando mais alto: conferir Personalizar > cores do tema |
| Link do menu sem efeito ao passar o mouse (sem cor de hover nem sublinhado) | o widget de lista de ícones só tinha a cor normal pelas globais; o hover existia só no CSS separado, que nenhuma importação carregava | corrigido na v0.3.14 nas duas pontas: o widget ganhou a cor de hover pela global de destaque (`text_color_hover`) e o CSS geral, com as regras do link do menu, passou a viajar **dentro** do kit completo (chave `custom_css`) |
| Menu continua serifado e a sacola continua com caixa, mesmo com o JSON novo | a tipografia e o botão do carrinho são do tema/widgets Pro, e o JSON não vence essa briga sozinho | **v0.3.9, com autorização da cliente:** cole o conteúdo de `bloco-b/css/iara-cabecalho.css` em **Elementor > Configurações do site > CSS personalizado** (se a opção não existir, em Personalizar > CSS adicional). É o CSS do protótipo mirando nas classes `iara-*` do cabeçalho: menu em Jost 12px em linha, sacola sem caixa e sem valor, faixa e ícones conferidos |
| Marca voltou ao retângulo gigante "Logo." | o widget Logo do site está sem imagem definida | na v0.3.9 a marca é o **logotipo que a cliente subiu**: antes de importar, defina essa imagem como logo do site (Personalizar > Identidade do site, ou Elementor > Configurações do site > Logo do site). O CSS limita a altura a 54px, mas sem logo definido o placeholder volta |
| **Cabeçalho "completamente errado" de novo: imagem genérica no lugar da marca, menu serifado, sacola com caixa, e o CSS "não pegou"** | análise minuciosa da v0.3.10: três provas na captura. (1) A imagem de montanhas é o placeholder do widget Logo do site: o logotipo subido na mídia **não estava definido como logo do site**. (2) Menu serifado mesmo com CSS que força Jost com prioridade: esse CSS **não estava ativo na página** (não colado, não salvo ou cache). (3) A caixa da sacola é o botão padrão do widget de carrinho do WooCommerce. Causa comum: o cabeçalho dependia de widgets que o tema e o WooCommerce estilizam por conta própria | **correção estrutural na v0.3.10, sem depender de CSS nem de mídia:** saem Logo do site, Menu de navegação e Carrinho do WooCommerce. Ficam só widgets básicos com fonte/cor das globais: marca em **texto** (igual ao protótipo, que é texto), faixa e menu em **lista de ícones em linha** (pedido da cliente: lista de ícones em vez de elemento de texto), e busca/conta/desejos/sacola como **ícones** simples com link. O CSS vira reforço opcional (mesmo arquivo, atualizado). Quem quiser o logotipo em imagem troca os dois títulos pelo widget Logo do site no editor, DEPOIS de definir a imagem como logo do site |
| Menu com um **check (✓) na frente de cada item** e fontes serifadas em títulos de benefícios e cartões | causa raiz achada no código-fonte do Elementor (v0.3.11): (1) item de lista de ícones sem `selected_icon` definido ganha o ícone padrão do Elementor, que é o `fa fa-check`; (2) a tipografia global da lista de ícones se chama **`icon_typography`**, e a dos cartões é **`title_typography`/`description_typography`**. Com a chave errada ("typography", "typography_title"), o Elementor ignora a fonte global e o tema impõe a serifada dele | corrigido no gerador (ajuste automático em todos os arquivos) e **travado na conferência**: nenhum item nasce sem `selected_icon` (vazio quando não tem ícone) e nenhuma chave errada passa. Benefícios da home também igualados ao protótipo (rótulo em caixa alta, ícone 26px, fundo suave) e o "VER TUDO" das seções virou texto puro, sem o preenchimento marrom |
| Home e outras páginas sem imagem nenhuma | os widgets de imagem estavam com o endereço vazio ("escolher no editor") | na v0.3.10 eles já nascem apontando para as fotos do protótipo (endereço público do repositório), então a importação já mostra hero, categorias, ocasiões, editorial, coleção e capítulos do lookbook. O pacote `bloco-b/imagens/iara-costa-imagens.zip` (no kit) traz os 39 arquivos para subir na Mídia; depois de subir, quem quiser troca o endereço pela mídia, página a página. Produtos, posts e a foto do produto continuam vindo do WooCommerce/Gutenberg, não do template |
| Menu não aparece | o menu `principal` ainda não existe no site | criar em Aparência > Menus (Início, Loja, Coleção, Sobre, Contato) e conferir o slug |
| Ícones da direita apertados ou sumidos | com o "Logo." gigante, a linha estourava | some junto com a correção da marca; conferir também em tela estreita |
| Embaixo do cabeçalho aparece um rodapé genérico do tema | o rodapé do projeto ainda não foi importado ou está sem condição | importar o `02-rodape.json` e definir **Entire Site** no Theme Builder |

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
| `11-blog.json` | Diário | Arquivo de posts | vitrine dinâmica dos textos do Gutenberg |
| `12-post.json` | Artigo do diário | Post único | capa, título, texto do Gutenberg e "Continue lendo" |
| `13-busca.json` | Busca | Resultados de busca | campo de busca, resultados e saída para a loja |
| `14-404.json` | Página não encontrada | Página 404 | mensagem e os botões para loja, início e contato |
| `15-sobre.json` | Sobre a Iara Costa | Página | história, missão, ateliê e escolha das peças (textos [PROPOSTA]) |
| `16-contato.json` | Contato | Página | formulário, canais de atendimento e atalho do FAQ |
| `17-faq.json` | Perguntas frequentes | Página | perguntas por assunto e a faixa de ajuda |
| `18-guia-medidas.json` | Guia de medidas | Página | como medir, tabela [PREENCHER] e dúvidas de tamanho |
| `19-lookbook.json` | Coleção Terra & Linho | Página | editorial em três capítulos, com foto, texto e compra |
| `20-trocas.json` | Trocas e devoluções | Página | desistência, troca, defeito, solicitação e reembolso |
| `21-envio.json` | Envio e entrega | Página | prazos, frete grátis, rastreio e problemas de entrega |
| `22-privacidade.json` | Política de Privacidade | Página | esqueleto das 8 seções para o jurídico |
| `23-termos.json` | Termos de uso | Página | esqueleto das 8 seções para o jurídico |
| `24-cookies.json` | Política de Cookies | Página | esqueleto das 6 seções para o jurídico e o banner LGPD |

### 5.2 As páginas (próximas partes)

**O Bloco B está completo: os 24 arquivos foram entregues.** Cada página do
protótipo virou um arquivo, nos mesmos endereços do protótipo, para o site nascer
com os links certos:

| Parte | Arquivos | O que é |
|---|---|---|
| 1 | `01` e `02`, mais as globais | cabeçalho, rodapé, cores e fontes do site |
| 2 | `03` | página inicial |
| 3 | `04` e `05` | loja e página do produto |
| 4 | `06` a `10` | sacola, finalizar compra, pedido recebido, minha conta e desejos |
| 5 | `11` a `24` | diário, artigo, busca, 404, sobre, contato, perguntas, guia de medidas, coleção, trocas, envio e as três páginas legais |

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
2. Importar as cores e as fontes globais com o pacote da seção 3.0
   (`ajusta-ids.py` da seção 3.3 só no plano B) e conferir com o
   `blocob_confere.py`.
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

11. Importar o lote editorial e institucional (`11` a `24`), criar cada página
    no endereço da tabela 5.2 e deixar as legais como rascunho.
12. Conferir o site inteiro no celular e no computador: nenhuma página sem
    cabeçalho e rodapé, nenhum `[PREENCHER]` publicado.

Com os 24 arquivos no ar e conferidos, o Bloco B está fechado. O próximo bloco
é o Bloco C: o kit de instalação, os CSVs de produtos e posts e os guias de
segurança, SEO, testes, desempenho, e-mail e go-live.
