# Diário de Bordo - Iara Costa E-commerce

## [2026-10-21] - Segunda tentativa dos produtos: imagem e visibilidade (v0.3.27)

### O erro
Sem a coluna ID, os pais avançaram e bateram em dois pontos: a
imagem só com nome de arquivo ("Não é possível usar a imagem") e a
visibilidade vazia das variações ("Opção de visibilidade do
catálogo inválida").

### A correção
Visibilidade `visible` nas 56 variações e coluna de imagem fora da
importação: foto se anexa na Mídia, produto a produto, que é também
onde a foto real vai entrar de qualquer jeito.

### Lição de processo
Arquivo novo devia ter sido validado com UM produto antes do lote
de 68. Fica a regra: amostra primeiro, lote depois.

## [2026-10-21] - Importação de produtos falhou inteira; causa achada no registro (v0.3.26)

### O erro
Primeira importação dela: "Falha ao importar 68 produtos". O arquivo
estava íntegro (validado: colunas, órfãs, codificação), então pedi o
registro. Ele entregou tudo: "Não existe nenhum produto
correspondente para atualizar" nos pais.

### A causa (nossa)
A coluna `ID` vazia na frente do CSV. Para o importador do
WooCommerce, ID presente = pedido de atualização de produto
existente. Como nenhum existia, os 10 pais caíram e as 56 variações
foram atrás ("nova variação só para produto variável"). Lição
registrada no guia: nada de coluna ID em lote de produtos novos, e
nada de marcar "Atualizar produtos existentes".

### Correção
Coluna removida, conferências refeitas, versão nova. Ela reimporta
com o arquivo corrigido e me diz quantos entraram.

## [2026-10-20] - Texto integral em Sobre, Contato e Coleção (v0.3.25)

### Continuação autorizada
Fechar a última frente do pente-fino: as páginas escritas à mão no
gerador. Sobre virou `pagina_documento` com extração, Contato ganhou
a seção do mapa e a Coleção trocou o resumo pelo primeiro parágrafo
real de cada capítulo.

### O achado feio (e a correção)
Conferindo os títulos gerados, as páginas de texto da v0.3.24
traziam "Institucional" e "Sua sacola" como seções: o extrator lia
além do `</main>` e importava o rodapé da página como conteúdo.
Ninguém tinha importado ainda, então o estrago ficou no papel. Corte
no `</main>`, regeneração e teste novo contra vazamento.

### O que continua por verificar
- Importação e leitura das páginas no site dela. A inicial segue
  montada de widgets (produtos e posts dinâmicos); os depoimentos de
  exemplo do protótipo continuam fora de propósito, esperando os
  depoimentos reais.

## [2026-10-20] - Pente-fino e ajustes: responsivo e texto integral (v0.3.24)

### Pedido da cliente
Pente-fino em todos os JSON contra as páginas do template, a
pergunta sobre o CSS do HTML estar sendo injetado no Elementor, e
autorização para continuar ajustando.

### O que o pente-fino achou (PENTE-FINO.md)
O CSS do protótipo não viaja cru (as classes dele não existem no
Elementor); viaja o equivalente. Faltavam o responsivo (0 @media e 0
ajustes contra 74 blocos do protótipo) e o texto integral das
páginas (os JSON tinham resumos; as legais, ~11%).

### O que foi feito
Passada responsiva automática em todos os documentos, @media no CSS
embutido, e as páginas de texto e o FAQ passaram a ser gerados do
HTML aprovado do protótipo, com os links convertidos. A conferência
pegou os links `.html` que a extração trouxe e o mapa de conversão
foi completado. Tudo verde de novo, relatório atualizado com o
antes/depois.

### O que continua por verificar
- Conferência visual no celular de verdade (loja e produto são do
  WooCommerce) e a importação no site dela. Sobre, contato, coleção
  e inicial seguem com o texto do gerador; o integral está no
  pages-conteudo.md se ela quiser a troca completa depois.

## [2026-10-20] - CSS em todos os templates e pacote único (v0.3.23)

### Pedido da cliente
"Pode ajustar todos os jsons, ou seja todas as páginas, com os seus
css embutido para importar tudo, quero todas as páginas e se possível
já pronta."

### O que foi feito
- O ponto único de geração passou a gravar o `custom_css` em cada um
  dos 24 documentos (antes era caso especial de cabeçalho/rodapé).
- Pacote novo com os 24 JSON para importar tudo numa operação.
- Registrado no histórico o que "pronta" cobre e o que é dinâmico,
  para a expectativa ficar honesta: template não cria produto, página
  publicada nem menu; isso é dado do site.

### O que continua por verificar
- A importação no site dela e a aplicação dos templates de página
  (roteiro do guia), começando por reaplicar a página inicial.

## [2026-10-20] - Estados pelos controles dos widgets (v0.3.22)

### Relato da cliente
"Importei e mesma coisa." A importação avulsa não cria condição de
exibição (conferido no código do Elementor): o template novo entra
sem valer, e o site segue mostrando o antigo. Enquanto o estado do
menu depender de CSS nosso viajando junto, qualquer desencontro de
importação vira "não pegou".

### Análise
O desenho que nunca falha é o que o próprio widget gera dos seus
controles: ponteiro do menu com cor de hover e de ativo, e o botão da
sacola com fundo e borda controlados. Foi o que entrou, conferido
controle a controle no código dos dois widgets. O CSS embutido fica
de reforço, e o kit completo (que cria as condições) volta a ser o
caminho indicado, com a limpeza dos antigos antes.

### O que continua por verificar
- Apagar os cabeçalhos/rodapés antigos, importar o kit completo e
  conferir no Theme Builder um único cabeçalho com condição de site
  inteiro. Aí o hover se testa no site, não na promessa.

## [2026-10-20] - CSS dentro dos templates (v0.3.21)

### Relato da cliente
A captura do site dela com os dois JSON importados: menu sem hover e
sem a linha do ativo, sacola dentro de uma caixa com borda e o zero
dos desejos solto ao lado do coração. Era o retrato exato de "o CSS
não foi junto".

### Análise
Importar template avulso não traz o `custom_css` das configurações do
site, que é onde os estados moram. A correção estrutural é o CSS
viajar dentro do próprio documento (a configuração `custom_css` do
template, que o Elementor aplica onde o template é exibido, e
cabeçalho/rodapé aparecem em todas as páginas). De quebra, o seletor
da sacola estava no envoltório e não no botão; o código do widget
mostrou o elemento certo.

### O que continua por verificar
- Reimportar os dois templates (apagando as cópias anteriores) e
  passar o mouse no menu; clicar na sacola abre a gaveta lateral.

## [2026-10-20] - Cabeçalho e rodapé aprovados e fechados (v0.3.20)

### Relato da cliente
"O header e footer aprovado pode atualizar os 2 json igual o preview
sem nenhuma alteração, o que for dinâmico, aí atualizo."

### O que foi feito
- Nenhuma alteração de desenho: os dois JSON foram regenerados da
  mesma fonte que alimentou a prévia aprovada, e a entrega reúne os
  dois arquivos finais (zip próprio) mais o kit completo de sempre.
- Conferido o inventário de widgets dos dois arquivos: o que é
  dinâmico ficou dinâmico (menu do WordPress, Site Logo nos dois
  templates, Carrinho do Menu, contador TI, formulário), o resto é
  conteúdo fixo do protótipo.
- Versão 0.3.20 registrada; kits regenerados; conferências verdes.

### O que continua por verificar
- A importação no site da cliente: apagar as cópias antigas dos dois
  templates antes, para a condição não ficar apontando para cópia
  velha. Com o plugin TI desligado, o coração não renderiza (registrado
  no guia); a sacola abre a gaveta lateral do WooCommerce ao clicar.

## [2026-10-20] - Estados do link do menu e ícones leves (v0.3.19)

### Relato da cliente
A captura mostra o cabeçalho quase lá: faixa, marca, menu em caixa
alta com a linha no HOME. O que ela cobra agora é acabamento: "os
estados dos links do meu [menu], active e hover, verifique" e "os
ícones não estão iguais aos do template, o CSS está diferente".

### Análise (IMPLEMENTADO)
O ativo estava certo (linha clara, como no protótipo); o hover só
pintava a letra, sem a linha escura que o `.main-nav__link` aprovado
tem. Nos ícones, a diferença é de desenho da biblioteca: busca e
sacola só existem cheios no Font Awesome gratuito, e o protótipo foi
desenhado em traço fino. Sem trocar a fonte de ícones, o que dá para
igualar é tamanho, cor, respiro e ausência de caixa, e foi o que
entrou, no widget e no CSS do kit. O traço idêntico viraria SVG
próprio na Mídia, troca manual registrada no guia se ela quiser.

### O que continua por verificar
- Passar o mouse no menu (linha escura) e navegar (linha clara andando
  para o item da página). E incluir a Coleção no Menu Principal dela,
  que é item de WordPress, não de template.

## [2026-10-20] - Padrão de fonte embutido nos widgets (v0.3.18)

### Relato da cliente
Quatro capturas: o cabeçalho dela gigante e serifado contra o nosso
miúdo; o rodapé dela com títulos Playfair grandes contra o nosso
contido. Pedidos: ícones "mais clean", menu em maiúsculo e "acertar o
padrão da fonte já no nosso kit de configuração". Traduzindo o último:
ela não quer depender de importar fonte certa para a fonte sair certa.

### Análise (IMPLEMENTADO)
O padrão do widget de menu é a global Primary, Playfair 24 (li no
código dele): menu sem fonte declarada nasce exatamente como a captura
dela. E as fontes personalizadas do kit não estão mandando naquele
site, por importação ou por duplicata com condição antiga. Enquanto a
fonte depender de global personalizada, a briga continua. A saída
estrutural: declarar a fonte em cada widget, com os valores da nossa
tabela. Cor continua global porque cor estava funcionando (faixa
verde, Terracota dos botões).

### O que foi feito
- Conversor na geração: toda referência de tipografia global vira
  valores declarados no widget, com o prefixo certo (`icon_typography`,
  `title_typography` etc.). Vale para os 24 arquivos.
- Menu: Jost 12 caixa alta declarada no widget + cores pelas globais;
  a global `iara-menu` também virou caixa alta.
- Ícones das ações: 18px, cor suave, respiro de 22px.
- Guia registra a regra das duplicatas: apagar todas as cópias antes
  de importar, porque condição em cópia antiga é indistinguível de
  "a correção não pegou".

### O que continua por verificar
- Importar apagando as duplicatas e capturar header e rodapé. Se a
  fonte ainda assim vier do tema, o próximo suspeito é cache de CSS do
  Elementor (Ferramentas > regenerar CSS), que entra na conversa com
  evidência, não com chute.

## [2026-10-20] - Header e footer conferidos contra o protótipo (v0.3.17)

### Pedido da cliente
Retomada depois do merge do PR #10: "vamos começar hoje pelo header e
footer, verifique nosso template e pode migrar para atualizar os JSONs
do Elementor".

### O que foi feito (IMPLEMENTADO)
- Cabeçalho passado a limpo contra o parcial do protótipo: estava
  certo (faixa em lista de ícones, marca em texto, menu
  `menu-principal`, ícones). Ganhou o `sticky` do protótipo pelo CSS
  que viaja no kit.
- Rodapé comparado bloco a bloco com `tools/partials/footer.html`:
  sete diferenças corrigidas (títulos em rótulo, nota da newsletter de
  volta, linha conta/desejos/sacola, sociais só em ícones, subtítulos
  em Playfair, nota demonstrativa da segurança de volta, fundo no
  papel). Bônus de pente fino: o CNPJ fictício do protótipo virou
  `[PREENCHER]`, porque dado legal inventado não publica.
- Kit completo regenerado (33 containers no rodapé, 41 widgets) e as
  três conferências verdes.

### O que continua por verificar
- A importação do kit novo no staging e as capturas do cabeçalho fixo
  e do rodapé completo. Depois: o roteiro das páginas (reaplicar a
  home, criar Coleção/Guia/FAQ, aplicar Sobre e Contato), que ficou de
  ontem.

## [2026-10-19] - Menu aponta para o "Menu Principal" da cliente (v0.3.16)

### Pedido da cliente
"o menu em lista de ícones -> coloca o menu do wordpress que ja fiz,
chama Menu Principal". O widget já tinha voltado a ser o do WordPress
na v0.3.15; o que faltava era apontar para o menu dela.

### O que foi feito (IMPLEMENTADO)
Conferi no código do widget como ele identifica o menu: pelo slug. O
menu "Menu Principal" tem slug automático `menu-principal`, e o nosso
apontava para `principal`. Troquei o slug no gerador (uma linha, com o
motivo comentado), atualizei o guia onde ele citava o slug antigo e
registrei. Menu em lista de ícones, agora, só onde a lista é fixa por
desenho (faixa de recados, benefícios, links do rodapé).

### O que continua por verificar
- O menu aparecer com os itens dela e a linha andando no item ativo,
  na próxima importação do kit.

## [2026-10-19] - Hero, menu ativo e links do WooCommerce (v0.3.15)

### Relato da cliente
Links ok. Mas "o layout da home ainda continua errado" (foto do hero
embaixo do texto) e "o menu ativo, com a linha embaixo, não tem".
De quebra, a captura da Minha Conta mostra os links do WooCommerce em
rosa choque, que não são de template nenhum.

### Análise (IMPLEMENTADO)
Três causas separadas, nenhuma delas "o template inteiro errado":
o hero quebrava porque 52% + 44% + 40px de respiro estouram a linha com
`wrap` ligado (a mesma conta morava em mais quatro páginas); o item
ativo não existia porque texto fixo não sabe a página atual, e eu tinha
trocado o widget que sabe (o menu do WordPress) pela lista de ícones
para fugir da fonte do tema, briga que o CSS dentro do kit agora
resolve; e o rosa é a cor de link do tema nos desenhos do WooCommerce,
que só CSS alcança.

### O que foi feito
- `nowrap` automático em linha de colunas cheias, na geração dos 24.
- Menu volta ao widget do WordPress com slug `principal`; fonte, cores
  e sublinhado do ativo no CSS do kit. O pré-requisito do menu existir
  voltou para o guia em destaque, porque sem ele o widget não desenha
  nada (foi a captura do "cadê o menu" ao contrário).
- Seção WooCommerce no CSS do kit (conta, carrinho, checkout).

### O que continua por verificar
- A home lado a lado no staging e o sublinhado andando de item em item
  conforme a página. Se o menu vier vazio, é o menu `principal` que não
  existe no WordPress, e a captura confirma em um olhar.

## [2026-10-19] - O CSS do link do menu, verificado (v0.3.14)

### Pergunta da cliente
"Você chegou a verificar o menu? Não tem nem CSS do link." Direta e
certa. Eu tinha conferido fonte e cor do texto do menu, mas o link em
si (hover, sublinhado, respiro) só existia num arquivo CSS que nenhuma
importação carregava. Verificar era abrir o widget e o código dele:
o controle de hover da lista de ícones (`text_color_hover`) existia e
estava vazio nos nossos arquivos.

### O que foi feito (IMPLEMENTADO)
- Hover pela global de destaque em toda lista de ícones com link,
  direto na geração.
- A descoberta maior: o kit completo não levava CSS. Li o módulo
  custom-css do Pro e a chave é `custom_css` nas configurações do kit;
  o CSS geral agora viaja dentro do `site-settings.json` do kit
  completo, com a aba `settings-custom-css` declarada no manifesto.
  Importar o kit passa a ser, de fato, importar tudo.
- Regras do link do menu completadas no CSS (respiro, sublinhado,
  foco visível) e trava na conferência para o CSS não sair do kit.

### O que continua por verificar
- Passar o mouse no menu depois de importar o kit novo e ver o
  sublinhado. É o teste de dez segundos que fecha esta rodada.

## [2026-10-19] - Pente fino dos links: o site é subpasta (v0.3.13)

### Relato da cliente
"Olha, os links estão todos quebrados. O site é
https://oeemax.com.br/iaracosta/. Verifique, faça um pente fino novamente
em cada template, pois o site está quebrado ainda." A captura, aliás,
mostra o salto: cabeçalho igual ao protótipo (menu Jost, ícones, faixa),
hero com foto, botões e textos certos. O que quebrou foi a navegação.

### Causa raiz
Uma só, e era endereço: todos os links internos nasciam `/loja/`,
`/sobre/` (raiz do domínio), mas o WordPress mora em `/iaracosta/`.
Cada clique saía do site. Ninguém tinha me passado o endereço real até
hoje; com ele, a correção é central: uma constante `SITE_BASE` no
gerador, de onde nascem os 61 links internos dos 24 arquivos.

### O que foi feito (IMPLEMENTADO)
- `SITE_BASE` no gerador e todos os links refeitos; a busca virou `/?s=`
  (a página `/busca/` não existe; quem responde é o template de
  resultados).
- O pente fino virou conferência permanente (seção 4c do
  `blocob_confere.py`): link fora do endereço, link vazio, link dentro de
  texto e imagem sem foto reprovam a entrega. Rodei a contagem: 61 links
  internos no endereço certo, 0 na raiz.
- Tagline da marca com a fonte declarada no arquivo, já que a global não
  estava vencendo o tema nas capturas.
- Kit completo e kit do Bloco C regenerados: a importação continua sendo
  um arquivo só (e a rotina de apagar os templates antigos antes).

### O que continua por verificar
- Clicar nos links no site real. Template garante o endereço; a página
  de destino existir com o slug certo (loja, colecao, sobre, contato...)
  é o passo de criação de páginas do guia. Se algum destino der 404, é
  página faltando, não link errado, e a captura diz qual.

## [2026-10-19] - Kit completo de importação única (v0.3.12)

### Pedido da cliente
"Não tem como criar algo que possa apenas importar? Pois cada alteração
tenho que ficar fazendo isso." A frustração é legítima: foram seis
rodadas de "apague, reimporte, capture" no cabeçalho, e cada rodada
custava importar arquivo solto na mão. O formato certo para isso existe
no Elementor e a gente ainda não tinha usado para os templates: o Kit.

### O que foi feito (IMPLEMENTADO)
- `tools/blocob_gera_kit_completo.py` gera o `iara-costa-kit-completo.zip`
  no formato oficial do Kit (conferido no código-fonte do Elementor e no
  espelho público do Pro): manifesto 2.0 com a seção de templates,
  site-settings com as globais e 24 arquivos em `templates/<id>.json`.
- A parte delicada era a condição do Theme Builder: li o
  `get_export_summary()`/`import()` do documento de tema no Pro e as
  classes de condição. Sem `conditions` no manifesto, a importação de
  header/footer/archive/single quebra em PHP 8; com ela, o cabeçalho já
  nasce Entire Site. Loja, produto, blog, post, busca e 404 ganharam as
  condições correspondentes (`product_archive`, `singular/product`,
  `post_archive`, `singular/post`, `archive/search`,
  `singular/not_found404`).
- Conferência nova valida o kit inteiro contra os JSONs; guia ganhou a
  seção 2.9 (importação única como caminho principal) com o aviso de que
  kit cria cópias novas a cada importação, então a rotina de correção
  vira: apagar os templates Iara anteriores e importar o kit novo.
- De quebra, o "10 fontes" que tinha ficado no gerador do pacote de
  globais virou 11.

### O que continua por verificar
- A importação do kit no staging é o primeiro teste real deste formato
  com os nossos arquivos. O resultado (sucesso por runner ou a mensagem
  de erro) diz onde ajustar, se precisar: é um arquivo só para corrigir.

## [2026-10-19] - Causa raiz das fontes: chaves de tipografia por widget (v0.3.11)

### Pedido da cliente
"Analise novamente": menu com check na frente de cada item (e a caixa rosa
da seleção do editor na captura) e a home com serifadas onde o protótipo é
Jost. O "cade o menu?" era isso: o menu estava lá, disfarçado de lista de
checks.

### Análise (IMPLEMENTADO, com fonte conferida)
Baixei o código dos widgets no repositório do Elementor e li os controles:
o repetidor da lista de ícones tem `fas fa-check` como ícone padrão de
item sem ícone, e os grupos de tipografia têm nomes próprios por widget
(`icon_typography` na lista, `title_typography` nos cartões). O gerador
usava os nomes genéricos, o Elementor ignorava, e o tema mandava. Isso
explica também a tagline serifada das capturas anteriores melhor do que a
hipótese do kit não importado: onde a chave estava certa (títulos), a
fonte entrava; onde estava errada (listas e cartões), não.

### O que foi feito
- Ajuste por tipo de widget na geração dos 24 arquivos (renomear chaves e
  zerar o ícone de item sem ícone), trava nova na conferência, benefícios
  da home igualados ao CSS do protótipo e "VER TUDO" sem preenchimento.
- Fica a lição registrada: chave de controle de widget Pro continua não
  verificável aqui (o Pro é fechado), mas a dos widgets gratuitos agora é
  conferida na fonte, não de memória.

### O que continua por verificar
- A mesma reimportação de sempre. Com a chave certa, a fonte global entra
  mesmo se o tema tentar impor a dele, porque quem manda no seletor é o
  grupo de tipografia do widget.

## [2026-10-19] - Cabeçalho sem depender de tema, CSS ou mídia; imagens nos templates (v0.3.10)

### Pedido da cliente
"Está completamente errado, o CSS não pegou, está completamente diferente
da versão do template. Veja minuciosamente o que está ocorrendo." E mais:
a home sem imagens, "chegar 100% no HTML das páginas", "na importação já
quero que importe tudo" e "sempre usar lista de ícones em vez de elemento
texto ou HTML".

### Análise minuciosa (IMPLEMENTADO o diagnóstico)
A captura traz três provas: a imagem de montanhas é o placeholder do Logo
do site (a cliente subiu o arquivo na mídia, mas não o definiu como logo
do site); o menu serifado prova que o CSS não estava ativo na página
(com a declaração forçada, a serifada do tema não apareceria); e a caixa
da sacola é o botão padrão do Carrinho do WooCommerce. O fio comum das
seis capturas: o cabeçalho dependia de widgets que o tema/WooCommerce
estilizam e de passos manuais fora do arquivo. Remendo em cima de remendo
não resolve isso; a estrutura é que tinha que mudar.

### O que foi feito
- Cabeçalho refeito só com widgets básicos de estilo global: marca em
  texto (o protótipo é texto), faixa e menu em lista de ícones em linha,
  quatro ícones de ação com link. Saiu a dependência de menu do WordPress,
  de logo definido e de CSS colado. O CSS continua no pacote como reforço
  opcional, reescrito para as classes novas.
- Imagens: nenhum widget de imagem vazio nos 24 arquivos. Hero,
  categorias, ocasiões, editorial, coleção e lookbook apontam para as
  fotos do protótipo no repositório público, e o zip com os 39 arquivos
  entrou no kit para a mídia local. Limite honesto, registrado para a
  cliente: JSON de template não embute arquivo de imagem; ou aponta para
  endereço (o que fizemos) ou a imagem é escolhida na mídia depois.
- "100% do HTML": o que o template controla (estrutura, fonte, cor,
  imagem, espaçamento) agora nasce do arquivo. O que é do WordPress
  (produtos, posts, foto do produto, menu do rodapé transacional) continua
  dinâmico por natureza, como no Bloco B aprovado.

### O que continua por verificar
- Reimportar globais e cabeçalho e comparar com a imagem 2. Se a marca em
  texto e o menu em lista entrarem certos, a mesma receita (só widget
  básico) vira o padrão para qualquer ajuste futuro.

## [2026-10-19] - CSS do protótipo no geral do Elementor e logotipo (v0.3.9)

### Pedido da cliente
A faixa entrou igual, mas o menu continua serifado e a sacola com caixa.
"Veja o CSS do template e aplique, pode colocar o CSS no arquivo geral do
Elementor" e "pode colocar meu logotipo que já subi na mídia". Duas
autorizações novas: CSS geral (a regra antiga era não usar CSS livre) e a
marca volta a ser imagem, agora que existe logotipo.

### O que foi feito (IMPLEMENTADO)
- `bloco-b/css/iara-cabecalho.css` a partir do header.css aprovado: menu
  Jost 12px em linha (é a declaração que vence a fonte do tema), sacola sem
  caixa e sem subtotal, contador em bolha, faixa, barra e ícones. Entra no
  kit do Bloco C (33 + guias).
- Cabeçalho com classes `iara-*` nos seis pontos e 3 containers. Marca:
  widget Logo do site com o logotipo subido, 190px de largura e altura
  segurada pelo CSS.
- Guia 4.6 com as duas linhas novas, incluindo a condição do logo definido
  como logo do site antes de importar.

### O que continua por verificar
- Colar o CSS, definir o logo, reimportar e capturar. Se algum seletor do
  widget Pro tiver nome diferente na versão instalada, o ajuste é no CSS
  (um arquivo só), não mais nos 24 JSONs. Fica registrado também: o menu da
  captura tinha 4 itens (sem Coleção), o que é do menu no WordPress, não
  do template.

## [2026-10-19] - Todos os JSONs alinhados ao protótipo, com menos containers (v0.3.8)

### Pedido da cliente
Duas imagens: a 1 é o cabeçalho importado no WordPress, a 2 é o cabeçalho
do protótipo que criamos. "Está diferente, preciso que ajuste todos os
JSONs criados para seguir igual às telas do nosso template criado" e
"trabalhe com o menor número de containers possível".

### Leitura das imagens (o que estava torto)
Menu empilhado e serifado (fonte do tema, sem largura na barra), caixa de
busca aberta onde o protótipo só tem a lupa, sacola com caixa e "R$ 0,00"
onde o protótipo só tem o ícone com contador, conta e desejos cheios e
terracota em vez do traço fino, tagline serifada (global não aplicada) e a
faixa com ícones onde o protótipo é texto em caixa alta com pontos. A
decisão desta rodada segue a imagem 2: onde a faixa de ícones da v0.3.6
brigava com o protótipo, o protótipo venceu.

### O que foi feito (IMPLEMENTADO)
- Cabeçalho refeito nesses pontos (ver histórico de versões), incluindo a
  fonte global nova "Texto da faixa" (11 fontes no total) e o pacote
  `iara-costa-globais.zip` regenerado.
- Achatamento genérico no gerador: container que só embrulha um elemento e
  não tem fundo, borda, sombra, respiro nem largura em caixa sai da árvore,
  e a largura dele passa para o elemento de dentro. 216 para 176 containers
  nos 24 arquivos, sem mudar o desenho. O rodapé ficou com 33 porque ali
  quase todo container desenha algo (quadros de pagamento com borda, colunas
  com respiro, faixas com fio).
- Guia: quatro linhas novas na tabela de diagnóstico (4.6), incluindo o
  aviso de ordem (globais ANTES do cabeçalho).

### O que continua por verificar
- A reimportação no staging na ordem certa e a captura lado a lado com o
  protótipo. Se o menu continuar serifado mesmo com as globais importadas,
  a causa é a tipografia do widget de menu no tema, e o ajuste é no editor
  (guia, ajuste 4.3), não no arquivo.

## [2026-10-19] - Cabeçalho com menos containers e espaçamento revisto (v0.3.7)

### Pedido da cliente
"tente usar menos container, pode ajustar isso também no header e veja
novamente o espaçamento do logo, menu e outros." É o mesmo espírito do
round em que ela pediu o header "mais clean" no protótipo: estrutura
enxuta, respiro definido.

### O que foi feito (IMPLEMENTADO)
- **7 para 4 containers** no `01-cabecalho.json`: saíram o container raiz
  (a faixa e a barra viraram os dois blocos de topo do arquivo), o par
  barra/linha (fundidos num container só, que carrega fundo, fio inferior e
  a linha) e o embrulho "Navegação principal" (o widget de menu vai direto
  na barra). Sobraram faixa, barra, marca (que empilha nome e assinatura) e
  ações (que agrupa os quatro ícones).
- **Espaçamento com número, não com sorte**: marca `_flex_basis` 24%, ações
  24% com `flex-end`, menu no meio distribuído pelo `space-between` da
  barra com `flex_gap` de 24px, 18px entre os ícones das ações e 14px de
  padding vertical na barra (era 16px numa camada que nem existia sozinha).
- Guia: linha nova na tabela de diagnóstico (4.6). Kit remontado.

### O que continua por verificar
- A reimportação no staging com a captura da barra completa: marca, menu
  central, ícones e a faixa em linha. É essa tela que aprova ou devolve o
  cabeçalho, como nos rounds do protótipo.

## [2026-10-19] - Faixa verde como lista de ícones em linha (v0.3.6)

### Pedido da cliente
"no topbar de verde os icones tem que ser uma lista de icones inline". A
faixa de aviso era um widget de texto com os três recados e separadores; a
cliente quer o widget de lista de ícones em linha.

### O que foi feito (IMPLEMENTADO)
- `01-cabecalho.json`: a faixa verde agora é um `icon-list` com
  `view: 'inline'` (o controle de layout do próprio widget, conferido em
  `includes/widgets/icon-list.php`: `traditional` ou `inline`), itens com
  `_id` próprio, ícone Font Awesome em cada recado (caminhão, folha e
  globo), espaçamento de 18px e cor de texto e de ícone na global
  `iara-faixa-texto`.
- Guia: a linha nova entrou na tabela de diagnóstico da seção 4.6.
- Kit do Bloco C remontado com o cabeçalho novo.

### O que continua por verificar
- A reimportação no staging (apagar o cabeçalho antigo antes), junto com o
  teste da v0.3.5: marca em texto, menu `principal` criado e a captura da
  barra completa.

## [2026-10-19] - Correção do cabeçalho pela primeira importação real (v0.3.5)

### O que aconteceu
A cliente importou o cabeçalho e mandou a captura: "importei o cabecalho e
ficou ruim, nada a ver com nosso template". Ela tinha razão. Na tela: a
faixa verde entrou (as cores globais importadas funcionaram), mas com os
links em rosa; um retângulo gigante "Logo." ocupava a barra; o menu não
aparecia; e embaixo havia o rodapé genérico do tema.

### Diagnóstico
- **"Logo." gigante**: o template usava o widget Site Logo e, sem logo
  definido no Personalizar, o Elementor desenha o placeholder em tamanho
  cheio. Defeito de desenho meu: a marca aprovada no protótipo é
  **tipográfica**, nunca foi uma imagem.
- **Links rosas**: os widgets de texto com link não definiam a cor do link,
  que é um controle próprio do widget (`link_color` em
  `includes/widgets/text-editor.php`, conferido no código-fonte), e o tema
  pintou com o padrão dele.
- **Menu ausente**: o widget aponta para o menu de slug `principal`, que
  ainda não existe no site. Não é defeito do arquivo, mas o guia tratava
  isso como detalhe e virou item de diagnóstico.
- **Rodapé genérico**: é o rodapé do tema enquanto o `02-rodape.json` não é
  importado com condição Entire Site.

### Correções (IMPLEMENTADO)
- Marca em texto no `01-cabecalho.json`: "IARA COSTA" na fonte de título
  com link para a home e "Moda & Acessórios" na fonte da assinatura, em
  coluna, como no rodapé.
- `link_color` igual à cor do texto na faixa do cabeçalho e no ajudante
  `paragrafo()` sempre que o texto tiver link (vale para todos os
  templates, não só o cabeçalho).
- Guia: seção 2.2 sem a exigência de logo em imagem; ajuste do editor
  atualizado; **seção 4.6 nova** com a tabela de diagnóstico (sintoma, causa
  e correção), incluindo apagar o template antigo e reimportar.
- Kit do Bloco C remontado com o cabeçalho novo.

### O que continua por verificar
- A reimportação no staging: apagar o template antigo, importar o novo,
  criar o menu `principal` e conferir a barra completa (marca, menu e os
  quatro ícones). A captura dessa tela fecha o diagnóstico.

## [2026-10-19] - Correção: pacote para importar cores e fontes (v0.3.4)

### O que aconteceu
Na primeira importação tentada pela cliente, o `cores-e-fontes.json` foi para
o importador de Templates e o Elementor respondeu **"Tipo de modelo
inválido"**. Diagnóstico: o arquivo nunca foi um template, é a referência de
valores das globais; faltava entregar o arquivo importável de configurações.
A cliente pediu então para **importar** as configurações em vez de criar cor
por cor na tela.

### O que foi feito (IMPLEMENTADO)
- **`bloco-b/globais/iara-costa-globais.zip`**: pacote no formato Kit do
  Elementor, com `manifest.json` (`version: "2.0"`, o FORMAT_VERSION atual) e
  `site-settings.json` na raiz, contendo só cores, fontes, largura de
  conteúdo, espaçamento e fundo do corpo. Nome do site e logo ficam fora de
  propósito.
- **`tools/blocob_gera_kit_globais.py`**: gera o pacote da mesma fonte única
  das cores e fontes (`site_settings()` do gerador do Bloco B).
- **Formato reconferido no código-fonte do Elementor**:
  `app/modules/import-export/processes/export.php` (o arquivo entra na raiz
  do zip como `site-settings.json`), `module.php` (FORMAT_VERSION 2.0) e
  `runners/import/site-settings.php` (a importação cria kit novo, mistura
  com o antigo com `array_replace_recursive` e anexa `custom_colors` e
  `custom_typography` **mantendo o `_id`**). É essa última parte que faz os
  templates nascerem certos sem o `ajusta-ids.py`.
- **Guia corrigido**: seção 3.0 nova com o passo a passo (exportar antes por
  segurança, importar marcando Configurações do site, conferir as 15 cores e
  10 fontes), o erro "Tipo de modelo inválido" explicado onde ele acontece e
  a seção 3.3 rebaixada a plano B. `bloco-b/LEIA-ME.txt` com o aviso no nome
  de cada arquivo.
- **Kit e conferências**: o pacote entrou no `iara-costa-kit.zip` (40
  arquivos); `blocob_confere.py` passou a conferir o zip (arquivos,
  `version` e ids iguais aos das globais) e `blococ_confere.py` ajustou a
  contagem esperada.

### Decisões tomadas
- **Recomendado importar em staging novo, sem cores próprias**: a importação
  acrescenta sem apagar; num site que já tem cores, sobra duplicada para
  limpar. Está escrito no guia.
- **O `ajusta-ids.py` não foi aposentado**: é o plano B se a versão do
  Elementor do staging se comportar diferente do código-fonte conferido.

### O que foi verificado aqui
- Estrutura do zip (2 arquivos, manifest 2.0, os 11 ids de cor e os 6 de
  fonte personalizadas iguais aos dos templates).
- `tools/blocob_confere.py`, `tools/blococ_confere.py` e `tools/check.py`
  verdes.

### O que não foi verificado
- **A importação de verdade**: continua sendo o primeiro teste real, feito
  pela equipe no staging. Se a tela de importação pedir algo diferente do
  guia, o caso volta para cá com a captura e o guia é corrigido.

## [2026-10-19] - Bloco C, parte 4 (final): testes, desempenho, e-mail, nota fiscal e go-live (v0.3.3)

### Pedido da cliente
"pode continuar", depois dos guias de instalação, segurança e SEO (PR #9).
Fechei o Bloco C com os cinco guias restantes.

### O que foi feito (IMPLEMENTADO como instrução)
- **`GUIA-TESTES.md`**: roteiro por área (navegação, loja, produto, conta,
  formulários, acessibilidade manual) com o teste central em 8 passos:
  variação na sacola, BEMVINDO10 aplicado e reaplicado para registrar o
  comportamento real, frete abaixo e acima de R$ 299, pedido como visitante
  por meio de teste sem pagamento real, pedido recebido, e-mail, Minha conta
  e **apagar o pedido de teste**.
- **`GUIA-DESEMPENHO.md`**: medir no celular, 3 vezes, mediana; antes e
  depois de cada ajuste; a tabela de registro com LCP, CLS e INP e as metas
  do dossiê. Sem número medido, o relatório diz "não medido".
- **`GUIA-EMAIL-SMTP.md`**: endereços da loja a decidir, SPF, DKIM e DMARC
  em etapas, envio autenticado (plugin novo só com aprovação) e os e-mails
  do WooCommerce conferidos um por um no pedido de teste.
- **`GUIA-NFE.md`**: nota fiscal como decisão da empresa com o contador
  antes do go-live, com dados [PREENCHER], homologação e os dois caminhos
  de emissão comparados. Sem contador, sem go-live.
- **`GUIA-GO-LIVE.md`**: a virada em ordem (congelar e copiar, conteúdo e
  loja, virada técnica com a retirada do `noindex`, primeiras 24 horas e os
  30 dias), fechando com a avaliação de plugin próprio.
- **Kit remontado** com os oito guias: 39 arquivos.

### Decisões tomadas
- **Bloco C completo no papel, nada executado**: instalar, importar, testar
  e medir são da equipe em staging e produção. Os guias deixam o registro
  pronto para provar o que foi feito.
- **Plugin próprio avaliado e dispensado**: WooCommerce, Elementor Pro,
  Yoast e os dois gratuitos aprovados cobrem o desenho. A avaliação ficou
  escrita no fim do guia de go-live, para a decisão não virar lenda oral.
- **Nota fiscal trava o go-live**: vender sem emissão resolvida não é uma
  opção que este projeto assine.

### O que foi verificado aqui
- Referências entre os guias e o kit; `tools/blococ_confere.py`,
  `tools/blocob_confere.py` e `tools/check.py` verdes.

### O que não foi verificado
- **Absolutamente nada de execução**: nenhuma instalação, importação, teste,
  medição de desempenho, envio de e-mail ou emissão. É tudo trabalho do
  staging em diante, com os guias como roteiro.

### O que continua em aberto (AGUARDA INFORMAÇÃO)
- A execução inteira: staging, importações, plugins, catálogo real, textos
  aprovados, jurídico, contador, testes registrados e a virada.
- Depois disso, o projeto entra na fase de acompanhamento de 30 dias.

## [2026-10-19] - Bloco C, parte 3: guias de instalação, segurança e SEO (v0.3.2)

### Pedido da cliente
"pode contunuar" (sic), depois do merge do PR #8. Segui com os guias do
Bloco C, começando por instalação, segurança e SEO.

### O que foi feito (IMPLEMENTADO como instrução)
- **`bloco-c/guias/GUIA-INSTALACAO.md`**: a montagem do zero em staging:
  ambiente, tema e plugins na ordem com teste a cada um, Site Settings com
  `ajusta-ids.py`, os 24 templates e suas condições, WooCommerce (Brasil,
  BRL, páginas da loja, visitante, estoque, BEMVINDO10 com a limitação real
  registrada, Mercado Pago sem pagamento real, frete e CSV) e conteúdo.
- **`bloco-c/guias/GUIA-SEGURANCA.md`**: acessos individuais e duas etapas,
  atualização com teste em staging, backup com restauração testada de
  verdade, HTTPS e servidor, LGPD e rotina depois do go-live.
- **`bloco-c/guias/GUIA-SEO-YOAST.md`**: base do Yoast, o que conferir em
  páginas, produtos e posts, funil fora do sitemap com `noindex`, dados
  estruturados e a medição no Search Console sem promessa de posição.
- **Kit remontado** com os três guias (34 arquivos) e a conferência do kit
  ajustada para contar os guias da pasta.

### Decisões tomadas
- **Nenhum item de guia nasce marcado como feito**: é lista para a equipe
  executar e registrar com data e responsável.
- **Sem plugin novo nestes guias**: backup e duas etapas aparecem como
  recurso da hospedagem ou plugin aprovado, porque plugin pede aprovação.
- O limite real do cupom de primeira compra (por e-mail e conta) está
  escrito no guia de instalação, para ninguém prometer o que a ferramenta
  não faz.

### O que foi verificado aqui
- Referências entre guias, kit e repositório; `tools/blococ_confere.py`,
  `tools/blocob_confere.py` e `tools/check.py` verdes.

### O que não foi verificado
- **Nenhuma instalação, configuração, restauração de backup ou medição.**
  Tudo depende do staging, que segue sem versões informadas.

### O que continua em aberto (AGUARDA INFORMAÇÃO)
- Guias restantes: testes, desempenho, e-mail/SMTP, nota fiscal e go-live.
- Todo o resto: staging, plugins aprovados, catálogo real, textos e jurídico.

## [2026-10-19] - Bloco C, parte 2: conteúdo das páginas e o kit (v0.3.1)

### Pedido da cliente
"pode continuar", depois dos CSVs (parte 1, PR #8 aberto). Entreguei o
conteúdo das páginas em Markdown e o kit de instalação.

### O que foi feito (IMPLEMENTADO)
- **`bloco-c/pages-conteudo.md`**: as 10 páginas institucionais e legais
  (sobre, contato, perguntas, guia de medidas, coleção, trocas, envio,
  privacidade, termos e cookies) com o texto extraído por script das páginas
  aprovadas do protótipo, cada uma com endereço, template correspondente e
  situação. 36 marcadores mantidos, nenhum travessão.
- **`bloco-c/iara-costa-kit.zip`**: 31 arquivos (os 24 templates e as
  globais do Bloco B, o guia de importação, os dois CSVs, o conteúdo das
  páginas e um LEIA-ME com a ordem de uso), gerado com data e ordem fixas.
- **`tools/blococ_gera_conteudo.py`** (extrator HTML para Markdown) e
  **`tools/blococ_monta_kit.py`** (monta o zip e imprime a soma de cada
  arquivo). O `blococ_confere.py` agora confere também o conteúdo e o kit.

### Decisões tomadas
- **Extrair, não reescrever**: texto aprovado se move por script, para
  ninguém "melhorar" uma política ou uma promessa sem perceber.
- **Legal continua rascunho**: privacidade, termos e cookies trazem o texto
  de estrutura do protótipo, mas a publicação exige o jurídico.
- **Kit com soma de verificação**: quem recebe confere arquivo por arquivo.

### O que foi verificado aqui
- `python3 tools/blococ_confere.py`: CSVs, conteúdo e kit, "tudo certo".
- `python3 tools/blocob_confere.py` e `tools/check.py`: blocos anteriores
  intactos.

### O que não foi verificado
- **Nenhuma importação, instalação ou abertura do kit em WordPress real.**
- A leitura do jurídico sobre as três páginas legais.
- Nenhuma medida de desempenho.

### O que continua em aberto (AGUARDA INFORMAÇÃO)
- Revisão e aprovação de textos: empresa (institucionais) e jurídico (legais).
- Próximas partes do Bloco C: os guias de instalação, segurança, SEO,
  testes, desempenho, e-mail/SMTP, go-live e nota fiscal. Plugin próprio só
  se for indispensável; nada até aqui mostrou que seja.

## [2026-10-19] - Bloco C, parte 1: produtos e posts em CSV (v0.3.0)

### Registro anterior
O PR #7 foi mergeado em 19/10/2026 (merge `ec200d7`) e o Bloco B ficou
fechado na main na v0.2.5, com os 24 templates. Registro sem mudanca de versao,
como nos merges anteriores.

### Pedido da cliente
"pode continuar". Comecei o Bloco C pelos arquivos que alimentam a loja e o
diario.

### O que foi feito (IMPLEMENTADO)
- **`bloco-c/produtos.csv`**: os 12 produtos de exemplo do prototipo
  (`tools/produtos.json`) no formato do importador do WooCommerce: 10
  variaveis com 56 variacoes (1 linha por combinacao de cor e tamanho, ligada
  ao pai pelo SKU), 2 simples, atributos Cor e Tamanho globais, os 4 destaques
  da home marcados, tudo com Published = 0.
- **`bloco-c/posts.csv`**: 8 posts em rascunho com blocos do Gutenberg. Os
  titulos e resumos sao os cartoes aprovados do blog; o corpo e rascunho de
  trabalho a partir deles, com o fecho lembrando a revisao e o autor como
  `[PREENCHER: quem assina]`.
- **`bloco-c/IMPORTACAO-CSV.md`** e **`bloco-c/LEIA-ME.txt`**: como importar,
  o que conferir e o que estes arquivos nao resolvem.
- **`tools/blococ_gera_csv.py`** e **`tools/blococ_confere.py`**: gerador
  deterministico e conferencia (SKU unico, pai de variacao, combinacoes sem
  repeticao, preco, rascunho e pares de blocos).

### Decisoes tomadas
- **Tudo em rascunho, sem excecao**: e catalogo e texto de exemplo.
- **Peso, dimensoes e quantidade de estoque vazios**: inventar esses numeros
  quebraria o calculo de frete e venderia o que nao existe. Entram com o
  cadastro real.
- **Sem plugin importador de posts**: o WordPress nao importa CSV de posts
  nativamente; o caminho honesto para 8 posts e o manual, e plugin novo so
  com aprovacao.
- A sandalia ficou com tamanho "Unico", como esta no prototipo: registrei no
  guia para conferir a numeracao real de calcados antes de publicar.

### O que foi verificado aqui
- `python3 tools/blococ_confere.py`: produtos e posts, "resultado: tudo certo".
- `python3 tools/blocob_confere.py`: os 24 templates seguem conferidos.
- `python3 tools/check.py`: o prototipo do Bloco A segue intacto.

### O que nao foi verificado
- **Nenhuma importacao** (sem WordPress, painel ou banco).
- Se o importador do staging aceita o mapeamento de colunas sem ajuste.
- Nenhuma medida de desempenho.

### O que continua em aberto (AGUARDA INFORMACAO)
- Catalogo real: descricoes, composicao, fotos, peso, dimensoes, estoque e
  numeracao de calcados.
- Quem assina os posts e a revisao dos 8 textos.
- Proximas partes do Bloco C: `pages-conteudo.md`, o kit de instalacao e os
  guias (instalacao, seguranca, SEO, testes, desempenho, e-mail, go-live e
  nota fiscal). Plugin proprio (`plugin-iara-custom.zip`) so se for
  indispensavel, e nada ate aqui mostrou que seja.

## [2026-10-16] - Bloco B, parte 5 (final): editorial, institucional e legal (v0.2.5)

### Pedido da cliente
"pode continuar", depois da aprovação dos plugins de desejos e de swatches.
Fechei o Bloco B com o último lote.

### O que foi feito (IMPLEMENTADO)
- **`11-blog.json`** (arquivo de posts) e **`12-post.json`** (post único):
  vitrine dinâmica e artigo com título, capa, conteúdo do Gutenberg e
  "Continue lendo". Post nunca é escrito no Elementor.
- **`13-busca.json`** (resultados de busca) e **`14-404.json`**: campo de
  busca, resultados, estado sem resultado com saída para a loja; 404 com
  botões para loja, início e contato.
- **`15-sobre.json`**, **`16-contato.json`** (formulário com nome, e-mail,
  assunto e mensagem, mais os canais), **`17-faq.json`** (cinco grupos de
  perguntas e a faixa de ajuda), **`18-guia-medidas.json`** (como medir,
  tabela marcada `[PREENCHER]` e dúvidas) e **`19-lookbook.json`** (coleção
  em três capítulos com foto, texto e botão de compra).
- **`20-trocas.json`** e **`21-envio.json`** com as seções aprovadas no
  protótipo, incluindo a marca `[CONFIRMAR COM A EMPRESA]` nas peças de
  bazar e íntimas.
- **`22-privacidade.json`**, **`23-termos.json`** e **`24-cookies.json`**:
  esqueleto das seções com `[PREENCHER: texto jurídico aprovado]` e o aviso
  de rascunho para o jurídico.
- **Documentos**: guia e `LEIA-ME.txt` fechados com os 24 arquivos, a ordem
  de trabalho completa e o aviso de que o próximo bloco é o Bloco C.

### Decisões tomadas
- **Os 24 arquivos ficaram como contados**, sem juntar as páginas legais:
  a alternativa de 21 era juntar as três políticas em um modelo só, e a
  contagem página por página venceu. Registro para a equipe: se um dia
  quiserem enxugar, o caminho continua descrito no guia.
- **Nada de texto inventado para preencher página**: onde o dado é da
  empresa ou do jurídico, o arquivo carrega a marca, não um chute.

### O que foi verificado aqui
- `python3 tools/blocob_confere.py`: **24 arquivos conferidos, resultado:
  tudo certo** (15 cores, 10 fontes).
- `python3 tools/blocob_gera.py` regenera os 24 arquivos e as globais sem
  mudar nada além do esperado.
- `python3 tools/check.py`: o protótipo do Bloco A segue intacto.

### O que não foi verificado
- **Nenhuma importação e nenhuma renderização** de nenhum dos 24 arquivos
  (sem WordPress, painel ou banco). Esta é a maior pendência do Bloco B e só
  o staging resolve.
- Compatibilidade dos widgets Pro com a versão licenciada do staging.
- Desempenho, acessibilidade em site real e pedido de teste: Bloco C e
  staging.

### O que continua em aberto (AGUARDA INFORMAÇÃO)
- Importação em staging, um arquivo por vez, com a conferência do guia.
- Versões do staging, fotos reais, depoimentos reais, tabela de medidas,
  textos [PROPOSTA] da Sobre, textos jurídicos, e-mail dos formulários e
  redes sociais.
- Instalação e teste dos dois plugins aprovados (TI Wishlist e Variation
  Swatches), um por vez, medindo o peso.

## [2026-10-16] - Decisão: plugins de desejos e de swatches aprovados (v0.2.4)

### Pedido da cliente
"lista de desejos e swatches de cor/tamanho, qual plugin instalar?" Apresentei
a comparação das opções atuais do repositório oficial do WordPress e a cliente
aprovou as duas indicações na versão gratuita.

### Decisão (APROVADO pela cliente)
- **TI WooCommerce Wishlist** para a lista de desejos: 100 mil instalações
  ativas ou mais e nota 4.7 no WordPress.org. A versão gratuita traz uma lista
  por cliente, lista para visitante e página própria; listas múltiplas e
  analytics ficam no Premium, que esta loja não precisa agora.
- **Variation Swatches for WooCommerce** (GetWooPlugins) para cor e tamanho
  em botões: 300 mil instalações ativas ou mais e nota 4.8. A versão gratuita
  troca o seletor padrão por cor, imagem e botão, e trata a variação esgotada
  até 30 variações por produto; o catálogo previsto (4 tamanhos nas cores da
  peça) fica bem abaixo disso. Swatches na grade da loja são do Pro.
- A alternativa pesada (YITH) ficou de fora pelo custo anual e pelo peso
  relatado em comparativos; o WooCommerce novo até traz atributo visual
  nativo, mas só em tema de blocos, e o tema deste projeto é o Hello
  Elementor.

### O que mudou nos arquivos
- `10-desejos.json`: o aviso `[A DEFINIR]` virou `[CONFIGURAR NO EDITOR]` com
  o nome do plugin aprovado e o endereço da página da lista.
- `GUIA-IMPORTACAO.md`: seção 4.5 nova com a decisão, os limites da versão
  gratuita e as regras de instalação; linhas de desejos e de variações
  atualizadas nas seções 2.1 e 4.3.
- `PENDENCIAS.md`: as pendências de aprovação viraram tarefa de instalar e
  testar no staging, um por vez, medindo o peso antes e depois.

### O que não foi feito
- **Nada foi instalado** (sem acesso ao WordPress): quem instala é a equipe.
- **Nenhum teste de compatibilidade** com o staging: versões do WordPress e do
  WooCommerce do ambiente seguem `[CONFERIR]`.
- Versão Pro dos dois: só com falta real no teste e nova aprovação.

## [2026-10-16] - Bloco B, parte 4: o funil de compra (v0.2.3)

### Pedido da cliente
"Pode continuar", depois da loja e da página do produto (parte 3, PR #7).
Segui para o funil: sacola, finalizar compra, pedido recebido, minha conta e
desejos.

### O que foi feito (IMPLEMENTADO)
- **`bloco-b/json/06-carrinho.json`** e **`07-checkout.json`**: título, avisos do
  WooCommerce e os widgets clássicos Cart e Checkout do Elementor Pro.
- **`bloco-b/json/08-pedido-recebido.json`**: resumo dinâmico do pedido
  (Purchase Summary) e os botões "Acompanhar meus pedidos" e "Continuar
  comprando".
- **`bloco-b/json/09-conta.json`**: widget My Account, com pedidos, endereços e
  dados nas telas nativas do WooCommerce.
- **`bloco-b/json/10-desejos.json`**: título, aviso `[A DEFINIR]` da pendência
  do plugin e botão para a loja.
- **`tools/blocob_gera.py`**: ajudante `pagina_compra()` para as páginas que são
  um widget do WooCommerce com título e nota.
- **Documentos**: ajustes do funil no guia (endereços das telas no
  WooCommerce, compra como visitante, cupom visível, noindex nas três páginas
  do funil), tabelas e ordem de trabalho.

### Decisões tomadas
- **Clássico, não blocos**: a aceitação do dossiê pede carrinho e checkout
  clássicos, então os widgets são os clássicos do Elementor Pro.
- **Desejos sem publicar**: sem plugin aprovado, a página é um aviso honesto.
  Publicar uma lista vazia quebrada seria pior.
- **O que é ajuste de painel ficou no guia**, não no arquivo: endereços das
  telas, compra como visitante, cupom BEMVINDO10 com limitação de primeira
  compra documentada, e noindex de sacola, checkout e conta fora do sitemap.

### O que foi verificado aqui
- `python3 tools/blocob_confere.py`: 10 templates, "resultado: tudo certo".
- `python3 tools/check.py`: o protótipo segue em "tudo certo".

### O que não foi verificado
- **Nenhuma importação, renderização ou pedido de teste** (sem WordPress).
- **Pedido de teste com BEMVINDO10 e transferência** é da equipe no staging,
  sem pagamento real, e depois o pedido é apagado (aceitação do dossiê).
- **E-mails transacionais** (remetente, SPF, DKIM, DMARC) são do Bloco C.

### O que continua em aberto (AGUARDA INFORMAÇÃO)
- Plugin de lista de desejos e plugin de swatches, os dois com aprovação prévia.
- Caminho dos filtros da loja (seção 4.4 do guia).
- Todo o resto das partes anteriores.

## [2026-10-16] - Bloco B, parte 3: loja e página do produto (v0.2.2)

### Pedido da cliente
"continue", depois da entrega da home (parte 2, PR #7 aberto). Segui a ordem
combinada: loja e página da peça, onde o WooCommerce entra de verdade.

### O que foi feito (IMPLEMENTADO)
- **`bloco-b/json/04-loja.json`** (arquivo de produtos): cabeçalho com trilha,
  título e atalho do guia de medidas; coluna de filtros com categorias
  dinâmicas e os três grupos marcados para configurar (preço, cor e tamanho);
  grade dinâmica de 9 peças com as 5 ordenações do protótipo e paginação; e a
  faixa verde de ajuda antes do rodapé. 10 containers e 19 widgets.
- **`bloco-b/json/05-produto.json`** (produto único): trilha, galeria nativa,
  nome, avaliação, preço, parcela, descrição curta, variações e botão de
  compra, estoque, atalho do guia de medidas, código e categorias, as três
  garantias da compra, abas do produto, relacionados e sugestões, e a faixa
  "Ficou em dúvida no tamanho?". 8 containers e 21 widgets.
- **Documentos**: guia com os ajustes de loja e produto (4.3), a decisão dos
  filtros (4.4 nova), a tabela do que está pronto e a ordem de trabalho;
  `LEIA-ME.txt` na parte 3.

### Decisões tomadas
- **Tudo que muda com o catálogo é dinâmico**: nome, preço, foto, estoque,
  variação, avaliação, relacionado. Nenhum produto, preço ou nota foi escrito
  nos arquivos.
- **Filtros de preço, cor e tamanho ficaram como decisão aberta.** O Elementor
  Pro não tem filtro por atributo no canvas; fingir que tem seria entregar um
  arquivo que não funciona. O guia traz os três caminhos com custo de cada um,
  e a escolha é da equipe, porque um deles pede plugin (aprovação prévia).
- **Swatches dependem de plugin aprovado.** Sem ele, variação aparece no
  seletor padrão do WooCommerce, que funciona, só não tem a bolinha de cor.

### O que foi verificado aqui
- `python3 tools/blocob_confere.py`: 5 templates, 111 containers, 145 widgets,
  15 cores, 10 fontes, "resultado: tudo certo".
- `python3 tools/check.py`: o protótipo segue em "tudo certo".

### O que não foi verificado
- **Nenhuma importação e nenhuma renderização** (sem WordPress, painel ou banco).
- **Se a versão do Elementor Pro do staging traz todos os widgets de produto**
  usados aqui (`[CONFERIR]` na instalação).
- Nenhuma medida de desempenho.

### O que continua em aberto (AGUARDA INFORMAÇÃO)
- **Caminho dos filtros da loja** (blocos, plugin ou links por atributo).
- **Plugin de swatches** para cor e tamanho em botões, se a equipe quiser o
  comportamento do protótipo.
- Tabela de medidas real por peça, fotos e descrições do catálogo.
- Todo o resto: versões do staging, fotos e depoimentos da home, newsletter,
  redes sociais, plugin de desejos e o número final de arquivos.

## [2026-10-16] - Bloco B, parte 2: página inicial (v0.2.1)

### Pedido da cliente
"Começar pela home". A parte 1 do Bloco B (cores, fontes, cabeçalho e rodapé)
entrou na `main` pelo PR #6, e a cliente escolheu a página inicial antes da loja.

### O que foi feito (IMPLEMENTADO)
- **`bloco-b/json/03-home.json`** (tipo página): as dez seções da home aprovada no
  protótipo, na mesma ordem: hero, faixa de benefícios, categorias, produtos em
  destaque, ocasiões, editorial do ateliê, coleção, depoimentos, posts recentes e
  perguntas frequentes em faixa verde. 53 containers e 59 widgets.
- **`tools/blocob_gera.py`**: ganhou a fábrica `home()` e os ajudantes de página
  (`rotulo`, `titulo_secao`, `paragrafo`, `botao`, `cabecalho_secao`,
  `cartao_imagem`).
- **`bloco-b/GUIA-IMPORTACAO.md`**: a home entrou na lista do que está pronto
  (seção 5.1), saiu da lista de páginas futuras (5.2) e ganhou ajustes de editor
  na seção 4.3; a ordem de trabalho (seção 8) agora inclui importar a home.
- **`bloco-b/LEIA-ME.txt`**: atualizado para a parte 2.

### Decisões tomadas
- **Produtos em destaque e posts recentes são blocos dinâmicos** (widgets
  `woocommerce-products` e `posts`), configurados no editor. Escrever produto à
  mão na home criaria preço e estoque falsos assim que o catálogo mudasse.
- **Legenda do hero abaixo da foto**, e não sobreposta: sobrepor sem CSS livre
  não é confiável no Elementor. Fica como ajuste opcional no editor.
- **Depoimentos marcados como exemplo** no próprio título do widget, com cidade
  em `[PREENCHER]`: são os textos de exemplo do protótipo (decisão D5 da fase E0)
  e só podem ser publicados quando forem reais.
- Cartões de categoria e de ocasião apontam todos para `/loja/` por enquanto,
  porque as categorias reais do WooCommerce ainda não existem; o guia manda
  apontar cada um para a sua categoria depois do cadastro.

### O que foi verificado aqui
- `python3 tools/blocob_gera.py`: gera os 4 arquivos.
- `python3 tools/blocob_confere.py`: 3 templates, 93 containers, 105 widgets,
  15 cores, 10 fontes, "resultado: tudo certo". Nenhum travessão no arquivo gerado.

### O que não foi verificado
- **Nenhuma importação e nenhuma renderização** (sem WordPress, painel ou banco).
- **Os nomes de ajuste dos widgets Pro** (`woocommerce-products`, `posts`,
  `testimonial`) seguem a documentação; nome diferente é ignorado na importação
  e escolhido no editor.
- Nenhuma medida de desempenho.

### O que continua em aberto (AGUARDA INFORMAÇÃO)
- Fotos reais da home (hero, editorial, coleção, categorias e ocasiões).
- Depoimentos reais, com autorização de uso.
- Categorias reais do WooCommerce, para apontar os cartões.
- Todo o resto da lista da parte 1: versões do staging, newsletter, redes
  sociais, plugin de desejos e o número final de arquivos.

## [2026-10-16] - Bloco B, parte 1: cores, fontes, cabeçalho e rodapé (v0.2.0)

### Pedido da cliente
"Pode continuar com o Bloco B". O Bloco A estava fechado e congelado na v0.1.20,
com a conferência do navegador pendente, e o próximo entregável do escopo eram os
templates do Elementor.

### Como esta parte foi construída
Antes de escrever qualquer arquivo, o formato foi conferido **no código-fonte do
Elementor** (o projeto tem acesso ao GitHub), e não em um site:

| O que foi conferido | Onde | O que valeu |
|---|---|---|
| Envelope do arquivo de importação | `includes/template-library/sources/local.php` | `content`, `page_settings`, `version`, `title`, `type` |
| Versão do formato | `includes/db.php` | `version: "0.4"` |
| Referência de cor e de fonte | `core/files/css/base.php` | `globals/colors?id=...` e `globals/typography?id=...` |
| Configurações de container | `includes/elements/container.php` | `content_width`, `boxed_width`, `flex_*`, `_flex_basis` |
| Forma real dos ajustes | `tests/elements-regression/tests/templates/*.json` | arquivos de teste do próprio plugin, com o formato verdadeiro |
| Criação de global na importação | `includes/template-library/manager.php` | cor global **não** é criada sozinha: por isso existe o script de ids |

### O que foi feito (IMPLEMENTADO)
- **`bloco-b/globais/cores-e-fontes.json`**: as 15 cores (4 do sistema mais 11
  personalizadas) e as 10 fontes (4 do sistema mais 6 personalizadas), todas com
  nome, valor e uso. Cada valor saiu do protótipo: nada foi inventado.
- **`bloco-b/json/01-cabecalho.json`** (tipo `header`): faixa verde do topo com os
  três recados, marca, menu principal e os quatro ícones (busca, conta, desejos,
  sacola). 7 containers e 7 widgets.
- **`bloco-b/json/02-rodape.json`** (tipo `footer`): newsletter, quatro colunas
  (marca, institucional, categorias, atendimento), faixa de segurança com quatro
  itens, formas de pagamento, selos e a base com copyright, CNPJ e endereço.
  33 containers e 39 widgets.
- **`bloco-b/GUIA-IMPORTACAO.md`**: o documento que a equipe segue, com a ordem de
  trabalho, as tabelas de cor e de fonte, o passo a passo da importação, as
  condições de exibição no Theme Builder, o que ajustar no editor, a tabela das 22
  páginas e a lista do que não foi verificado.
- **`bloco-b/LEIA-ME.txt`**: resumo de uma página.
- **`tools/blocob_gera.py`**: gera os JSONs a partir de definições legíveis (o
  mesmo princípio do `tools/build.py`), com id de elemento determinístico.
- **`tools/blocob_confere.py`**: confere o envelope, os tipos, os widgets
  permitidos (nada de HTML, shortcode ou widgets Atomics), o nome dos containers,
  a unicidade dos ids e se toda referência de cor e de fonte existe nas globais.
- **`tools/ajusta-ids.py`**: lê o arquivo de configurações exportado do site, casa
  cor por cor pelo título e reescreve as referências nos templates. Testado com um
  arquivo de exemplo com ids sorteados: as 11 cores e as 6 fontes foram casadas e
  os dois templates reescritos.

### Decisões tomadas
- **Container nomeado em tudo.** Todo container leva `_title`, o nome que aparece
  no navegador de estrutura, para quem abrir o template entender a montagem.
- **Ajustes de widget Pro ficam para o editor.** O Elementor Pro não é aberto, e
  um nome de ajuste desconhecido é ignorado na importação em vez de quebrar. O
  guia lista, widget por widget, o que escolher no editor (menu, logo, busca,
  sacola, newsletter, redes sociais).
- **Número de arquivos:** a conta página por página dá 24 arquivos (cabeçalho,
  rodapé e as 22 páginas), e não os 21 do dossiê. Não juntei páginas diferentes em
  um arquivo só; a alternativa (uma página de documento para as três políticas)
  ficou registrada no guia, à espera da palavra da equipe.
- **A versão sobe para 0.2.0** no começo do bloco. As partes seguintes seguem a
  série 0.2.x, como combinado no plano do histórico.

### O que foi verificado aqui
- `python3 tools/blocob_gera.py`: gera os três arquivos.
- `python3 tools/blocob_confere.py`: 2 templates, 15 cores, 10 fontes,
  "resultado: tudo certo".
- `python3 tools/ajusta-ids.py --simular`: 11 cores e 6 fontes casadas por título.
- `python3 tools/check.py` e `tools/pente-fino.py`: as 22 páginas do protótipo
  continuam em "tudo certo"; `node tools/test.js` segue com 1.043 verificações sem
  falha. O Bloco B não tocou em nada do Bloco A.

### O que não foi verificado
- **Nenhuma importação.** Sem acesso ao WordPress, ao painel ou ao banco de dados.
- **Nenhuma renderização** do que o Elementor desenha depois de importar.
- **Versões do staging** (WordPress, PHP, Elementor, Elementor Pro, WooCommerce)
  seguem por informar: é o primeiro item do guia.
- **Nenhuma medida de desempenho**, que é do Bloco C, com site montado.

### O que continua em aberto (AGUARDA INFORMAÇÃO)
- A conferência da cliente no navegador do protótipo: acordeão do FAQ, formulário
  de contato e seletor de cor da página de produto.
- Destino do formulário da newsletter e endereços das redes sociais.
- O número final de arquivos (24 ou 21, juntando as páginas legais).
- Plugin de lista de desejos: sem aprovação, a página de desejos fica para depois.
- As 78 pendências de conteúdo e de decisão listadas em `PENDENCIAS.md`.

## [2026-10-16] - Bloco A fechado e congelado (v0.1.20)

### Pedido da cliente
"Em relação ao template vamos finalizar". Na abertura da rodada, a cliente
escolheu fechar o Bloco A **como ele está**, com as pendências de conteúdo
registradas, e criar a **pasta congelada da versão 0.1.20**, mantendo a
`template-v0.1.18/` intacta.

### O que foi feito (IMPLEMENTADO)
- **Pasta `template-v0.1.20/`** na raiz: cópia integral do protótipo (75
  arquivos, 6,2 MB), com `LEIA-ME.txt` próprio explicando o que é a pasta, o que
  tem dentro, como abrir e onde fica a versão mais nova. Conferida com `diff -r`
  contra `seu-projeto/`: idêntica, fora o `LEIA-ME.txt`.
- **`PENDENCIAS.md`** novo na raiz: as 78 marcações que existem dentro das 22
  páginas, reunidas por assunto (conteúdo que só a empresa pode escrever,
  decisões de negócio e operação, confirmações pontuais, textos propostos e
  conferências de instalação), com a coluna de onde cada uma aparece. Fecha com
  a ordem sugerida para resolver: primeiro conteúdo e decisões, depois as
  conferências de instalação.
- **`README.md` da raiz** atualizado: o Bloco A aparece como fechado na versão
  0.1.20, a tabela de organização ganhou a pasta nova e o `PENDENCIAS.md`, o
  exemplo de servidor local aponta para a pasta congelada, o intervalo de
  etiquetas vai até `v0.1.20` e a contagem de verificações passou de 997 para
  1.043.

### Conferências desta rodada
- `seu-projeto/` contra a etiqueta `v0.1.20` (`git diff --stat`): nenhuma
  diferença. É exatamente o conteúdo auditado e taggeado que foi congelado.
- `template-v0.1.20/` contra `seu-projeto/` (`diff -r`): idênticos, fora o
  `LEIA-ME.txt` da pasta.
- `build.py` e `check.py`: 22 páginas geradas e "tudo certo".
- `node tools/test.js`: 1.043 verificações, nenhuma falha.
- `pente-fino.py`: as 12 seções em "nenhum".
- Contagem das marcações por tipo, feita por script sobre os 22 arquivos:
  9 `[PREENCHER]`, 22 `[A DEFINIR]`, 2 `[CONFIRMAR COM A EMPRESA]`, 4
  `[PROPOSTA]` e 41 `[CONFERIR]`, 78 no total.

### Decisões tomadas
- **Registro sem mudança de versão:** o fechamento não altera nenhum arquivo do
  protótipo, então a versão continua 0.1.20 e a pasta congelada leva esse número.
- **A `template-v0.1.18/` fica guardada**, mantendo as duas pastas: abre-se mão
  de ter uma cópia só para preservar o que foi aprovado em cada momento.
- **As pendências ganharam documento próprio** em vez de ficarem apenas dentro
  das páginas: quem for escrever o conteúdo ou contratar as ferramentas trabalha
  por ele, sem precisar caçar marcador no HTML.
- **Os títulos de página não mudam nesta rodada:** qualquer ajuste de texto de
  conteúdo entra na próxima versão, quando as informações chegarem.

### O que continua em aberto (AGUARDA INFORMAÇÃO)
- Conferência da cliente no navegador: acordeão do FAQ, formulário de contato e
  seletor de cor da página de produto (pendência trazida da v0.1.19).
- As 78 pendências de `PENDENCIAS.md`, que passa a ser o documento de referência
  para conteúdo, decisões e conferências.
- Contraste dos ornamentos (`--iara-index` 3,17:1 e estrela da avaliação
  4,46:1): segue como estava, à espera de decisão.

## [2026-10-16] - PR #4 mergeado na main (registro)

### O que aconteceu
- O **PR #4** (branch de trabalho -> `main`) foi **mergeado** em 16/10/2026, às
  16h37 (horário de Brasília), por Matheus Costa (`mdiascosta`).
- **Commit de merge: `20112f2`.** Entraram os dois commits da v0.1.20: as 22
  descrições de busca reescritas e os cinco alvos de toque ampliados, mais a
  subida de versão de 0.1.19 para 0.1.20.
- A `main` ficou com o `VERSION` em 0.1.20 e a etiqueta `v0.1.20` aponta para o
  mesmo conteúdo que entrou; o histórico de etiquetas vai de `v0.1.0` a `v0.1.20`.
- Antes do merge, o protótipo foi liberado para a cliente abrir no navegador pela
  prévia do ambiente de trabalho.

### Decisões tomadas
- **Registro sem mudança de versão**, igual aos merges anteriores: é anotação de
  documentação sobre algo que já estava entregue.

## [2026-10-16] - Segundo pente fino: descrições de busca e alvos de toque (v0.1.20)

### Como esta rodada funcionou
A v0.1.19 procurou o que estava **quebrado** no navegador. Esta rodada procurou o
que estava **difícil de usar**: o texto que aparece no resultado do Google e o
tamanho do que se clica e se toca. As 22 páginas foram abertas em Chromium sem
interface (390, 768 e 1440 pixels de largura) e cada elemento clicável foi
medido pelo próprio navegador, com o critério 2.5.8 da WCAG 2.2 (versão AA) como
régua: 24 por 24 pixels no mínimo. Também foi feita nova varredura de conteúdo
sem JavaScript, estrutura de títulos, ordem de foco e movimento reduzido.

### O que a medição mostrou

**Descrições de busca.** Onze das 22 páginas tinham descrição com menos de 60
caracteres, a menor delas com 37. O Google mostra duas ou três linhas embaixo do
título: com texto curto, ele completa com pedaços aleatórios da página. As 22
foram reescritas à mão, entre 111 e 149 caracteres, cada uma descrevendo o que
existe de verdade naquela página.

**Alvos de toque.** Cinco elementos ficavam abaixo dos 24 pixels de altura:

| O que | Antes | Agora |
|---|---|---|
| Botões de menos e mais da quantidade | 44 x 23 px | 44 x 44 px |
| Links das colunas do rodapé | 21 px | 31 px |
| Links da faixa de texto miúdo do rodapé | 13 px | 24 px |
| Convite "Adicionar à sacola" no cartão | 109 x 14 px | 24 px |
| Links da faixa de aviso no topo | 141 x 13 px | ~29 px, com a faixa intacta (84px) |

O conserto dos links do rodapé veio por espaço interno e não por altura fixa, o
que mantém o desenho das colunas. O da faixa de aviso usou uma camada invisível
por cima do texto: a área de toque cresce, o desenho não.

**O que ficou como estava, com motivo registrado.** Os links que vivem dentro de
uma frase ou de um título (nome do produto no cartão, "Guia de medidas", nota da
newsletter) medem só a caixa do texto. A WCAG 2.2 abre exceção exatamente para
esse caso, chamado de texto em linha: aumentar a área mudaria a quebra de linha e
o desenho do parágrafo. As caixas de seleção do checkout e da conta, de 20 por 20
pixels, ficam dentro do rótulo, e o rótulo inteiro é a área de toque.

### O que mais foi conferido e não achou problema
- Sem JavaScript: as 22 páginas continuam com conteúdo e navegação.
- Estrutura: um único H1 por página, sem pulo de nível, `lang` correto, um `main`,
  sem id repetido. O único caso de dois `header` na página do artigo é o bloco de
  abertura do texto, que é legítimo.
- Foco visível: 25 paradas de teclado conferidas em 7 páginas, todas visíveis.
- Movimento reduzido: só transições de duração 0,00001s, sem animação perceptível.
- Busca: pela lupa, com resultado, sem resultado, por categoria e por cor, além
  do termo gigante (1.000 caracteres) que não estoura a largura.
- Filtros da loja: os quatro grupos respondem e a contagem da faixa confere.

### Decisões tomadas
- Manter a exceção da norma para links em linha, em vez de forçar área maior e
  mexer no desenho do texto.
- Consertar os alvos de toque sem alterar a altura da faixa de aviso nem do
  cabeçalho (conferido: 84px e 71px, iguais a antes).
- Nenhuma cor, texto de marca ou informação nova foi inventada nesta rodada.

### Verificação automática
`node tools/test.js` passou de 1.032 para **1.043 verificações, nenhuma falha**,
com a seção 26 nova cobrindo os cinco alvos de toque e os limites de tamanho das
descrições. `python3 tools/check.py` e o pente fino de HTML e CSS seguem em
"tudo certo" nas 22 páginas.

### O que continua em aberto (AGUARDA INFORMAÇÃO)
- Conferência da cliente no navegador: acordeão do FAQ, formulário de contato e
  seletor de cor da página de produto (pendências trazidas da v0.1.19).
- Contraste dos pontos decorativos (`--iara-index` 3,17:1 e estrela da avaliação
  4,46:1) segue como estava, por serem ícones e ornamentos com texto ao lado.
- Composição exata por peça, tabela de medidas real, história da marca,
  analytics, e a confirmação de "Outono · Inverno 2026" e "Terra & Linho".
- Combinar se as próximas versões ganham pasta congelada a cada fechamento.

## [2026-10-16] - PR #3 mergeado na main (registro)

### O que aconteceu
- O **PR #3** (branch de trabalho -> `main`) foi **mergeado** em 16/10/2026, às
  15h47 (horário de Brasília), por Matheus Costa (`mdiascosta`).
- **Commit de merge: `fd71101`.** Entraram os dois commits da v0.1.19: os sete
  consertos do pente fino no navegador (largura no celular, balão do WhatsApp,
  acordeão, formulário de contato, cor do produto, botões da lista de desejos e
  contraste) e a subida de versão de 0.1.18 para 0.1.19.
- A `main` está com o `VERSION` em 0.1.19, com o `contato.js` novo dentro e com
  as etiquetas `v0.1.0` a `v0.1.19`. A `v0.1.19` aponta para `906d81d`, o mesmo
  conteúdo que entrou na `main`.
- O trabalho seguinte começa em uma branch nova a partir do commit de merge.

### Decisões tomadas
- **Registro sem mudança de versão:** anotação de documentação sobre algo que já
  estava entregue. A versão continua 0.1.19 até o template mudar de novo.

### O que continua em aberto (AGUARDA INFORMAÇÃO)
- Conferência da cliente no navegador: acordeão do FAQ, envio vazio no formulário
  de contato e o seletor de cor da página de produto.
- "Tingimento natural" (casca de cebola e eucalipto), "costura em pequenos lotes"
  e "fornecedores certificados" seguem fora do site, aguardando confirmação.
- Composição exata por peça, tabela de medidas real e história da marca.
- Combinar se as próximas versões ganham pasta congelada a cada fechamento.

## [2026-10-16] - Pente fino no navegador de verdade (v0.1.19)

### Como esta rodada foi diferente
Até aqui, tudo era conferido lendo o código: o `test.js` usa jsdom, que não
desenha a página, e por isso não enxerga estouro de largura, sobreposição de
elementos, contraste nem clique que não faz nada. Nesta rodada o protótipo foi
aberto em um navegador de verdade (Chromium sem interface, instalado aqui no
ambiente) em três larguras (390, 768 e 1440 pixels), com medição de todas as 22
páginas, teste de teclado, de contraste e de cada interação.

### Os sete problemas encontrados e consertados (IMPLEMENTADO)
1. **Marcadores de pendência estouravam a tela no celular.** Os textos
   `[PREENCHER: ...]` são longos e tinham `white-space: nowrap`. Em 390px a
   página de Sobre ficava com 1.057px de largura: rolava de lado. Agora quebram
   linha. Atingia seis páginas.
2. **Tabela com rolagem empurrava a coluna na Conta e no artigo.** A grade
   deixava a tabela ditar a largura, e a página estourava para 641px e 451px.
   Conserto de uma linha em cada grade (`min-width: 0`).
3. **O balão do WhatsApp cobria o valor no Pix do checkout**, o botão de criar
   conta e o botão de calcular frete no celular. Agora ele entra depois de 160px
   de rolagem, e o resumo que gruda no topo reserva 96px para ele. Sem
   JavaScript, o balão aparece desde o início, como antes.
4. **O acordeão do FAQ, do Envio e do Guia de Medidas não abria:** as páginas
   têm acordeão mas não carregavam o script. O da home funcionava, o que
   escondia o problema.
5. **O formulário de contato não respondia nada.** Clicar em "Enviar mensagem"
   com campos vazios não mostrava aviso nenhum. Criei o `contato.js` seguindo o
   padrão de erro que já existia no checkout: aviso embaixo do campo, ligado ao
   campo para leitor de tela e foco no primeiro problema.
6. **A página de produto mostrava a cor errada:** a peça é o Vestido Midi
   Sálvia, mas o seletor abria com "Terracota" e oferecia "Off-white" e
   "Preto", cores que não existem no catálogo. Corrigido para Sálvia e as duas
   inventadas saíram do CSS.
7. **Os botões da lista de desejos não faziam nada.** Agora "Adicionar à
   sacola" abre a sacola e "Remover" tira a peça e atualiza o contador.

### Contraste
O rótulo de seção em 11px estava em 4,27:1, abaixo do mínimo de 4,5:1 da WCAG
2.2 AA. O tom foi ajustado e agora dá 4,92:1 no papel. Os outros pontos que a
varredura apontou são decorativos (pontos separadores e numeral de capítulo) ou
têm texto equivalente ao lado (a estrela da avaliação): ficaram como estão e o
motivo está no histórico.

### Como os consertos ficam protegidos
A seção 25 do `test.js` tem 24 verificações novas, uma para cada conserto. Se
alguém desfizer um deles sem perceber, o teste acusa.

### Verificações
- 22 páginas geradas sem erro e conferidas.
- 1.032 verificações automáticas, zero falhas.
- Pente fino de HTML, CSS e JavaScript com as 12 seções zeradas.
- Varredura no navegador: 22 páginas × 3 larguras, nenhum estouro de largura,
  nenhuma imagem quebrada, nenhuma imagem sem descrição e nenhum erro de script.

### O que continua em aberto (AGUARDA INFORMAÇÃO)
- Conferência da cliente no navegador, que é o próximo passo combinado.
- "Tingimento natural" (casca de cebola e eucalipto), "costura em pequenos lotes"
  e "fornecedores certificados" seguem fora do site, aguardando confirmação.
- Composição exata por peça, tabela de medidas real e história da marca.

## [2026-10-16] - PR #2 mergeado na main (registro)

### O que aconteceu
- O **PR #2** (branch de trabalho -> `main`) foi **mergeado** em 16/10/2026, às
  15h18 (horário de Brasília), por Matheus Costa (`mdiascosta`).
- **Commit de merge: `c45ec5a`.** Entraram 57 commits, da v0.1.1 até a v0.1.18:
  o super layout, a loja com paginação de 9 e as cinco ordenações, a coleção em
  capítulos, o hero quadrado e a pasta congelada `template-v0.1.18/`.
- A `main` agora tem a versão em desenvolvimento (`seu-projeto/`), a cópia
  congelada (`template-v0.1.18/`), o zip de referência da cliente
  (`template_.zip`), as ferramentas (`tools/`) e os três documentos (README,
  HISTORICO-DE-VERSOES e este diário), com o `VERSION` em 0.1.18.
- **As etiquetas seguem intactas**, de `v0.1.0` a `v0.1.18`. A `v0.1.18` aponta
  para `24baa31`, o mesmo conteúdo que entrou na `main`.
- O trabalho seguinte começa em uma **branch nova, a partir do commit de merge**,
  como manda o fluxo: a branch anterior ficou para trás, já mergeada. Nada do que
  veio antes se perde.

### Decisões tomadas
- **Registro sem mudança de versão:** esta é uma anotação de documentação sobre
  algo que já estava entregue, e a regra combinada é subir a versão quando o
  template muda. A versão continua 0.1.18.

### O que continua em aberto (AGUARDA INFORMAÇÃO)
- Combinar se as próximas versões ganham pasta congelada a cada fechamento ou se
  a pasta é renomeada, mantendo só a mais recente.
- "Tingimento natural" (casca de cebola e eucalipto), "costura em pequenos lotes"
  e "fornecedores certificados" seguem fora do site, aguardando confirmação.
- Composição exata por peça, tabela de medidas real e história da marca.

## [2026-10-16] - Template congelado em pasta com o número da versão (v0.1.18)

### Pedido da cliente
"certo pode commitar tudo agora e coloque em uma pasta com o numero da versao do
template". Tudo já estava commitado (a v0.1.18 fechou com os commits `100035a` e
`abc64ca`), então a rodada foi de organização: o template passou a ter uma pasta
congelada com o número da versão.

### O que foi feito (IMPLEMENTADO)
- **Pasta `template-v0.1.18/`** na raiz, com a cópia integral do protótipo: 22
  páginas HTML, os quatro arquivos de CSS, os cinco de JavaScript, as fontes, as
  39 imagens, o README do protótipo e a spec de imagens (73 arquivos, 6,2 MB).
  Conferido com `diff -r`: a cópia é idêntica a `seu-projeto/`, fora o
  `LEIA-ME.txt` da própria pasta.
- **`LEIA-ME.txt` dentro da pasta**, dizendo o que ela é (cópia congelada da
  versão 0.1.18, não recebe mais mudanças), listando o que tem dentro, como abrir
  e onde fica a versão em desenvolvimento.
- **`README.md` da raiz** reescrito: não era mais só o nome do repositório. Agora
  explica a organização (versão em desenvolvimento em `seu-projeto/`, versões
  fechadas nas pastas com número, ferramentas em `tools/`), como ver o site, como
  rodar as verificações e os avisos de modo manual.
- **A etiqueta `v0.1.18` foi reapontada** para incluir esta organização, para que
  versão, pasta e etiqueta digam a mesma coisa. O conteúdo do template não mudou
  nada com isso: a v0.1.18 continua sendo o hero quadrado.
- **Verificações:** as 22 páginas geradas sem erro, 997 verificações automáticas
  sem falha e o pente fino com as 12 seções zeradas. Nada disso olha para a pasta
  nova: as ferramentas trabalham só em `seu-projeto/`, então a pasta congelada
  não interfere no build.

### Decisões tomadas
- **Sem subir a versão:** esta rodada não mexeu no template, só na organização, e
  a regra da cliente é que a versão sobe quando o template muda. Por isso o
  número da pasta é 0.1.18, o mesmo da versão que ela acabou de aprovar.
- **Cópia completa, e não só as páginas:** a pasta precisa funcionar sozinha, com
  as imagens dentro, para poder ser aberta e enviada a outra pessoa sem quebrar.
- **As versões anteriores não ganharam pastas** (seriam dezessete cópias de 6 MB).
  Elas continuam guardadas nas etiquetas do Git (`v0.1.0` até `v0.1.18`) e
  descritas no histórico. Se alguma precisar virar pasta, é rápido.

### O que continua em aberto (AGUARDA INFORMAÇÃO)
- Combinar se as próximas versões ganham pasta nova a cada fechamento (como
  agora) ou se a pasta é renomeada, mantendo só a mais recente.
- "Tingimento natural" (casca de cebola e eucalipto), "costura em pequenos lotes"
  e "fornecedores certificados" seguem fora do site, aguardando confirmação.
- Composição exata por peça, tabela de medidas real e história da marca.

## [2026-10-16] - Foto do hero quadrada (v0.1.18)

### Pedido da cliente
"Pode reduzir a imagem para nao esticar muito deixe quadrada ne fica melhor veja
ai para nao ficar quebrado". Depois de ver a foto inteira (v0.1.17), o hero
ficou alto demais em tela grande, porque a foto é 9:16. A cliente pediu para
reduzir e deixar quadrada.

### O que foi feito (IMPLEMENTADO)
- **Foto em 1:1**, com corte centralizado. O hero deixa de esticar: no desktop a
  imagem fica com no máximo 560px, alinhada à direita.
- **Enquadramento conferido na foto real**, com três recortes quadrados lado a
  lado: pelo topo (corta a parte de cima do cabelo), pelo centro e pelo pé (corta
  a cabeça). O central é o único que mantém o rosto, o cabelo e a blusa de linho
  no quadro, então é o que o CSS usa (`object-position: center 50%`).
- **Quando a foto definitiva chegar em 1:1**, não haverá corte nenhum, porque a
  proporção do arquivo passa a bater com a da moldura. Documentado em
  `SPECS-DE-IMAGEM.md`, que agora pede a foto do hero em 1200×1200.
- **Verificações:** 22 páginas geradas sem erro; 997 verificações automáticas e
  zero falhas; pente fino de HTML/CSS/JS com as 12 seções zeradas.

### Decisões tomadas
- O corte é feito só pelo CSS, sem mexer no arquivo da imagem: o JPG original
  continua intacto, o que preserva o uso dele em outras telas e a checagem de
  direitos.
- O limite de 560px vale só a partir de 1021px; no celular a foto continua
  ocupando a largura toda, agora quadrada.

### O que continua em aberto (AGUARDA INFORMAÇÃO)
- Conferência da cliente no navegador: se quiser a foto ainda menor no desktop, o
  limite de 560px é o número a mexer (uma linha).
- "Tingimento natural" (casca de cebola e eucalipto), "costura em pequenos lotes"
  e "fornecedores certificados" seguem fora do site, aguardando confirmação.
- Composição exata por peça, tabela de medidas real e história da marca.

## [2026-10-16] - Hero com a foto inteira e a descrição sobre a imagem (v0.1.17)

### Pedido da cliente
"tem que acertar a imagem e essa breve descricao em cima da imagem que nao foi
feito tb", junto com o print do hero do template. Na nossa página a foto estava
numa moldura retrato (com corte) e a legenda ficava embaixo da imagem, alinhada
à esquerda. No template a foto aparece com um quadrinho branco por cima, no
canto inferior direito, com o numeral "01" em uma linha e a descrição em duas.

### Duas respostas que fecharam a dúvida
1. **Enquadramento:** a foto aparece inteira, sem corte (a opção "como no print",
   com moldura 4:5, foi descartada pela cliente).
2. **Legenda:** texto do template, "Blusa de Linho Terracota, tingida com argila
   do Vale do Paraíba". Com essa escolha, a cliente confirmou que o tingimento
   com argila é real, e o texto voltou ao site (ele tinha saído na v0.1.16 por
   falta de confirmação).

### O que foi feito (IMPLEMENTADO)
- **Foto inteira:** a moldura retrato (6:7 e 5:6) e o recorte saíram. A foto usa
  a proporção original (768×1376) e ocupa a largura da coluna, como no zip.
- **Selo sobre a foto:** caixa de fundo papel, borda fina, recuos de 20px,
  largura máxima de 220px (os mesmos números do template), numeral "01" em linha
  própria e a descrição em duas ou três linhas.
- **Celular:** abaixo de 721px o selo desce para baixo da foto, para não cobrir
  a modelo (mesma decisão do template).
- **Verificações:** `build.py` e `check.py` com as 22 páginas certas; 993
  verificações automáticas e zero falhas (a seção 24 é nova e cobre a foto sem
  recorte, o selo em cima da foto e o texto confirmado); `pente-fino.py` com as
  12 seções zeradas.

### Continua aguardando confirmação (fora do site)
"Tingimento natural" (argila, casca de cebola e folhas de eucalipto), "costura
em pequenos lotes" (30 a 60 peças por edição, remuneração justa) e "fornecedores
certificados" seguem fora do protótipo: a confirmação desta rodada foi só sobre
o tingimento com argila do Vale do Paraíba, que é o texto do selo.

### O que continua em aberto (AGUARDA INFORMAÇÃO)
- Conferência no navegador: com a foto inteira, o hero fica bem alto em tela
  grande (a foto é 9:16). Se ficar exagerado, o caminho é limitar a largura da
  coluna da foto ou voltar a uma moldura, e isso é uma linha de CSS.
- Composição exata por peça, tabela de medidas real e história da marca.

## [2026-10-16] - Coleção em capítulos, como o zip (v0.1.16)

### Pedido da cliente
A cliente mandou a captura do primeiro capítulo do zip ("01 · Terracota / O barro
que veste") e disse que a página de coleção do template não está igual. Estava
certo: a nossa página da coleção ainda era uma grade de quatro looks com etiquetas
de peças, e o zip tem três capítulos editoriais, cada um com uma foto grande, o
texto do capítulo e duas peças à venda embaixo.

### O que foi feito (IMPLEMENTADO)
- **Capa da coleção**, como no zip: centralizada, com a trilha de navegação, o
  nome "Terra & Linho", a chamada e quatro fichas (doze peças, do P ao GG, feito
  no Brasil, modelagem autoral). Esta página deixou o cabeçalho de página das
  outras telas e abre como editorial, do mesmo jeito que o produto e o artigo.
- **Três capítulos**: 01 Terracota ("O barro que veste"), 02 Sálvia ("Verde que
  acalma") e 03 Cru ("O branco que não é básico"). Cada um traz a foto grande de
  um lado, o texto e duas peças do catálogo do outro, e o convite "Comprar o
  capítulo". O capítulo do meio inverte os lados, como no zip, e abaixo de 1021px
  a foto vai para cima e o texto desce.
- **Cartão enxuto nos capítulos**, igual ao do zip: foto com selo, coração dos
  desejos, categoria, nome e preço. Sem nota, sem tamanhos e sem o convite da
  sacola. O cartão da loja continua completo.
- **As peças de cada capítulo são as do catálogo real**, separadas por cor:
  terracota (blusa de linho e vestido longo), sálvia (vestido midi e calça
  pantalona) e cru (camisa de linho e saia midi).
- **Verificações:** `build.py` e `check.py` com as 22 páginas certas; `test.js`
  com 980 verificações e zero falhas (a seção 23 cobre capa, capítulos, cartões e
  as regras de CSS); `pente-fino.py` com as 12 seções zeradas.

### Afirmações do zip que saíram hoje (a empresa não confirmou)
Ao revisar a página da coleção, apareceram frases que vieram do template e que
ninguém confirmou. Elas saíram e entraram as informações que a empresa confirmou
por escrito (linho, algodão egípcio e viscose de alta gramatura; modelagem, corte
e confecção próprios; produção em Cerquilho, SP; troca em 30 dias):
- "tingido com argila", "tingimento natural" (argila, casca de cebola, eucalipto);
- "costura em pequenos lotes", "de 30 a 60 peças por edição", "remuneração justa
  para costureiras parceiras";
- "fornecedores certificados" e "origem declarada na etiqueta";
- "18 peças" na vitrine da coleção (são doze);
- "troca em 7 dias" no carrinho e na página Sobre (a troca é em 30 dias; 7 dias
  é o direito de arrependimento do Código de Defesa do Consumidor).

### Decisões tomadas
- **A capa não leva estação.** O zip escreve "Outono · Inverno 2026"; nada disso
  foi confirmado, então a capa abre direto no nome da coleção.
- **As fichas do zip** (18 peças, tingimento natural, edições numeradas) foram
  trocadas pelas fichas verdadeiras deste catálogo.
- **A nota de produção das fotos** continua no fim da página, agora falando de
  abertura de capítulo e fotos de peça em 4:5.

### O que continua em aberto (AGUARDA INFORMAÇÃO)
- Confirmar o nome da coleção ("Terra & Linho"), que veio do template, e a
  estação, se a coleção tiver uma.
- Conferência no navegador: a página da coleção tem fotos muito altas (as
  imagens são 9:16, como as do zip) e vale ver a proporção em tela grande.
- Composição exata por peça, tabela de medidas real e história da marca.

## [2026-10-16] - Coleção com a paginação e a ordenação do zip (v0.1.15)

### Pedido da cliente
"a pagina de coleção tem que seguir a do template que enviei pode ajustar". Na
rodada anterior eu tinha avisado que o layout do zip estava seguido em tudo menos
na paginação, porque o dossiê pedia o catálogo inteiro em uma grade só. O pedido
de agora revê aquela decisão a favor do zip.

### O que foi feito (IMPLEMENTADO)
- **Linha da coleção**, como no zip: logo abaixo do fio do cabeçalho, a faixa de
  peças visíveis ("Mostrando 1–9 de 12 peças"), o recado de tamanhos (vestuário
  feminino do P ao GG) e o atalho do guia de medidas. O recado de tamanhos saiu
  da barra de ferramentas, que ficou com o que é do zip: o botão Filtros, a
  contagem e a ordenação.
- **Paginação**, com o desenho do zip: quadrados de 44px centrados no rodapé da
  grade, a página atual com fio de tinta, setas que desligam no começo e no fim.
  Nove peças por página, que é a conta do zip (52 peças em 6 páginas). Com o
  catálogo de 12 peças, ficam duas páginas: 9 e 3. Quando um filtro deixa o
  resultado em uma página só, a barra desaparece.
- **A faixa acompanha** os filtros e a página ("Mostrando 10–12 de 12 peças" na
  segunda página), e ao trocar de página a grade volta ao topo, descontando o
  cabeçalho fixo. O filtro novo sempre recomeça da primeira página, então ninguém
  fica preso numa página que deixou de existir.
- **Cinco formas de ordenar**, as do zip e do WooCommerce: mais recentes, mais
  populares, menor preço, maior preço e melhor avaliados. As duas últimas usam a
  nota e o número de avaliações que já apareciam no cartão. A ordenação por nome
  saiu, porque não existe no zip.
- **Acessibilidade:** a paginação é um `nav` com rótulo, a página atual é um
  texto marcado com `aria-current` (não se clica no que já está aberto), as setas
  desligadas são botões desabilitados e o foco acompanha a troca de página, para
  o leitor de tela anunciar a nova página.
- **Avisos corrigidos:** saiu da página o recado interno "sem paginação, conforme
  o dossiê" e o Diário deixou de dizer que a loja não pagina.
- **Verificações:** `build.py` e `check.py` com as 22 páginas certas; `test.js`
  com 938 verificações e zero falhas (a seção 22 cobre a paginação, a faixa e as
  cinco ordenações); `pente-fino.py` com as 12 seções zeradas; `data-nome` saiu do
  cartão porque nenhum JavaScript o lia mais.

### Decisões tomadas
- **Nove peças por página.** É o número que a própria paginação do zip revela (52
  peças em 6 páginas). Se a cliente preferir o catálogo inteiro em uma grade só,
  volta com uma linha em `filtros.js`.
- **A lista de categorias, as cores e a faixa de preço continuam os do catálogo
  real** (sete categorias, cinco cores, R$ 149 a R$ 789), e não os do zip, que
  descrevem uma loja de 52 peças com oito categorias. O desenho segue o zip; os
  números são os nossos.
- **Sem JavaScript a coleção continua inteira:** a grade traz as 12 peças no
  HTML, a faixa diz "Mostrando 1–12 de 12 peças" e a barra de paginação não
  aparece.

### O que continua em aberto (AGUARDA INFORMAÇÃO)
- Conferência no navegador: a paginação, a rolagem até o topo da grade e o
  comportamento das setas precisam de uma tela de verdade; o jsdom não rola.
- Composição exata por peça (percentual de fibra) e tabela de medidas real.
- História da marca para a página Sobre, analytics e pixels para a privacidade.

## [2026-10-16] - Resumo fixo na sacola, coleção no layout do zip e artigo novo (v0.1.14)

### Pedido da cliente
Três pedidos numa mensagem. No primeiro, a cliente mandou a captura do card
"Resumo" da sacola: o alinhamento de dentro estava errado e, ao rolar a página,
o resumo deveria ficar preso na tela. No segundo, pediu um layout novo e mais
moderno para o `post.html`. No terceiro, pediu que a página de coleção siga o
layout do zip de referência. Junto veio a "Especificação da Marca e Regras de
Negócio" atualizada, que respondeu o que faltava.

### O que foi feito (IMPLEMENTADO)
- **Alinhamento do resumo.** O campo e o botão das duas linhas (cupom e cálculo
  do frete) estavam presos por uma margem calculada à mão de 26px: ela acertava o
  botão do cupom por sorte e empurrava o "Calcular" 25px abaixo do campo do CEP.
  Agora a linha é uma grade de duas colunas alinhadas pela base: campo e botão
  terminam exatamente na mesma altura, com a mesma altura de toque de 44px.
  Os valores do resumo ficaram numa coluna de número com largura fixa, então
  R$ 974,00 e R$ 15,00 terminam na mesma linha vertical.
- **Resumo preso ao rolar.** O `position: sticky` já estava escrito, mas não
  funcionava, e a causa não era ele: o `body` tinha `overflow-x: hidden`, que
  transforma o body numa caixa de rolagem e desliga o `position: sticky` de tudo
  que está dentro dele. Trocado por `overflow-x: clip`, que corta o excesso sem
  criar caixa de rolagem, com o `hidden` guardado para navegador antigo. O resumo
  e o cabeçalho do site voltaram a acompanhar a rolagem. O resumo ganhou teto de
  altura: se ele for mais alto que a janela, rola por dentro em vez de esconder o
  botão de finalizar.
- **Página de coleção no layout do zip.** A coluna de filtros acompanha a rolagem
  e começa direto em Categorias (o título "Filtros" ficou só para leitor de tela e
  para a gaveta do celular), fechando com as ações no fim: botão "Aplicar filtros"
  e link "Limpar filtros". A contagem passou a dizer "12 peças nesta seleção",
  como no zip. O cartão de produto virou uma coluna com 12px entre as partes e a
  grade ganhou o espaçamento do zip, com mais ar entre as linhas do que entre as
  colunas.
- **Layout novo do artigo.** A página do diário deixou o cabeçalho centralizado com
  a foto embaixo e passou a ter capa em duas colunas (texto à esquerda, foto à
  direita), índice "Neste texto" que acompanha a leitura e marca a seção atual,
  barra fina de progresso, uma citação de respiro, uma chamada para o guia de
  medidas e o fecho com etiquetas de assunto, compartilhar e autoria. O JavaScript
  novo (`artigo.js`) cuida da barra, do índice e do botão de copiar o link, e
  falha em silêncio se algo não estiver disponível.
- **Retirada no ateliê confirmada:** segunda a sexta, das 10h às 17h, depois do
  aviso de "Pronto para Retirada" por e-mail. Entrou no checkout, no Envio e no
  Contato, e saiu o marcador que pedia essa informação.
- **Boleto bancário habilitado**, pelo Mercado Pago: vence em 2 dias úteis e o
  pedido é liberado depois da compensação bancária, com o valor cheio (sem o
  desconto do Pix). Virou o terceiro cartão de pagamento no checkout e entrou no
  rodapé, nos Termos, nas Perguntas frequentes, na página de Produto e na Home.
- **Reembolso com prazo:** Pix em 2 dias úteis depois da conferência da peça,
  cartão com estorno solicitado em 3 dias úteis (o lançamento depende da data de
  fechamento da operadora) e boleto com depósito ou Pix em 3 dias úteis.
- **Peças de liquidação e bazar:** troca pelo mesmo modelo em outro tamanho,
  conforme o estoque; se não houver o tamanho, o cupom de troca vale o valor
  efetivamente pago na compra.
- **Tecidos e origem:** as peças usam linho, algodão egípcio e viscose de alta
  gramatura, com modelagem, corte e confecção 100% autorais, feitos no Brasil, no
  ateliê de Cerquilho - SP.
- **Autoria do diário:** os textos passam a ser assinados por Iara Costa e Equipe
  de Criação, como a empresa definiu.
- **Verificações:** `build.py` e `check.py` com as 22 páginas certas; `test.js` com
  907 verificações e zero falhas (a seção 21 cobre o resumo, o boleto, a retirada,
  a coleção e o artigo novo); `pente-fino.py` com as 12 seções zeradas; as quatro
  páginas mexidas carregadas em jsdom sem nenhum aviso de JavaScript.

### Decisões tomadas
- **A loja continua sem paginação.** O zip mostra paginação na listagem, mas o
  dossiê do projeto é explícito: o catálogo aparece inteiro, sem paginação. O
  layout do zip foi seguido em tudo o mais. Quando o catálogo passar de 30 peças,
  o assunto volta à mesa. *(Revisto na v0.1.15: a cliente pediu a paginação do
  zip e a loja passou a paginar de 9 em 9.)*
- **O convite "Adicionar à sacola" continua sempre visível.** O CSS do zip tem um
  convite que só aparece no hover, mas o próprio HTML do zip usa um link comum, e
  esconder uma ação de compra atrás do mouse prejudica o celular. O CSS morto
  daquele hover não foi trazido.
- **O cabeçalho da página de coleção ficou como a cliente aprovou na v0.1.10**
  (trilha e nome da página, sem fundo), com a contagem e o guia de medidas na
  barra de ordenação, e não dentro do cabeçalho como no zip.

### O que continua em aberto (AGUARDA INFORMAÇÃO)
- Composição exata de cada peça (percentual de cada fibra) e a tabela de medidas
  real de cada produto.
- História da marca, em dois ou três parágrafos, para a página Sobre.
- Itens de privacidade que dependem das ferramentas escolhidas: analytics,
  pixels, retenção e transferência internacional.
- Ordem de serviço e conferência das peças devolvidas (procedimento interno).

## [2026-10-16] - Cartões de envio e pagamento no checkout e as regras de negócio fechadas (v0.1.13)

### Pedido da cliente
A cliente enviou duas imagens de referência do fechamento de compra: na primeira,
três formas de envio em cartões com rádio, título, linha de apoio e valor; na
segunda, as formas de pagamento em cartões (Pix com a etiqueta verde "5% OFF") e os
campos de cartão aparecendo quando o cartão de crédito é escolhido. Junto veio a
"Especificação da Marca e Regras de Negócio", que respondeu o que estava em aberto:
frete grátis pelo valor líquido, os R$ 15,00 só no PAC do Sudeste, parcela mínima de
R$ 50,00, troca em 30 dias com a primeira gratuita, arrependimento de 7 dias com
frete da loja, prazos de produção, cuidados das peças, encarregado de dados, data
das páginas legais e a marca do cabeçalho em 20px.

### O que foi feito (IMPLEMENTADO)
- **Cartões de opção no checkout.** As três formas de envio (PAC, SEDEX e Retirar no
  ateliê) e as duas de pagamento (Pix e cartão) viraram cartões clicáveis no padrão
  da imagem: rádio, título, linha de apoio e valor à direita. O cartão escolhido
  ganha borda e fundo claros, pelo `:has()` do CSS e também pela classe `.is-selected`
  que o JavaScript marca, para navegadores que ainda não têm `:has()`.
- **Campos do cartão, só na demonstração.** Número, nome impresso, validade, CVV e
  parcelas aparecem quando o cartão é escolhido, com máscaras de digitação. Nenhum
  campo tem atributo `name`, então nada é enviado ao finalizar, e nada é guardado: o
  aviso no topo do bloco explica que, no site publicado, esses campos são do Mercado
  Pago e o número do cartão nunca passa pela loja. É a diferença entre mostrar o
  comportamento pedido e simular uma cobrança.
- **Valores conferidos no protótipo.** Cesta de exemplo: produtos R$ 974,00, cupom
  BEMVINDO10 R$ 97,40, líquido R$ 876,60, Pix (5% off) R$ 832,77, cartão R$ 876,60 e
  parcelas sem juros de 1x R$ 876,60 até 6x de R$ 146,10, respeitando a parcela
  mínima de R$ 50,00.
- **Frete grátis pelo valor líquido.** O limite de R$ 299 passou a considerar o que
  sobra depois do cupom e do desconto do Pix, em todas as páginas que falam do
  assunto: Envio, Carrinho, Perguntas frequentes e o recado da gaveta da sacola.
- **R$ 15,00 confirmado como regra do PAC** em SP, RJ, MG e ES. O SEDEX e as demais
  regiões ficam com o valor calculado pelos Correios. O texto de dúvida saiu da
  página de Envio e do resumo para a equipe.
- **Prazos de produção:** 2 dias úteis para pronta entrega e de 5 a 7 dias úteis para
  peças sob encomenda ou sob medida, antes da postagem. Entraram no produto, no
  Envio, no pedido recebido e nas perguntas frequentes.
- **Trocas e devoluções:** 30 dias corridos para troca de tamanho, com a primeira
  troca por conta da loja (postagem reversa dos Correios), e 7 dias de
  arrependimento com o frete de retorno também da loja. A tabela de prazos da página
  de Trocas saiu de `[A DEFINIR]` para os valores confirmados.
- **Cuidados das peças:** lavar à mão ou em ciclo delicado com sabão neutro, sem
  alvejante à base de cloro, secar à sombra e na horizontal e passar até 110°C,
  respeitando a etiqueta interna.
- **Privacidade:** o encarregado de dados (DPO) passou a ser o Departamento
  Jurídico, com o e-mail `dpo@iaracosta.com.br`, no lugar do canal genérico. A data
  das três páginas legais ficou em 16 de outubro de 2026, com nota para atualizar no
  go-live se o jurídico mudar o texto.
- **Marca do cabeçalho em 20px**, como a especificação pede, e a limpeza das regras
  `.radio` do CSS, que ficaram sem uso quando o checkout passou a usar `.choice`.
- **Verificações:** `build.py` e `check.py` com as 22 páginas certas; `test.js` com
  819 verificações e zero falhas (a seção 20 é nova e cobre os cartões, os valores,
  os campos do cartão, as máscaras e as regras novas); `pente-fino.py` com as 12
  seções zeradas.

### Decisões tomadas
- **Boleto não entrou.** Ele aparece na segunda imagem de referência, mas a
  especificação da empresa confirma Pix e cartão pelo Mercado Pago. Continua fora até
  a empresa confirmar, como já valia desde a v0.1.12.
- **Retirada no ateliê entrou como opção do checkout**, com o endereço confirmado e
  os dias e horários marcados como `[A DEFINIR]`, porque essa informação não veio.
- **Os campos do cartão são demonstração.** Em site publicado, quem coleta os dados
  do cartão é o Mercado Pago. No protótipo eles existem para mostrar o comportamento
  pedido, sem `name` e sem envio.

### O que continua em aberto (AGUARDA INFORMAÇÃO)
- O ateliê faz retirada? Em que dias e horários? (está no checkout, no Contato e na
  página de Envio como `[A DEFINIR: dias e horários de retirada]`)
- Composição, cuidados específicos e país de origem de cada peça.
- Autoria dos textos do diário e quem assina o conteúdo.
- Prazo em dias para processar o reembolso e a regra para peças de liquidação.
- Itens de privacidade que dependem das ferramentas escolhidas: analytics, pixels,
  retenção e transferência internacional.

## [2026-10-16] - Dados da empresa e regras de venda confirmados

### Pedido da cliente
A cliente informou, em uma mensagem só, os dados da empresa e as regras comerciais
que estavam em aberto no site: razão social, nome fantasia, CNPJ, inscrição
estadual, endereço do ateliê, telefone/WhatsApp, e-mail e horário de atendimento;
a regra de frete (Correios com cálculo por CEP, R$ 15,00 no Sudeste, grátis acima
de R$ 299); o gateway (Mercado Pago, Pix com 5% de desconto e cartão em até 6x sem
juros) e a regra do cupom BEMVINDO10 (10% na primeira compra, para clientes novos,
sem acúmulo).

### O que foi preenchido (IMPLEMENTADO)
- **Identificação da empresa no rodapé de todas as 22 páginas:** Iara Costa Moda
  Feminina LTDA, CNPJ 12.345.678/0001-90, Rua das Flores, nº 140, Sala 02, Centro,
  Cerquilho - SP, CEP 18520-000. É o que o Decreto 7.962/2013 exige que esteja
  visível.
- **Atendimento:** contato@iaracosta.com.br, (15) 99123-4567 (telefone e WhatsApp)
  e segunda a sexta, das 9h às 18h, com prazo de resposta de 24 horas úteis. Os
  dois viraram link de verdade (`mailto:` e `tel:`).
- **Formas de pagamento:** Pix com 5% de desconto e cartão de crédito em até 6x
  sem juros, processados pelo Mercado Pago. O rodapé passou de oito formas
  ilustrativas para as três confirmadas (gateway, Pix e cartão).
- **Frete:** Correios com cálculo por CEP. No Sudeste, R$ 15,00 (escrito como PAC);
  nas demais regiões, o valor calculado; acima de R$ 299, grátis.
- **Cupom BEMVINDO10:** 10% na primeira compra, para clientes novos, uso pessoal e
  não cumulativo com outras promoções nem com peças em liquidação.
- **Páginas de política:** Termos e Privacidade ganharam a identificação completa
  do controlador e o canal de privacidade (o mesmo e-mail, com o assunto
  "Privacidade"), e o Contato ganhou o endereço do ateliê no quadro do mapa.

### O que saiu do site (IMPLEMENTADO)
Boleto, transferência bancária, PayPal e as bandeiras de cartão (Visa, Mastercard,
American Express e Diners) não foram confirmados pela empresa e saíram de todas as
páginas, incluindo o rodapé e o checkout. Também saíram os valores de exemplo de
PAC e SEDEX (R$ 24,90 e R$ 39,90) e os prazos de "5 a 9" e "2 a 4" dias úteis, que
eram ilustrativos: agora a página aponta o cálculo dos Correios pelo CEP.
No `loja.js`, a função `regiaoDoCep` reconhece a faixa do Sudeste (São Paulo, Rio,
Espírito Santo e Minas) e só escolhe o texto do recado: o valor de verdade continua
vindo do gateway de frete.

### Reconciliação com o que já estava escrito (RECOMENDADO)
- O dossiê previa **frete grátis acima de R$ 199**; a decisão de R$ 299 veio antes e
  vale. O protótipo nunca mostrou 199.
- O rodapé mostrava **oito formas de pagamento** como ilustração da imagem enviada
  pela cliente. A regra do projeto é não afirmar o que não está confirmado, então
  ele passou a mostrar as três confirmadas.
- A home anunciava **"troca fácil em 30 dias"** com frete da primeira troca por
  conta da loja. Isso nunca foi confirmado e ficou marcado como `[A DEFINIR]` na
  faixa de benefícios: prazo e frete de troca são decisão da empresa.

### O que continua em aberto (AGUARDA INFORMAÇÃO)
- Se o valor fixo de R$ 15,00 no Sudeste vale para o PAC e o SEDEX ou só para o PAC.
- Se o frete grátis considera o subtotal antes ou depois do cupom.
- Prazo de produção, usado em "envio em até X dias úteis" e na página de pedido.
- Prazo e frete da troca por tamanho, e quem paga o frete na devolução por
  arrependimento.
- Encarregado de dados (DPO) e data de aprovação das três páginas legais.
- Composição, cuidados e país de origem das peças; autoria dos textos do diário.

### Verificação (VERIFICADO EM ARQUIVO)
- `python3 tools/build.py` e `python3 tools/check.py`: 22 páginas, "tudo certo".
- `node tools/test.js`: **720 verificações, nenhuma falha**. O bloco novo (§19)
  confere os dados da empresa no rodapé das 22 páginas, os canais de atendimento
  como links, a ausência de boleto, PayPal e transferência bancária em todo o site,
  a ausência dos valores de exemplo que saíram, as regras de frete e de cupom nas
  páginas e a função de faixa de CEP no `loja.js`.
- Pente fino com as doze conferências zeradas.
- **O que isto não é:** nenhuma das regras foi testada em gateway ou em conta dos
  Correios, porque não existe conta ligada. É conferência de arquivo.

### Nota operacional sobre o repositório
Antes de gravar esta versão, o clone local do projeto apareceu com o histórico
reduzido ao primeiro commit (o workspace foi restaurado de um estado antigo). Nada
foi perdido: o histórico completo, as etiquetas `v0.1.0` a `v0.1.11` e o branch de
trabalho foram recuperados do GitHub e conferidos um a um antes de continuar. O
conteúdo dos arquivos no workspace estava íntegro e nenhuma alteração da v0.1.12
precisou ser refeita.

### Estado
- `VERSION` = 0.1.12. Versão anterior preservada na etiqueta `v0.1.11`.
- Branch `arena/e067653e-iaracostaoficial`, PR #2 aberto (não mergeado).

## [2026-10-16] - Pente fino no HTML e no CSS e o JavaScript do template

### Pedido da cliente
"Faça um pente fino em todos os arquivo do template e veja se possui algum html ou
css quebrado e veja que o template passado tem os arquivos js, pode verificra e
ajsutar em nosso template." Leitura feita: (1) varrer todo o HTML e o CSS do
protótipo atrás de quebrado e consertar o que aparecesse; (2) conferir os arquivos
de JavaScript do zip e adaptar o que fizesse sentido.

### Pente fino (IMPLEMENTADO)
Escrito um conferidor que lê os arquivos com parser de verdade, não com busca de
texto: `html5lib` para o HTML e `tinycss2` para o CSS. Ele roda as doze
conferências abaixo e só lê, não conserta nada. Placar final: **nenhum achado**.

| Conferência | Resultado |
|---|---|
| Erros de sintaxe do HTML e do CSS | nenhum |
| Classes usadas no HTML sem nenhuma regra no CSS | nenhuma (17 são caixas de contexto, conferidas uma a uma) |
| Regras de CSS que não aparecem em nenhum HTML | nenhuma (as sete sem uso foram removidas ou viraram demonstração) |
| Ids repetidos na mesma página | nenhum |
| Links internos e âncoras que não existem | nenhum |
| `aria-controls`, `aria-labelledby`, `aria-describedby` e `for` apontando para o nada | nenhum |
| Imagens e arquivos locais que não existem, `<img>` sem `alt`, sem `aria-hidden` ou sem medida | nenhum |
| Campos de formulário sem rótulo acessível | nenhum |
| Ganchos `data-*` no HTML que nenhum JS lê | nenhum |
| Ganchos que o JS lê e não existem no HTML | nenhum |
| Estilos escritos direto no HTML (`style="..."`) | zero |
| Ids usados no CSS ou no JS que não existem no HTML | nenhum |

### O que estava quebrado de verdade (IMPLEMENTADO)
- **Dois atributos inválidos.** Termos e Cookies tinham `<p margin-bottom:0">`. O
  estilo foi escrito como se fosse atributo: o navegador descarta o trecho como
  resto de tag. Virou `<p class="mb-0">`, com a regra na folha de estilo.
- **Duas imagens do resumo do checkout sem medida declarada.** O tamanho estava só
  dentro de um `style=""`; o gerador só corrige medida em atributo, então as duas
  ficaram com o valor antigo. Agora declaram as medidas reais do arquivo
  (`768x1376`) e o tamanho visual vem do CSS.
- **Quarenta estilos escritos direto no HTML** viraram regras com nome, dentro do
  CSS: linha do resumo que empilha, botão de fechar o pedido, caixa de links,
  título de caixa, item de sacola em miniatura e campo de largura dupla. Cada
  regra é presa à tela pela classe `page-*` que o `<body>` já carrega, então nada
  vaza de uma página para outra.
- **CSS sem uso.** Saíram `.cart-count` (o contador antigo da sacola), o bloco
  `.section--sage`, quatro cores de swatch que nenhum produto usava e o
  `style="width:0%"` da gaveta, que agora é regra de CSS.
- **O esqueleto de carregamento, o erro de campo e os três estados de estoque**
  eram CSS sem uso. Em vez de apagar, viraram demonstração para a equipe: o
  produto mostra os três estados de estoque lado a lado e uma referência do estado
  carregando, e o checkout mostra um campo com erro, com a marca para leitor de
  tela (`aria-invalid` e `aria-describedby`).

### JavaScript do template (IMPLEMENTADO)
O zip traz **dois** arquivos: `header.js` (15 KB) e `loja.js` (24 KB). O que foi
aproveitado, adaptado à nossa marcação e às decisões do dossiê:

| Do template | O que entrou aqui |
|---|---|
| `safeInit`: cada melhoria inicia isolada | Nas quatro folhas de JS. Antes, um erro na galeria deixava o acordeão sem funcionar; agora uma falha avisa no console e as outras melhorias seguem de pé |
| Máscara de CEP | Na sacola e no checkout, no formato `00000-000` |
| Máscara de telefone | No checkout, no formato brasileiro `(15) 99123-4567` |
| Recado que muda conforme o meio de pagamento | No checkout, com texto próprio para Pix, cartão, boleto e transferência |
| Botões + e − e remover peça | Na sacola, recalculando subtotal, desconto, frete e total na hora |
| Cupom com validação | Só o BEMVINDO10 do dossiê: 10% na primeira compra, aceito maiúscula ou minúscula, recado claro quando o código não é reconhecido |
| Cálculo de frete | Confere o CEP e responde com a regra confirmada (grátis acima de R$ 299); o resto fica `[A DEFINIR]` |
| Trava de rolagem da gaveta, com compensação por script | Resolvido em CSS (`scrollbar-gutter: stable`): o conteúdo não anda para o lado quando a gaveta abre, e sem script |

### O que do template NÃO entrou, e por quê (RECOMENDADO)
- **Valores de frete fixos.** O zip devolve PAC R$ 24,90 e SEDEX R$ 39,90 com
  prazos. Não existe contrato de frete ainda: inventar esses números seria pior do
  que responder `[A DEFINIR]`.
- **Número de cartão na própria página.** O zip tem máscara e validação de cartão.
  Os dados do cartão são digitados na página segura do gateway, que ainda não foi
  contratado; o protótipo não pede número de cartão em campo nenhum.
- **Recursos presos ao WordPress.** O resto dos dois arquivos chama carrinho do
  WooCommerce, painel de conta e filtro por URL. São do Bloco B, quando houver site
  para testar.

### Dois ganchos que o pente fino levantou, e a decisão
- `data-nav` **não** é código morto: é a marca que o `tools/build.py` lê para
  escrever `aria-current="page"` no item do menu da página atual. O pente fino
  passou a reconhecer isso, para não apontar de novo.
- `data-drawer-open` é a porta de entrada da mini-sacola: qualquer botão com esse
  gancho abre a gaveta. No protótipo o ícone do cabeçalho continua levando para a
  página da sacola, que foi o comportamento aprovado, então nenhuma tela usa o
  gancho. Fica mantido como porta de entrada, documentado.

### Régua de verificação agora vive no repositório (IMPLEMENTADO)
O teste de navegador e o pente fino existiam só fora do projeto e se perdiam a cada
rodada. Agora são `tools/test.js` (jsdom) e `tools/pente-fino.py`, com o
`package.json` que instala o jsdom e o passo a passo no README do protótipo. O site
publicado não depende de Node: são ferramentas de conferência para a equipe.

### Verificação (VERIFICADO EM ARQUIVO)
- `python3 tools/build.py` e `python3 tools/check.py`: 22 páginas, "tudo certo".
- `node tools/test.js`: **649 verificações, nenhuma falha**. O bloco novo (§18)
  confere: nenhum `style=""` no HTML, nenhum atributo inválido, cada classe que
  estava sem CSS agora tem regra, o CSS morto não voltou, a regra de movimento
  reduzido cobre o esqueleto, os três estados de estoque e o campo com erro
  existem, cupom válido e inválido, CEP incompleto e completo, frete grátis acima
  de R$ 299, o botão + recalculando o subtotal, a remoção de uma peça, as duas
  máscaras, o recado do pagamento trocando com o rádio e nenhum campo de cartão no
  protótipo.
- `python3 tools/pente-fino.py`: as doze conferências zeradas.
- Servidor local no ar para a conferência visual.
- **O que isto não é:** não é teste em navegador de verdade, nem leitura por leitor
  de tela, nem medição de Lighthouse. Isso continua com o time, como manda o
  dossiê.

### Estado
- `VERSION` = 0.1.11. Versão anterior preservada na etiqueta `v0.1.10`.
- Branch `arena/e067653e-iaracostaoficial`, PR #2 aberto (não mergeado).
- Perguntas da v0.1.10 seguem abertas: nome da marca em 24px como no zip e os 9px
  e 8px do Caption e do Tagline do template.

## [2026-10-16] - Fontes na escala do template e cabeçalho de página limpo

### Pedido da cliente
Com a imagem de uma página de produto do template do zip em mãos (1456px de
largura): "o tamanho da fonte utilizada aqui, pode ajustar nosso template para não
ficar muito grande" e "em relação ao pageheader vamos deixar sem o fundo, apenas
com uma borda abaixo e apenas com o breadcrumb e o nome da página, bem clean, em
relação ao tamanho da fonte do template siga o tamanho que passei no zip".

### Reconferência do template (zip)
A tabela tipográfica do zip (`assets/css/style.css` §00.4 e §04) é: **Display
24px** (nome da marca, título de página, título de produto, hero e faixas),
**Heading 18px** (títulos de seção e de card), **Body 15px**, Small 12px, Micro
11px, Caption 9px e Tagline 8px. No zip nenhum tamanho fica escrito em pixel solto:
tudo sai de token. O `.iara-page-head` do zip é só espaçamento, sem fundo e sem
borda, e o título dele (h1) usa a classe `.iara-display`: Playfair 400, 24px,
entrelinha 1.1 e entreletra 0.105em. Nossos tokens Display/Heading/Body/Small/Micro
já batiam com o zip; o que estava fora eram os clamps de título (32 a 60px) e o
cabeçalho de página, que a cliente rejeitou por ter faixa de fundo e enfeites.

### O que foi feito (IMPLEMENTADO)
- **Escala.** Os clamps grandes saíram: nome da página, hero, título de produto,
  faixas verdes e frases de destaque passaram a ler os tokens do template (Display
  24px ou Heading 18px). Os tokens `--fs-h1`, `--fs-h2` e `--fs-h3` agora apontam
  para a escala do zip, então a redução vale para o site inteiro de uma vez.
- **Tratamento Display.** `h1` (nome da página, título de produto e hero) e os
  títulos das faixas verdes usam o mesmo desenho do zip: Playfair 400, entrelinha
  1.1 e entreletra 0.105em. Os h2 e h3 seguem o Heading do zip, com a entreletra
  curta de 0.02em que o próprio template usa.
- **Cabeçalho de página.** Saiu a faixa de fundo, saíram o fio curto e a linha de
  olho. Ficaram a trilha de navegação, o nome da página e um fio embaixo, com
  respiro em cima e embaixo. O `h1` está em 24px.
- **Texto de apoio.** Estava dentro do cabeçalho; passou para logo abaixo do fio,
  em bloco próprio (`.page-intro`), em 17 páginas. O cabeçalho ficou só com trilha
  e nome, como pedido.
- **Loja.** A contagem de peças e o recado "Vestuário feminino do P ao GG" ficavam
  dentro do cabeçalho e não fazem parte do desenho limpo. Foram para a barra da
  coleção, ao lado de "Ordenar por", que é onde a contagem pertence; abaixo de
  1021px descem para uma linha própria, alinhados pelo fio.
- **Contador e micro-textos.** O selo de contagem da sacola e a linha de apoio do
  hero estavam em 10px; subiram para 11px, o mínimo da regra de contraste do
  projeto.
- **Limpeza de CSS.** Saíram as regras que só existiam para o cabeçalho antigo
  (fio curto, linha de olho, grade interna e a linha de apoio da loja).

### Decisão que precisa da cliente
- O zip usa **Caption 9px** e **Tagline 8px**. Aqui os dois continuam em 11px,
  porque a decisão E0 do dossiê e a regra de contraste do projeto (abaixo de 14px
  só Ink ou Ink Soft) não deixam descer tanto em fundo claro. Se ela quiser os
  valores literais do template, é uma decisão nova e o texto pequeno perde
  contraste.
- O nome da marca no header segue em 18px a 21px. O zip usa 24px, mas o header foi
  aprovado em 15/10 e aumentar o logotipo mexe no equilíbrio dele; fica como
  pergunta.

### O que ainda não entrou
- As margens escritas direto no HTML das telas internas continuam anotadas como
  limpeza pendente (não mudam nada no visual).

### Verificação (VERIFICADO EM ARQUIVOS)
- `python3 tools/build.py` e `python3 tools/check.py`: 22 páginas, "tudo certo".
- Teste com jsdom: **603 verificações, nenhuma falha**. O bloco novo (§17) confere
  a escala: reprova qualquer `font-size` acima de 24px nos quatro arquivos de CSS
  (as aspas grandes do depoimento são a única exceção declarada), confere os
  tokens Display 24 / Heading 18 / Body 15, exige que o CSS do cabeçalho tenha fio
  embaixo e nenhum fundo, e que as peças antigas do cabeçalho não voltem. O
  mesmo bloco confere o que saiu de dentro do cabeçalho e não podia desaparecer:
  a contagem de peças, o recado "do P ao GG" com o atalho do guia de medidas e a
  linha "Última atualização" das três páginas legais.
- O bloco do cabeçalho conferido nas 17 páginas internas: só trilha e título
  dentro, sem texto de apoio, e a trilha continuando única na página.
- Servidor local no ar para a conferência visual.
- Não é medição de navegador real: navegador, leitor de tela e Lighthouse ficam
  por conta do time, como manda o dossiê.

### Estado
- `VERSION` = 0.1.10. Versão anterior preservada na etiqueta `v0.1.9`.
- Branch `arena/e067653e-iaracostaoficial`, PR #2 aberto (não mergeado).

## [2026-10-16] - Minha conta, Contato e Sobre refeitos com as referências da cliente

### Pedido da cliente
Com cinco imagens do template em mãos: Minha conta adaptada às imagens 1 e 2,
Contato adaptado às imagens 3, 4 e 5 ("do lado direito pode colocar bordas, veja
no depoimento da home se fica bom; veja também os background de cada seção"),
Sobre com o primeiro bloco em texto à esquerda e imagem à direita mais uma seção
de missão, visão e compromisso, e a página de coleção verificada conforme o
template sugerido.

### O que foi feito (IMPLEMENTADO)
- **Minha conta (imagens 1 e 2).** A página ganhou o que faltava: no topo, dois
  cartões lado a lado, "Já sou cliente / Entrar" e "Primeira compra / Criar
  conta", com e-mail, senha, "Manter conectada", aceite dos Termos e da Política
  de Privacidade e botão de largura inteira em cada cartão. Abaixo, o painel da
  cliente logada com navegação lateral (Painel, Meus pedidos, Lista de desejos,
  Endereços, Meus tamanhos, Dados da conta e Sair) e os pedidos em tabela, com
  colunas de pedido, data, peças, total e status em selo, mais o atalho
  "Solicitar troca". A seção "Meus tamanhos" é nova e está marcada como
  `[A DEFINIR]`: só faz sentido se a empresa decidir guardar as medidas da
  cliente, e isso precisa entrar na Política de Privacidade.
  Segurança: os formulários são demonstração e há aviso explícito para não digitar
  senha de verdade; no site publicado, login e cadastro são do WooCommerce.
- **Contato (imagens 3, 4 e 5).** O formulário passou a viver em um quadro de
  papel e os canais de atendimento da direita viraram quadros com borda, a mesma
  linguagem dos depoimentos da home, sobre uma seção com fundo Hover Soft. Os
  campos obrigatórios ganharam asterisco e a linha "Campos com * são
  obrigatórios". Fundos conferidos seção por seção: atendimento em fundo suave,
  referência de estado em papel, mapa em fundo suave e dúvidas rápidas em papel.
  A seção do mapa segue o template, mas com uma decisão: o endereço do ateliê
  ainda não foi informado, e inventar um ponto no mapa seria pior do que não ter
  mapa. No lugar dele ficou um quadro de exemplo com a instrução de onde o mapa
  real entra, e a legenda marcada como `[PREENCHER]`. O bloco "Dúvidas rápidas"
  traz quatro perguntas, com as respostas copiadas palavra por palavra da página
  de Perguntas frequentes.
- **Sobre.** O primeiro bloco passou a ser texto à esquerda e imagem à direita,
  como pedido. Entrou a seção "Missão, visão e compromisso" em três cartões. Os
  três textos são `[PROPOSTA]`: foram escritos a partir do que já estava nesta
  página e no resto do site (informação antes da venda, curadoria pequena,
  nenhuma pressa artificial), e cada cartão tem o selo para ninguém publicar sem
  revisar, porque missão e visão são a voz da marca. A frase de posicionamento
  saiu do meio do texto corrido e virou faixa com fundo suave, e entrou uma faixa
  com três fotos do processo (costura, tingimento e cerâmica), todas imagens que
  já estavam no projeto e previstas para esta página na SPECS-DE-IMAGEM.
  A lista "O que a gente defende" saiu: o conteúdo dela está no cartão de
  compromisso e na lista "Compromissos com o cliente", que continuam na página.
- **Coleção.** O cabeçalho ganhou a linha de apoio do template: "Vestuário
  feminino do P ao GG" e o atalho para o guia de medidas, ao lado da contagem de
  peças que já existia.
- **Limpeza de CSS.** Saíram da folha de estilo o bloco da galeria antiga do
  Sobre (que a página não usa mais), os cartões de atalho da conta e a cabeça dos
  cartões de pedido. Nada disso tinha uso no HTML depois da mudança.

### O que ainda não entrou
- Carrinho, checkout, desejos, busca, produto e a página do post seguem com o
  layout anterior, e os espaçamentos escritos direto no HTML dessas telas
  continuam anotados como limpeza pendente.
- Telefone, e-mail, prazo de resposta e endereço do Contato seguem como
  `[PREENCHER]`: são dados da empresa.

### Verificação (VERIFICADO EM ARQUIVOS)
- `python3 tools/build.py` e `python3 tools/check.py`: 22 páginas, "tudo certo".
- Teste com jsdom: **527 verificações, nenhuma falha**. O bloco novo confere os
  dois cartões da conta, os atalhos da navegação (nenhum apontando para lugar
  nenhum), a tabela de pedidos com cinco colunas e três linhas, os selos de
  status, o quadro do formulário de contato, os quadros dos canais, os asteriscos
  dos campos obrigatórios, o quadro do mapa (e a ausência de mapa de endereço
  inventado), as quatro dúvidas rápidas e a linha de apoio do cabeçalho da loja.
- Servidor local no ar em `http://localhost:8080` para a conferência visual.
- Não é medição de navegador real: navegador, leitor de tela, contraste em tela e
  Lighthouse ficam por conta do time, como manda o dossiê.

### Estado
- `VERSION` = 0.1.9. Versão anterior preservada na etiqueta `v0.1.8`.
- Branch `arena/e067653e-iaracostaoficial`, PR #2 aberto (não mergeado).

## [2026-10-16] - Rodapé com pagamento e segurança, cabeçalho de página e renovação das internas

### Pedido da cliente
Três pedidos no mesmo recado: (1) acrescentar no rodapé as formas de pagamento e
a área de segurança, seguindo a captura enviada; (2) o cabeçalho das páginas
internas estava "muito simples", pedir sugestão e ajustar; (3) renovar o layout
das páginas internas, que estavam ruins, usando como exemplo o template do zip.

### O que foi feito (IMPLEMENTADO)
- **Rodapé, formas de pagamento e segurança.** A faixa de segurança ganhou dois
  quadros: "Formas de pagamento", com oito formas (Visa, Mastercard, American
  Express, Diners Club, Mercado Pago, PayPal, Pix e Boleto) em quadros de texto,
  e "Segurança", com dois selos desenhados (cadeado e escudo) e as legendas
  "Site seguro / SSL 256 bits" e "Navegação verificada / Sem páginas suspeitas".
  Decisão de segurança e de direito de marca: as capturas de referência mostram
  logotipos de terceiros (bandeiras de cartão, Pix, selo SSL, Google Safe
  Browsing). Nada disso foi copiado para o protótipo: são marcas de outras
  empresas e os certificados só podem ser exibidos quando existirem de verdade,
  com o gateway contratado. No protótipo vão texto e desenho próprio, e o aviso
  de conferência com a empresa continua embaixo da faixa.
- **Cabeçalho das páginas internas.** A trilha de navegação saiu do bloco
  solto que ficava acima e entrou para dentro do cabeçalho; abaixo dela veio um
  fio curto em Terracota e uma linha de olho em maiúsculas, que diz de que parte
  do site a página é ("Central de ajuda" no FAQ, "A marca" na Sobre, "Documento
  legal" nas páginas legais). O bloco ganhou uma faixa de fundo suave
  (Hover Soft) com fio embaixo, o título ficou responsivo (32 a 52px) e a
  contagem de peças, quando existe, continua alinhada pela base do texto.
  São 17 páginas com esse cabeçalho. Quatro telas ficam de fora por desenho:
  produto (a galeria é o topo da página), post (o cabeçalho do artigo tem
  autoria e data), 404 e pedido recebido (as duas são telas centralizadas de
  estado, com a trilha solta).
- **Página Sobre renovada.** Duas fotos na abertura, uma descendo em relação à
  outra; faixa com quatro números (12 peças, R$ 299 de frete grátis, 6x sem
  juros, 7 dias para desistir) e uma frase de posicionamento com fio em
  Terracota. Os números saem de decisões já tomadas pela cliente e de copy que já
  está no site; a frase reaproveita um texto que já existia na própria página.
  Nenhum número, prêmio ou depoimento foi inventado.
- **Índice de leitura.** FAQ, guia de medidas, trocas, envio, privacidade,
  termos e cookies ganharam uma coluna à esquerda com atalhos para cada seção,
  que fica fixa enquanto a página rola no computador e vira uma lista no topo no
  celular. Os títulos das seções das páginas legais receberam identificador, o
  que permite mandar o link direto de um item para outra pessoa.
- **Guia de medidas, Diário e lookbook.** Os três passos do guia aparecem
  numerados em serifa; o destaque do Diário ganhou corpo de texto próprio (a
  classe existia no HTML sem nenhum estilo e o texto ficava colado na foto); o
  lookbook passou a um ziguezague de duas colunas, com cada look numerado e o
  texto dentro do cartão.
- **Limpeza de CSS.** As margens que estavam escritas dentro do HTML dessas
  páginas (margens de seção, de aviso e de título) passaram para o CSS, e o
  seletor dos selos do rodapé deixou de depender de "span dentro de span":
  agora tem classe própria. Nesta limpeza, três blocos da faixa de segurança do
  rodapé foram tocados por engano por um script e devolvidos ao formato original
  no mesmo momento.

### O que ainda não entrou
- Carrinho, checkout, conta, desejos, busca, contato, produto e a página do post
  continuam com o layout anterior. São telas de tarefa, com formulário e lista,
  e a renovação delas pede uma rodada própria: mexer em carrinho e checkout sem
  esse cuidado pode quebrar o fluxo de compra.
- Os outros ~40 espaçamentos escritos direto no HTML dessas telas seguem
  anotados como limpeza pendente.

### Verificação (VERIFICADO EM ARQUIVOS)
- `python3 tools/build.py` e `python3 tools/check.py`: 22 páginas, "tudo certo".
- Teste com jsdom: **479 verificações, nenhuma falha** (inclui o bloco novo §15,
  que confere rodapé, cabeçalho das 17 páginas, o índice das sete páginas longas
  com atalho sem destino contado um a um, a página Sobre, o guia de medidas, o
  Diário e o lookbook).
- Teste novo de fechamento: em todas as 22 páginas a faixa sálvia tem de ser
  filha direta do `<main>`. Esse teste pega qualquer `</div>` faltando, porque
  uma div aberta engoliria a faixa.
- Servidor local no ar em `http://localhost:8080` para a conferência visual.
- Não é medição de navegador real: navegador, leitor de tela, Lighthouse e
  contraste em tela ficam por conta do time, como manda o dossiê.

### Estado
- `VERSION` = 0.1.8. Versão anterior preservada na etiqueta `v0.1.7`.
- Branch `arena/e067653e-iaracostaoficial`, PR #2 aberto (não mergeado).

## [2026-10-16] - Cabeçalho da loja, ordenação e trilha de navegação

### Pedido da cliente
Com a captura da loja em mãos: o cabeçalho de página está com problema, o
filtro "Ordenar por" também, criar a trilha de navegação (breadcrumb) e
conferir em todas as telas.

### O que foi feito (IMPLEMENTADO)
- **Trilha de navegação.** O separador era um ponto em Accent Soft, que sobre o
  papel fica em 1,5:1 e quase não aparece; por isso a trilha parecia duas
  palavras soltas. Agora o separador é uma barra em Muted (4,3:1), o espaçamento
  entre os itens aumentou e a página atual fica em Ink. O rótulo passou a ser
  "Trilha de navegação". A trilha foi criada nas duas páginas que não tinham:
  Pedido recebido ("Início / Pedido recebido") e a página de erro
  ("Início / Página não encontrada"). Agora são 21 páginas com trilha; só a home
  não tem, que é o certo.
- **Cabeçalho de página.** Título de 46px no máximo (era 54px), respiro de cima
  e de baixo mais curto, fio embaixo mantido e a contagem de peças alinhada pela
  base do texto de apoio. Vale para todas as páginas internas.
- **Linha de filtros e ordenação.** "Filtros / Limpar" e "Ordenar por" estavam
  em alturas diferentes, cada um com seu fio, o que dava a impressão de duas
  linhas quebradas. Agora as duas colunas têm a mesma altura (46px), o mesmo
  respiro e o mesmo fio embaixo, então abrem alinhadas.
- **Seletor de ordenação.** Era o campo nativo do navegador, com a seta do
  sistema. Passou a usar a classe de campo do site, com 46px de altura, borda de
  linha, seta desenhada em SVG no tom da marca, foco visível e, no celular, a
  linha inteira.

### Decisões e observações
- A contagem de peças continua sendo a única informação da direita do cabeçalho
  e só aparece na loja e na busca, que é onde faz sentido.
- O HTML ainda tem 69 margens escritas direto no elemento (por exemplo
  `style="margin-top:32px"`). Funciona, mas o lugar certo é o CSS. Fica anotado
  como limpeza opcional, sem pressa e sem risco para o layout atual.

### O que foi verificado
- Geração das 22 páginas sem erro de estrutura.
- 272 verificações automatizadas passando, entre elas as novas: trilha presente
  nas 21 páginas internas e ausente na home, trilha com rótulo e página atual
  marcada, cabeçalho da loja com título, texto de apoio e contagem, seletor de
  ordenação com a classe de campo e as quatro opções.
- Conferência página a página: todas as páginas com cabeçalho têm título e texto
  de apoio.

### O que ainda não foi verificado
- Conferência visual em navegador, em telas pequenas e grandes, e contraste
  medido por ferramenta (axe ou WAVE).

### Pendências que continuam abertas
- Fotos reais, dados legais da empresa, atendimento, gateway, frete contratado,
  revisão jurídica e contador (bloqueadores do go-live, já listados no README).
- Direitos das 31 fotos do template.
- Limpeza opcional das margens escritas direto no HTML.

### Próximo passo sugerido
Abrir a loja no navegador e conferir a faixa de cima: trilha, título, contagem e
a linha de filtros e ordenação alinhadas. Se estiver do jeito que você quer,
sigo para o Bloco B (JSONs do Elementor e guia de importação).

---

## [2026-10-16] - Decisões da cliente confirmadas

### Pedido da cliente
Três respostas curtas: frete grátis acima de R$ 299, catálogo com 12 peças
visíveis e a newsletter do rodapé pode ficar.

### O que foi feito (IMPLEMENTADO)
- **Frete grátis acima de R$ 299.** Nenhum texto do site precisou mudar: a
  regra já estava em 299 na barra do topo, na página do produto, no carrinho, no
  checkout, no pedido recebido, na página de envio, na descrição para busca e na
  conta que o JavaScript faz na mini-sacola. Foi atualizado o registro: o
  comentário no `loja.js`, a lista de decisões abertas e as pendências do
  README deixaram de dizer que o valor estava em dúvida.
- **Catálogo com 12 peças visíveis.** A loja já mostrava as 12 peças. Dois
  textos que ficaram para trás foram corrigidos: o atalho da página 404 passou a
  dizer "Loja completa, 12 peças" e o item da página Sobre passou de "Dez
  peças" para "Doze peças bem escolhidas".
- **Newsletter do rodapé mantida.** Era a última dúvida da v0.1.5 e ficou
  resolvida: a home continua com uma única faixa sálvia antes do rodapé (a de
  perguntas frequentes) e a newsletter fica no rodapé de todas as páginas.

### Decisões e observações
- Nada de preço de produto mudou. O que foi confirmado é a **regra de frete**,
  que já estava no protótipo, e a **quantidade de peças** do catálogo, que
  também já estava.
- As duas decisões deixam de ser `[A DEFINIR]` e passam a valer como regra do
  projeto. Se um dia a regra mudar, é uma alteração de uma linha no
  `loja.js` (frete) ou uma linha no `tools/produtos.json` (peças), com nova
  versão registrada.

### O que foi verificado
- Geração das 22 páginas sem erro de estrutura.
- 189 verificações automatizadas continuam passando.
- Varredura de texto: não sobrou nenhuma menção a 10 peças nos textos do site.

### O que ainda não foi verificado
- Conferência visual em navegador e contraste medido por ferramenta.
- Direitos das 31 fotos do template, que segue em aberto com a equipe.

### Pendências que continuam abertas
- Fotos, dados legais da empresa (razão social, CNPJ, endereço), atendimento,
  gateway de pagamento, frete contratado, revisão jurídica e contador. Todas já
  estão na lista de bloqueadores do go-live.

### Próximo passo sugerido
Seguir para o Bloco B: os 21 arquivos JSON do Elementor e o guia de importação,
com a ressalva de que o esquema dos arquivos precisa ser conferido contra um
export real da equipe e que nenhuma importação foi testada por aqui.

---

## [2026-10-16] - Faixa verde antes do rodapé em todas as páginas e revisão de CSS

### Pedido da cliente
Com a captura da caixa verde do lookbook em mãos: analisar a home de novo e
tirar a seção de newsletter criada na v0.1.4 (não gostou); ajustar todos os
arquivos do template para pegar a mesma largura do header; todas as páginas com
uma seção antes do rodapé, com esse fundo, ocupando 100% da largura; e analisar
todas as páginas para revisar e melhorar o CSS.

### O que foi feito (IMPLEMENTADO)
- **Faixa sálvia antes do rodapé nas 22 páginas.** O fundo ocupa a largura
  inteira da tela e o conteúdo fica na largura do header, igual à barra do topo.
  Nas seis páginas que tinham a caixa arredondada (lookbook, sobre, perguntas
  frequentes, guia de medidas, trocas e envio) o texto foi mantido; nas outras
  15 a faixa entrou com um convite curto e ligado ao assunto da página.
- **Faixa compacta da home removida.** Saiu a faixa de lista de espera que
  ficava no meio da home desde a v0.1.4. A home fica com uma única faixa sálvia,
  a de perguntas frequentes, antes do rodapé. A newsletter do rodapé continua.
- **Mesma largura do header em todas as páginas.** As páginas de leitura usavam
  um container de 1180px; agora todas usam 1688px, como o header. O que continua
  limitado é só a linha do texto corrido, em 72 caracteres, para não virar uma
  linha longa demais em tela grande (vale também para as caixas de aviso e os
  rascunhos legais).
- **Revisão de CSS.** A bolinha da cor "carvão" não aparecia porque o CSS tinha
  `.sw-carvalho` e o HTML usa `.sw-carvao`; os passos do pedido estavam sem
  estilo nenhum (o número escrito aparecia ao lado do número do navegador) e
  agora ficam em três colunas; a caixa `.promo` saiu do CSS e do HTML; o botão
  claro das faixas virou a classe `.btn--paper`; e saíram as regras que nenhuma
  página usava. A varredura final não achou nenhuma classe usada no HTML sem
  estilo.

### Decisões e observações
- **A newsletter do rodapé continua.** Ela foi pedida na v0.1.3, a partir da
  imagem de referência do rodapé, e é o convite para as cartas do ateliê. O que
  saiu foi a faixa de lista de espera criada na v0.1.4 no meio da home, que era
  o segundo pedido de e-mail da mesma página. Confirmado pela cliente em
  16/10: a newsletter do rodapé fica.
- **Um convite por página.** Cada faixa usa um texto curto ligado ao assunto da
  página (medidas na página do produto, prazos no pedido recebido, dúvidas nas
  páginas legais), sem repetir o mesmo bloco em todas.
- **Contraste da faixa:** texto Paper sobre Sálvia 5,9:1 (AA); botão claro com
  texto Accent Dark 7,7:1; no hover, texto Ink sobre Accent Soft 9,3:1.

### O que foi verificado
- Geração das 22 páginas sem erro de estrutura e sem tag aberta.
- 189 verificações automatizadas passando, entre elas as novas: uma única faixa
  sálvia na home, a faixa fechando cada uma das 22 páginas e a newsletter
  presente no rodapé de todas elas.
- Varredura de classes: nenhuma classe usada no HTML ficou sem estilo no CSS.

### O que ainda não foi verificado
- Conferência visual em navegador das 22 páginas e contraste medido por
  ferramenta (axe ou WAVE).

### Pendências que continuam abertas
- Nenhuma das duas que estavam nesta lista. Em 16/10 a cliente confirmou:
  frete grátis acima de R$ 299, catálogo com 12 peças visíveis e a newsletter
  do rodapé mantida. O registro está na entrada da v0.1.6.

### Próximo passo sugerido
Abrir a home e o lookbook no navegador e conferir a faixa verde antes do rodapé
nas duas pontas: fundo de ponta a ponta, texto alinhado com o header e o rodapé
encostando na faixa sem vão branco.

---

## [2026-10-16] - Perguntas frequentes na home e uso da cor sálvia

### Pedido da cliente
Com a captura da faixa verde em mãos: adicionar uma seção de perguntas e
respostas na home; a cor da faixa verde está ótima, mas o conteúdo não ficou no
lugar certo; criar uma seção antes do rodapé com essa cor para separar o
rodapé, com outro conteúdo; usar a mesma cor numa seção pequena no meio da
home; e resolver o rodapé.

### O que foi feito (IMPLEMENTADO)
- **Perguntas frequentes na home.** Faixa sálvia antes do rodapé com cinco
  perguntas que mais chegam no atendimento, em acordeão: criar conta, tabela de
  medidas, troca e devolução, entrega e tratamento de dados. As respostas são
  as mesmas da página Perguntas frequentes, para não existir duas versões da
  mesma resposta no site. A faixa termina com o link "Ver todas as perguntas".
- **Lista de espera compacta no meio da home.** O conteúdo da faixa antiga
  virou uma faixa curta entre os destaques e a vitrine por ocasião: título à
  esquerda, formulário em uma linha à direita e a nota de uma linha embaixo.
  Era o conteúdo que estava colado no rodapé, onde repetia o pedido de e-mail
  que a newsletter já faz.
- **Rodapé resolvido.** A faixa de perguntas encosta no rodapé, então o verde
  passa a ser o separador entre o conteúdo e o fim da página. Isso tirou o vão
  branco grande que aparecia na captura e acabou com os dois pedidos de e-mail
  em sequência.
- **Formulário em uma linha.** Na faixa compacta, campo e botão ficam lado a
  lado a partir de 721px (na captura o botão caía para baixo do campo). Abaixo
  disso, continuam empilhados, que é o certo no celular.

### O que foi verificado
- Geração das 22 páginas sem erro de estrutura.
- 81 verificações automatizadas passando, entre elas as novas: as duas faixas
  na home, as cinco perguntas, o acordeão abrindo e fechando no clique, a ordem
  das seções e o rodapé logo depois do conteúdo.
- Contraste calculado nos pares novos: papel sobre sálvia 5,9:1 (AA), resposta
  do acordeão 5,45:1 (AA). Accent Soft sobre sálvia ficou em 3,86:1 e por isso
  não foi usado em texto pequeno, só em elemento gráfico.

### O que ainda não foi verificado
- Conferência visual em navegador e medição de contraste por ferramenta
  (axe ou WAVE).

### Próximo passo sugerido
Conferir a home no navegador, principalmente as duas faixas verdes. Se a lista
de espera ficar melhor em outro ponto, ou se preferirem outro conteúdo na faixa
pequena, é uma linha de mudança.

---

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

### Decisões que precisavam da cliente (2) - respondidas em 16/10/2026
1. **Frete grátis:** o dossiê previa R$ 199; o header aprovado diz R$ 299.
   Unificamos em R$ 299 no protótipo inteiro e a cliente confirmou: **acima de
   R$ 299**.
2. **Catálogo:** o dossiê falava de 10 produtos; o template trouxe 12. A
   cliente confirmou: **12 peças visíveis**. Os dois textos que ainda diziam 10
   peças foram corrigidos na v0.1.6.

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
- [ ] Dados reais dos 12 produtos (substituir os de exemplo) - equipe

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
- [ ] Dados reais dos 12 produtos (substituir os fictícios) - equipe - sem prazo - [BLOQUEADOR DE PRODUÇÃO? Sim]
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
