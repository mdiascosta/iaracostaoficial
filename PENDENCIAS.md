# Pendências: o que ainda depende de informação

**Onde estamos:** o Bloco A (o protótipo HTML da loja) está fechado na versão
0.1.20 e congelado em `template-v0.1.20/`. Cada ponto que dependia de informação
da empresa ficou marcado dentro da própria página, para não se perder.

**O que este documento é:** o resumo dessas marcações em um lugar só. São
**78 marcações nas 22 páginas**. Nenhuma delas atrapalha a leitura do protótipo,
mas todas precisam estar resolvidas antes de o site ir ao ar.

| Marcação no site | O que significa | Quantas |
|---|---|---|
| `[PREENCHER]` | texto que só a empresa pode escrever | 9 |
| `[A DEFINIR]` | decisão de negócio, de operação ou de fornecedor | 22 |
| `[CONFIRMAR COM A EMPRESA]` | ponto que precisa de um sim ou não | 2 |
| `[PROPOSTA]` | texto escrito por mim, aguardando aprovação | 4 |
| `[CONFERIR]` | conferência na hora de instalar ou de publicar | 41 |
| **Total** | | **78** |

---

## 1. Conteúdo que só a empresa pode escrever (`[PREENCHER]`, 9)

| O que falta | Onde aparece | Observação |
|---|---|---|
| Tabela de medidas real de cada peça | `guia-medidas.html`, `produto.html` | as medidas de hoje são de exemplo, para o layout ficar de pé |
| Percentual real de cada fibra | `produto.html` | a ficha da peça pede a composição exata |
| Peso e dimensões da embalagem | `produto.html` | entram no cálculo do frete |
| História real da marca, em dois ou três parágrafos | `sobre.html` | de onde veio a ideia, quando começou, quem está à frente do negócio |
| Detalhe real do processo de compra | `sobre.html` | quantas peças são testadas por coleção e quem aprova |
| Apresentação de quem assina o diário | `post.html` | o blog é escrito por quem desenha e costura as peças |
| Termo de uso de imagem e crédito da modelo | `lookbook.html` | só se houver modelo fotografada |
| Data da versão aprovada dos documentos legais | `privacidade.html`, `termos.html` | entra quando o jurídico aprovar cada rascunho |

## 2. Decisões de negócio e de operação (`[A DEFINIR]`, 22)

**Fiscal e dinheiro**

| O que decidir | Onde aparece | Observação |
|---|---|---|
| Emissão de nota fiscal | `faq.html`, `privacidade.html` | definir com a contabilidade quem emite e por qual sistema |
| Regra de custo em nova tentativa de entrega | `termos.html` | quem paga quando a primeira tentativa não é recebida |
| Peças de bazar: entram na troca? | `trocas.html` | decisão comercial |
| Conferência das peças devolvidas | `trocas.html` | procedimento interno |

**Ferramentas, contas e fornecedores**

| O que decidir | Onde aparece | Observação |
|---|---|---|
| Ferramenta de medição de audiência | `cookies.html`, `privacidade.html` | por exemplo, Google Analytics 4 |
| Pixel de rede social | `cookies.html` | se haverá e qual |
| Proteção contra robôs no formulário e no checkout | `cookies.html` | qual serviço |
| Serviço de e-mail transacional | `privacidade.html` | provedor que envia os e-mails de pedido |
| Hospedagem | `privacidade.html` | onde ficam o site e o banco de dados |
| Emissor de nota fiscal | `privacidade.html` | mesma decisão do item fiscal, na tabela de quem trata dados |
| Contas a ativar antes do go-live | `privacidade.html` | Mercado Pago e Correios aparecem nomeados |
| País onde cada serviço guarda dados | `privacidade.html` | a equipe confirma em que país cada ferramenta armazena |

**Loja e atendimento**

| O que decidir | Onde aparece | Observação |
|---|---|---|
| Mostrar peças esgotadas no catálogo e aviso de reposição | `faq.html` | muda o comportamento da vitrine |
| Serviço de ajuste de roupas | `guia-medidas.html` | se não existir, a pergunta sai da página |
| Guardar a medida da cliente no cadastro | `conta.html` | se ficar, precisa entrar na Política de Privacidade |
| Horário de atendimento dos pedidos do site | `termos.html` | é o mesmo das 9h às 18h de segunda a sexta? |
| Como o cliente encerra a conta | `termos.html` | procedimento interno |
| Visitas ao ateliê | `contato.html` | somente com agendamento prévio, se a empresa receber no local |

**Privacidade e dados (LGPD)**

