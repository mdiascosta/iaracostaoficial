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

### Estados de interface demonstrados

O dossiê pede que todos os estados de tela estejam representados. Onde procurar:

### Novidades da v0.1.2 (ajustes pedidos pela cliente)

| Ajuste | Como ficou |
|---|---|
| Largura das seções | A grade acompanha a barra do header: 1688px. Páginas de leitura ficam em 1180px, para a linha não ficar longa demais |
| Cores das seções | Três fundos da própria paleta: areia claríssimo (Hover Soft), terracota claro (Accent Soft, no editorial) e sálvia (na faixa da lista de espera) |
| Loja | Filtro à esquerda em coluna de 240px: categorias, faixa de preço, cor e tamanho. No celular vira gaveta pelo botão "Filtros" |
| Rodapé | Enxuto: quatro colunas curtas, identificação da empresa e links de política. Saíram a newsletter e a faixa de selos |
| Newsletter | Ficou só na faixa verde sálvia da home, para não pedir o mesmo e-mail duas vezes na mesma página |

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
| Carregando | classe `.skeleton` no CSS, exemplo em `produto.html` |
| Busca sem resultado | `busca.html`, seção final |
| Produto esgotado | `produto.html`, final da página |
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
- **Não há cálculo automático.** Preços, fretes e totais são textos escritos no
  HTML. Quem calcula de verdade é o WooCommerce.
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
- Prazos, fretes e valores de pagamento são ilustrativos.
- Razão social, CNPJ, endereço e contatos estão como `[PREENCHER]`.

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
- [ ] Razão social, CNPJ e endereço (exigência do Decreto 7.962/2013).
- [ ] E-mail e WhatsApp de atendimento, com horário.
- [ ] Gateway de pagamento e solução de frete contratados.
- [ ] Regras de parcelamento e desconto no Pix definidas.
- [ ] **Frete grátis: R$ 199 ou R$ 299?** O dossiê dizia R$ 199 e o header
      aprovado diz R$ 299. O protótipo está todo em R$ 299.
- [ ] **Catálogo de 10 ou 12 peças?** O protótipo está com 12, como o template.
- [ ] **Direitos das 31 fotos** vindas do template de referência.
- [ ] Regras finas do cupom BEMVINDO10 e do frete grátis definidas.
- [ ] Regime tributário e emissão de nota fiscal definidos com o contador.
- [ ] Revisão jurídica das três páginas legais e de trocas.
- [ ] Plugin de lista de desejos aprovado, ou o coração sai do header.