| O que decidir | Onde aparece | Observação |
|---|---|---|
| Lista de quem trata os dados (tabela de operadores) | `privacidade.html` | só fecha depois das contratações |
| Prazo de guarda dos dados do pedido e da nota | `privacidade.html` | conferir com o contador |
| Prazo de guarda dos registros de acesso | `privacidade.html` | conforme a legislação aplicável |

## 3. Confirmações pontuais (`[CONFIRMAR COM A EMPRESA]`, 2)

| O que confirmar | Onde aparece | Observação |
|---|---|---|
| Cenário das fotos dos capítulos da coleção | `lookbook.html` | o zip sugere barro cru, mata e superfície clara; confirmar o que a produção vai usar |
| Brincos e itens de uso íntimo fora da troca | `trocas.html` | exceção válida apenas dentro das regras do CDC |

## 4. Textos aguardando aprovação (`[PROPOSTA]`, 4)

| O que aprovar | Onde aparece | Observação |
|---|---|---|
| Missão, visão e compromisso | `sobre.html` | os três cartões foram escritos a partir do que já está no site e esperam ajuste com as palavras da marca |

## 5. Conferências na instalação e no go-live (`[CONFERIR]`, 41)

**5.1 A mesma nota nas 22 páginas (22).** A faixa de segurança do rodapé, que
mostra selos e certificados, é demonstrativa durante o protótipo. No go-live ela
só entra de verdade quando o certificado do gateway estiver ativo e as bandeiras
estiverem habilitadas na conta do Mercado Pago.

**5.2 Coisas que o tema resolve no Bloco B (6).**

| O que conferir | Onde aparece |
|---|---|
| Contagem e faixa da loja saem do próprio tema | `loja.html` |
| Contagem da busca sai do próprio tema | `busca.html` |
| Prazo de armazenagem nos Correios é definido pela própria empresa | `envio.html` |
| Proteção anti-robô do formulário de contato | `contato.html` |
| Mapa do Google depende do endereço confirmado | `contato.html` |
| Tabelas de medidas podem variar por fornecedor | `guia-medidas.html` |

**5.3 Datas, links e cadastros (13).**

| O que conferir | Onde aparece | Observação |
|---|---|---|
| Data de cada documento legal | `cookies.html`, `privacidade.html`, `termos.html`, `trocas.html` | muda quando o jurídico aprovar a versão final |
| Link "Preferências de cookies" no rodapé | `cookies.html` | entra junto com o banner de cookies |
| Cadastro de teste desligado | `conta.html` | antes de publicar |
| Redação final dos prazos e do trecho do CDC | `trocas.html`, `termos.html` | com o jurídico |
| Prazo de guarda dos dados | `privacidade.html` | com o contador |
| Texto sobre pagamentos ativos | `faq.html` | precisa acompanhar o que estiver ativo na conta do gateway no dia da publicação |

---

## 6. Itens que nasceram com o Bloco B (templates do Elementor)

| O que falta | Onde aparece | Observação |
|---|---|---|
| Versões do staging (WordPress, PHP, Elementor, Elementor Pro, WooCommerce) | `bloco-b/GUIA-IMPORTACAO.md`, seção 2 | é o primeiro item da instalação: sem elas não dá para confirmar o que o site suporta |
| Destino do formulário da newsletter | rodapé, campo do formulário | está como `[PREENCHER]` até a ferramenta de newsletter ser escolhida |
| Endereço do Instagram e do Pinterest | rodapé, coluna Atendimento | hoje os dois links estão como `[PREENCHER]` |
| Nome do menu principal | cabeçalho, widget Menu | o template aponta para o menu de slug `principal` |
| Logo do site | cabeçalho, widget Site Logo | entra em Aparência > Personalizar > Identidade do site |
| Plugin de lista de desejos | página de desejos e ícone do coração | sem aprovação, a página fica para depois |
| Número final de arquivos do Bloco B (24 ou 21) | `bloco-b/GUIA-IMPORTACAO.md`, seção 5.2 | a conta página por página dá 24; juntar as três páginas políticas levaria a 21 |

## Como usar este documento

- **Nada aqui foi inventado para preencher espaço.** Onde não havia informação
  confirmada, o site mostra o marcador em vez de um dado falso.
- **Cada item é uma mudança pequena.** Quando a resposta chega, o texto entra na
  página, o marcador sai e a versão sobe, com o registro em
  `HISTORICO-DE-VERSOES.md` e `DIARIO-DE-BORDO.md`.
- **A ordem sugerida:** primeiro o conteúdo e as decisões (seções 1 a 4), que são
  o que a cliente vê; depois as conferências de instalação (seção 5), que andam
  junto com os blocos B e C.
- **Os documentos legais continuam sendo rascunhos.** Privacidade, Termos e
  Cookies levam o aviso de que precisam de revisão jurídica antes de publicar.
